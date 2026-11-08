#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run a MIP through the LSB pipeline: MIP in (required) → chunks → stages → teacher cards.

A MIP is a Micro-Lesson Scaffold: one MIP is one MLS unit and MIP tasks are
MLS steps (see `sgmsb.mip`). Two things are fixed here that LSB leaves open:

* the input is a schema-valid MIP document, stamped with its `variant_id`;
* the breakdown is derived from the MIP's task chunks (`mip_to_mls`, at most
  7 steps per unit), never chosen: `--ask` is rejected outright, and any
  breakdown keys in `--answers` are overridden with the chunk-derived values
  before the run is handed to `lsb.run.main`.

Stage limits stay fully user-tunable through `--answers` (cards, max cards,
added steps) and `--no-eb` / `--no-cl` / `--no-pb`, used verbatim.

    python -m sgmsb.run mip.json --dry-run
    python -m sgmsb.run variants.json --pick baseline --answers limits.json --no-pb --out runs/mip-01

Exit status: 0 the sequence passed, 1 it did not (or the MIP/chunks failed
validation, or the forced breakdown did not hold), 2 usage or API error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from lsb import run as lrun
from lsb import validate as v

from sgmsb import mip as M

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"

BREAKDOWN_KEYS = ("single_module", "max_units", "focus")
FOCUS_PER_SECTION = "one unit per source section"


def render_mip_source(mip: dict, mls: dict) -> str:
    """Deterministic source text: the MIP header, then one section per chunk."""
    lines = [
        f"# {mip.get('title', '').strip()}",
        f"Domain: {mip.get('domain', '').strip()} | "
        f"Owner: {mip.get('target_stakeholder', '').strip()} | "
        f"Duration: {mip.get('duration', '').strip()}",
        f"Objective: {mip.get('objective', '').strip()}",
    ]
    if (mip.get("description") or "").strip():
        lines.append(mip["description"].strip())
    for u in mls["mls_units"]:
        lines.append(f"## {u['title']}")
        for t in u["tasks"]:
            lines.append(f"{t['step']}. [{t['role']}] {t['action']}")
    return "\n".join(lines) + "\n"


def forced_answers(n_chunks: int) -> dict:
    """Breakdown answers derived from the chunks; the user cannot change these."""
    return {
        "single_module": False,
        "max_units": max(2, min(n_chunks, 5)),
        "focus": FOCUS_PER_SECTION,
    }


def record_mip(out_dir: Path, info: dict) -> None:
    """Add MIP provenance to the run's summary.json; skip silently if absent."""
    try:
        summary_file = out_dir / "summary.json"
        summary = json.loads(summary_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    summary["mip"] = info
    try:
        summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m sgmsb.run", description=__doc__.split("\n\n")[0])
    ap.add_argument("mip", type=Path, help="MIP JSON file (required; validated before anything runs)")
    ap.add_argument("--pick", default=None, help="key to pick when the file holds several MIPs")
    ap.add_argument("--ref", default=None, help="source identifier (default: the MIP title)")
    ap.add_argument("--grade-band", choices=["Primary", "Middle", "High"])
    ap.add_argument("--time-block", type=int, metavar="MINUTES", help="class period length, 5-120")
    ap.add_argument("--context-file", type=Path, help="educator's notes about their setting")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--backend", default="claude-code", choices=["claude-code", "muse", "gemini", "api"])
    ap.add_argument("--model", default=None, help="model id (default: the backend's default)")
    ap.add_argument("--ask", action="store_true",
                    help="rejected: the MIP chunks fix the breakdown (tune stages via --answers)")
    ap.add_argument("--answers", type=Path, metavar="FILE",
                    help="JSON stage limits (breakdown keys are overridden from the MIP chunks)")
    ap.add_argument("--max-revisions", type=int, default=2)
    ap.add_argument("--no-eb", action="store_true", help="skip the Evidence-Based stage")
    ap.add_argument("--no-cl", action="store_true", help="skip the Connected Learning stage")
    ap.add_argument("--no-pb", action="store_true", help="skip the Participatory Budgeting stage")
    ap.add_argument("--max-stage-revisions", type=int, default=1)
    ap.add_argument("--out", type=Path, help="output directory (default runs/<timestamp>)")
    ap.add_argument("--dry-run", action="store_true", help="assemble and check the requests; no API calls")
    return ap


def load_mip(path: Path, pick: str | None) -> tuple[dict | None, int]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read {path}: {e}", file=sys.stderr)
        return None, 2
    mip = raw[pick] if pick else raw
    if pick and pick not in raw:
        print(f"error: no key {pick!r} in {path}", file=sys.stderr)
        return None, 2
    if not isinstance(mip, dict) or "tasks" not in mip:
        print("error: not a MIP document (need an object with tasks)", file=sys.stderr)
        return None, 2
    return mip, 0


def chunk_and_gate(mip: dict, args: argparse.Namespace) -> tuple[dict | None, int]:
    """Break the MIP into chunks and validate them; (None, 1) gates the run."""
    mls = M.mip_to_mls(mip, grade_band=args.grade_band or "Middle",
                       time_block_minutes=args.time_block or 45)
    report = v.validate(mls)
    gating = [c for c in report.checks if c.id != "D10"]
    d10 = next(c for c in report.checks if c.id == "D10")
    if not all(c.passed for c in gating):
        print(v.format_text(report))
        print("error: MIP chunks failed MLS validation; nothing to run", file=sys.stderr)
        return None, 1
    if not d10.passed:
        print("note: D10 regional terms deferred to 05-decompose")
    return mls, 0


def merge_answers(user: dict, n_chunks: int) -> tuple[dict, list[str]]:
    """Overlay the forced breakdown answers on the user's stage limits."""
    merged = {k: val for k, val in user.items() if k not in BREAKDOWN_KEYS}
    overridden = [k for k in BREAKDOWN_KEYS if k in user]
    merged.update(forced_answers(n_chunks))
    return merged, overridden


def audit_forcing(out_dir: Path, n_chunks: int) -> list[str]:
    """Check choices.json shows the forced breakdown; [] means ok or skipped.

    Skipped (no file to read) on --dry-run and when LSB failed before
    recording its choices.
    """
    try:
        choices = json.loads((out_dir / "choices.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(choices, dict):
        return []
    expected = forced_answers(n_chunks)
    return [f"{k} is {choices.get(k)!r}, want forced {expected[k]!r}"
            for k in BREAKDOWN_KEYS if choices.get(k) != expected[k]]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.ask:
        print("error: --ask is unavailable: the MIP's task chunks fix the breakdown; "
              "tune stages via --answers", file=sys.stderr)
        return 2
    mip, rc = load_mip(args.mip, args.pick)
    if mip is None:
        return rc
    vid = M.stamp_variant_id(mip)
    errors = M.validate_mip(mip)
    if errors:
        print(f"variant_id: {vid}")
        print("MIP schema: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    mls, rc = chunk_and_gate(mip, args)
    if mls is None:
        return rc
    n_chunks = len(mls["mls_units"])

    user_answers: dict[str, Any] = {}
    if args.answers:
        try:
            user_answers = json.loads(args.answers.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: cannot read answers file {args.answers}: {e}", file=sys.stderr)
            return 2
        if not isinstance(user_answers, dict):
            print(f"error: answers file {args.answers} must hold a JSON object", file=sys.stderr)
            return 2
    merged, overridden = merge_answers(user_answers, n_chunks)
    if overridden:
        print(f"note: breakdown keys {overridden} overridden from {n_chunks} MIP chunk(s)")

    ref = args.ref or mip.get("title", "")
    out_dir = args.out or RUNS / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "00-mip.json").write_text(json.dumps(mip, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "00-chunks.json").write_text(json.dumps(mls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_file = out_dir / "00-mip-source.md"
    source_file.write_text(render_mip_source(mip, mls), encoding="utf-8")
    answers_file = out_dir / "01-sg-answers.json"
    answers_file.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    forwarded: list[str] = [str(source_file), "--ref", ref]
    for flag in ("grade-band", "time-block", "context-file", "effort", "backend",
                 "model", "max-revisions", "max-stage-revisions"):
        value = getattr(args, flag.replace("-", "_"))
        if value is not None:
            forwarded += [f"--{flag}", str(value)]
    for flag in ("no-eb", "no-cl", "no-pb", "dry-run"):
        if getattr(args, flag.replace("-", "_")):
            forwarded.append(f"--{flag}")
    forwarded += ["--answers", str(answers_file), "--out", str(out_dir)]

    rc = lrun.main(forwarded)
    record_mip(out_dir, {"variant_id": vid, "title": mip.get("title", ""),
                         "source_file": str(args.mip), "ref": ref, "chunks": n_chunks})
    if rc == 0:
        problems = audit_forcing(out_dir, n_chunks)
        if problems:
            print("error: forced breakdown did not hold:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return 1
    return rc


if __name__ == "__main__":
    sys.exit(main())

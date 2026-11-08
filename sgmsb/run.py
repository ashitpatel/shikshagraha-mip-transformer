#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run a MIP through the LSB pipeline: MIP in (required) → stages → teacher cards.

A MIP is a Micro-Lesson Scaffold: one MIP is one MLS unit and MIP tasks are
MLS steps (see `sgmsb.mip`). Unlike LSB's free-text source, the MIP is not
optional here — every run starts from a schema-valid MIP document, stamped
with its `variant_id`. Every framework (evidence-based, Connected Learning,
participatory budgeting) stays optional, and all framework UX (`--ask`,
`--answers`, `--no-eb` / `--no-cl` / `--no-pb`, choices.json) is LSB's,
used verbatim: this command validates and renders the MIP, then hands the
run to `lsb.run.main`.

    python -m sgmsb.run mip.json --dry-run
    python -m sgmsb.run mip.json --ref "School resources" --ask
    python -m sgmsb.run variants.json --pick baseline --no-pb --out runs/mip-01

Exit status: 0 the sequence passed, 1 it did not (or the MIP failed schema
validation), 2 usage or API error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from lsb import run as lrun

from sgmsb import mip as M

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"


def render_mip_source(mip: dict) -> str:
    """Deterministic source text for the pipeline: the MIP, whole and verbatim."""
    lines = [
        f"# {mip.get('title', '').strip()}",
        f"Domain: {mip.get('domain', '').strip()} | "
        f"Owner: {mip.get('target_stakeholder', '').strip()} | "
        f"Duration: {mip.get('duration', '').strip()}",
        f"Objective: {mip.get('objective', '').strip()}",
    ]
    if (mip.get("description") or "").strip():
        lines.append(mip["description"].strip())
    lines.append("## Tasks")
    for t in sorted(mip.get("tasks", []), key=lambda x: x.get("seq", 0)):
        name = (t.get("name") or "").strip()
        subs = "; ".join(s.strip() for s in t.get("sub_tasks", []) if s and s.strip())
        lines.append(f"{t.get('seq', '?')}. {name}" + (f" — {subs}" if subs else ""))
    return "\n".join(lines) + "\n"


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
    ap.add_argument("--ask", action="store_true", help="ask about the breakdown and each stage's limits")
    ap.add_argument("--answers", type=Path, metavar="FILE",
                    help="JSON answers for the --ask questions (sweeps answer without stopping)")
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


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
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

    ref = args.ref or mip.get("title", "")
    out_dir = args.out or RUNS / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "00-mip.json").write_text(json.dumps(mip, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_file = out_dir / "00-mip-source.md"
    source_file.write_text(render_mip_source(mip), encoding="utf-8")

    forwarded: list[str] = [str(source_file), "--ref", ref]
    for flag in ("grade-band", "time-block", "context-file", "effort", "backend",
                 "model", "answers", "max-revisions", "max-stage-revisions"):
        value = getattr(args, flag.replace("-", "_"))
        if value is not None:
            forwarded += [f"--{flag}", str(value)]
    for flag in ("ask", "no-eb", "no-cl", "no-pb", "dry-run"):
        if getattr(args, flag.replace("-", "_")):
            forwarded.append(f"--{flag}")
    forwarded += ["--out", str(out_dir)]

    rc = lrun.main(forwarded)
    record_mip(out_dir, {"variant_id": vid, "title": mip.get("title", ""),
                         "source_file": str(args.mip), "ref": ref})
    return rc


if __name__ == "__main__":
    sys.exit(main())

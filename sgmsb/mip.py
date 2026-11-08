#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""MIP compatibility: validate a Shikshagraha MIP, stamp its variant_id, convert it to an MLS DAG.

A MIP is a Micro-Lesson Scaffold: one MIP is one MLS unit and MIP tasks are
MLS steps. This module is the naming/shape bridge for that identity (a MIP
over 7 tasks spans units, since an MLS unit holds at most 7 steps).

    python3 -m sgmsb.mip schema/examples/mip-variants.json --pick baseline --validate
    python3 -m sgmsb.mip path/to/mip.json --out sequence.json

The adapter is mechanical on purpose: it validates the MIP against
schema/mip.schema.json, assigns the stable content id from
schema/variant_id.py (never invented by a model), and converts MIP tasks into
an MLS_DAG_Sequence the sgmsb pipeline can run. Region-neutral wording is the
pipeline's job (05-decompose strips it); the adapter keeps task text verbatim
so D10 may flag terms like CRP until then.

Conversion rules:
  * macro_objective is the MIP objective, verbatim (SMT check C3).
  * tasks (by seq) become steps in order; sub_tasks are appended to the action
    text after a semicolon.
  * role is Peer_Facilitator when the task's x_transform names a student_role,
    else Lead_Educator.
  * tasks chunk into units of at most 7 steps (D03); units chain linearly
    since MIP tasks are ordered.
  * duration_weeks per unit is the MIP duration spread across units, clamped
    to 2..4 (D04). "N weeks" counts N, "N months" counts 4N, anything else
    counts 4.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from lsb import validate as v

ROOT = Path(__file__).resolve().parents[1]
MIP_SCHEMA = json.loads((ROOT / "schema" / "mip.schema.json").read_text(encoding="utf-8"))

DURATION_RE = re.compile(r"(\d+)\s*(week|month)", re.IGNORECASE)


def _variant_id_fn():
    """Load variant_id() from schema/variant_id.py without touching sys.path."""
    path = ROOT / "schema" / "variant_id.py"
    spec = importlib.util.spec_from_file_location("sgmsb_variant_id", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.variant_id


variant_id = _variant_id_fn()


def validate_mip(mip: dict) -> list[str]:
    """Schema errors for a MIP document; empty means valid (SMT check C1)."""
    return [
        f"{'/'.join(map(str, e.path))}: {e.message}"
        for e in Draft202012Validator(MIP_SCHEMA).iter_errors(mip)
    ]


def parse_duration_weeks(duration: str) -> int:
    m = DURATION_RE.search(duration or "")
    if not m:
        return 4
    n, unit = int(m.group(1)), m.group(2).lower()
    return n * 4 if unit.startswith("month") else n


def _step_action(task: dict) -> str:
    action = task["name"].strip()
    subs = [s.strip() for s in task.get("sub_tasks", []) if s and s.strip()]
    if subs:
        action += "; " + "; ".join(subs)
    return action


def _step_role(task: dict) -> str:
    xt = task.get("x_transform") or {}
    if isinstance(xt, dict) and xt.get("student_role"):
        return "Peer_Facilitator"
    return "Lead_Educator"


def mip_to_mls(
    mip: dict,
    grade_band: str = "Middle",
    time_block_minutes: int = 45,
    resource_intensity_score: int = 2,
) -> dict:
    """Convert a MIP document to an MLS_DAG_Sequence (tasks must already validate)."""
    tasks = sorted(mip["tasks"], key=lambda t: t["seq"])
    total_weeks = parse_duration_weeks(mip.get("duration", ""))
    chunks = [tasks[i : i + 7] for i in range(0, len(tasks), 7)]
    weeks_each = min(4, max(2, -(-total_weeks // len(chunks))))
    units = []
    for i, chunk in enumerate(chunks, start=1):
        uid = f"MLS-M{i:02d}"  # plain sequence id: "MIP" here would trip D10's term match
        title = mip["title"] if len(chunks) == 1 else f"{mip['title']} (part {i}/{len(chunks)})"
        seqs = [t["seq"] for t in chunk]
        units.append(
            {
                "mls_id": uid,
                "title": title,
                "dependencies": [f"MLS-M{i - 1:02d}"] if i > 1 else [],
                "macro_alignment": (
                    f"Implements tasks {seqs[0]}-{seqs[-1]} of '{mip['title']}' "
                    "toward the objective."
                    if len(seqs) > 1
                    else f"Implements task {seqs[0]} of '{mip['title']}' toward the objective."
                ),
                "duration_weeks": weeks_each,
                "tasks": [
                    {"step": n, "role": _step_role(t), "action": _step_action(t)}
                    for n, t in enumerate(chunk, start=1)
                ],
            }
        )
    return {
        "macro_objective": mip["objective"],
        "global_context": {
            "grade_band": grade_band,
            "time_block_minutes": time_block_minutes,
            "resource_intensity_score": resource_intensity_score,
        },
        "mls_units": units,
    }


def stamp_variant_id(mip: dict) -> str:
    """Assign mip['x_transform']['variant_id'] from content; return the id."""
    vid = variant_id(mip)
    mip.setdefault("x_transform", {})["variant_id"] = vid
    return vid


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sgmsb.mip", description=__doc__.split("\n\n")[0])
    ap.add_argument("mip", type=Path, help="a MIP JSON file (or a file holding several under keys)")
    ap.add_argument("--pick", default=None, help="key to pick when the file holds several MIPs")
    ap.add_argument("--validate", action="store_true", help="report MIP + MLS check verdicts")
    ap.add_argument("--grade-band", default="Middle", choices=["Primary", "Middle", "High"])
    ap.add_argument("--time-block", type=int, default=45)
    ap.add_argument("--resource-score", type=int, default=2)
    ap.add_argument("--out", type=Path, default=None, help="write the MLS JSON here (else stdout)")
    args = ap.parse_args(argv)

    try:
        raw = json.loads(args.mip.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read {args.mip}: {e}", file=sys.stderr)
        return 2
    mip = raw[args.pick] if args.pick else raw
    if args.pick and args.pick not in raw:
        print(f"error: no key {args.pick!r} in {args.mip}", file=sys.stderr)
        return 2
    if not isinstance(mip, dict) or "tasks" not in mip:
        print("error: not a MIP document (need an object with tasks)", file=sys.stderr)
        return 2

    vid = stamp_variant_id(mip)
    mip_errors = validate_mip(mip)
    mls = None
    if not mip_errors:
        mls = mip_to_mls(
            mip,
            grade_band=args.grade_band,
            time_block_minutes=args.time_block,
            resource_intensity_score=args.resource_score,
        )
    report = v.validate(mls) if mls is not None else None

    if args.validate:
        print(f"variant_id: {vid}")
        print(f"MIP schema: {'PASS' if not mip_errors else 'FAIL'}")
        for e in mip_errors:
            print(f"  - {e}")
        if report is None:
            return 1
        print(v.format_text(report))
        # D10 (regional terms) is deferred: the adapter keeps MIP text verbatim
        # and 05-decompose neutralises it. Everything else gates the verdict.
        gating = [c for c in report.checks if c.id != "D10"]
        d10 = next(c for c in report.checks if c.id == "D10")
        if not d10.passed:
            print("note: D10 regional terms deferred to 05-decompose")
        return 0 if all(c.passed for c in gating) else 1

    if mls is None:
        print("error: MIP failed schema validation; nothing to convert", file=sys.stderr)
        for e in mip_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    text = json.dumps(mls, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())

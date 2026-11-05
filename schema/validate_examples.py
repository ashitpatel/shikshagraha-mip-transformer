#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the schema examples, and check that the event schema rejects what it must.

    python3 schema/validate_examples.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from variant_id import variant_id  # noqa: E402


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> int:
    mip_v = Draft202012Validator(load("mip.schema.json"), format_checker=FormatChecker())
    ev_v = Draft202012Validator(load("mip-usage-event.schema.json"), format_checker=FormatChecker())
    failures = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {label}" + (f"  ({detail})" if detail and not ok else ""))

    # 1. Example MIP variants: valid, ids correct, parent link correct.
    variants = load("examples/mip-variants.json")
    for kind, mip in variants.items():
        errs = [e.message for e in mip_v.iter_errors(mip)]
        check(f"mip example '{kind}' is schema-valid", not errs, "; ".join(errs[:3]))
        check(f"mip example '{kind}' variant_id matches content",
              mip["x_transform"]["variant_id"] == variant_id(mip))
    check("transformed.parent_variant_id == baseline.variant_id",
          variants["transformed"]["x_transform"]["parent_variant_id"] == variants["baseline"]["x_transform"]["variant_id"])

    # 2. variant_id ignores its own metadata but changes with content.
    t = copy.deepcopy(variants["transformed"])
    t["x_transform"]["pipeline"]["revisions"] = 9
    check("variant_id ignores pipeline metadata", variant_id(t) == variants["transformed"]["x_transform"]["variant_id"])
    t["tasks"][0]["name"] += "."
    check("variant_id changes when content changes", variant_id(t) != variants["transformed"]["x_transform"]["variant_id"])

    # 3. Example usage events: valid, and consistent with the variants.
    known_ids = {m["x_transform"]["variant_id"] for m in variants.values()}
    events = [json.loads(line) for line in (HERE / "examples/usage-events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    for e in events:
        errs = [x.message for x in ev_v.iter_errors(e)]
        check(f"event '{e['event_type']}' is schema-valid", not errs, "; ".join(errs[:3]))
    referenced = {v for e in events for v in (e.get("offer", {}).get("offered_variant_ids", [])
                                              + [e.get("choice", {}).get("chosen_variant_id")]
                                              + [e.get("mip", {}).get("variant_id")]) if v}
    check("events reference only known variant ids", referenced <= known_ids, str(referenced - known_ids))

    # 4. Negative tests: the event schema must reject these.
    base = next(e for e in events if e["event_type"] == "outcome_reported")
    offered = next(e for e in events if e["event_type"] == "offered")
    bad_cases = {
        "per-student field in outcome": lambda e: e["outcome"].__setitem__("student_scores", {"stu_1": 40}),
        "student name inside an indicator": lambda e: e["outcome"]["indicators"][0].__setitem__("student", "Ravi"),
        "owner name / phone at top level": lambda e: e.__setitem__("owner_phone", "9999999999"),
        "raw UDISE code instead of pseudonym": lambda e: e["school"].__setitem__("school_pseudo_id", "09123456789"),
        "extra school field (village name)": lambda e: e["school"].__setitem__("village", "Rampur"),
        "outcome_reported without outcome": lambda e: e.pop("outcome"),
    }
    for label, mutate in bad_cases.items():
        e = copy.deepcopy(base)
        mutate(e)
        check(f"rejects {label}", not ev_v.is_valid(e))
    e = copy.deepcopy(offered)
    e.pop("offer")
    check("rejects 'offered' without offer details", not ev_v.is_valid(e))
    e = copy.deepcopy(offered)
    e["event_type"] = "abandoned"
    e["progress"] = {"tasks_total": 7, "tasks_done": 2}
    check("rejects 'abandoned' without abandon_reason", not ev_v.is_valid(e))

    print(f"\n{'All checks passed.' if not failures else f'{failures} check(s) failed.'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

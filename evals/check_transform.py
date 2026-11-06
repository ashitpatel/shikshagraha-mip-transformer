#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Deterministic checks on 40-transform outputs (the parts of the critic that code can do).

    python3 evals/check_transform.py <run-folder>

Expects <run-folder>/inputs/<id>.json (with BASELINE_MIP_JSON, GATES_JSON) and
<run-folder>/transform/<id>.json (the 40-transform output). For each case it writes
<run-folder>/transform/<id>.checks.json, including SCHEMA_ERRORS for the critic, and prints a table.
Checks: schema (C1), size limits (C2), objective kept (C3), owner unchanged (C5), gate consistency
for labels (part of C8), numbers in rationale only if quoted from EB supportable claims (part of C9),
an "untested" rationale item (part of C9), task names of at most 20 words (part of C17), and a cost
that is "nil", "not stated" or contains an amount (part of C18). It also assigns variant_id / parent_variant_id.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "schema"))
from variant_id import variant_id  # noqa: E402

SCHEMA = json.loads((ROOT / "schema" / "mip.schema.json").read_text(encoding="utf-8"))
EB_TEXT = (ROOT / "frameworks" / "evidence-based-practices.md").read_text(encoding="utf-8")
EB_CLAIMS = " ".join(re.findall(r"\"([^\"]+)\"", " ".join(
    l for l in EB_TEXT.splitlines() if "Supportable claims" in l)))


def weeks(duration: str) -> float | None:
    d = (duration or "").lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(week|month|day)", d)
    if not m:
        return None
    n, unit = float(m.group(1)), m.group(2)
    return n if unit == "week" else n * 4 if unit == "month" else -(-n // 7)


def check(base: dict, out: dict, gates: dict) -> dict:
    mip = out.get("mip", {})
    r = {}
    errs = [f"{'/'.join(map(str, e.path))}: {e.message}" for e in Draft202012Validator(SCHEMA).iter_errors(mip)]
    r["C1_schema"] = not errs
    tasks = mip.get("tasks", [])
    added = sum(1 for t in tasks if (t.get("x_transform") or {}).get("change") == "added")
    wb, wn = weeks(base.get("duration", "")), weeks(mip.get("duration", ""))
    r["tasks"], r["added"], r["weeks"] = len(tasks), added, f"{wb}->{wn}"
    r["C2_size"] = len(tasks) <= 9 and added <= 2 and (wn is None or (wn <= 8 and (wb is None or wn - wb <= 1)))
    norm = lambda s: re.sub(r"\W+", " ", (s or "").lower()).strip()
    r["C3_objective_kept"] = norm(base.get("objective")) in norm(mip.get("objective"))
    r["C5_owner_kept"] = norm(base.get("target_stakeholder")) == norm(mip.get("target_stakeholder"))
    text = json.dumps(mip, ensure_ascii=False).lower()
    pb_abstain = (gates.get("gate_pb", {}).get("pb_process") or {}).get("decision") == "ABSTAIN"
    cl_abstain = (gates.get("gate_cl", {}).get("connected_learning") or {}).get("decision") == "ABSTAIN"
    eb_abstain = (gates.get("gate_eb", {}).get("evidence_based") or {}).get("decision") == "ABSTAIN"
    cited = set(re.findall(r"\b((?:CL|PB|EB)-[a-z][a-z-]*)", json.dumps([t.get("x_transform", {}) for t in tasks])))
    r["C8_labels"] = not ((pb_abstain and "participatory budgeting" in text and "never" not in text)
                          or (cl_abstain and any(c.startswith("CL-") for c in cited))
                          or (eb_abstain and any(c.startswith("EB-") for c in cited)))
    rationale = (mip.get("x_transform") or {}).get("rationale", [])
    bad_numbers = []
    for item in rationale:
        claim = item.get("claim", "") if isinstance(item, dict) else str(item)
        for num in re.findall(r"\d+(?:\.\d+)?\s*(?:%|SD)?", claim):
            if num.strip() and num.strip() not in EB_CLAIMS and not re.fullmatch(r"\d+", num.strip()):
                bad_numbers.append(num.strip())
    r["C9_numbers_sourced"] = not bad_numbers
    r["C9_untested_item"] = any("untested" in json.dumps(i).lower() for i in rationale) or not rationale
    long_names = [t.get("seq") for t in tasks if len((t.get("name") or "").split()) > 20]
    r["C17_short_names"] = not long_names
    cost = ((mip.get("x_transform") or {}).get("cost") or "").strip().lower()
    r["C18_cost"] = cost in ("nil", "not stated") or bool(re.search(r"\d", cost))
    r["long_task_names"] = long_names
    r["schema_errors"] = errs
    r["unsourced_numbers"] = bad_numbers
    return r


def main() -> int:
    run = Path(sys.argv[1])
    cols = ["C1_schema", "C2_size", "C3_objective_kept", "C5_owner_kept", "C8_labels", "C9_numbers_sourced", "C9_untested_item",
            "C17_short_names", "C18_cost"]
    print(f"{'case':42} tasks added weeks       " + " ".join(c.split('_')[0] for c in cols))
    for t in sorted((run / "transform").glob("*.json")):
        if t.name.endswith(".checks.json"):
            continue
        inp = json.loads((run / "inputs" / t.name).read_text(encoding="utf-8"))
        out = json.loads(t.read_text(encoding="utf-8"))
        base = inp["BASELINE_MIP_JSON"]
        r = check(base, out, inp["GATES_JSON"])
        xt = out.setdefault("mip", {}).setdefault("x_transform", {})
        xt["parent_variant_id"] = variant_id(base)
        xt["variant_id"] = variant_id(out["mip"])
        t.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        (run / "transform" / (t.stem + ".checks.json")).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{t.stem:42} {r['tasks']:>5} {r['added']:>5} {r['weeks']:11} " + " ".join("✔ " if r[c] else "✘ " for c in cols))
        for e in r["schema_errors"][:3]:
            print(f"{'':44}schema: {e[:110]}")
        if r["long_task_names"]:
            print(f"{'':44}task names over 20 words: {r['long_task_names']}")
        if r["unsourced_numbers"]:
            print(f"{'':44}unsourced numbers in rationale: {r['unsourced_numbers']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

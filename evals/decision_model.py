#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Executable model of the fit-check (gate) decision rules, for static analysis.

    python3 evals/decision_model.py            # run all cases, print a comparison table
    python3 evals/decision_model.py --strict   # exit 1 if any case falls outside 'acceptable'

The rules below transcribe prompts/30-gate-cl.md, 31-gate-pb.md and 32-gate-eb.md (and the
EB-scope / CL-scope / PB-scope cards) as literally as possible, **after** the fixes F1–F13 from
reports/Decision path analysis.md. Comments name the finding each rule fixes.

Inputs are hand-coded *classification facts* (what 20-classify should output), not raw MIP text,
so this tests the decision logic in isolation from the model's reading of the MIP.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CASES = Path(__file__).resolve().parent / "decision_cases.json"
GATES = ["connected_learning", "pb_process", "pb_prioritise", "pb_allocate", "budget_capped_choice", "evidence_based"]


# ---------------------------------------------------------------- gates, transcribed

def gate_cl(f: dict) -> tuple[str, list[str]]:
    notes = []
    if not f["student_learning"]:
        return "ABSTAIN", notes
    if f["owner"] in ("HM", "SMC") and not f["students_core"]:
        return "PARTIAL", notes                       # incidental student participation (F7 fix)
    if not f.get("cl_gap_feasible", True):            # steps 2–4: no real, feasible gap
        return "ABSTAIN", notes
    return "APPLY", notes


def gate_pb(f: dict) -> tuple[dict, list[str]]:
    notes, d = [], {}
    # Public outcome is always satisfiable by an added report-back task (F13 clarification).
    d["pb_process"] = "APPLY" if (f["constituency"] and f["resource"] in ("money", "space", "materials")) else "ABSTAIN"
    d["pb_prioritise"] = "APPLY" if (f["options"] >= 2 and f["collective"]) else "ABSTAIN"
    voters = "APPLY" in (d["pb_process"], d["pb_prioritise"])          # F1 fix: someone must vote
    if not voters:
        d["pb_allocate"] = "ABSTAIN"
    elif f["money_confirmed"] == "yes" and f["costed_options_exceed"]:
        d["pb_allocate"] = "APPLY"
    elif f["choice_among_costed_items"]:                               # F6 fix: defined trigger
        d["pb_allocate"] = "CONDITIONAL"
    else:
        d["pb_allocate"] = "ABSTAIN"
    d["budget_capped_choice"] = "APPLY" if (f["hard_cap"] and f["options"] >= 2 and d["pb_process"] == "ABSTAIN") else "ABSTAIN"
    return d, notes


def gate_eb(f: dict) -> tuple[str, list[str]]:
    """Ordered evaluation (F3 fix); unknown preconditions become questions (F4 fix);
    plan-to-routine only for learning objectives (F2 fix)."""
    notes = []
    # Step 1: foundational or behind -> Tier 1 cards with confirmed preconditions
    if f["foundational"] or f["below_level"] == "yes":
        confirmed, unknown = [], []
        def check(card, conds):
            vals = [f[c] if isinstance(f[c], str) else ("yes" if f[c] else "no") for c in conds]
            if all(v == "yes" for v in vals):
                confirmed.append(card)
            elif all(v in ("yes", "unknown") for v in vals):
                unknown.append(card)
        check("level-grouping", ["below_level", "protected_slot"])
        check("tutoring", ["below_level", "volunteers"])
        if f["early_reading"]:
            confirmed.append("akshara")
        if f["fidelity_relevant"]:
            check("fidelity-loop", ["state_materials"])
        if confirmed:
            if unknown:
                notes.append(f"open questions for: {unknown}")
            return "APPLY", notes
        if unknown:
            notes.append(f"CONDITIONAL: ask about {unknown}")
            return "CONDITIONAL", notes
    # Step 2: subject teaching -> Tier 2 pilot
    if f["subject_teaching"]:
        return "PARTIAL", notes
    # Step 3: planning-only with a learning objective -> plan-to-routine
    if f["planning_only"] and f["objective_is_learning"]:
        return "PARTIAL", notes
    # Step 4
    return "ABSTAIN", notes


def run(f: dict) -> tuple[dict, list[str]]:
    d, notes = {}, []
    d["connected_learning"], n1 = gate_cl(f)
    pb, n2 = gate_pb(f)
    d.update(pb)
    d["evidence_based"], n3 = gate_eb(f)
    return d, n1 + n2 + n3


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    short = {"connected_learning": "CL", "pb_process": "PBp", "pb_prioritise": "PBv", "pb_allocate": "PBa",
             "budget_capped_choice": "BCC", "evidence_based": "EB"}
    print(f"{'case':38} " + " ".join(f"{short[g]:>12}" for g in GATES))
    outside = 0
    for c in cases:
        d, notes = run(c["facts"])
        cells = []
        for g in GATES:
            ok = d[g] in c["acceptable"].get(g, [d[g]])
            exact = d[g] == c["expected"].get(g, d[g])
            outside += not ok
            cells.append(f"{('✔' if exact else '~' if ok else '✘')} {d[g][:10]:>10}")
        print(f"{c['id']:38} " + " ".join(cells))
        for n in notes:
            print(f"{'':40}- {n}")
    print(f"\n{outside} decision(s) outside the acceptable set. ✔ exact · ~ acceptable · ✘ outside")
    return 1 if (args.strict and outside) else 0


if __name__ == "__main__":
    sys.exit(main())

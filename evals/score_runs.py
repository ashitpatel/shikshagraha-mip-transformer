#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Score fit-check outputs produced outside run_gates.py (e.g. by agents or a chat assistant).

    python3 evals/score_runs.py evals/runs/<folder>/out

Each file in the folder is <fixture-id>.json containing at least
{"gate_cl": {...}, "gate_pb": {...}, "gate_eb": {...}} in the formats specified by
prompts/30-gate-cl.md, 31-gate-pb.md and 32-gate-eb.md. Writes summary.md next to the folder.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "evals" / "gate_fixtures.json"
GATES = ["connected_learning", "pb_process", "pb_prioritise", "pb_allocate", "budget_capped_choice", "evidence_based"]
PB_GATES = GATES[1:5]


def decisions(out: dict) -> dict:
    d = {"connected_learning": (out.get("gate_cl", {}).get("connected_learning") or {}).get("decision"),
         "evidence_based": (out.get("gate_eb", {}).get("evidence_based") or {}).get("decision")}
    for g in PB_GATES:
        d[g] = (out.get("gate_pb", {}).get(g) or {}).get("decision")
    return {k: (v.split()[0].upper() if isinstance(v, str) and v else v) for k, v in d.items()}


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    fixtures = {f["id"]: f for f in json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"]}
    rows, exact, accept, total, missing = [], 0, 0, 0, []
    for fid, fx in fixtures.items():
        p = folder / f"{fid}.json"
        if not p.exists():
            missing.append(fid)
            continue
        got = decisions(json.loads(p.read_text(encoding="utf-8")))
        cells = []
        for g in GATES:
            e, ok = got[g] == fx["expected"][g], got[g] in fx["acceptable"][g]
            exact += e
            accept += ok
            total += 1
            cells.append(f"{'✔' if e else '~' if ok else '✘'} {got[g]}" + ("" if e else f" (exp {fx['expected'][g]})"))
        rows.append(f"| {fid} | " + " | ".join(cells) + " |")
    lines = [f"# Fit-check results: {folder.parent.name}", "",
             "| Fixture | " + " | ".join(GATES) + " |", "|---|" + "---|" * len(GATES), *rows, ""]
    if total:
        lines.append(f"**Exact:** {exact}/{total} ({exact/total:.0%}) · **Acceptable:** {accept}/{total} ({accept/total:.0%}) · "
                     f"**Outside:** {total-accept}")
    if missing:
        lines.append(f"\nMissing outputs: {', '.join(missing)}")
    lines.append("\n✔ exact · ~ acceptable alternative · ✘ outside the acceptable set")
    text = "\n".join(lines) + "\n"
    (folder.parent / "summary.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

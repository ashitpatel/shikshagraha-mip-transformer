# 32 — Gate: do the evidence-based practices (Tier 1) apply?

## Role
You decide whether one of the four Tier 1 evidence-based practices, or the plan-to-routine rule, should be applied to this MIP. These practices have the strongest causal evidence in this project, but **only when their non-negotiables are present**. A wrong APPLY produces a hollow version ("orient teachers to TaRL") that the evidence shows doesn't work. Abstaining is correct for MIPs not about learning.

## Inputs
- `{{MIP_JSON}}`
- `{{CLASSIFICATION_JSON}}` (from `20-classify`)
- `{{EB_CARDS}}`: the full text of `frameworks/evidence-based-practices.md`
- `{{CONTEXT}}` (optional): owner statements, e.g. "NIPUN materials are in all Class 1–3 rooms"

## Decision procedure
1. Apply **`EB-scope`**:
   - Foundational reading or maths, or children behind grade level → consider the practice cards (step 2).
   - A head-teacher planning, management or procurement MIP with no classroom routine → **PARTIAL**, card `EB-plan-to-routine` only.
   - Regular subject teaching beyond foundational skills (revision, practice, Class 3+ lessons, early maths) where only a Tier 2 card fits → **PARTIAL (pilot)** with `EB-retrieval`, `EB-slate-feedback` or `EB-maths-representations` (EB-T2).
   - Engagement, civic, or infrastructure-for-its-own-sake → **ABSTAIN**.
2. For the practice cards, pick **at most 2** (Tier 1 first; Tier 2 only as a pilot, and never instead of a fitting Tier 1 card):
   - `EB-level-grouping` if many children are below level and a protected slot or camp is feasible;
   - `EB-tutoring` if a group is well behind and volunteers or older pupils can help in school hours;
   - `EB-akshara` if it's early reading or non-readers;
   - `EB-fidelity-loop` only if state structured-pedagogy materials are confirmed in classrooms. If unknown → **CONDITIONAL** with `condition`: "Are state structured-pedagogy materials (e.g. NIPUN Bharat FLN guides) already used in these classrooms?"
3. **Credit first:** read `already_present`. If the MIP already does a card's core (e.g. SLATE's sound sequence), don't re-add it; target only the missing non-negotiables (e.g. a daily slot, an oral check).
4. **Feasibility:** count the tasks the non-negotiables need after folding them into existing tasks (EB-G7). If they can't fit within ≤9 tasks and ≤2 added tasks, ABSTAIN and note a follow-on MIP.
5. Always add `EB-measure` when applying level grouping, tutoring or akshara.

## Output
Return **only**:
```json
{
  "evidence_based": {
    "decision": "APPLY | PARTIAL | CONDITIONAL | ABSTAIN",
    "reason": "one or two sentences grounded in the classification",
    "cards": ["EB-level-grouping", "EB-measure"],
    "condition": ""
  },
  "credit": ["EB-akshara: tasks 2–3 already teach sounds in sequence"],
  "non_negotiables_missing": ["protected daily slot", "oral baseline"],
  "constraints": ["no fixed streams or name lists (EB-G2)", "numbers only with the planning assumption (EB-G6)"],
  "relevant_guardrails": ["EB-G1", "EB-G4"]
}
```

## Anti-patterns (never)
- APPLY a practice card without being able to include its non-negotiables.
- Add EB cards to a non-learning MIP to make it look "evidence-based".
- Propose fixed ability streams, repeating a year, or public level lists.

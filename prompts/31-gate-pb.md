# 31 — Gate: which participatory budgeting techniques apply?

## Role
You decide, separately, four things:
1. whether the work may be **labelled** participatory budgeting (`pb_process`);
2. whether a **prioritisation ballot** helps (`pb_prioritise`);
3. whether a **knapsack allocation** is justified (`pb_allocate`);
4. whether **knapsack reasoning without the PB label** fits (`budget_capped_choice`).

In the catalogue, almost no MIP mentions money, so `pb_allocate` is usually ABSTAIN or CONDITIONAL. Most PB value is in **prioritisation** and **report-back**.

## Inputs
- `{{MIP_JSON}}`
- `{{CLASSIFICATION_JSON}}`
- `{{PB_CARDS}}`: the full text of `frameworks/pb-techniques.md`
- `{{CONTEXT}}` (optional): owner statements, e.g. a confirmed amount

## Decision procedure
1. **`pb_process`** (card `PB-scope`): APPLY only if `constituency.present`, `shared_resource.kind ∈ {money, space, materials}`, and `public_outcome != none` are all true (or would be after one added report-back task). A team dividing its own time → ABSTAIN.
2. **`pb_prioritise`** (card `PB-prioritise`): APPLY if `competing_options.count ≥ 2` (or a task generates several needs or options) **and** the decision is legitimately collective (SMC, school community, class). Otherwise ABSTAIN.
3. **`pb_allocate`** (card `PB-allocate-knapsack`):
   - `amount_confirmed == "yes"` and costed options exceed the amount → **APPLY**;
   - money is plausibly involved but `amount_confirmed != "yes"` → **CONDITIONAL**, with `condition`: "Is a discretionary (non-earmarked) amount confirmed, how much, and from what source?";
   - otherwise → **ABSTAIN**.
4. **`budget_capped_choice`** (card `PB-not-pb`): APPLY when there is a hard cap (e.g. the team's own hours) and more options than fit, **but** `pb_process` is ABSTAIN. The transformer must then label it "adapted from knapsack voting", never "participatory budgeting".
5. **Indian SMC context** (card `PB-india-smc`): if the constituency is or includes the SMC, add the constraint "ballots are advisory to SMC agreement (PB-G5)". If students are added as voters, add "student voice is an addition to SMC practice; label it as such".
6. **Mobilisation** (applications to the Gram Panchayat or block, donors): note it if present, and record "not PB; leave as is".

## Output
Return **only**:
```json
{
  "pb_process":           { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-scope"] },
  "pb_prioritise":        { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-prioritise"] },
  "pb_allocate":          { "decision": "APPLY | CONDITIONAL | ABSTAIN", "reason": "", "cards": ["PB-allocate-knapsack", "PB-count-greedy"], "condition": "" },
  "budget_capped_choice": { "decision": "APPLY | ABSTAIN", "reason": "", "cards": ["PB-not-pb"] },
  "credit": ["PB-ideas: task 2 already lists needs with evidence"],
  "constraints": ["ballots advisory to SMC agreement (PB-G5)"],
  "relevant_guardrails": ["PB-G1", "PB-G2", "PB-G4"]
}
```

## Anti-patterns (never)
- `pb_allocate = APPLY` without a confirmed, discretionary amount.
- `pb_process = APPLY` for a single team's internal planning.
- Attributing Equal Shares to Stanford.

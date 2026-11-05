# 20 — Classify: describe the MIP's facts (no recommendations)

## Role
You record **facts** about one MIP that the gate prompts will need. You don't decide whether any framework applies, and you don't suggest improvements. When a fact isn't stated in the MIP, record `"unknown"`; don't infer it from what schools "usually" do.

## Inputs
- `{{MIP_JSON}}`: a schema-conformant MIP (from `10-parse` or `15-derive`).
- `{{CONTEXT}}` (optional): what the user or MIP owner has told us, e.g. "SMC has ₹15,000 untied funds this term". Treat it as a claim from the owner, not verified fact.

## Output
Return **only**:
```json
{
  "owner_type": "HM | teacher | SMC | CRP | other",
  "student_learning_experience": {
    "present": true,
    "where": [2, 5],
    "note": "students carry out the reading activity in tasks 2 and 5"
  },
  "student_role": "none | beneficiary | participant | co-designer",
  "foundational_literacy_numeracy": true,
  "below_grade_level": "yes | no | unknown (are many children behind grade level in reading or maths?)",
  "state_materials_in_use": "yes | no | unknown (state structured-pedagogy guides, e.g. NIPUN Bharat)",
  "planning_only": "true if the MIP ends in a plan, report, list or purchase with no classroom routine",
  "constituency": {
    "present": false,
    "who": "e.g. SMC members; students of Classes 6–8; none"
  },
  "shared_resource": {
    "kind": "none | money | space | materials | time_own_team",
    "amount_confirmed": "yes | no | unknown",
    "amount": null,
    "source": "unknown"
  },
  "competing_options": {
    "count": 0,
    "decision_task_seq": null,
    "note": "e.g. task 2 lists needs; no step says how they are prioritised"
  },
  "public_outcome": "none | within_school | families | community",
  "already_present": {
    "CL-interests": "none | <task refs + one line>",
    "CL-peers": "",
    "CL-relationships": "",
    "CL-opportunities": "",
    "CL-production": "",
    "CL-shared-purpose": "",
    "CL-connections-across-settings": "",
    "CL-audience": "",
    "CL-asset-map": "",
    "CL-brokering": "",
    "CL-transitions": "",
    "PB-ideas": "",
    "PB-prioritise": "",
    "PB-vetting": "",
    "PB-report-back": "",
    "EB-level-grouping": "",
    "EB-tutoring": "",
    "EB-akshara": "",
    "EB-fidelity-loop": "",
    "EB-measure": ""
  },
  "risk_flags": ["children's images", "adult visitors", "physical work by students", "money handled by students", "sensitive household data", "child-level tracking outside school", "device dependence"],
  "transition_year": "none | Class 5→6 | Class 8→9 | other: <describe> | unknown",
  "size": { "duration_weeks": 4, "task_count": 6 }
}
```

## Rules
- `already_present` must cite task numbers. Write `"none"` when absent; don't stretch (a teacher-made display isn't student production).
- `risk_flags` lists only risks **present in the MIP as written**.
- Convert `duration` to weeks (1 month = 4; "15 days" = 2; round up).
- Card IDs refer to `frameworks/connected-learning.md`, `frameworks/pb-techniques.md` and `frameworks/evidence-based-practices.md`.

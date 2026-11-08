# Golden examples

Twelve reference cases for the transformer's gates and transformations. Sources are listed in [../sources.md](../sources.md); the schema is [../../schema/mip.schema.json](../../schema/mip.schema.json).

| # | File | Input type | Connected Learning | PB: prioritise / process | PB: allocate (knapsack) | What it tests |
|---|---|---|---|---|---|---|
| 1 | [civics-lab.md](civics-lab.md) | New MIP (generation) | APPLY | APPLY | APPLY | The full PB case: real fund, constituency, public result; counting rule; student safeguarding |
| 2 | [time-knapsack.md](time-knapsack.md) | New MIP (generation) | APPLY | **ABSTAIN** | APPLY (technique only) | Borrowing knapsack reasoning without the PB label |
| 3 | [slate-language-adventure.md](slate-language-adventure.md) | Resource → derived MIP | APPLY (augment) | ABSTAIN | ABSTAIN | Keep the objective (foundational literacy); no invented evidence; offline by default |
| 4 | [learning-centre-playbook.md](learning-centre-playbook.md) | Resource → derived MIP | APPLY (targeted) | ABSTAIN | ABSTAIN | Credit what exists; interests + connections across settings; visitor safeguarding |
| 5 | [school-development-plan.md](school-development-plan.md) | Resource (SDP process) | **ABSTAIN** | APPLY (partial) | CONDITIONAL | Don't use the CL label on governance work; the SMC is the decision body |
| 6 | [catalogue-school-resources.md](catalogue-school-resources.md) | **Catalogue MIP** | **ABSTAIN** | APPLY | CONDITIONAL | Prioritise vs. allocate vs. mobilise; the ballot informs SMC agreement |
| 7 | [catalogue-real-world-projects.md](catalogue-real-world-projects.md) | **Catalogue MIP** | APPLY | ABSTAIN | ABSTAIN | Students move from beneficiaries to choosers, peers and presenters within the same task skeleton |
| 8 | [transition-class8-to-9.md](transition-class8-to-9.md) | Seed (catalogue pattern re-targeted) | APPLY | ABSTAIN | ABSTAIN | Ecosystem cards (transitions, brokering, asset map); **critic test**: a tracking variant must fail C19 |
| 9 | [catalogue-reading-by-level.md](catalogue-reading-by-level.md) | **Catalogue MIP** | APPLY (deferred) | ABSTAIN | ABSTAIN | **Evidence-based (level grouping + oral baseline/endline): APPLY**. Every non-negotiable included; EB takes priority over CL; **critic tests**: hollow "orient on TaRL" and fixed-stream variants must fail C20 |
| 10 | [catalogue-tutoring-chaupal.md](catalogue-tutoring-chaupal.md) | **Catalogue MIP** | PARTIAL (deferred) | ABSTAIN | ABSTAIN | **Evidence-based (in-school volunteer tutoring + oral check): APPLY**. A community event becomes daily in-school tutoring; **critic test**: evening or at-home one-to-one tutoring must fail C20 and C10 |
| 11 | [catalogue-letters-and-sounds.md](catalogue-letters-and-sounds.md) | **Catalogue MIP** | APPLY (deferred) | ABSTAIN | ABSTAIN | **Evidence-based (daily sound-symbol block + oral check): APPLY**. App made optional, objective kept; **critic tests**: drill-only and device-dependent variants |
| 12 | [catalogue-observation-fidelity-loop.md](catalogue-observation-fidelity-loop.md) | **Catalogue MIP** | ABSTAIN | ABSTAIN | ABSTAIN | **Evidence-based (feedback loop on state lesson guides): CONDITIONAL → APPLY** once materials are confirmed; **critic test**: an inspection-style rating form must fail C20 |

## Conventions every example follows
- **Credit what's there before adding:** an "Already present" section comes before any change.
- **Task table:** each task is marked *unchanged / modified / added*, with the principle or technique it serves and a guardrail where relevant.
- **Size limits** (from the catalogue profile): ≤8 weeks, ≤9 tasks, ≤2 added tasks, no new paid inputs unless a budget is confirmed. Longer designs become chained MIPs.
- **The MIP owner stays an adult** (HM, teacher, SMC). Students get roles inside tasks.
- **Rationale:** only supportable claims, and effects are labelled untested.
- **"Before" content:** summarised or paraphrased from the source and referenced by ID; the harness loads the originals.

## Gate naming
Examples written before the prompts use column labels such as "PB: prioritise / process". The machine-readable gate names (schema `x_transform.gates` and the gate prompts) are: `connected_learning`, `pb_process`, `pb_prioritise`, `pb_allocate`, `budget_capped_choice`, and (added after the evidence scan) `evidence_based`. When building the gate eval, map each example's table to these six. The expected `evidence_based` answers are in `../gate_fixtures.json`; the example files don't cover them yet.

## Still to do
- ~~Write the framework reference cards~~ Done: [../../frameworks/connected-learning.md](../../frameworks/smt/connected-learning.md) and [../../frameworks/pb-techniques.md](../../frameworks/smt/pb-techniques.md). Every card ID cited in the examples is defined. Citations were verified on 2026-11-04 (each card file has a verification log). Outstanding: the RTE wording should be checked against the gazette text.
- Have practitioners review the expected gate decisions before using them as ground truth.
- Add more **abstain** cases from the catalogue (e.g. an HR or HM-admin MIP where neither framework applies) so gate accuracy is tested on the common case.

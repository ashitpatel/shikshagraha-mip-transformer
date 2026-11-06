# Decision path analysis: how the agent chooses a method for a MIP

*Analysis of the instructions as of commit `1a938a6`, 6 November 2026. No live model was run; this checks the rules as written.*

## Verdict

**The decision path is mostly correct, but not yet reliable enough to trust unattended.** Applied carefully, the written rules reproduce the intended decisions for all 12 reference cases (72 decisions: 67 exact, 5 acceptable alternatives, 0 wrong).

Edge cases expose **three rule defects**:
- a budget ballot can be selected when there's no one to vote;
- the "plan-to-routine" rule fires on MIPs that aren't about learning;
- the evidence-based scope rules overlap, with no order of evaluation.

Four further problems are about **ambiguity rather than wrong logic**:
- undefined facts;
- no rule for unknown facts;
- a priority rule that ignores tier and objective;
- a reviewer that can't catch a wrong choice of method.

There are also two **inconsistencies between surfaces**: the agent kit says 19 checks where there are 20, and a card and its prompt disagree on one threshold. All are fixable with small text changes (see "Recommended fixes").

---

## 1. Approach used

The analysis treats the instructions as a specification and checks them in five steps.

| Step | What was done | Why |
|---|---|---|
| **1. Extract the decision path** | Read every instruction surface that decides which method to use, and wrote the rules down as one procedure: facts → six fit-check decisions → card selection → priority when space is tight → review. The surfaces: the agent-kit core instructions (what free-tier and custom assistants follow), `prompts/20-classify`, `30-gate-cl`, `31-gate-pb`, `32-gate-eb` and `40-transform`, the three scope cards (`CL-scope`, `PB-scope`, `EB-scope`), and the review checklist. | You can only verify a path you've written down precisely. |
| **2. Check the specification itself** | Checked the extracted rules for: **consistency** across surfaces (do the agent kit, prompts and cards say the same thing?); **completeness** (does every combination of facts lead to a decision?); **determinism** (are terms and thresholds defined?); **ordering** (when rules overlap, is precedence stated?); **reachability** (can every decision occur, including "doesn't apply"?); and **alignment** with the evidence ranking and the guardrails. | Most failures in instruction-following systems come from gaps and overlaps in the rules, not from the model. |
| **3. Build an executable model** | Transcribed the fit-check rules into a small deterministic program, [`evals/decision_model.py`](../evals/decision_model.py), as literally as possible. Every place where the text had to be interpreted is marked `AMBIGUITY` in the code. The program also flags rule gaps it hits at run time. | Running the rules exposes overlaps and gaps that reading misses, and makes the check repeatable after edits. |
| **4. Test it on cases** | Ran the model on 20 cases ([`evals/decision_cases.json`](../evals/decision_cases.json)). Twelve mirror the reference fixtures, compared with their expected and acceptable answers. Eight are **edge cases** built to probe boundaries: money with no group; foundational maths with unknown levels; a head-teacher FLN plan; senior-secondary revision; a class vote with no money; an HR plan; a transition with children behind; an event with logistics. Inputs are hand-coded *classification facts*, isolating the decision logic from the model's reading of the MIP. | The fixtures test the intended paths; the edge cases test what the rules do where no one has looked. |
| **5. Classify and prioritise findings** | Each finding records where it occurs, how it was found (reading or model run), a concrete failure scenario, severity, and a proposed fix. | So fixes can be targeted and re-verified with the same model. |

**Severity scale:**
- **High:** produces a wrong or unsafe choice of method.
- **Medium:** produces inconsistent or unpredictable choices, or lets a wrong choice through review.
- **Low:** wording or traceability.

---

## 2. The decision path as specified

```
MIP ──► size check (≤8 weeks, ≤9 tasks; else take one slice)
     ──► classify: facts only (student learning? owner? group? resource? money confirmed? options?
                    below grade level? foundational? state guides in use? planning-only? transition year?
                    already present? risks?)
     ──► six fit checks, decided independently:
           EB  evidence-based practices   APPLY / PARTIAL (plan-to-routine or Tier 2 pilot) / CONDITIONAL / ABSTAIN
           CL  Connected Learning         APPLY / PARTIAL / ABSTAIN
           PB  process · prioritise · allocate · budget-capped choice (each APPLY / CONDITIONAL / ABSTAIN)
     ──► card selection (EB ≤2 practice cards + oral check; CL ≤3; PB techniques as decided)
     ──► revise within limits; when space runs out: EB → PB → CL, rest becomes a follow-on MIP
     ──► review (C1–C20); ≤2 revision rounds; else return the original with reasons
```

**What holds up:**
- Every decision value is reachable.
- "Doesn't apply" is reachable on every fit check.
- The all-abstain path ends cleanly with the original card.
- The safety rules don't depend on the choice of method; the review enforces them whatever was chosen.
- The order of the evidence ranking (EB above PB and CL as learning levers) is reflected in the priority rule.

---

## 3. Results of the executable model

`python3 evals/decision_model.py` (✔ exact, ~ acceptable alternative, ✘ outside the acceptable set):

| Case | CL | PB process | PB vote | PB allocate | Budget-capped | EB |
|---|---|---|---|---|---|---|
| 1 Civics Lab (seed) | ~ APPLY | ✔ | ✔ | ✔ | ✔ | ~ PARTIAL¹ |
| 2 Time-Knapsack (seed) | ✔ | ✔ | ✔ | ✔ | ✔ | ~ PARTIAL² |
| 3 SLATE Land 1 | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| 4 Learning Centre | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| 5 School Development Plan | ✔ | ✔ | ✔ | ✔ CONDITIONAL | ✔ | ✔ PARTIAL |
| 6 School resources | ✔ | ✔ | ✔ | ✔ CONDITIONAL | ✔ | ✔ PARTIAL¹ |
| 7 Real World Projects | ✔ | ✔ | ✔ | ✔ | ✔ | ~ PARTIAL² |
| 8 Transition visit | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| 9 Reading by level | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| 10 Chaupal → tutoring | ~ APPLY | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| 11 Letters and sounds | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| 12 Observation loop | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| E1 HM buys books, money confirmed, no group | ✔ | ✔ | ✔ | **✘ APPLY** | ✔ | ~ PARTIAL¹ |
| E2 Class 2 maths, levels unknown | ✔ | ✔ | ✔ | ✔ | ✔ | ~ PARTIAL³ |
| E3 HM FLN plan, children behind | ✔ | ✔ | ✔ | ✔ | ✔ | ~ APPLY⁴ |
| E4 Class 11 chemistry revision | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ PARTIAL (pilot) |
| E5 Class vote on a field trip | ✔ | ✔ | ✔ APPLY | ✔ | ✔ | ✔ |
| E6 HR "teacher motivation" plan | ✔ | ✔ | ✔ | ✔ | ✔ | **✘ PARTIAL¹** |
| E7 Transition + children behind | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY |
| E8 Teacher Mela with logistics | ✔ | ✔ | ✔ | **✘ CONDITIONAL** | ✔ | ✔ |

Notes:
1. The plan-to-routine rule fired on a MIP whose objective isn't learning (finding F2).
2. A Tier 2 pilot fired on ordinary subject teaching; it's acceptable but shows how broad that branch is (finding F5).
3. A foundational MIP where no Tier 1 card fits fell through to Tier 2; the fall-through isn't specified (finding F3).
4. Both the "foundational" and "planning-only" branches match; the outcome depends on reading order (finding F3).

**Fixture totals:** 72 decisions, 67 exact, 5 acceptable, 0 outside. **Edge-case totals:** 48 decisions, 3 outside the intended outcome (E1, E6, E8).

---

## 4. Findings

| # | Severity | Finding | Where | How found | Failure scenario | Fix |
|---|---|---|---|---|---|---|
| **F1** | **High** | **A budget ballot can be chosen with no one to vote.** `pb_allocate` requires only confirmed money and more options than money, not a constituency or a collective decision. | `31-gate-pb` step 3; core instructions question 4 | Model run (E1) | An HM with a confirmed ₹15,000 for library books gets a "knapsack ballot" step that no group can run, or the HM "votes" alone. | Require `pb_process = APPLY` or `pb_prioritise = APPLY` before `pb_allocate` can be APPLY or CONDITIONAL; otherwise ABSTAIN. |
| **F2** | **High** | **The plan-to-routine rule over-triggers.** EB-scope (c) fires for *any* head-teacher planning, management or procurement MIP. That contradicts the card's own anti-pattern: "adding an EB card to a MIP whose objective isn't learning". | `EB-scope`; `32-gate-eb` step 1 | Model run (E6; fixtures 1 and 6) | An HR plan ("teacher motivation"), a shared-space improvement or an infrastructure list gets a forced classroom routine. | Limit (c) to planning MIPs **whose objective concerns learning or teaching** (SDP, academic plans, FLN plans). Otherwise ABSTAIN. Add `objective_is_learning` to `20-classify`. |
| **F3** | **High** | **The evidence-based scope branches overlap and aren't ordered.** Step 1 lists four branches (foundational or behind; planning-only; Tier 2; engagement or infrastructure) that can match together, with no precedence. There's also no fall-through when "foundational" matches but no Tier 1 card fits. | `32-gate-eb` step 1; `EB-scope` | Model run (fixtures 1, 6, 10; E2, E3, E7) | The Chaupal (community event *and* children behind) can ABSTAIN or APPLY depending on which branch the model reads first. An HM FLN plan can get "plan-to-routine only" instead of a practice card. | State the order: (1) foundational or behind → Tier 1 cards; (2) if none fits → Tier 2 pilot if subject teaching, else ask (F4); (3) planning-only with a learning objective → plan-to-routine; (4) else ABSTAIN. "Engagement or infrastructure" applies only if nothing above matched. |
| **F4** | Medium | **No rule for unknown facts.** Level grouping needs `below_level` and a protected slot; tutoring needs volunteers. These are usually *unknown* from a catalogue row, and only the fidelity loop has a CONDITIONAL path. | `32-gate-eb` step 2; `20-classify` | Model run (E2, fixture 12 note) | A Class 2 maths MIP with unknown levels silently drops level grouping, or applies it on a guess. | Add: if a Tier 1 card's precondition is *unknown*, return CONDITIONAL with the question ("Are many children below grade level?", "Can the HM protect a daily slot?", "Are volunteers available?"). |
| **F5** | Medium | **The priority rule ignores tier and objective.** "EB non-negotiables first, then PB, then CL" puts a **Tier 2 pilot** ahead of the method that serves the MIP's stated objective (e.g. CL for "Real World Projects", PB for the Civics Lab). | `40-transform` step 3; core instructions step 5 | Reading, plus fixture 7 and E4 | A projects MIP loses its interest-driven redesign to a retrieval-quiz pilot. | Priority: (1) EB **Tier 1** non-negotiables; (2) the method that serves the MIP's stated objective; (3) PB; (4) Tier 2 pilots; (5) CL. |
| **F6** | Medium | **"Money plausibly involved" is undefined**, so `pb_allocate` CONDITIONAL fires on any MIP with logistics or purchases. | `31-gate-pb` step 3 | Model run (E8) | A Teacher Mela gets a spurious "Is a discretionary amount confirmed?" question. | Define it as: "the MIP chooses among costed items for a shared purpose (procurement lists, improvement projects)". Event logistics and routine running costs don't count. |
| **F7** | Medium | **The card and its prompt disagree.** `CL-scope` gives PARTIAL for HM- or SMC-owned MIPs where students take part. `30-gate-cl` gives PARTIAL only when students appear in **exactly one** task, so HM MIPs with two or more student tasks get APPLY. | `CL-scope` vs `30-gate-cl` step 1 | Reading, confirmed by the model (fixtures 1 and 10: APPLY, where PARTIAL is expected) | HM-owned community MIPs get full Connected Learning redesigns that the card meant to limit. | Align them: PARTIAL for HM- or SMC-owned MIPs whenever students take part, with at most one target principle. |
| **F8** | Medium | **The reviewer can't catch a wrong choice of method.** The 20 checks verify that a revision is *consistent with* the fit-check decisions (C8) and well-formed. None checks whether a decision was *right* given the facts (a missed method, a wrong abstain), or whether the priority rule was followed. "REJECT: wrong gate applied" exists, but with no criteria. | `50-critic`; review checklist | Reading | A wrong ABSTAIN on a reading MIP with children behind passes review untouched. | Add **C21: decision check**. Re-derive each fit-check decision from the classification facts using the scope cards; flag mismatches, an unfollowed priority, and fitting methods left out without a "deferred" note. |
| **F9** | Medium | **The agent kit says "checks C1–C19"**, but the checklist and critic have **C20** (the evidence-based essentials). Assistants may stop at 19 and skip the check that prevents hollow evidence-based practices. | `agent-kit/src/core-instructions.md` and every generated package | Text search | A free-tier assistant reviews against 19 checks and passes a hollow "orient on TaRL" plan. | Change it to "C1–C20", and add a build check that the number in the instructions matches the checklist. |
| F10 | Low | The core instructions omit two criteria the prompts use: "legitimately collective" for a priority vote, and "public result" in the facts list. | Core instructions step 4 | Reading | A free-tier assistant adds a vote to a decision that isn't a group's to make. | Add both to step 4. |
| F11 | Low | The core instructions list evidence-based practices as **question 6** but say "check these first". | Core instructions step 4 | Reading | Smaller models follow list order and decide EB last. | Move EB to question 1. |
| F12 | Low | No machine-readable "deferred" or "pilot" state. Decisions show APPLY even when deferred for space, and "PARTIAL (pilot)" is free text. | `schema/mip.schema.json` gate definition | Reading | Logs and analyses can't tell an applied method from a deferred one, or a pilot from plan-to-routine. | Add `deferred: boolean` and `tier: 1 \| 2` to the gate object. |
| F13 | Low | The `pb_process` public-outcome condition is effectively always met ("or would be after one added report-back task"). | `31-gate-pb` step 1 | Model transcription | None harmful, because a report-back is always added. The condition just doesn't discriminate. | Keep it, but say explicitly that a report-back task satisfies it. |

---

## 5. Limitations of this analysis

- **It checks the rules, not the model.** It doesn't show how a given assistant actually follows them. Live runs (`evals/run_gates.py`) and trials of the agent kit are still needed.
- **The classification facts are hand-coded by the analyst.** Several findings (F2, F3, F6, F7) partly reflect how hard it is to classify reliably. A model could misjudge facts like "student learning present" or "planning-only", which the decision rules then amplify.
- **The executable model involves interpretation.** Each interpretation is marked in the code, so others can challenge it.
- **The edge cases' "intended outcomes" are the analyst's reading** of the cards' intent and anti-patterns. Practitioners should confirm them.
- **Only method selection was analysed.** Transform quality, teacher-card rendering and language quality are out of scope.

---

## 6. Recommended fixes, in order

1. **F1, F2, F3:** fix the three rule defects in `31-gate-pb`, `32-gate-eb`, `EB-scope` and the core instructions. Add `objective_is_learning` to `20-classify`.
2. **F9:** correct "C1–C19" to "C1–C20" and add a build check.
3. **F4, F6, F7:** add CONDITIONAL for unknown preconditions, define "money plausibly involved", and align `CL-scope` with `30-gate-cl`.
4. **F5, F8:** the refined priority rule and a new critic check C21.
5. **F10–F13:** wording and schema clean-ups.
6. Re-run `python3 evals/decision_model.py --strict` (update the model to the fixed rules and add E1, E6 and E8 to `gate_fixtures.json`), then run the live fit-check test.

---

## 7. Fixes applied (6 November 2026)

All 13 findings were fixed. The executable model was updated to the new rules, and every case was re-run.

| # | Fix | Files |
|---|---|---|
| F1 | A budget ballot now requires a voting group: `pb_allocate` is ABSTAIN unless `pb_process` or `pb_prioritise` is APPLY. | `31-gate-pb`, `PB-allocate-knapsack` card, core instructions (question 5) |
| F2 | Plan-to-routine applies only when the MIP's objective is about learning or teaching. A new classify fact, `objective_is_learning`, supports this. | `32-gate-eb`, `EB-scope` and `EB-plan-to-routine` cards, `20-classify`, core instructions |
| F3 | Evidence-based scope is evaluated in a fixed order, first match wins: Tier 1 with confirmed preconditions → CONDITIONAL if a precondition is unknown → Tier 2 pilot → plan-to-routine (learning objectives only) → ABSTAIN. If a plan-to-routine routine is a Tier 1 practice, it must include all its non-negotiables or become a follow-on MIP. | `32-gate-eb`, `EB-scope` card, core instructions |
| F4 | Unknown preconditions produce CONDITIONAL and a question. New classify facts: `protected_slot_feasible`, `volunteers_available` (yes/no/unknown), plus a rule to write "unknown" rather than guess. | `20-classify`, `32-gate-eb`, core instructions |
| F5 | New priority when space is tight: Tier 1 essentials → the method serving the MIP's objective → other PB → Tier 2 pilots → other CL. Methods that are applied but don't fit are marked `deferred: true`. | `40-transform`, core instructions, UX docs |
| F6 | "Money plausibly involved" is replaced by a defined fact, `choice_among_costed_items` (a procurement list or improvement options; not event logistics or running costs). | `20-classify`, `31-gate-pb`, core instructions |
| F7 | The Connected Learning card and its prompt now agree: PARTIAL when an HM- or SMC-owned MIP has *incidental* student participation (new fact `students_core`); APPLY when students' learning is the main activity. | `30-gate-cl`, `CL-scope` card, core instructions |
| F8 | New critic check **C21 (decision check)**: re-derive each decision from the facts, and flag a missed or wrong method, a guessed precondition, an unfollowed priority, or an unrecorded deferral. The critic now receives the classification. | `50-critic`, review checklist |
| F9 | The agent kit names C1–C21. The build now fails if the number of checks named in the instructions doesn't match the checklist. | core instructions, `agent-kit/build.py` |
| F10 | The core instructions now include "legitimately collective" for votes, "a public result" in the facts, and "class vote"/"group vote" wording when the PB label doesn't apply. | core instructions, `31-gate-pb` |
| F11 | Evidence-based practices are now question 1 in the agent kit. | core instructions |
| F12 | The gate schema gains `tier` (1 or 2) and `deferred` (boolean). | `schema/mip.schema.json`, `32-gate-eb` output, `40-transform` |
| F13 | It's now stated that an added report-back task satisfies the public-outcome condition. | `31-gate-pb` |

**Re-run** (`python3 evals/decision_model.py --strict`): **0 decisions outside the acceptable set** across all 20 cases, down from 3. The three former failures now come out as intended:
- **E1**, a budget ballot with no group: ABSTAIN.
- **E6**, an HR plan: no forced routine.
- **E8**, event logistics: no budget question.

Two edge cases changed for the better:
- **E2** (levels unknown) now asks instead of falling through to a pilot.
- **E3** (an HM FLN plan) now asks whether a daily slot can be protected.

Fixture 6 ("School resources") now expects EB ABSTAIN, because its objective is resources, not learning; PARTIAL remains acceptable if the owner frames the books or materials as serving learning. The three edge MIPs E1, E6 and E8 were added to `evals/gate_fixtures.json` as fixtures 13–15, so the live test covers them. The live test is now 60 calls.

**Still not verified:** whether a live model applies the fixed rules as the executable model does. Run `python3 evals/run_gates.py`.

---

## 8. Live test of the fixed rules (6 November 2026)

**Method.** No API key was available, so the fit-check stage was run with **15 fresh Claude agents in this session**, one per test input in `evals/gate_fixtures.json`.
- **Inputs:** each agent received only the plan and its context, written to answer-free input files.
- **Files allowed:** only `prompts/20-classify.md`, `30-gate-cl.md`, `31-gate-pb.md`, `32-gate-eb.md` and the three card files. Agents were barred from every file holding expected answers.
- **Steps:** each agent followed the classify prompt and then the three fit-check prompts exactly, and wrote JSON.
- **Scoring:** `evals/score_runs.py` scored the outputs against the expected and acceptable decisions (outputs are in `evals/runs/20261106-agents/`, which isn't committed).

This tests whether a Claude model applies the written rules. It doesn't test other assistants or free tiers.

**Results:**

| Fixture | connected_learning | pb_process | pb_prioritise | pb_allocate | budget_capped_choice | evidence_based |
|---|---|---|---|---|---|---|
| 1-civics-lab-seed | ✔ PARTIAL | ✔ APPLY | ✔ APPLY | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN |
| 2-time-knapsack-seed | ✔ APPLY | ✔ ABSTAIN | ✘ APPLY (exp ABSTAIN) | ✔ ABSTAIN | ✔ APPLY | ✔ ABSTAIN |
| 3-slate-land1 | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ APPLY |
| 4-playbook-august | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN |
| 5-sdp-process | ✔ ABSTAIN | ~ ABSTAIN (exp APPLY) | ✔ APPLY | ✘ ABSTAIN (exp CONDITIONAL) | ✔ ABSTAIN | ✔ PARTIAL |
| 6-catalogue-school-resources | ✔ ABSTAIN | ~ ABSTAIN (exp APPLY) | ✘ ABSTAIN (exp APPLY) | ✘ ABSTAIN (exp CONDITIONAL) | ✔ ABSTAIN | ✔ ABSTAIN |
| 7-catalogue-real-world-projects | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ~ PARTIAL (exp ABSTAIN) |
| 8-transition-class8-to-9-seed | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN |
| 9-catalogue-reading-by-level | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ APPLY |
| 10-catalogue-tutoring-chaupal | ~ APPLY (exp PARTIAL) | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ APPLY |
| 11-catalogue-letters-and-sounds | ✔ APPLY | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ APPLY |
| 12-catalogue-observation-fidelity-loop | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ APPLY |
| 13-edge-library-books-no-group | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ~ APPLY (exp ABSTAIN) | ✔ PARTIAL |
| 14-catalogue-teacher-motivation | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN |
| 15-catalogue-teacher-mela | ✔ ABSTAIN | ✔ ABSTAIN | ~ APPLY (exp ABSTAIN) | ✔ ABSTAIN | ✔ ABSTAIN | ✔ ABSTAIN |

**Exact:** 80/90 (89%) · **Acceptable:** 86/90 (96%) · **Outside:** 4

**Exact: 80/90 (89%). Acceptable: 86/90 (96%). Outside: 4.**

**What the misses showed** (from the agents' classification and reasons):

| # | Miss | Root cause | Fix (applied) |
|---|---|---|---|
| R1 | Team projects: priority vote APPLY for a 5-student team | "Legitimately collective" was read as *any* group, including a team deciding its own work | `collective_decision` is now defined in `20-classify`, `31-gate-pb`, the `PB-prioritise` card and the agent kit. It means the decision belongs by role or law to a group (school needs or shared money, space or materials → SMC; class or school-wide student choices). It holds even if one person currently decides. It excludes a team's or staff group's own work, and an HM's item choices within an agreed purpose. |
| R2 | School resources: priority vote ABSTAIN, budget ballot ABSTAIN (expected APPLY and CONDITIONAL) | The opposite reading: "collective" was taken to mean *currently decided by a group*, so the HM-only plan had no constituency, and F1's "someone must vote" then blocked the ballot | Same definition: competing school needs belong to the SMC even when the plan has the HM deciding alone, and the constituency is then the SMC |
| R3 | School Development Plan: budget ballot ABSTAIN (expected CONDITIONAL) | The definition of "choice among costed items" didn't mention development plans whose actions carry resource costs | The definition now includes "a school development or improvement plan whose actions carry resource costs" |

**Near-misses fixed at the same time:**
- **Lesson observation:** the agent reached the right answer (the feedback loop on state lesson guides) only through the planning branch, because the loop could be entered only via "foundational or behind". Step 1 now also triggers for **teaching-practice MIPs (observation, feedback, coaching) in classes using state guides**. Updated in `32-gate-eb`, `EB-scope`, the agent kit and the decision model.
- **The `tier` field for plan-to-routine** was set to 1 by one agent and left empty by another. It's now specified as null (plan-to-routine is a rule, not a practice).
- **Choosing Connected Learning targets** had no tie-break when more than 3 qualified. Added: prefer edits to existing tasks, then a fixed principle order.
- **An "off-site visit" risk flag** was improvised by one agent. It's now in the classify list.

**Acceptable alternatives worth watching** (not errors):
- Chaupal: CL APPLY rather than PARTIAL.
- Real World Projects: a Tier 2 pilot.
- Library books: budget-capped reasoning.
- Teacher mela: a group vote (now excluded by the R1 definition, since it's a staff group's own event).

**Size note:** the agent-kit instructions are now 7,997 characters, just under the 8,000-character limit. Further additions will need trimming elsewhere.

### Round 2: re-run of the affected inputs

Six fresh agents re-ran inputs 2, 5, 6, 12, 13 and 15 under the same blind conditions (outputs in `evals/runs/20261106-agents-r2/`).

| Fixture | CL | PB process | PB vote | PB allocate | Budget-capped | EB |
|---|---|---|---|---|---|---|
| 2 Team projects | ✔ | ✔ | ✔ ABSTAIN *(was ✘)* | ✔ | ✔ | ✔ |
| 5 School Development Plan | ✔ | ✔ APPLY *(was ~)* | ✔ | ✔ CONDITIONAL *(was ✘)* | ✔ | ✔ |
| 6 School resources | ✔ | ✔ APPLY *(was ~)* | ✔ APPLY *(was ✘)* | ✔ CONDITIONAL *(was ✘)* | ✔ | ✔ |
| 12 Lesson observation | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ APPLY (now via step 1 directly) |
| 13 Library books | ✔ | ✔ | ✔ | ✔ | ~ APPLY | ✔ |
| 15 Teacher mela | ✔ | ✔ | ✔ ABSTAIN *(was ~)* | ✔ | ✔ | ✔ |

**Round 2: 35/36 exact, 36/36 acceptable.** All four misses are fixed. The lesson-observation case now reaches the feedback loop through the intended route: the agent cited "a teaching-practice MIP … with state guides in use", not the planning branch.

**Latest result across all 15 inputs** (round-1 outputs for the 9 unaffected inputs plus the round-2 outputs; `evals/runs/20261106-combined/`):
- **87/90 decisions exact (97%), 90/90 acceptable (100%), 0 outside.**
- The three remaining non-exact decisions are acceptable alternatives:
  - Chaupal: CL APPLY rather than PARTIAL.
  - Real World Projects: an EB Tier 2 pilot.
  - Library books: budget-capped reasoning.

**Caveats:**
- **One run per input.** Model decisions vary between runs, so repeat runs would show how stable they are.
- **Only Claude was tested.** Behaviour in ChatGPT, Gemini or free tiers hasn't been checked.
- **Unaffected inputs weren't re-run.** The nine inputs not re-run were scored on round-1 wording. The round-2 changes were narrow (the collective-decision and costed-plan definitions, the fidelity-loop entry, a tie-break and a risk flag), but those inputs weren't re-run under them.
- **Only the fit-check stage was tested.** Transform, critic and render weren't run.

## 9. Pipeline test: rewrite, review and teacher card (6 November 2026)

**Goal:** check the stages after the fit checks. Five catalogue plans went through 40-transform → 50-critic (up to 2 revisions) → 60-render. Each step was run by a fresh agent that saw only its prompt, the framework cards and the case inputs, never the golden answers. A new script, [evals/check_transform.py](../evals/check_transform.py), runs the mechanical checks (schema C1, size C2, objective C3, owner C5, labels C8, rationale numbers C9) before each review and passes the schema errors to the reviewer. Outputs are in `evals/runs/20261106-pipeline/` (not committed).

| Plan | Fit-check input | Reviews | Outcome | Compared with the golden example |
|---|---|---|---|---|
| 14 Teacher motivation | all ABSTAIN | PASS | Returned unchanged (correct) | No golden example; matches the decision case |
| 12 Lesson observation | EB fidelity loop | PASS | 7 tasks, 0 added, 2→3 weeks | Matches Example 12 closely |
| 9 Reading by level | EB level grouping + akshara + measure; CL APPLY | REVISE (C1) → PASS | 6 tasks, 2 added, 4→5 weeks; protected daily slot, weekly regrouping, endline check | Matches Example 9's EB core. CL ideas went into modified tasks instead of being deferred (acceptable: no added task used) |
| 7 Real World Projects | CL APPLY; EB PARTIAL (retrieval) | REVISE (C1) → REVISE (C6) → PASS | 7 tasks, 1 added | CL changes match Example 7 (interest-chosen problems, peer roles, family audience). The added task is a retrieval check instead of Example 7's "ask an adult who uses this maths" |
| 6 School resources | PB prioritise APPLY; allocate CONDITIONAL | REVISE (C1, C13) → REVISE (C14) → REVISE (C14) | **Original returned with reasons** (limit of 2 revisions reached) | The drafts were close to Example 6. The last open issue: picture or oral ballots and women voting first covered SMC members but not parents |

**Result:** 4 of 5 plans produced a reviewed plan or a correct "no change". 1 plan fell back to the original, which is the designed safe outcome. No reviewer passed a harmful or unsupported change.

### Findings
1. **Gate fields were dropped when copied (fixed).** 3 of 5 first drafts failed the schema because they copied gates without `reason`, and the schema rejected `tier: null` for plan-to-routine. Fixed in [prompts/40-transform.md](../prompts/40-transform.md) (copy every field) and [schema/mip.schema.json](../schema/mip.schema.json) (`tier` allows null).
2. **Teacher cards are far over one page.** The revised cards for plans 7, 9 and 12 run to about 1,000–1,200 words each; the target is about 400. The render step may not condense, and the transform writes long task names. Proposed fix: the transform keeps each task name to one short sentence with detail in `sub_tasks`, and the card shows names plus guardrails only.
3. **Reviewers vary, and each round finds something new.** On plan 7 the second reviewer caught a mislabelled principle (CL-production, already strong) that the first missed. On plan 6 each round raised a different equity issue, so the revisions never converged. Proposed fix: the reviewer lists every issue in one pass (the prompt already asks for this), and the revision round re-checks the earlier issues explicitly.
4. **Transform missed guardrails at first.** Plan 6's first draft left out PB-G5 (ballot advisory to the SMC) and PB-G4 (accessible ballots). The reviewer caught both, but they belong in the transform's own checklist.
5. **No cost field.** The schema has no cost, so the render step wrote "Cost: Nil" without a source. Proposed fix: add an optional `cost` field, and render "not stated" when it's missing.
6. **Licence line.** The card for an unchanged plan credits the source but doesn't state its licence.
7. **Pronouns:** checked; no gendered pronouns for teachers in the drafts or cards.

**Caveats:** one run per plan; Claude only; five plans. The golden examples were written before the evidence-based gate existed, so EB additions (e.g. retrieval practice in plan 7) have no golden counterpart.

### Fixes applied, and a re-run of plans 6 and 9
| Finding | Fix |
|---|---|
| 2. Long cards | [40-transform](../prompts/40-transform.md): task names ≤20 words, ≤3 sub-tasks of ≤12 words, roles and artefacts ≤10 words, one-sentence guardrails, whole-plan rules stated once; shortening never drops a skill or check from the original task. [60-render](../prompts/60-render.md): about 450 words, sub-tasks dropped first when over, and a "Ground rules" section. `check_transform.py` flags task names over 20 words. |
| 3. Reviewer drift | [40-transform](../prompts/40-transform.md): apply each fix everywhere the same rule applies. [50-critic](../prompts/50-critic.md): find every issue in one pass; on a re-review, mark each earlier issue fixed or not, and flag new issues. |
| 4. Missed ballot rules | 40-transform lists PB-G4 (picture or spoken options and read-aloud help for every voter, women first, parents can vote outside meetings, turnout counted by gender) and PB-G5, plus a self-check before returning. |
| 5. Cost | Optional `x_transform.cost` in the schema: "nil", a stated amount, or "not stated". Critic C18 and `check_transform.py` check it. |
| 6. Licence | 60-render gives the original card a credit line with the licence, and "contributor not recorded" when the contributor is unknown. |

The agent kit's card template, checklist (C14, C17, C18), reviewer instructions and core instructions were updated to match. The core instructions are 7,995 characters, within the 8,000 limit.

**Re-run** (`evals/runs/20261106-pipeline2/`, fresh blind agents, same inputs):

| Plan | Before the fixes | After the fixes |
|---|---|---|
| 6 School resources | REVISE ×3, so the original was returned | REVISE (objective wording, counting rule stated late, order of steps) → **PASS**. The parent-ballot inclusion rules were in the first draft. Card: 516 words |
| 9 Reading by level | REVISE → PASS; card about 1,050 words | REVISE (C4: shortening had dropped "understand"; a transition card neither used nor deferred; per-group counts) → **PASS**. Card: 716 words |

**What the re-run shows:**
- The equity issue that stopped plan 6 didn't recur, and the revision converged in one round.
- The re-review reported every earlier issue by name.
- Cards are 30–50% shorter but still over the target of about 450 words. In plan 9 the "What changed" table alone is about 200 words and repeats the steps.
- The word limits had a side effect, which the reviewer caught: a shortened task name lost a skill. The transform prompt now forbids that.

**Two-sided card (applied after the re-run).** The teacher card now has a one-page front to run from (title, steps, ground rules, indicators, open questions, attribution) and a back for the HM, SMC or reviewer ("What changed and why"). The change is in [60-render](../prompts/60-render.md), the kit's card template, the README and the UX docs. Both cards were re-rendered by fresh agents:

| Plan | Front (target first set at 450, then 550) | Back | Original card |
|---|---|---|---|
| 6 School resources | 407 words ✔ | 155 words | 86 words |
| 9 Reading by level | 540 words (about 90 over) | 130 words | 91 words |

In both, the render step dropped every sub-task list to fit and pointed to the catalogue row. Plan 9's front is still over the target because all 5 of its tasks changed and each carries a role, an artefact and a guardrail.

**Decision:** the front's target is now **about 550 words**, one A4 page at normal print size, so both fronts fit. Updated in 40-transform, 60-render, the kit's card template and the regeneration prompts.

**Still open:**
- **Licence assumption.** The reviewer noted that the catalogue record doesn't state its licence; the attribution assumes CC BY-SA.

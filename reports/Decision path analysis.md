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

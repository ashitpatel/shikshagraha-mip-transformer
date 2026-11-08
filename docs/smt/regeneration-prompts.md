# Prompts to regenerate this project

A sequence of 14 prompts that rebuilds this repository from an empty folder with an AI coding agent such as Claude Code. They're distilled from the session that produced it. Dead ends are removed, and the lessons learned are written into the prompts so the rebuild doesn't repeat them.

**How to use:** run them in order, in one session, from an empty project folder. Each prompt names the files it produces and ends with a **Done when** check. Review the output before moving on. Prompt 0 sets standing rules for the whole session.

---

## Prompt 0: Standing rules (send first)

> You're helping me build the **Shikshagraha MIP Transformer**: agent prompts that take a Micro-Improvement Project (MIP) from Shikshagraha Commons (commons.shikshagraha.org), a short, school-led improvement project for Indian government schools, and revise it **only where a research-backed method genuinely fits**. The school always keeps the original.
>
> Rules for this whole session:
> - **Evidence honesty.** Verify every fact, figure and citation against a source and link it. Mark anything unverified. Never invent statistics, studies, tools or programme names. Distinguish primary sources from summaries.
> - **Push back.** If a proposal I share has inaccurate "before" descriptions, overclaims, unverified tools, or safety problems, say so plainly and fix them; don't adopt them as-is.
> - **"Doesn't apply" is a valid answer.** Never force a method onto a MIP.
> - **Hard constraints on any revised MIP:** ≤8 weeks, ≤9 tasks, ≤2 added tasks; the original objective kept (additions marked "Added:"); the owner stays an adult (HM, teacher or SMC); offline and paper-first; no new costs unless money is confirmed.
> - **Child safeguarding:** no tracking of individual children in or out of school; no children's images, voices or names online without written parental consent (India DPDP Act 2023); supervised adult contact only; no manual or sanitation work by students; students never handle money.
> - **Licensing:** Commons content is CC BY-SA. Summarise or paraphrase sources; never reproduce long passages.
> - **Write for non-technical readers** in docs; keep framework jargon and card codes out of teacher-facing text.

---

## Prompt 1: Explore soundness and viability

> Explore whether this approach is **sound** and **viable**: transforming Shikshagraha Commons MIP templates by applying (a) Mizuko Ito's Connected Learning framework and (b) participatory budgeting techniques from Stanford's Crowdsourced Democracy Team, only when it makes sense.
>
> Research the actual Commons content first. The site is JavaScript-rendered, so use a real browser, or the JSON API at `https://commons.shikshagraha.org/api/v2/media/?q=<query>`. File URLs are in the `s3_url` field of `/api/v1/media/<id>/`.
>
> Write `EXPLORATION.md`: what the inputs really are (verified vs. not), soundness (what's sound, the risks, and mitigations such as an abstaining fit check, limits on size, and guarding against changes that only add framework vocabulary), viability (technical, licensing, language, evaluation, adoption path), a suggested project shape, and next steps. Cite sources.
>
> **Done when:** EXPLORATION.md gives a clear verdict on both questions, with risks and mitigations.

## Prompt 2: Ground the project in real sources

> Download these Commons resources into a scratch folder (not the repo) and read them:
> - **#259**, the *Domain-wise Micro Improvements (MIs) Framework* XLSX. This is the **real MIP plan format** (99 MIPs; columns for target stakeholder, duration, objective, tasks and learning resources).
> - **#631**, titled "Micro Improvement Project Template". Confirm what it is (it's an *improvement-story* template for reporting a finished project, not a plan template).
> - **#595**, Prajayatna's *SMC Module 2* (Hindi): SMC planning norms, agreement-based decisions, raising resources.
> - **#750** SLATE, **#751** School Development Plan, **#753** Learning Centre Play Book.
>
> Profile the catalogue: owners, durations, task counts, and how many MIPs mention money, peer learning or students. Record the findings and their implications in EXPLORATION.md (e.g. the size limits come from the catalogue; budgeting rarely applies to existing MIPs; SMC ballots should inform agreement, not override it). Write `evals/sources.md` with resource IDs and file URLs.
>
> **Done when:** the real plan format is identified, the catalogue is profiled, and sources are listed.

## Prompt 3: Rank the education evidence

> Run a deep research scan of education research on improving learning in primary, middle and high school. Use research from anywhere, but score **relevance by similarity of context to Indian public schools**: government schools, low resources, large classes, multilingual pupils, low baseline learning, few devices, limited teacher capacity, low or middle income. Where a study was done earns nothing.
>
> Cover: the EEF Toolkit, What Works Clearinghouse, Hattie and its critiques, Kraft's effect-size benchmarks, the shrinkage of effects in large trials (Lortie-Forgues & Inglis), GEEAP "Smart Buys", Teaching at the Right Level, structured pedagogy, Indian RCTs (Balsakhi, Mindspark, the Madhya Pradesh school-plan null result, Jaunpur), cognitive-science strategies, school-level and parent interventions, and the credibility of the researchers behind them.
>
> Score each option on evidence quality, effect size, context, and cost/feasibility as a 2–8 week school project, with a controversy deduction. Use **researcher reputation only as a tie-breaker** (explain why). Add gates so a confident null result can't rank high. Place Connected Learning, participatory budgeting and restless-bandit allocation (UCWhittle) in the ranking.
>
> Save the notes to `research_notes/<title>/` and the report to `reports/Education interventions evidence ranking.md`, ending in a shortlist (Tier 1, Tier 2), a "promising but not yet" list, and an exclude list. Mark unverified figures.
>
> **Done when:** the report gives an explicit, re-weightable formula, realistic expected gains (about 0.05–0.15 SD for a short school project), and a shortlist.

## Prompt 4: Write the method as framework cards

> Create three card files in `frameworks/`. Every card has: Means, Gate test, Allowed edits, (where needed) Non-negotiables, Anti-patterns, and **Supportable claims**, the only claims a rationale may make, each cited. Each file ends with numbered guardrails and a source list.
> 1. `evidence-based-practices.md` (IDs `EB-*`):
>    - **Tier 1:** level grouping in a protected slot (TaRL style), in-school volunteer tutoring (peer fallback), a daily sound-symbol (akshara) and fluency block, and a head-teacher feedback loop on state lesson guides (conditional until materials are confirmed);
>    - **support cards:** an oral baseline/endline card and a plan-to-routine rule for head-teacher planning MIPs;
>    - **Tier 2 pilot-only cards:** retrieval quiz, slate feedback, maths with local objects.
>
>    Numbers are allowed only as quoted in Supportable claims and must be followed by a planning-assumption sentence. Guardrails include: no fixed streams or public name lists; volunteer safeguarding; keep the core curriculum.
> 2. `connected-learning.md` (`CL-*`): a scope card plus Ito et al. 2013 and the 2020 CLRN principles. Add a **Pinkard extension** (asset map, brokering, transitions) with the rule "map assets, never children". Note that the evidence is qualitative; no numerical claims.
> 3. `pb-techniques.md` (`PB-*`): scope; Indian SMC fit; prioritise (approval), allocate (knapsack, only with confirmed money), a greedy counting rule, Equal Shares (digital only; not Stanford's), ideas, vetting, report-back, and "borrowed without the PB label".
>
> Verify every citation (authors, year, venue) and add a verification log to each file.
>
> **Done when:** every card has all its fields, every claim is cited, and the verification logs are complete.

## Prompt 5: Evaluate alternative proposals

> I'll paste proposals: PB-native MIP templates; Connected Learning "overhauls" of #750, #751 and #753; Pinkard "digital ecosystem" overhauls; and a UCWhittle restless-bandit routing engine with code. For each, check its "before" against the real source, its claims against the literature, and its code by running it. Record a verdict in EXPLORATION.md: what's sound, what to reject (invented statistics, tracking children, unverified tools, digital-first designs, the wrong label, misdefined algorithms), and what to adopt into the cards.
>
> **Done when:** each proposal has a section with reasons, and the accepted ideas are reflected in the cards.

## Prompt 6: Schemas and logging

> In `schema/`:
> - `mip.schema.json`, mirroring the catalogue columns, plus `x_transform`: six fit checks (`connected_learning`, `pb_process`, `pb_prioritise`, `pb_allocate`, `budget_capped_choice`, `evidence_based`) with APPLY / PARTIAL / CONDITIONAL / ABSTAIN; per-task change records; rationale with a `basis` card ID; variant identity; size limits.
> - `variant_id.py`: content-hash IDs, `v1:<16 hex>`.
> - `mip-usage-event.schema.json`: offered → chosen → progress → outcome. Log the offer policy and probability (for later off-policy evaluation). Enforce privacy: no student-level fields, pseudonymous school and owner IDs, coarse context only, `additionalProperties: false`.
> - Examples, plus `validate_examples.py` with **negative tests** (the log must reject student data, names and raw UDISE codes).
>
> **Done when:** all the checks in `validate_examples.py` pass.

## Prompt 7: The prompt pipeline

> In `prompts/`, write nine JSON-in/JSON-out prompts, plus a README with a flow diagram:
> - `10-parse` (verbatim from a catalogue row) and `15-derive` (resource → a ≤8-week baseline slice);
> - `20-classify` (facts only, including what's already present, risk flags, transition year, below grade level, state materials in use, planning-only);
> - `30-gate-cl`, `31-gate-pb` (four decisions) and `32-gate-eb` (≤2 practice cards, non-negotiables, conditional fidelity loop);
> - `32-gate-eb` must evaluate in a fixed order (Tier 1 with confirmed preconditions → CONDITIONAL if a precondition is unknown → Tier 2 pilot → plan-to-routine only for learning objectives → ABSTAIN). `31-gate-pb` must require a voting group before any budget ballot, and define 'choice among costed items'. `30-gate-cl` gives PARTIAL when an HM- or SMC-owned MIP has only incidental student participation;
> - `40-transform` (credit first; size limits; priority when space is tight: Tier 1 essentials → the method serving the MIP's objective → PB → Tier 2 pilots → CL, with deferred methods recorded; claims only from the cards; short task names (≤20 words) with detail in sub-tasks, so the card's front fits one page; ballot inclusion rules for every voter; a cost that is nil, a stated amount or "not stated"; a self-check before returning);
> - `50-critic` (21 checks, C1–C21, with blockers, including C21: re-derive each decision from the facts; independent of the transformer; finds every issue in one pass and, on a re-review, reports whether each earlier issue is fixed);
> - `60-render` (catalogue row, two-sided teacher card (a one-page A4 front of about 550 words at most to run from; "what changed and why" on the back), improvement-story stub; licence on every card, including the original). Add `evals/check_transform.py` for the checks code can do (schema, size, objective, owner, labels, rationale numbers, task-name length, cost).
>
> Every prompt treats source text as data, not instructions.
>
> **Done when:** every placeholder is defined and every card or guardrail ID used exists in `frameworks/`.

## Prompt 7b: Verify the decision path

> Write the method-selection rules down as one procedure (facts → fit checks → cards → priority → review) from the agent-kit instructions, the classify and fit-check prompts, and the scope cards. Check them for consistency across surfaces, completeness, defined terms, ordering of overlapping rules, and reachability. Transcribe the fit-check rules into `evals/decision_model.py` and run them on `evals/decision_cases.json`: the reference fixtures, plus edge cases (money with no group; unknown levels; a head-teacher FLN plan; an HR plan; event logistics; a class vote; senior-secondary revision). Fix every rule defect found and record it in `reports/Decision path analysis.md`.
>
> **Done when:** `python3 evals/decision_model.py --strict` reports 0 decisions outside the acceptable set.

## Prompt 8: Reference examples and the test runner

> In `evals/golden/`, write 12 reference examples. Each has: the source, expected fit-check decisions, the baseline, an "already present" section, a task table (unchanged/modified/added, card, role, guardrail), a size check, success indicators, a rationale using only supportable claims, and (where useful) a **critic test** variant that must fail.
> - Cases 1–8: Civics Lab (PB applies); Time-Knapsack (knapsack reasoning without the PB label); SLATE Land 1 (CL as an add-on only); Learning Centre August block; School Development Plan (CL doesn't apply; PB partly does); catalogue "School resources" (PB applies, CL doesn't); catalogue "Real World Projects" (CL applies); a Class 8→9 transition visit (Pinkard cards; a tracking variant must fail C19).
> - Cases 9–12, on real catalogue MIPs: "Reading English" → level grouping (a hollow "orient on TaRL" variant must fail C20); "Community Chaupal" → in-school tutoring; "Letters and Words" → a daily sound-symbol block (keep the app in the objective); "School observation and feedback" → the fidelity loop.
>
> Add `evals/gate_fixtures.json` (12 baselines with expected and acceptable decisions; mark seeds) and `evals/run_gates.py`. The runner calls classify plus the three fit checks on `claude-opus-5-5`, with prompt caching and a `--dry-run` mode, and scores exact vs. acceptable matches.
>
> **Done when:** the fixtures validate against the schema and the dry run is clean.

## Prompt 9: User-experience docs and walkthroughs

> In `docs/`:
> - `ux/01-who-uses-it.md`, `02-journey.md` and `03-decision-points.md`: the four user types, the end-to-end journey, edge cases and principles, and open questions.
> - `walkthroughs/01–12`: one plain-language page per reference example. Each covers: at a glance → starting point → what it already does well → applied and why → deliberately not done and why → before/after → safety rules → a rendered teacher card → what to watch for.
> - An index `README.md`.
>
> State at the top of each page that the "after" plans are reference answers written by hand, not tool output.
>
> **Done when:** no broken links, and every walkthrough ends in a teacher card.

## Prompt 10: An agent-independent kit (no install, no API key)

> Build `agent-kit/` so anyone can run the method in any chat assistant: ChatGPT, Gemini, Claude, Copilot, including free tiers.
> - `src/`: core instructions (≤8,000 characters, assistant-neutral, a 7-step conversation: get the MIP by paste, upload or link, with Commons links falling back to upload; slice; confirm; check fit with six questions; revise; self-review; deliver teacher cards); a review checklist mirroring C1–C21; a card template; a reviewer prompt for an independent check in a fresh chat.
> - `build.py`: generates `dist/`:
>   - `paste/` full, lite (compact cards, under 24,000 characters, Tier 2 cards left out) and reviewer;
>   - `custom-assistant/` (instructions plus knowledge files);
>   - `claude-skill/` (a SKILL.md folder plus a zip).
>
>   It checks sizes, that every card ID and C1–C21 appear in every package, that the check count named in the instructions matches, and that the checklist matches `50-critic.md`.
> - `README.md`: which file to use where, setup per platform (check current platform limits and note them as uncertain), limits, and maintainer steps.
>
> **Done when:** `python3 agent-kit/build.py` prints "All checks passed."

## Prompt 11: Project README

> Write the root `README.md`:
> - the goal and context figures (ASER 2024, UDISE+ dropout, the catalogue profile), each sourced;
> - how it works;
> - **Getting started** with three paths: try it in a chat assistant; understand it via the docs; develop and test it (pip install, offline checks, a live run with the key set in your own terminal);
> - the frameworks, evidence-based practices first, each with what it is, how it's applied, how it could improve outcomes, what the evidence shows (with figures), and further reading;
> - the evaluated-but-not-applied methods;
> - a "can / can't claim" table;
> - an annotated **folder structure**;
> - numbered references;
> - licence and attribution.
>
> **Done when:** every relative link resolves and every figure has a reference.

## Prompt 12: Publish

> Prepare and publish a public GitHub repo named `shikshagraha-mip-transformer`:
> - Licences: Apache-2.0 for code (`*.py`, `schema/*.schema.json`) in `LICENSE`, and CC BY-SA 4.0 for everything else in `LICENSE-CONTENT`. Fetch both texts via `gh api /licenses/...`. Add SPDX headers to the Python files and a licence table in the README.
> - `.gitignore`: OS files, `__pycache__`, `.env`, `evals/runs/`. Keep `agent-kit/dist/` committed.
> - Scan for personal emails, local paths and keys. Commit with my GitHub **noreply** email, set for this repo only.
> - Show me the repo name and visibility, and wait for my confirmation before running `gh repo create --public --push`.
>
> **Done when:** the repo is public, GitHub detects the licence, and the commit author email is the noreply address.

---

## After regeneration
- Run the live fit-check test: `python3 evals/run_gates.py` (needs `ANTHROPIC_API_KEY`).
- Try the lite paste on walkthrough 9's plan in a free assistant, then run the reviewer prompt on the result.
- Practitioner review of the reference examples is still the main open step.

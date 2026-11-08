# MIP Transformer — Exploration: Soundness & Viability

*Date: 2026-11-04 · Status: exploration, no code or prompts written yet*

## 1. The proposal in one sentence

A set of agent prompts that takes a **Micro-Improvement Project (MIP) template** from Shikshagraha Commons and, **only where it fits**, reworks it with **Connected Learning** (Ito et al.) and **participatory budgeting (PB) techniques from Stanford's Crowdsourced Democracy Team**, so the MIP a school actually runs is better.

## 2. What the inputs actually are (verified vs. not)

| Input | What I verified | Gap |
|---|---|---|
| **MIP template** | Commons resource #631, titled "Micro Improvement Project Template". **Resolved (§9):** it's a *story template for reporting a finished project* (file name "Unbundle 3.0 – Gallery Walk – Improvement Stories"), not a planning template. | — |
| **MI catalogue** | ShikshaLokam *"Domain-wise Micro Improvements (MIs) Framework"* (XLSX, #259). **Resolved (§9):** 99 MIPs in the actual plan format: owner, duration, objective, tasks, learning resources. This is the real input format. | — |
| **Related Commons assets** | Clubs & Cabinet Booklet, PBL Toolkit (Mantra4Change), School Development Plan, Learning Centre Play Book (student voice, peer teaching). | — |
| **Scale** | shikshagraha.org claims 1.37M+ micro-improvements in schools. | Which app executes MIPs, and whether completion data is reachable, is unconfirmed. |
| **Connected Learning** | 2013: interest-powered, peer-supported, academically oriented, production-centered, shared purpose, openly networked. 2020 CLRN revision: interests / relationships / opportunities, sponsorship of youth interests, shared practices, connections across settings. | — |
| **Stanford PB** | Open-source platform (pbstanford.org). Voting methods: approval, **knapsack** (budget-constrained), ranked, plus remote/digital ballots. Has run youth PB (Boston ages 12–25, Chicago 47th Ward, Long Beach). | Stanford's contribution is mainly **ballot design and aggregation**, not the whole PB cycle. The cycle (idea collection → proposal development → vote → implement → monitor) is general PB practice. |

**Implication:** the template's exact fields aren't confirmed yet, so §5 below is built on the fields the Commons description names.

## 3. Soundness: is the idea right?

### What's sound

1. **Connected Learning fits MIPs that face students.** Pedagogy, student engagement, clubs, reading, and inclusivity MIPs are mostly about what students do. CL asks the right questions of them: whose interest drives this, who supports whom, what gets produced, and who sees it. Commons already pushes this way (the PBL Toolkit, Clubs & Cabinets, peer-led SLATE), so CL **sharpens a direction the ecosystem already takes**. It isn't a foreign import.
2. **PB fits MIPs about choosing and allocating.** Many schools must pick *which* MI to do from the domain catalogue, or how to spend a discretionary amount. Candidate pots include the Samagra Shiksha composite school grant (partly earmarked), SMC funds and CSR/community contributions. RTE gives SMCs a statutory role in the School Development Plan. A light PB step (SMC + student cabinet propose → knapsack-vote within a cap) **has a legitimate institutional home**.
3. **The "when it makes sense" clause is the core of the design, not a footnote.** A transformer with an explicit fit gate that can abstain is sound. One that always applies both frameworks is not.

### Where it's weak or risky

| Risk | Why it matters | Mitigation |
|---|---|---|
| **Framework-washing** | LLMs readily add "peer-supported, interest-driven" wording without changing a single task. The output *looks* improved and isn't. | Every change must alter a **task, role, deliverable or decision rule**. The critic rejects changes that only rename things. |
| **Breaking the "micro"** | A full PB cycle takes weeks of ideation, proposals and a vote. For an MIP that takes a head teacher 4 weeks, that kills feasibility. | Hard limits: duration change ≤ +X%, task count ≤ +N, no new paid inputs. Use a "PB-lite" (one 30-min class or SMC session with a paper knapsack ballot). |
| **Category error** | CL is a theory of *youth* learning. Applying it to "repair the water tank" or "teacher attendance" is forced. Stretching CL to teachers-as-learners is defensible, but it's an extension, not Ito's framework. | The fit gate mostly says **No CL** for Infrastructure/HR/Governance MIPs, unless students are real participants (e.g. a student cabinet audits the toilets). |
| **No money, no PB** | Most MIPs cost little or nothing. Reframing "budget" as time or attention is a stretch. | Apply PB only when there's (a) a real pot or (b) a real choice among options. Otherwise abstain. |
| **Thin evidence** | CL's evidence is mostly ethnographic. School and youth PB evidence is mostly about civic engagement, not learning outcomes. | Claim better MIP *design quality and participation*, not better learning outcomes, until there's field data. |
| **Indian context** | Exam pressure, large classes, low device access ("openly networked" ≠ smartphones), multilingual delivery, gender and caste dynamics in who gets to vote or speak. | Default to offline/paper mechanisms. Add an equity check (who is excluded?). Output in the MIP's language. |

**Verdict on soundness:** sound **as conditional enrichment** with an abstaining fit gate and hard limits that keep the MIP small. Not sound as a blanket "apply CL + PB to every MIP."

## 4. Viability: can it be built and used?

| Dimension | Assessment |
|---|---|
| **Technical** | High. Parse → classify → gate → transform → critique → render is a standard LLM pipeline. Per-MIP cost is trivial. |
| **Content access** | Good. Commons is open access and CC BY-SA. **Outputs that derive from Commons templates must also be CC BY-SA and attribute ShikshaLokam.** Plan for this from day one. |
| **Language** | Medium. Hindi and Kannada quality is acceptable on frontier models. Smaller languages need native reviewers. |
| **Evaluation** | **The hardest part.** You need (1) a golden set of 15–30 real MIPs across domains, (2) a rubric covering fit, micro-ness preserved, actionability, equity and no framework-washing, and (3) practitioner raters (HMs, Mantra4Change/ShikshaLokam staff) doing blind original-vs-transformed comparisons. LLM-as-judge can only pre-screen. |
| **Adoption path** | **The biggest unknown.** Improved MIPs matter only if they reach the app or library schools pick from. Options, from least to most dependent: (a) publish improved MIPs back to Commons as derivatives, (b) a tool for MIP authors at NGOs and DIETs, (c) integration with the ShikshaLokam pipeline. (b) works without partner buy-in. (c) needs a partnership. |
| **Effort to a credible prototype** | Roughly 2–3 weeks: get the template and catalogue, write prompts and schema, build the golden set, run a rater round. |

**Verdict on viability:** technically easy and legally clean. Real viability depends on **evaluation with practitioners** and **an adoption channel**. Treat it as an authoring aid for MIP designers, not an autonomous generator.

## 5. Suggested shape of the project

> **Status (2026-11-04):**
> - **Built:** `schema/` (plus usage logging), `frameworks/` (verified citations), `evals/golden/` (12 examples), `prompts/` (9 prompts), `evals/run_gates.py` (developer test of classify and gates), `docs/` (UX and 12 walkthroughs), and **`agent-kit/`**. The agent kit is an agent-independent, no-install version for any chat assistant: a paste-in prompt (full or lite) for free tiers, a custom-assistant package, a Claude Skill, and a reviewer prompt, all generated from one source by `agent-kit/build.py`.
> - **Added after the evidence scan:** `frameworks/smt/evidence-based-practices.md`, with the Tier 1 practices from `reports/Education interventions evidence ranking.md`, a new fit check (`prompts/smt/32-gate-eb.md`), critic check C20, and the EB gate in the test fixtures and the agent kit.
> - **Not done:** live runs of anything; practitioner review; (Golden Examples 9–12 and walkthroughs 9–12 now cover all four Tier 1 practices; Tier 2 has pilot cards in `frameworks/smt/evidence-based-practices.md`.)

```
ShikshagrahaMIPTransformer/
  frameworks/
    connected-learning.md      # principle cards: test question, MIP edits allowed, anti-patterns
    pb-techniques.md           # PB-lite patterns: idea round, knapsack/approval ballot, report-back
  schema/mip.schema.json       # normalised MIP (mirrors the real template once obtained)
  prompts/
    10-parse.md                # catalogue row (XLSX) -> schema
    15-derive.md               # playbook/toolkit resource -> catalogue-sized baseline MIP
    20-classify.md             # domain, actors, cost, student-facing?, choice-point?
    30-gate-cl.md              # APPLY / PARTIAL / ABSTAIN + reasons
    31-gate-pb.md              # APPLY / ABSTAIN (needs real pot or real choice)
    40-transform.md            # field-level edits, each tagged with principle + rationale
    50-critic.md               # micro-ness, framework-washing, equity, feasibility, fidelity
    60-render.md               # back to template format + change log + CC BY-SA attribution
  evals/
    golden/                    # real MIPs + expert-annotated expected gate decisions
    rubric.md
```

### Mapping: what each framework is allowed to change

| Principle / technique | Test question (gate) | Allowed MIP edit |
|---|---|---|
| Interest-powered | Can students shape the topic or format? | Add a student-choice step within the task |
| Peer-supported | Is there peer work students could lead? | Assign peer roles (buddy reader, club lead) |
| Academically oriented | Does it link to curriculum or future paths? | Tie the deliverable to a syllabus outcome |
| Production-centred | Is there a tangible output? | Make evidence a student-made artefact (display, wall magazine) |
| Shared purpose | Do adults and students share the goal? | Co-plan step with SMC or student cabinet |
| Openly networked / connections across settings | Can work be seen beyond class, offline OK? | Showcase to parents or community at an SMC meeting |
| PB idea round | Are there ≥2 plausible options? | Short structured idea collection (students + SMC) |
| Knapsack / approval vote | Is there a cap (₹ or time)? | Paper ballot within the cap, tallied publicly |
| Report-back | Was a decision made collectively? | Add a "publish result + progress" task |

## 6. Recommended next steps

1. **Get the real inputs:** the MIP Template DOCX (#631) and the Domain-wise MIs XLSX from Commons. Lock the schema to the actual fields.
2. Pick 15–30 MIPs across all six domains. Hand-annotate the expected gate decisions. Include cases that *should* abstain (they test the gate).
3. Write the prompts in §5. Run them on the golden set and check gate accuracy before anyone looks at transformation quality.
4. Run a blind rater round with 3–5 practitioners.
5. Decide the adoption channel (Commons derivative, authoring tool, or partner integration) and reach out to ShikshaLokam/Mantra4Change if it's (c).

## 7. Assessment of two proposed PB-native MIP templates (added 2026-11-04)

Two candidate templates were proposed: **Civics Lab** (a knapsack vote over a fixed school fund) and **Time-Knapsack** (a knapsack vote over a team's 20 project hours).

### What they settle

- **They show the case where the PB fit check should say "apply".** Civics Lab has a real fund, several competing options, a constituency of students, and a public outcome. That is exactly the shape §3 says PB needs.
- **"Thick agency guardrails" are a good pattern.** Rules like "no evidence, no issue", "no price, no ballot" and "the ballot can't exceed the cap" make participation change the work, not just the wording. That is the anti-framework-washing rule from §3, written as a template feature. Adopt it in the transform and critic prompts.
- **They overlap with Connected Learning.** Each step leaves an artefact (production-centred), work happens in squads (peer-supported), and the vote serves a common goal (shared purpose). So PB and CL are not separate lenses here; one plan can carry both.
- **They reveal a third mode.** The transformer was scoped to *enrich existing MIPs*. These are *PB-native MIPs written from scratch*. The project should decide whether it does enrichment, generation, or both.

### What they don't settle

- **Usefulness is still unproven.** These are designs, not evidence. Whether they produce better improvements, more participation, or civic learning in Indian government schools needs a pilot.
- **Micro-ness.** Civics Lab has mapping, a vetting board, costing, an election and execution. Realistically that's 6–10 weeks of coordination. It needs a time box, or a "lite" path (one mapping period, one ballot session).

### Specific issues to fix

| Template | Issue | Suggested fix |
|---|---|---|
| Civics Lab | **"Knapsack" and "Equal Shares" are mixed up.** Knapsack voting (Goel et al., Stanford) is a *ballot format*: each voter fills a budget. The Method of Equal Shares (Peters, Skowron et al.) is an *aggregation rule*, and to my knowledge it doesn't come from the Stanford team. The template defines the ballot but never says how ballots are counted. | State the counting rule explicitly. On paper, the simplest is: count votes per project, then fund in vote order while the money lasts. Equal Shares fits more fairly but is hard to tally by hand. Rename the artefact (e.g. "Ballot Tally & Funded List"). |
| Civics Lab | **US framing.** "PTA micro-grant" and "$250" don't match Indian government schools. Spending normally goes through the SMC and head teacher, and much of the composite school grant is earmarked. | Name the funding source as SMC-approved discretionary funds, untied composite-grant headroom, or a CSR/community pot. Keep procurement with the HM/SMC; students specify and verify, they don't handle cash. |
| Civics Lab | **Student labour.** "Squads … build the improvements" is a real safeguarding and optics risk in India, where students cleaning or doing manual work is a sensitive issue. | Limit students to safe tasks (design, signage, monitoring, art, inventory). Adults or vendors do physical and hazardous work. |
| Civics Lab | **Gatekeeping.** A peer "vetting board" can screen out ideas from quieter or marginalised students before the vote. | Vet on feasibility and price only, not merit. Publish what was rejected and why. Spread board seats across grades, genders and sections. |
| Civics Lab | **Coverage.** Grades 6–12 excludes primary-only schools, which are a large share of government schools. | Add a primary variant (picture ballot, class-level vote, teacher-assisted costing). |
| Time-Knapsack | **It's prioritisation, not participatory budgeting.** A team of 4–5 dividing its own hours is scope management (MoSCoW or agile). PB is a *constituency* allocating a *shared public resource*. Calling this PB is the framework-washing §3 warns about. | Present it as a *knapsack-reasoning* routine borrowed from PB, or as a PBL/Connected Learning scaffold, not as PB. |
| Time-Knapsack | **It isn't a school micro-improvement.** It's a classroom routine for students. A MIP is owned by a teacher or HM and improves the school. | Reframe the MIP as "Teacher introduces time-budgeted scoping in PBL projects for Class X", with this routine as the student activity. |
| Time-Knapsack | **Time isn't like money.** Hours aren't freely swappable between students with different skills, and estimates are uncertain. Knapsack assumes known costs. | Add a buffer (e.g. plan to 16 of 20 hours) and a mid-sprint re-scope checkpoint. |

### Implications for the transformer

- Use the two templates (after fixes) as **golden examples**: Civics Lab for "PB applies", Time-Knapsack for "knapsack technique applies, PB label does not". The revised versions are [evals/golden/civics-lab.md](evals/golden/civics-lab.md) and [evals/golden/time-knapsack.md](evals/golden/time-knapsack.md).
- Split the PB fit check into **PB process** (needs a constituency, a shared resource and a public outcome) versus **budget-constrained choice technique** (any prioritisation under a hard cap).
- Make guardrails a required output field for every participatory step.

## 8. Assessment of three proposed Connected Learning before/after examples (added 2026-11-04)

The examples: **SLATE Language Adventure**, **Learning Centre Play Book**, and **School Development Plan (SDP)**, each with a before, an after and a rationale.

### What they show well

- **Connected Learning can change tasks, not just wording.** Each "after" changes what people actually do: produce stories, bring community experts in, run co-design workshops. That's the bar from §3.
- **"Connections across settings" is the strongest fit with Shikshagraha.** The Play Book's community-expert mapping is Connected Learning's 2020 principle almost exactly. It lines up with Shikshagraha's Samaaj–Sarkaar (society–government) framing. This is the most convincing case so far that Connected Learning adds something the Commons doesn't already have.

### Problems that would be harmful if used as golden examples

| # | Example | Problem | Why it matters | Fix |
|---|---|---|---|---|
| 1 | SLATE | **Made-up evidence:** "Dr. Ito's research demonstrates … learning retention triples compared to standard worksheets." | Ito's Connected Learning research is mostly ethnographic and design-based. I know of no finding like this. A golden example with an invented statistic teaches the transformer to invent statistics, which is the worst failure for a tool practitioners will trust. | Delete it. Rationales may cite only claims from a vetted reference card (`frameworks/smt/connected-learning.md`) and must not quote numbers without a source. |
| 2 | SLATE | **Replaces foundational phonics** with storytelling. | SLATE targets phonological awareness and word recognition: foundational literacy, where the evidence and national FLN policy (NIPUN Bharat) favour systematic, structured instruction. Dropping the sequence changes the MIP's objective. | **Add, don't replace.** Keep the 4-land phonics sequence. Each land ends with a squad-made story (spoken, drawn, or recorded) on a theme students choose, using that land's target words. |
| 3 | SLATE | **Children's voices and photos in an open cross-district gallery.** | Child safeguarding. India's DPDP Act 2023 requires verifiable parental consent to process children's data. Device access is also uneven. | Offline by default (class or school display). Sharing digitally needs parental consent, no faces or full names, and teacher moderation. |
| 4 | All three | **The "befores" are caricatures** ("rigid", "compliant feedback", "chore"), and they don't appear to be the real Commons text. | If the "before" is weakened, every "after" looks like an improvement, and the eval measures nothing. | The "before" must be **quoted from the actual Commons resource**, with its resource ID. |
| 5 | Play Book | Execution tracking moves **from the teacher to a student assembly**. | The MIP still needs an accountable adult owner. | Students *co-track* on a public board; the teacher stays the MIP owner. |
| 6 | Play Book | **Community adults in the classroom**; a "makerspace ecosystem". | Safeguarding (HT approval, supervised visits). A makerspace adds resources and scope beyond the original layout MIP. Also note caste and gender dynamics in which "traditional" skills get showcased. | HT-approved, supervised expert visits. Use existing materials. One community-linked project per term. |
| 7 | SDP | **This isn't Connected Learning.** Community surveys and co-design workshops with parents and officials are *participatory governance*. Connected Learning is about how young people learn. | It's the mirror image of Time-Knapsack: a legitimate idea under the wrong framework label. | Connected Learning gate: **ABSTAIN** (or PARTIAL, only if the youth survey work is designed as a learning experience). Send it to the PB / participatory-process gate instead. |
| 8 | SDP | **It bypasses the SMC.** | Under the RTE Act, the **SMC prepares the School Development Plan**. A co-design process that doesn't go through the SMC is weaker in law and in practice. | The SMC convenes the workshops and adopts the plan. If there's a development fund, a knapsack ballot on SDP priorities fits naturally here. |
| 9 | SDP | **"AI Saathi"** | I couldn't verify that this tool exists in the Shikshagraha ecosystem. | Name only tools that have been verified; otherwise "a simple paper or phone survey". |
| 10 | SDP | **SDP published publicly for anyone to remix** | It may contain safety gaps, child data or staffing issues. | Publish a redacted summary only. |
| 11 | SDP / all | **Micro becomes macro.** Officials, district-wide galleries, makerspaces. | Breaks the MIP's scale (§3). | Keep the hard limits: duration, task count, no new paid inputs. |

### Implications for the transformer

- **A new hard rule: no invented evidence.** The critic checks every claim in a rationale against the reference card. Any number without a source is rejected.
- **A new hard rule: keep the objective.** A transformation may add to the original MIP's core method but may not replace it, especially in foundational literacy and numeracy.
- **A safeguarding check on every output:** child data and media, adult visitors, physical tasks.
- **The gates now cover four cases**, each with a golden example:
  - both frameworks apply: Civics Lab;
  - knapsack technique applies, PB label doesn't: Time-Knapsack;
  - Connected Learning applies: SLATE (after fixes), Play Book (after fixes);
  - Connected Learning label doesn't apply, a participatory process does: SDP.
- **"Before" texts must be real Commons content**, tied to resource IDs and loaded from the source at eval time (see [evals/sources.md](evals/sources.md)).

### Update after reading the sources

The three source documents were downloaded and read. **All three supplied "befores" understated the originals:**
- SLATE has no worksheets; it already has peer learning circles, sight-word charts, reading corners, and a Learner's Mela of student-made stories.
- The Play Book already invites local experts and includes Neighbourhood Explorer, Students as Teachers, and a year-end exhibition.
- The SDP already includes teachers, the SMC and students, and cites the SMC's RTE role.

So the real Connected Learning gains are smaller and more targeted than the examples suggested. That makes the transformer's **"credit what exists"** step essential. The revised golden examples are:
- [evals/golden/slate-language-adventure.md](evals/golden/slate-language-adventure.md): Connected Learning applies, as augmentation
- [evals/golden/learning-centre-playbook.md](evals/golden/learning-centre-playbook.md): Connected Learning applies, targeting interests and connections across settings
- [evals/golden/school-development-plan.md](evals/golden/school-development-plan.md): Connected Learning abstains; the participatory budgeting process partly applies

The SDP's drafting table (*Challenge · SMART goal · Solution · Steps · Timeline · Who · Resources · Monitoring*) is a good interim MIP schema.

## 9. What the source files show (added 2026-11-04)

Three more Commons files were downloaded and read: #631 (template), #259 (MI catalogue), #595 (Prajayatna SMC Module 2).

### 9.1 The "MIP Template" (#631) is a story template, not a plan template

Its fields: project name · project leader (with photo) · school name & location · objective · year/month · implementation story covering (A) background, (B) why, i.e. the challenge, (C) how the challenge affected the school or leader, (D) stakeholders involved, (F) step-by-step actions ("the most important part"), (G) things kept in mind · outcome (what shifted) · testimonials · photos.

**Implications:**
- It describes **what happened after** a project, so it isn't the input to transform.
- It's a good **output format for documenting** transformed MIPs once they've been run.
- Stories written in this format are the best available **evidence of what works**, if Shikshagraha has a corpus of them.

### 9.2 The MI catalogue (#259) is the real input format, and it sets the "micro" limits

The columns are: Domain sheet · Sub-category · Title · Contributed by · Template link · **Target stakeholder** · **Duration** · Description · **Objective** · Project-level learning resource · **Task # / Task name / Sub-task** · Task-level learning resource (often on `bodh.shikshalokam.org`). The schema is in [schema/mip.schema.json](schema/mip.schema.json).

Profile of the 99 MIPs (counted from the file):

| Measure | Finding | Implication |
|---|---|---|
| Owner | ~60 HM/HT/school leader, ~27 teachers, a few SMC/CRP/DIET | Students are never owners. Student roles belong **inside tasks**. |
| Duration | 54 are "1 month", 21 "2 weeks", max "2 months" | Hard limit: ≤8 weeks. Longer designs get split into chained MIPs. |
| Tasks | Mostly 5–7, max 12 | Hard limit: ≤9 tasks, ≤2 added. |
| Domains | Pedagogy 31 · Beneficiary Satisfaction 25 · Management & Governance 16 · Access & Infrastructure 14 · HR 10 · Inclusive 3 | — |
| Mention of money | **0** mention grant, fund, budget or cost (10 mention "procure") | **The PB gate will almost never fire on existing MIPs.** PB's value is in *new* MIPs and in *choosing which* MIP to do. |
| Student agency | "Student" appears in 61, but as beneficiaries. **0** mention peer, club or cabinet. | **Connected Learning has real room** in the ~31 teacher-owned pedagogy MIPs. |
| SMC / community / parents | 45 | Good hooks for "connections across settings" and SMC-led prioritisation |
| Showcase / display | 24 | Production-centred outputs are partly there already |

The workbook also has a sheet **"Domains for SolvED_Students"**, a student-facing list of domains. That suggests a student-led problem-solving track exists or was planned. If so, it's the most natural home for both frameworks. Worth asking Shikshagraha about.

**Better golden inputs from the real catalogue:**
- **"School resources"** (Access & Infrastructure, HM, 2 weeks): assess resources → detail needs → identify community support → list what to procure → share with CRP. This is a natural PB case: add an SMC prioritisation vote between "detail needs" and "list what to procure".
- **"Real World Projects"** (Pedagogy, maths teachers, 1 month): the teacher designs projects → introduces them → supports weekly → student showcase. This is a natural Connected Learning case: students pick the real-world problem from their own interests, and peer roles plus a family audience are added to the existing showcase.

**Consequence for the golden examples (done):** SLATE and the Play Book were recast through a **resource → derived baseline MIP → transformed MIP** step. They're now SLATE Land 1 (6 weeks, 7 tasks) and the Play Book's August "Neighbourhood month" (6 weeks, 7 tasks). Two catalogue MIPs were added as Examples 6 and 7. All seven are indexed in [evals/golden/README.md](evals/golden/README.md). This suggests the pipeline needs a step before transformation: **derive a catalogue-shaped MIP from a resource** when the input is a playbook or toolkit rather than a catalogue row.

### 9.3 SMC Module 2 (#595, Prajayatna, Hindi) changes how PB should be framed

This is an 8-session SMC training on the School Development Plan and resources. Relevant points:
- **Consensus, not voting:** it stresses collective decisions with everyone's agreement, and equal voice for women and men.
- **Structure checks:** its SMC self-check asks about 50% women members, a woman chair or vice-chair, parents from every class and caste, regular meetings, and whether **grants are disclosed in meetings**.
- **Two kinds of needs:** it separates *immediate* needs (cleanliness, drinking water, enrolment, identifying dropouts) from *long-term* ones (extra classrooms, computer room). Its dimensions are enrolment, attendance, basic resources, learning and management, with explicit attention to children with disabilities.
- **Resources are broader than money**, and they're **mobilised, not just allocated**. Parents, the Gram Panchayat, block-level departments, local businesses (approached through the SMC or Gram Panchayat, not individually) and individual donors are all sources. One session teaches how to write formal applications to the Gram Panchayat or block.
- **SDP cycle:** needs assessment by priority → realistic goals with timelines → action plan → clear teacher responsibilities → periodic review.

**What this means for PB in this setting:**
1. **The budget usually isn't fixed; it's assembled.** Knapsack voting assumes a known pot. Here, most of what an SMC achieves comes from mobilising and applying to the Gram Panchayat, block or donors. So the more useful PB technique is often **prioritisation** (approval or ranked voting on needs), followed by mobilisation. Knapsack applies only to whatever *is* discretionary.
2. **A ballot should inform consensus, not override it.** The module's norm is agreement reached together. A paper approval vote works best as a *visible input* to the SMC's discussion: it shows everyone's priorities, including women's and disadvantaged parents', before discussion starts. The SMC then reaches agreement. This also addresses the risk of louder voices dominating.
3. **Students are absent from the SMC module.** The student voice in Golden Examples 1 and 5 is an *addition* to the SMC norm, not part of it. That's defensible, but it should be presented as an addition.

**Updates applied to the design:**
- The PB gate distinguishes **prioritise** (approval/ranked; no fixed budget needed), **allocate** (knapsack; needs a confirmed discretionary amount), and **mobilise** (not a PB technique; leave to the source MIP).
- PB outputs are framed as *advisory input to SMC agreement*.

## 10. Assessment of the proposed Pinkard-based overhauls (added 2026-11-04)

The proposal applies Dr. Nichole Pinkard's work (Digital Youth Network, learning-ecosystem mapping, pathways across settings) to the same three Commons resources (#750, #753, #751).

### How it relates to what's already here

**Pinkard's work is part of the Connected Learning lineage.** She's a co-author of the 2020 CLRN report (card source [S2]). Her distinctive contributions are design-level:
- the **Digital Youth Network** (in-school and out-of-school media-arts programmes with mentors; see Barron, Gomez, Pinkard & Martin, *The Digital Youth Network*, MIT Press, 2014, to verify);
- **mapping a city's learning opportunities** (Chicago City of Learning, the DYN "OST Landscaping" toolkit) to find gaps and inequities in access;
- **pathways**, meaning deliberate links from one opportunity to the next.

So this is best treated as a **narrow extension of the Connected Learning cards**, not a third framework.

### What's worth adopting

| Idea | Indian-school form | Card (proposed) | Already partly present? |
|---|---|---|---|
| **Map community learning assets** | A chart-paper map of **places, programmes and people**: panchayat library, NGO centres, sports grounds, craftspeople, a health worker. **Not children.** | `CL-asset-map` (extends connections across settings) | Yes. Play Book's Neighbourhood Explorer and learning wall; the SMC module's session 6 on identifying resources |
| **Brokering / pathways:** an adult connects a student to the *next* opportunity | A teacher or mentor tells a student (and a parent) about one specific local opportunity linked to their interest | `CL-brokering` (extends relationships + opportunities) | Thin. Dream Job Map stays abstract. |
| **Attention to transitions** | Plans for students moving Class 5→6 or 8→9, where children change school and dropout risk rises | `CL-transitions` (scope note) | Not present in the catalogue profile |

### What should be rejected or reshaped

| Proposal element | Problem | Reshape |
|---|---|---|
| **SDP:** HMs track students' library visits, youth-group participation and home digital use; "AI Saathi processes this data pool" | **Monitoring children outside school.** Personal data of minors needs verifiable parental consent under the DPDP Act 2023, and collecting it is disproportionate for a school plan. An AI generating MIPs from it adds opacity. This is the most serious problem in any proposal so far. | Map **assets, not children**: aggregate and anonymous. Fits the SMC module's resource identification step. CL still **ABSTAINS** on the SDP; the asset map feeds the PB "mobilise" step. |
| **SLATE:** podcasts, a platform critique circle, remixing, auto-tracked badges | Digital-first (CL-G4); children's voices online (CL-G5); replaces the phonics sequence (CL-G1) | Same as the revised Golden Example 3: offline production, consented optional audio, sequence kept |
| **Play Book:** "Mitra" voice alerts to parents; platform tracking of mentors | **Unverified tool**; adds platform dependence | A paper or phone message from the teacher; the asset map on the Learning Centre wall |
| Tools named "AI Saathi" and "Mitra" | I couldn't confirm either as a Shikshagraha or ShikshaLokam product. The nearest match is Maharashtra's *Shiksha Saathi* (Rocket Learning), a different organisation and use. | Name only verified tools (rule already in §8) |
| **"Befores"** (grammar worksheets, printouts, "generic" activities, "exclusively internal" SDP) | **Inaccurate for the third time.** The sources (§8 update) have peer circles and a Mela, an existing expert and neighbourhood programme, and SMC and community involvement in the SDP. | Use source summaries |
| "DYN **proves** … deep, lasting literacy"; "**L3 (Learning Landscapes)** framework demonstrates…" | Overclaim (CL-G8). I couldn't verify the "L3 (Learning Landscapes)" framework name; the verified term is the OST *landscaping* toolkit. | Supportable phrasing: DYN research describes media production for real audiences, with mentors, as supporting digital literacy and identity; ecosystem mapping is used to find gaps in access. |

### Verdict
- **Sound in its core idea:** connect school learning to a mapped set of community opportunities, with adults who broker the next step. It fits Shikshagraha's society–government framing, and the transitions angle addresses a real gap in the catalogue.
- **Unsound as written:** it assumes a digital platform, surveils children's out-of-school lives, names unverified tools, and overstates the evidence.
- **Incremental value is modest**, because asset mapping already exists in the Play Book and the SMC module. The most distinctive additions are **brokering** and **transitions**.

**Adopted (2026-11-04):**
- `CL-asset-map`, `CL-brokering`, `CL-transitions` and guardrail **CL-G9** (map assets, never children) are in `frameworks/smt/connected-learning.md`, with sources S4 (verified) and S5 (secondary only).
- Critic check **C19** (blocker).
- `20-classify` now records `transition_year` and a child-tracking risk flag; `30-gate-cl` handles both.
- Golden Example 8, [evals/golden/transition-class8-to-9.md](evals/golden/transition-class8-to-9.md), plus gate fixture 8. The catalogue's only transition MIP is "School Exposure Visit" (entry to Std I), so the baseline re-targets that pattern to Class 8→9 and is flagged as a seed. It includes a critic test: a tracking variant must fail C19.

## 11. Assessment of the UCWhittle "intervention routing" proposal (added 2026-11-04)

The proposal: treat each **Section × Subject** as an arm of a restless multi-armed bandit (RMAB), with a binary state (below or above a foundational milestone) and four actions (status quo, SLATE kit, MIP project, weekend youth clinic). Learn transitions online with UCWhittle-style optimism, decaying memory and a novelty penalty. Then choose one action per arm each week with an integer program under kit and volunteer-hour budgets.

### Is the underlying research real? Yes.
- **UCWhittle:** Wang, K., Xu, L., Taneja, A., & Tambe, M. (2023). Optimistic Whittle Index Policy: Online Learning for Restless Bandits. *AAAI-23*, 37(8), 10131–10139. Kai Wang is first author; the proposal's "pioneered by Professor Lily Xu" overstates her role. It learns unknown transitions with confidence bounds and computes optimistic Whittle indices by solving a bilinear program.
- **Indian precedent:** Mate et al. (2022), *Field Study in Deploying Restless Multi-Armed Bandits* (AAAI-22). With the NGO ARMMAN (mMitra), RMABs chose which of ~23,000 mothers received limited live calls from health workers. That project shows RMABs **can** work for an Indian NGO, under specific conditions.

### Is this a use for *customising MIP content*? No. It's a different layer.
This project is a **design-time** tool: it rewrites what an MIP says. UCWhittle is a **run-time allocation** policy: it decides which classroom gets which programme this week. At most it could sit **downstream**, choosing among variants (e.g. baseline vs. CL-enriched) that this pipeline produces. It doesn't customise content.

### Soundness problems in the method as written

| # | Problem | Why it matters |
|---|---|---|
| 1 | **The "Whittle index" isn't a Whittle index.** The proposal uses a one-step difference in action values (active minus passive, each computed optimistically on its own). A Whittle index is the *subsidy* for passivity that makes the two actions equally attractive, which needs the indexability conditions. With **four actions** the standard Whittle index doesn't even apply; multi-action RMABs need different index methods. | The priority scores lack the guarantees attributed to UCWhittle. |
| 2 | **The reward points the wrong way.** In the code, `immediate_r = 1.0` when the section is in state 0 (*behind*). | The engine is rewarded for sections being behind. |
| 3 | **Data is far too thin.** A 12-week term gives each section-subject 12 transitions spread over 4 actions. Confidence radii stay huge, so "optimism" dominates and the choice is close to arbitrary. mMitra worked with tens of thousands of beneficiaries, *automatic* weekly signals (whether a call was listened to), and transitions estimated from **historical data clustered across arms**. | It would mostly allocate on noise unless data is pooled across many schools and terms. |
| 4 | **A weekly binary learning state per section needs measurement that doesn't exist.** "Bi-weekly micro-assessments" and weekly engagement logs for every section and subject are a large new burden on teachers. The catalogue's 99 MIPs have no such signal, and the Commons improvement-story template (#631) is a one-off narrative. | Without a cheap, reliable weekly signal, the loop can't run. mMitra's signal came free from the phone system. |
| 5 | **The hand-set novelty penalty** (0.05 per week after week 3) and the cross-school "leak" via Lipschitz distance are unvalidated assumptions, and the leak isn't implemented. | Unvalidated assumptions presented as mechanisms |
| 6 | **Equity is asserted, not designed.** Index policies can repeatedly pass over some arms (fairness in RMABs is its own research topic). Optimism means some classrooms are deliberately "explored" with interventions of unknown value. | Needs explicit fairness constraints (e.g. a minimum share for every section) and an ethics review. |

### Code defects (reproduced by running the estimation methods)
- `calculate_p_hat_and_radius` returns `p_hat` as a **2-element array**, so `min(1.0, p_hat + lambda_radius)` in the value and index methods raises `ValueError: The truth value of an array … is ambiguous`. **The engine fails on its first call.**
- The boredom penalty subtracts and then adds the same amount. On a scalar it's a **no-op**; on the array it also raises the error above.
- **No subject axis:** the ledger is `(sections, state, action, next_state)` and action age is `(sections, action)`, contradicting the "domain-isolated per subject" claim. Memory decay is applied to every subject's history whenever any one is updated.
- `log(t)` at `t = 1` gives a **zero confidence radius**, so there's no optimism at the start, when it matters most.
- The integer program's objective refers to an undefined `cohort_metadata_list` (a `NameError`). `pulp` also isn't installed here.

### Fit with Shikshagraha's model
- **Agency:** a micro-improvement is chosen and led by the HM or teacher ("pick one thing"). Centrally routing interventions to classrooms reverses that ownership. It also cuts against the PB direction in this project, where communities and SMCs choose.
- **Data protection:** section-level aggregates respect CL-G9 better than child-level tracking, but home-language and engagement proxies still need a purpose and consent review.

### Verdict
- **Soundness:** the research base is real, but this adaptation misdefines the index, rewards the wrong state, and its code doesn't run.
- **Viability now:** low. The weekly outcome signal, the data volume and the central allocation authority it assumes don't exist in the MIP system.
- **Relevance to this project:** it isn't a content-customisation method.

### What *would* be viable, and how it connects to this pipeline
1. **Record which variant was chosen and how it went.** Log, per MIP use: baseline vs. transformed variant, gate decisions, whether the owner completed it, and the improvement-story outcome (#631). This needs no new burden on teachers beyond what the platform already collects. **Done (schema level):** see [schema/mip-usage-event.schema.json](schema/mip-usage-event.schema.json), [schema/variant_id.py](schema/variant_id.py) and [schema/README.md](schema/README.md). Offers log the policy and the probability of what was shown first, so any later recommender can be evaluated offline. The schema rejects student-level data, names and raw school codes. Not yet wired into any platform.
2. **Compare variants with simple statistics first:** completion rates and owner ratings by domain and variant, pooled across schools.
3. **Only if the data supports it, add an *advisory* recommender:** a contextual bandit or Thompson-sampling recommender that suggests which variant to *offer first* to an HM, given the MIP's domain and school context. The HM still chooses, there's a minimum exploration share for every variant, and the recommender learns from completion data pooled across thousands of schools. The mMitra work is the right model for clustering arms, using historical data and running a field-study protocol.
4. **Scarce shared kits** (e.g. 10 SLATE boxes for 45 sections) are a real allocation problem. At school or cluster level, the **PB techniques** already in this project (a visible prioritisation, the SMC agreeing) are the more legitimate first tool. An optimiser could inform that discussion, not replace it.

## Sources

- [Shikshagraha Commons](https://commons.shikshagraha.org/) — MIP Template (resource 631), Domain-wise MIs Framework
- [Shikshagraha](https://shikshagraha.org/) · [Mantra4Change — Shikshagraha](https://www.mantra4change.org/shikshagraha/) · [District Collectives Playbook](https://shikshagraha.org/wp-content/uploads/2025/08/Shikshagraha-District-Collectives-Playbook.pdf)
- [Stanford Participatory Budgeting Platform](https://pbstanford.org/) · [Stanford Crowdsourced Democracy Team](https://voxpopuli.stanford.edu/projects) · [Boston youth PB](https://pbstanford.org/boston) · [Chicago 47th youth PB](https://pbstanford.org/chicago47_2020)
- [NWP — What Is Connected Learning?](https://teach.nwp.org/what-is-connected-learning/) · [CLRN final report (2020)](https://educatorinnovator.org/reflections-on-a-decade-of-engaged-scholarship-the-final-report-from-the-connected-learning-research-network/)

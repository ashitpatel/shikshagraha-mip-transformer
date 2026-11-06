# Shikshagraha MIP Transformer

**Agent prompts that improve Micro-Improvement Projects (MIPs) from [Shikshagraha Commons](https://commons.shikshagraha.org/) by applying evidence-based teaching practices, Connected Learning and participatory budgeting, only where they genuinely fit.**

> **Status (November 2026): exploration and prototype.** The method (framework cards, review checklist, prompts, schema, reference examples, user docs, and an agent kit for any AI chat assistant) is written and internally checked. **Nothing has been run live yet, and no practitioner has reviewed it.** The "after" plans in the examples are hand-written reference answers, not tool output. Treat every claim about learning outcomes below as a hypothesis to test.

---

## Goal

[Shikshagraha](https://shikshagraha.org/) is a movement to strengthen India's public schools through **micro-improvements**: small, school-led projects (typically 2–4 weeks, 5–7 tasks) that a head teacher or teacher picks and runs. Its site reports more than 1.37 million micro-improvements in schools [R1]. ShikshaLokam's catalogue of these projects (the *Domain-wise Micro Improvements Framework*, Commons #259) lists 99 MIPs across six domains.

This project asks one question: **can an AI assistant make a given MIP better at improving learning, without making it bigger, riskier or less the school's own?**

It does that by:
1. **checking** each MIP against three sets of methods: **evidence-based practices** with the strongest trial evidence in contexts like Indian public schools (teaching by learning level, in-school tutoring, daily sound-symbol reading practice, head-teacher feedback on state lesson guides; see the [evidence ranking](reports/Education%20interventions%20evidence%20ranking.md)), **Connected Learning** (Ito et al.), and **participatory budgeting** (from Stanford's Crowdsourced Democracy Team and related work);
2. **applying** them only where they fit, and saying plainly when they don't;
3. **keeping** the original objective, the "micro" size, and the adult owner;
4. **reviewing** every revision against 21 checks, including whether the right methods were chosen (no invented evidence, no tracking of children, no money handled by students, offline by default, and so on);
5. **delivering** teacher cards for the original *and* the revised plan, so the school chooses. The front of each card (one page) is what the teacher runs from; the back of the revised card says what changed and why.

### Why this might matter
- **Learning levels are low and recovering slowly.** In ASER 2024 (rural India), **23.4%** of government-school children in Std III could read a Std II-level text, the highest in the survey's history, and **44.8%** of Std V children could [R2]. Roughly three in four Std III children in government schools still can't.
- **Students drift away before they drop out.** Secondary-level dropout was about **14.1%** in 2023-24 (UDISE+, as reported in secondary analyses), against about **1.9%** at primary [R3]. The *Learning Centre Play Book* in Commons was written because children "gradually disengage" before leaving [R4].
- **The catalogue treats students mostly as beneficiaries.** Of the 99 catalogue MIPs, "student" appears in 61, but **none** mention peer learning, clubs or cabinets, and **none** mention a grant, fund, budget or cost (our count of Commons #259). That leaves room for student agency, and very little room for budgeting methods.

---

## How it works

```
MIP (paste / upload / link) ──► read it ──► check fit ──► revise (only if it fits) ──► review (21 checks) ──► teacher cards
                                   │            │
                         long resource?    "doesn't apply" is a valid, common answer
                         → one ≤8-week slice
```

The same method ships in two forms:
- **For anyone, now:** the **[agent kit](agent-kit/README.md)**, a paste-in prompt (full or lite), a custom-assistant package, a Claude Skill and an independent reviewer prompt. It works in ChatGPT, Gemini, Claude, Copilot and free tiers. No install, no API key.
- **For developers:** **[prompts/](prompts/README.md)**, nine JSON-in/JSON-out prompts, a [schema](schema/README.md), and a [test runner](evals/run_gates.py) for the fit checks.

---

## Getting started

Pick the path that matches what you want to do.

### 1. Try it on a MIP (5 minutes, any AI chat assistant, free tiers included)
1. Open a **new chat** in ChatGPT, Gemini, Claude, Copilot or similar.
2. Copy all of [agent-kit/dist/paste/mip-transformer-full.md](agent-kit/dist/paste/mip-transformer-full.md) and send it as your first message. If the assistant has a small context window, or ignores the steps, use [mip-transformer-lite.md](agent-kit/dist/paste/mip-transformer-lite.md) instead.
3. When it asks, paste a MIP's text or upload the file downloaded from [Shikshagraha Commons](https://commons.shikshagraha.org/). Commons links often don't open for assistants, so use the resource page's **Download** button. Then answer its questions: your role, the card language, and any open question such as "Are state lesson guides in use?"
4. You get teacher cards for the original and the revised plan, with what changed and why.
5. **Optional, recommended:** in a *fresh* chat, paste [mip-reviewer.md](agent-kit/dist/paste/mip-reviewer.md), then the original and revised plans, for an independent check.

To try it on a known case, use the starting plan from [walkthrough 9](docs/walkthroughs/09-reading-by-learning-level.md) and compare the result with the walkthrough. For a reusable assistant (a ChatGPT Project, a Gemini Gem, a Claude Project or Skill), see [agent-kit/README.md](agent-kit/README.md).

### 2. Understand what it does (15 minutes, no setup)
1. [docs/ux/02-journey.md](docs/ux/02-journey.md): the end-to-end journey.
2. Two or three walkthroughs from [docs/README.md](docs/README.md). Start with [9](docs/walkthroughs/09-reading-by-learning-level.md) (an evidence-based practice), [6](docs/walkthroughs/06-school-resources.md) (participatory budgeting) and [7](docs/walkthroughs/07-real-world-projects.md) (Connected Learning).
3. [The evidence ranking](reports/Education%20interventions%20evidence%20ranking.md): why these methods, and why they're ordered as they are.

### 3. Develop or test it (Python 3.10+)
Install the two libraries used:

```bash
python3 -m pip install anthropic jsonschema
```

Check everything offline (no API key needed):

```bash
python3 schema/validate_examples.py && python3 evals/decision_model.py --strict && python3 evals/run_gates.py --dry-run && python3 agent-kit/build.py
```

Run the live fit-check test. This makes 60 calls on Claude Opus 5.5, costing a few dollars. Set the key in your own terminal; don't paste it into a chat:

```bash
export ANTHROPIC_API_KEY=...
```

```bash
python3 evals/run_gates.py
```

Results go to `evals/runs/<timestamp>/summary.md`. After editing anything in `frameworks/` or `agent-kit/src/`, rerun `python3 agent-kit/build.py` to regenerate the kit. Keep `agent-kit/src/review-checklist.md` in step with `prompts/50-critic.md`.

---

## The frameworks

> **How they rank.** A scan of the education research ([reports/Education interventions evidence ranking.md](reports/Education%20interventions%20evidence%20ranking.md)) scored 33 options. It weighed evidence quality, effect size, similarity of context to Indian public schools, and feasibility, with researcher reputation used only as a tie-breaker. **Four evidence-based practices came out on top (section 0 below). Connected Learning and participatory budgeting score low as *learning* levers** (no causal learning-outcome evidence). They stay in the project as an engagement design lens and as a way to choose among evidence-based options.

### 0. Evidence-based practices (Tier 1 of the evidence ranking)

**What they are.** Four practices with randomised-trial evidence from public-school systems with low baseline learning, large classes and constrained teachers (India, Kenya, Zambia, South Africa), plus high-rated syntheses. They're applied **only with their non-negotiables**, the components without which the trials show no effect. Full cards: [frameworks/evidence-based-practices.md](frameworks/evidence-based-practices.md).

| Practice | What it adds to a MIP | Key evidence (from the cards' supportable claims) |
|---|---|---|
| **Teaching by learning level** (Teaching at the Right Level style) | An oral baseline; a protected daily slot or camp with flexible level groups; a weekly review of level movement; an endline | Indian trials: about 0.15 SD with a dedicated daily hour by government teachers, about 0.70 SD with 40-day volunteer camps, and **no effect** with training alone [E1]. Kenya: about 0.14 SD [E3]. Zambia national scale-up: about 0.10 SD literacy and 0.15 SD numeracy [E4]. A GEEAP "Great Buy" [E11]. |
| **In-school tutoring** by local volunteers (older pupils as fallback) | Recruit 2–6 volunteers; tutor the children furthest behind in school hours with a scripted activity | Balsakhi (Indian municipal schools): about 0.14 SD in year one and 0.28 SD in year two, fading after the programme [E5]. Meta-analysis of 89 RCTs: about 0.29 SD, in-school stronger [E7]. |
| **Daily sound-symbol (akshara) and fluency block** | 15–20 minutes daily of explicit, sequenced sound-symbol work, decodable text, and a weekly oral reading check | Rated "strong" by the What Works Clearinghouse [E9]. EEF +5 months [E8]. All eight high-performing large-scale reading programmes in a 120-study LMIC review used explicit sub-skill teaching [E10]. |
| **Head-teacher feedback on state lesson guides** (only where materials exist) | Weekly observation against a ≤5-item checklist tied to the day's lesson, plus content-specific feedback | Structured pedagogy averages about 0.23 SD in language and 0.14 SD in maths [E12]. On-site coaching in South Africa: about 0.23 SD [E13]. A head teacher's loop is a lighter copy, so expect less. |
| **Plan-to-routine rule** (for head-teacher planning MIPs) | Turn the plan's top priority into a classroom routine; tie purchases to the routine that uses them | School self-assessment and improvement plans had **no learning effect** across 1,774 Madhya Pradesh schools [E14] |

**Realistic expectations.** Large preregistered education trials average about **0.06 SD** [E15]. A school-led 4–8 week version should be planned at about **0.05–0.15 SD on an independent test**. That's a planning assumption, not a measured result, and every rationale must say so.

*References E1–E15 are listed in the card file's sources section.*

Each framework below lists: **what it is**, **how it is applied to a MIP** in this project, **how it could improve learning outcomes**, **what the evidence actually shows (with numbers where they exist)**, and **further reading**. The full, citation-checked rules are in [frameworks/connected-learning.md](frameworks/connected-learning.md) and [frameworks/pb-techniques.md](frameworks/pb-techniques.md).

### 1. Connected Learning (Mizuko Ito and the Connected Learning Research Network)

**What it is.** An approach to learning that is **interest-driven, supported by relationships, and connected to opportunity** (academic, economic or civic) [C1]. The 2013 agenda framed it as three spheres (interests, peer culture, academics) and three design features (production-centred, shared purpose, openly networked) [C1]. The 2020 review of a decade of research renamed the spheres **interests, relationships and opportunities**, and added **sponsorship of youth interests, shared practices, shared purpose and connections across settings** [C2]. It's explicitly an **equity agenda**: interest-driven learning tends to reach already-advantaged young people unless it is deliberately designed for everyone [C1, C2].

**How this project applies it to a MIP.** Through 12 "cards", each with a fit test, allowed edits, things to avoid, and the only claims a rationale may make:

| Card | What it adds to a MIP | Example |
|---|---|---|
| Interests | A student choice inside an existing task | Houses pick a theme for SLATE phonics posters ([walkthrough 3](docs/walkthroughs/03-slate-land-1.md)) |
| Peers | Rotating roles, peer feedback, students as teachers | Measurer, recorder, checker and presenter roles ([walkthrough 7](docs/walkthroughs/07-real-world-projects.md)) |
| Relationships | A short, supervised contact with a community adult | Interviewing a tailor or shopkeeper ([walkthrough 4](docs/walkthroughs/04-learning-centre-neighbourhood-month.md)) |
| Opportunities | Tie the activity to a syllabus outcome or pathway | Mastery checks kept unchanged |
| Production / audience | Students make something and show it to people who care | A poster walk; a family showcase |
| Shared purpose | A collective goal next to competition | A whole-grade bonus in SLATE |
| Connections across settings | Home and neighbourhood as content | Shop prices, cricket scores, rainfall |

It's **not** applied to administrative or governance MIPs (about 60% of the catalogue is owned by head teachers): calling community participation "Connected Learning" would be relabelling. In foundational literacy and numeracy, it may only **add**; it never replaces structured practice or mastery checks.

**How it could improve learning outcomes (mechanisms, not proven effects).**
- **Engagement and persistence.** Linking school tasks to students' own interests and to real audiences is how the framework explains sustained engagement [C1, C2]. That's the lever for students who are drifting away (see the dropout figures above).
- **Relevance and transfer.** Problems drawn from students' own surroundings (prices, crops, sport) give practice a meaning beyond the textbook.
- **Peer learning at scale.** Structured peer roles let one teacher reach more students, which already happens in SLATE's student-led circles.
- **Equity.** Choices open to all students, rotating roles, and offline production avoid privileging students with devices or confidence.

**What the evidence shows.** Be careful here: the evidence base is **mainly ethnographic, qualitative and design-based**, mostly from the US and UK and often out of school [C1–C3]. It describes *how and when* engagement happens; **it does not establish effect sizes on test scores.**
- *Hanging Out, Messing Around, and Geeking Out* is a **three-year ethnographic study** with 23 case studies of how young people learn with new media across home, after-school and online settings [C3].
- The network ran a **longitudinal survey** tracking interest development, persistence, civic participation and young people's sense of their future [C4]. We haven't found published headline figures from it that we can cite.
- Small programme studies report gains in confidence and STEM supports. One study of **54 youth aged 12–17** in an out-of-school STEM studio reported such gains, but it's small and self-reported [C5].
- **No evidence from Indian government schools is known to this project.** This project's rationale rules forbid claiming any numerical effect.

**Further reading:** [C1] [C2] [C3] [C4]; the MacArthur Foundation's [Research Network on Connected Learning](https://www.macfound.org/programs/pastwork/research-networks/research-network-connected-learning).

#### 1a. Learning ecosystems and pathways (Nichole Pinkard), an extension of Connected Learning

**What it is.** Pinkard (a co-author of the 2020 Connected Learning report [C2]) founded the **Digital Youth Network (DYN)** in 2006 in Chicago, linking in-school and out-of-school media-arts learning with mentors for economically disadvantaged middle-school students [P1]. Her later work **maps a city's learning opportunities** to find gaps in access: Chicago City of Learning identified out-of-school computer science opportunities in most of Chicago's 77 neighbourhoods [P2].

**How this project applies it.** Three cards, all bound by the rule **"map assets, never children"**:
- a **community learning-asset map** of places, programmes and consenting adults;
- **brokering**: a teacher connects each student to one concrete next opportunity;
- **transitions**: Class 5→6 and Class 8→9, when children often change school.

See [walkthrough 8](docs/walkthroughs/08-class-8-to-9-transition.md). A proposal to track students' out-of-school activity and have an AI flag "at-risk" children was **rejected** (privacy under India's DPDP Act 2023, and stigma).

**How it could improve outcomes.** It targets the point where secondary dropout rises [R3] with continuity: a personal next step, a peer buddy, and something that travels with the student.

**Evidence.** DYN was studied in a **three-year mixed-methods study** [P1], which reports on imaginative production, expertise with digital media tools, and students' willingness to share their skills. We haven't found effect sizes on academic outcomes. The Chicago mapping work is documented in secondary sources [P2, P3].

**Further reading:** [P1] [P2] [P3].

### 2. Participatory budgeting (Stanford Crowdsourced Democracy Team and related work)

**What it is.** A process where a group (residents, students, a school committee) **directly decides how a shared public resource is spent**: idea collection → proposal development and vetting → vote → implementation → report-back. Stanford's Crowdsourced Democracy Team contributed mainly **ballot design and counting**, especially **knapsack voting**, in which each voter picks projects whose costs fit within the real budget, so voters face the trade-offs themselves [B1]. Their open-source platform supports **approval, knapsack and ranked** ballots [B2]. A separate group introduced the **Method of Equal Shares**, which gives proportional outcomes to groups with different preferences [B3].

**How this project applies it to a MIP.** Through 10 cards, adapted to Indian School Management Committees (SMCs), whose statutory role under the RTE Act includes preparing the School Development Plan and monitoring grants [B5]:

| Technique | When it fits | Example |
|---|---|---|
| **Priority vote** (approval ballot) | ≥2 competing needs and a legitimate group decision | SMC ranks school needs ([walkthrough 6](docs/walkthroughs/06-school-resources.md)) |
| **Knapsack ballot** | Only with **confirmed, discretionary** money | Students allocate a ₹20,000 fund ([walkthrough 1](docs/walkthroughs/01-civics-lab.md)) |
| Counting rule, idea collection with evidence, vetting on feasibility only, report-back | Around any ballot | Rejections and results posted publicly |
| **Borrowed without the label** | A hard cap but no shared public resource | A team's 20 hours ([walkthrough 2](docs/walkthroughs/02-team-projects-time-budget.md)): "adapted from knapsack voting", not "PB" |

Two adaptations came from reading Prajayatna's SMC training module (Commons #595) [B4]:
- **Ballots inform the SMC's agreement; they don't replace it.**
- **Most school resources are raised, not drawn from a fixed pot**, so prioritising usually matters more than allocating.

**How it could improve learning outcomes (indirect).**
- **Better-targeted spending:** a visible, inclusive priority vote can surface needs that affect learning (water, toilets, books, accessibility) that one person might rank lower.
- **Accountability:** posted results and spending keep the SMC and school answerable to families.
- **Civic and mathematical learning for students:** weighing costs within a budget is practical arithmetic and decision-making.
- **Voice:** women members and quieter students are heard before discussion closes.

**What the evidence shows.** PB research mainly concerns **participation, legitimacy and civic learning**. **Evidence that it improves academic outcomes is thin.**
- **Knapsack voting** was the official ballot in **Boston's 2016 youth PB election** (Youth Lead the Change, ages 12–25) [B1].
- In **Phoenix Union High School District's** school PB, **3,854 students (~84%)** turned out to vote, and **786 students registered as Arizona voters** during the PB vote. These are programme-reported figures, and one case review notes **no formal evaluation** [B6, B7].
- A 2021 study (Gibbs, Bartlett & Schugurensky) is summarised by the Participatory Budgeting Project as finding **stronger political efficacy** and gains in democratic knowledge among students in school PB. We have not verified its methods or effect sizes [B8].
- **No Indian school-level PB evidence is known to this project.**

**Further reading:** [B1] [B2] [B3] [B6] [B8]; the [Participatory Budgeting Project's PB in Schools](https://www.participatorybudgeting.org/campaigns-advocacy/pb-in-schools/).

### 3. Evaluated but not applied: restless multi-armed bandits (UCWhittle)

**What it is.** An online learning method (Wang, Xu, Taneja & Tambe, AAAI 2023) for deciding which of many "arms" to act on each round under a budget, when outcomes are uncertain and change over time [U1]. A proposal suggested using it to route interventions (SLATE kits, MIPs, volunteer clinics) to classroom sections each week.

**Why it isn't applied.**
- It answers a **different question**: run-time allocation, not improving a MIP's content.
- The proposed adaptation **misdefined the index and rewarded sections for being behind**, and its code **failed on its first call**.
- It needs a **weekly outcome signal per section** that doesn't exist.
- It **reverses school ownership** of improvement.

Full analysis: [EXPLORATION.md §11](EXPLORATION.md).

**Evidence where it does work.** With the Indian NGO ARMMAN's mMitra maternal-health programme, a restless-bandit policy deciding which mothers received scarce live calls **reduced engagement drops by about 30%** compared with the standard of care. That was a 7-week study of **23,003 participants** [U2, U3]. A later evaluation found performance **not consistent across three deployments**; the 30% study was the best [U4]. That setting had an automatic weekly signal and tens of thousands of people, which is why it worked there.

**What we kept:** a privacy-restricted **usage log** ([schema/mip-usage-event.schema.json](schema/mip-usage-event.schema.json)), so a simple, *advisory* recommender could be tested later on real data.

### Other proposals evaluated
Several "overhaul" proposals were reviewed against the actual Commons sources. Common problems were "befores" that understated the originals, invented statistics, unverified tools, digital-first designs, and tracking of children. Accepted ideas became cards; the rest were reshaped or rejected, with reasons in [EXPLORATION.md](EXPLORATION.md) §7–§10.

---

## What this project can and can't claim about learning outcomes

| Can say | Can't say (yet) |
|---|---|
| The revisions apply research-described mechanisms (interest, peers, audience, inclusive decisions) to real MIPs, within safety and size limits | That any revised MIP improves test scores, attendance or dropout |
| Each rationale uses only claims supported by the cited sources | Any effect size for Connected Learning or school PB in Indian government schools |
| Success indicators are built in, including "no worse than before" checks for literacy | That the agent kit produces good output on any assistant: it hasn't been run |

**How to find out:** run the [fit-check test](evals/run_gates.py) → try the [agent kit](agent-kit/README.md) on the [walkthrough MIPs](docs/walkthroughs/) → have practitioners review the output → pilot in a few schools with the [usage log](schema/README.md) and randomised offer order → compare completion and indicators.

---

## Folder structure

```
ShikshagrahaMIPTransformer/
├── README.md                     ← you are here
├── EXPLORATION.md                soundness and viability analysis; assessment of every proposal
│
├── agent-kit/                    USE IT NOW in any AI chat assistant (no install, no API key)
│   ├── README.md                 which file to use for which assistant, and setup steps
│   ├── src/                      single source: instructions, review checklist, card template, reviewer
│   ├── build.py                  maintainers: regenerates dist/ and checks sizes and IDs
│   └── dist/                     GENERATED, ready to use
│       ├── paste/                mip-transformer-full.md, mip-transformer-lite.md, mip-reviewer.md
│       ├── custom-assistant/     instructions.txt + knowledge/ (ChatGPT Project, Gemini Gem, Claude Project…)
│       └── claude-skill/         mip-transformer/ folder + mip-transformer.zip
│
├── docs/                         READ FIRST if you're new
│   ├── README.md                 index
│   ├── ux/                       who uses it, the end-to-end journey, decision points
│   ├── walkthroughs/             12 plain-language examples (01–12), each ending in a teacher card
│   └── regeneration-prompts.md   14 prompts to rebuild this project from scratch with an AI coding agent
│
├── frameworks/                   THE METHOD: cards the prompts read
│   ├── evidence-based-practices.md   Tier 1 practices + Tier 2 pilot cards (EB-*)
│   ├── connected-learning.md         Connected Learning + Pinkard extension (CL-*)
│   └── pb-techniques.md              participatory budgeting techniques (PB-*)
│
├── prompts/                      DEVELOPER PIPELINE: 9 JSON-in/JSON-out prompts
│   ├── README.md                 flow diagram and orchestration notes
│   ├── 10-parse.md  15-derive.md  20-classify.md
│   ├── 30-gate-cl.md  31-gate-pb.md  32-gate-eb.md
│   └── 40-transform.md  50-critic.md  60-render.md
│
├── schema/                       DATA
│   ├── mip.schema.json           a MIP, plus x_transform (gates, changes, variant identity)
│   ├── mip-usage-event.schema.json   privacy-restricted log of how schools use a MIP
│   ├── variant_id.py             stable content IDs for MIP variants
│   ├── validate_examples.py      validates examples; checks the log rejects personal data
│   └── examples/                 a baseline and transformed MIP; one synthetic usage log
│
├── evals/                        TESTING
│   ├── golden/                   12 reference examples (technical versions of the walkthroughs)
│   ├── gate_fixtures.json        15 test inputs with expected fit-check decisions
│   ├── decision_model.py         executable model of the fit-check rules (no API needed)
│   ├── decision_cases.json       20 cases for the model, including edge cases
│   ├── run_gates.py              fit-check test runner (needs ANTHROPIC_API_KEY for live runs)
│   ├── sources.md                Commons documents the examples are built from
│   └── runs/                     created by live test runs
│
├── reports/
│   ├── Education interventions evidence ranking.md   33 options scored; how the Tier 1/2 practices were chosen
│   └── Decision path analysis.md     verification of how the agent chooses a method, and the fixes made
└── research_notes/
    └── Education interventions evidence ranking/     the five research notes behind that report
```

---

## References

**Context**
- [R1] Shikshagraha. https://shikshagraha.org/ (reported micro-improvement count, accessed November 2026).
- [R2] ASER Centre (2025). *ASER 2024 National Findings.* https://asercentre.org/wp-content/uploads/2022/12/ASER-2024-National-findings.pdf
- [R3] Mehta, A. C. *School Education in India: analysis based on UDISE+ 2023-24.* https://educationforallinindia.com/school-education-in-india-where-do-we-stand-udiseplus-2023-24/ (secondary analysis; check official UDISE+ tables before quoting).
- [R4] Vidhya Vidhai Foundation. *Learning Centre Play Book* (Shikshagraha Commons #753).

**Connected Learning**
- [C1] Ito, M., Gutiérrez, K., Livingstone, S., Penuel, B., Rhodes, J., Salen, K., Schor, J., Sefton-Green, J., & Watkins, S. C. (2013). *Connected Learning: An Agenda for Research and Design.* Digital Media and Learning Research Hub. https://researchonline.lse.ac.uk/id/eprint/48114
- [C2] Ito, M., Arum, R., Conley, D., Gutiérrez, K., Kirshner, B., Livingstone, S., Michalchik, V., Penuel, W., Peppler, K., Pinkard, N., Rhodes, J., Salen Tekinbaş, K., Schor, J., Sefton-Green, J., & Watkins, S. C. (2020). *The Connected Learning Research Network: Reflections on a Decade of Engaged Scholarship.* Connected Learning Alliance. https://archive.informalscience.org/sites/default/files/CLRN_Report.pdf
- [C3] Ito, M., et al. (2010). *Hanging Out, Messing Around, and Geeking Out.* MIT Press. doi:10.7551/mitpress/8402.001.0001
- [C4] Connected Learning Research Network. *Measuring experiences of interest-related pursuits in connected learning* (longitudinal survey paper). https://connectedlearning.uci.edu/wp-content/uploads/2019/05/Academic-Paper-Measuring-Experiences-of-Interest-Related-Pursuits-in-Connected-Learning-Longitudinal-Survey-of-Connected-Learning.pdf
- [C5] *Interest-Driven Learning Among Middle School Youth in an Out-of-School STEM Studio.* https://www.researchgate.net/publication/262992947_Interest-Driven_Learning_Among_Middle_School_Youth_in_an_Out-of-School_STEM_Studio

**Learning ecosystems (Pinkard)**
- [P1] Barron, B., Gomez, K., Pinkard, N., & Martin, C. K. (2014). *The Digital Youth Network: Cultivating Digital Media Citizenship in Urban Communities.* MIT Press. Review: https://blogs.lse.ac.uk/usappblog/2014/11/30/book-review-the-digital-youth-network-cultivating-digital-media-citizenship-in-urban-communities-by-brigid-barron-kimberley-gomez-nichole-pinkard-and-caitlin-k-martin
- [P2] Northwestern SESP (2020). *Researchers begin developing computer science ecosystem.* https://sesp.northwestern.edu/news-events/sesp-news/2020/researchers-begin-developing-computer-science-ecosystem.html
- [P3] STEM Learning Ecosystems. *Spotlight: Chicago STEM Pathways Cooperative.* https://stemecosystems.org/stem-ecosystems-spotlight-chicago-stem-pathways-cooperative/

**Participatory budgeting**
- [B1] Goel, A., Krishnaswamy, A. K., Sakshuwong, S., & Aitamurto, T. (2019). Knapsack Voting for Participatory Budgeting. *ACM Transactions on Economics and Computation*, 7(2), Art. 8. doi:10.1145/3340230. https://arxiv.org/abs/2009.06856
- [B2] Stanford Participatory Budgeting Platform. https://pbstanford.org/
- [B3] Peters, D., Pierczyński, G., & Skowron, P. (2021). Proportional Participatory Budgeting with Additive Utilities. *NeurIPS 34*, 12726–12737. https://arxiv.org/abs/2008.13276
- [B4] Prajayatna. *SMC Module 2: School Development Plan and Budgeting* (Shikshagraha Commons #595, Hindi).
- [B5] Right of Children to Free and Compulsory Education Act, 2009, §21–22 (as summarised in statutory commentary; check the gazette text).
- [B6] National Civic League. *Phoenix Schools Implement District-Wide Participatory Budgeting.* https://www.nationalcivicleague.org/promising-practices/phoenix-schools-implement-district-wide-participatory-budgeting-phoenix-az/
- [B7] Participedia. *Phoenix Union High School District Participatory Budgeting.* https://participedia.net/case/5586
- [B8] Gibbs, N. P., Bartlett, T., & Schugurensky, D. (2021). Does School Participatory Budgeting Increase Students' Political Efficacy? *Curriculum and Teaching*, 36(1). Summary: https://www.participatorybudgeting.org/lesson-1-school-pb-is-an-onramp-to-civic-education/

**Restless bandits**
- [U1] Wang, K., Xu, L., Taneja, A., & Tambe, M. (2023). Optimistic Whittle Index Policy: Online Learning for Restless Bandits. *AAAI-23*, 37(8), 10131–10139. https://ojs.aaai.org/index.php/AAAI/article/view/26207
- [U2] Mate, A., Madaan, L., Taneja, A., Madhiwalla, N., Verma, S., Singh, G., Hegde, A., Varakantham, P., & Tambe, M. (2022). Field Study in Deploying Restless Multi-Armed Bandits: Assisting Non-profits in Improving Maternal and Child Health. *AAAI-22*, 36(11), 12017–12025. https://arxiv.org/abs/2109.08075
- [U3] Google Research (2022). *Using ML to Boost Engagement with a Maternal and Child Health Program in India.* https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/
- [U4] *Decision-Focused Evaluation: Analyzing Performance of Deployed Restless Multi-Arm Bandits.* https://arxiv.org/abs/2301.07835

*Statistics are reproduced from the sources above. Where only secondary sources were available this is noted; check the primary source before quoting.*

---

## Licence and attribution

This repository is dual-licensed by file type:

| What | Licence | Files |
|---|---|---|
| **Code** | [Apache License 2.0](LICENSE) | `*.py` (`agent-kit/build.py`, `evals/run_gates.py`, `schema/variant_id.py`, `schema/validate_examples.py`) and the JSON Schemas (`schema/*.schema.json`) |
| **Content** | [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](LICENSE-CONTENT) | Everything else: docs, framework cards, prompts, agent-kit instructions and generated packages, reference examples, test fixtures, reports and research notes |

**Why CC BY-SA for content:** the examples, walkthroughs and cards adapt **Shikshagraha Commons** materials published under CC BY-SA, by ShikshaLokam, Mantra4Change, Vidhya Vidhai Foundation and Prajayatna. ShareAlike requires derivatives to carry the same licence.

**Attribution:** when you reuse content, credit "Shikshagraha MIP Transformer contributors" and keep the credit to the original Commons organisation on any derived MIP or teacher card ("Adapted from <title>, <organisation>, via Shikshagraha Commons. CC BY-SA."). Research cited in the reports and cards belongs to its authors and is linked, summarised or briefly quoted, not reproduced.

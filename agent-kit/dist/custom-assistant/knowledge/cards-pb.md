# CARDS-PB

> **Purpose:** the transformer and critic prompts read this file. Each card gives the **gate test**, the **edits allowed** to an MIP, **anti-patterns**, and **supportable claims**. Rationale claims must cite a card ID (`basis: PB-…`) and stay within that card's *Supportable claims*.
>
> **Primary sources** (paraphrased; verify exact details against the originals):
> - [P1] Goel, A., Krishnaswamy, A. K., Sakshuwong, S., & Aitamurto, T. (2019). Knapsack Voting for Participatory Budgeting. *ACM Transactions on Economics and Computation*, 7(2), Article 8, 27 pp. doi:10.1145/3340230. arXiv:2009.06856. An earlier version, "Knapsack Voting", appeared at Collective Intelligence 2015. Stanford Crowdsourced Democracy Team.
> - [P2] Stanford Participatory Budgeting Platform, https://pbstanford.org/. Open-source digital ballots supporting approval, knapsack and ranked voting, plus remote voting. Used for city and youth PB, e.g. Boston's Youth Lead the Change (ages 12–25), the Chicago 47th Ward youth PB (2020), and Long Beach's Youth Power PB (2022).
> - [P3] Peters, D., Pierczyński, G., & Skowron, P. (2021). Proportional Participatory Budgeting with Additive Utilities. *Advances in Neural Information Processing Systems 34* (NeurIPS 2021), 12726–12737. arXiv:2008.13276. It introduces the **Method of Equal Shares** (called "Rule X" in early versions). It's from this group, **not** the Stanford team.
> - [P4] Prajayatna, *SMC Module 2 – School Development Plan and Budgeting* (Shikshagraha Commons #595, Hindi): SMC norms of collective agreement, equal voice for women and men, resource mobilisation.
> - [P5] Right of Children to Free and Compulsory Education Act, 2009. **§21(2):** the SMC monitors the working of the school, prepares and recommends the School Development Plan, and monitors use of grants. **§22:** the SDP, which is the basis for government or local-authority plans and grants. *Exception:* SMCs of aided minority schools aren't required to prepare an SDP under §22. State rules set the timing and further functions.
>
> *Verified 2026-11-04 against publisher, proceedings and statutory-commentary records (see "Verification log" at the end). P5 wording is from secondary sources and state rules; check it against the gazette text before quoting.*

## What PB is, in one paragraph

Participatory budgeting is a process in which **members of a constituency directly decide, or directly shape the decision on, how a shared public resource is spent**. The usual phases are idea collection → proposal development and vetting → vote → implementation → report-back. The Stanford team's distinctive contribution is in **ballot design and counting**, especially **knapsack voting**: voters choose projects within the real budget, so they face the trade-offs themselves [P1, P2].

## Nature of the evidence (governs every card)

- PB research and evaluations concern **participation, legitimacy, civic learning, and allocation outcomes**. Evidence that **school or youth PB improves academic learning** is thin. **No Indian school-level PB evidence is known to this project.**
- **Never claim** numbers, "proven", or effects on learning outcomes from PB.
- Claims about *mechanisms* (what a knapsack ballot forces voters to consider) are fine. Claims about *impact* must be labelled untested.

## Scope cards

### PB-scope — when the *PB process* label applies
- **All three must hold:**
  1. a **constituency** (students of a school, SMC members, parents);
  2. a **shared public resource** (money, a space, scarce materials);
  3. a **public, accountable outcome**.
- **ABSTAIN when:** a team divides its *own* time or work (that's prioritisation; see `PB-not-pb`), or there's nothing to choose between.
- **Anti-patterns:** calling team scoping "PB"; calling community consultation "Connected Learning".

### PB-india-smc — fit with SMC practice (applies to every PB edit in Indian government schools)
- **Facts to respect:**
  - The SMC is the statutory body for the SDP and grant monitoring [P5].
  - SMC norms emphasise **reaching agreement together**, equal voice for women and men, and including parents from every class and community [P4].
  - Most resources are **mobilised** (from parents, the Gram Panchayat, block departments, local businesses or donors) rather than drawn from a fixed pot [P4].
  - Students aren't part of the SMC process; adding student voice is an **addition** and must be labelled as such.
- **Rule:** in SMC contexts, ballots are **advisory inputs to SMC agreement**, not binding votes, unless the SMC itself decides otherwise.

## Technique cards

### PB-prioritise — approval or ranked voting on needs or options
- **Means:** each participant ticks every option they support (approval) or orders them (ranked) [P2]. No costs are needed.
- **Gate test:** are there ≥2 competing needs or options, and is the decision legitimately collective?
- **Allowed edits:** add one ballot step before a decision task; show the tally visibly (chart paper); record the agreed order in the minutes.
- **Anti-patterns:** a ballot after the decision is already made; secret tallies; letting a ballot override the SMC's agreement process.
- **Supportable claims:** "Approval voting lets each participant support several options and shows the group's spread of priorities before discussion." "Approval and ranked ballots are among the methods supported by the Stanford PB platform."

### PB-allocate-knapsack — knapsack ballot within a fixed amount
- **Means:** each voter picks projects whose costs add up to no more than the real budget, so trade-offs are explicit [P1].
- **Gate test:** is there a **confirmed, discretionary amount** (₹ or another hard cap) **and** ≥2 costed options that together exceed it?
- **Allowed edits:** a costed proposal list plus a knapsack ballot (paper: a running-total column checked at the desk; digital: [P2]), with the counting rule stated beforehand (`PB-count-greedy`).
- **Anti-patterns:** using it when there's no confirmed amount; costs nobody has checked; earmarked funds treated as discretionary.
- **Supportable claims:** "A knapsack ballot asks each voter to stay within the real budget, so voters weigh costs and trade-offs themselves." "Knapsack voting was proposed and studied by the Stanford Crowdsourced Democracy Team." "Knapsack voting was used as the official ballot in Boston's 2016 youth participatory budgeting election (Youth Lead the Change)." [P1]

### PB-count-greedy — counting rule for paper ballots
- **Means:** count support per option; sort from most to least; fund down the list while money remains, skipping any option that doesn't fit; break ties by lower cost. It's simple enough to count by hand.
- **Gate test:** used whenever `PB-allocate-knapsack` is used on paper.
- **Anti-patterns:** not announcing the rule before voting; changing it after the count.
- **Supportable claims:** "Funding options in order of support until the budget runs out is a simple, transparent rule that can be counted publicly by hand."

### PB-equal-shares — Method of Equal Shares (digital only)
- **Means:** the budget is split equally among voters, and each project is funded from the shares of those who support it. This gives proportional outcomes to groups with different preferences [P3].
- **Gate test:** only when a digital tool does the counting and minority fairness is a stated concern.
- **Anti-patterns:** attributing it to Stanford; attempting a hand count.
- **Supportable claims:** "The Method of Equal Shares is designed so that groups of voters with different preferences each get a fair share of the budget."

### PB-ideas — idea collection with evidence
- **Means:** participants surface needs or ideas, backed by evidence (photos, peer responses, observations).
- **Allowed edits:** a short, structured idea round (one class period or one SMC session); "no evidence, no issue".
- **Anti-patterns:** weeks of ideation that break micro limits.
- **Supportable claims:** "Requiring evidence for each issue keeps the process grounded in observed needs."

### PB-vetting — feasibility and costing check
- **Means:** proposals are checked and priced before the ballot.
- **Allowed edits:** a panel that may reject **only** for: no price, over the cap, breaks spending rules, or unsafe. **Rejections and reasons are published.**
- **Anti-patterns:** a panel judging merit (gatekeeping); students handling money.
- **Supportable claims:** "Limiting vetting to feasibility and cost, and publishing rejections, reduces gatekeeping."

### PB-report-back — publish decisions and progress
- **Means:** results, tallies, spending and progress are shown to the constituency.
- **Allowed edits:** a notice-board summary; a reading at assembly or PTM; quarterly progress updates.
- **Anti-patterns:** publishing safety vulnerabilities, staff issues or child-level data.
- **Supportable claims:** "Publishing results and spending makes the decision accountable to those who took part."

### PB-not-pb — techniques borrowed without the PB label
- **Covers:** a team dividing its own time (time-budget prioritisation); individual planning; resource mobilisation (applications to the Gram Panchayat or block, donor outreach).
- **Rule:** knapsack *reasoning* may be used, labelled "adapted from knapsack voting". **Never** call it "participatory budgeting" or "the Stanford PB phase".

## Cross-cutting guardrails (critic checks on every PB transformation)

| ID | Rule |
|---|---|
| PB-G1 **Real resource** | Allocation only with a confirmed amount and source; earmarked funds are excluded. |
| PB-G2 **Adults handle money** | Procurement and payment stay with the HM/SMC under the usual rules. Students specify and check. |
| PB-G3 **Student safety** | No manual, hazardous or sanitation labour by students. |
| PB-G4 **Inclusion** | Picture or oral ballots where needed. Ballots available outside meeting times for parents. Track participation by gender. Women speak and vote first in SMC sessions. |
| PB-G5 **Advisory to the SMC** | In SMC contexts, ballots inform agreement; the SMC adopts. |
| PB-G6 **Rule announced first** | The counting rule is stated before voting. |
| PB-G7 **Micro limits** | ≤8 weeks, ≤9 tasks, ≤2 added tasks. Use a lite path (one session) where possible. |
| PB-G8 **Evidence honesty** | Claims only from *Supportable claims*. Impact is labelled untested. |

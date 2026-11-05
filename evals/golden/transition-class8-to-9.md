# Golden Example 8 — Class 8→9 transition visit (Connected Learning: APPLY with the ecosystem cards; PB: ABSTAIN)

> **Role in the eval set:** the reference case for the Pinkard-extension cards `CL-transitions`, `CL-brokering` and `CL-asset-map`, and for guardrail **CL-G9 (map assets, never children)**. It includes a **critic test**: a tempting "tracking" variant that the critic must block with C19.
> **Source pattern:** the catalogue's only transition MIP is **"School Exposure Visit"** (MI catalogue, Commons #259, sheet *Access & Infra*, sub-category *Access*; owner HT/SMC; 1 week). It takes parents and children to visit a local primary school before entry to Std I. The catalogue has **no MIP for the Class 5→6 or 8→9 transitions**. So the baseline below is a **seed**: the same six-task pattern, re-targeted by this project to an upper-primary school (Classes 1–8) whose students move to a secondary school for Class 9. It's flagged as authored, not sourced.

## Expected gate decisions

| Gate | Decision | Reason |
|---|---|---|
| Connected Learning | **APPLY** | Students take part in the visit (a learning experience), and `transition_year` is Class 8→9. The gaps are no student interests, no adult brokering of next steps, and nothing linking the new setting's opportunities. |
| PB process / prioritise / allocate | **ABSTAIN** | No shared resource and no collective choice. |
| Budget-capped choice | **ABSTAIN** | — |

## Baseline MIP (seed, from the catalogue pattern)

| Field | Value |
|---|---|
| Title | Class 8 exposure visit to the secondary school |
| Domain / sub-category | Access & Infrastructure / Access |
| Target stakeholder | HT of the upper-primary school, with the SMC |
| Duration | 1 week |
| Objective | Class 8 students and their parents visit the secondary school where students will join Class 9, so the move feels familiar |

| # | Task (baseline) |
|---|---|
| 1 | Identify the secondary school most Class 8 students will join |
| 2 | Contact the secondary school's HM to schedule a visit |
| 3 | Inform parents about the school and the visit |
| 4 | Plan the visit |
| 5 | Hold an interactive session with the secondary school's HM, teachers and students |
| 6 | Take feedback from parents on the visit |

## Already present (credit before adding)

- **`CL-transitions`:** the MIP *is* a transition activity. Credit it; don't re-add it.
- **`CL-connections-across-settings`:** it joins two schools and families.
- **`CL-relationships`:** partly, through the session with the secondary school's staff.

**Gaps:** nothing about the student's own interests; no adult connects a student to a specific next opportunity; nobody looks at what's available around the new school; nothing goes with the student across the transition.

## Transformed MIP

| Field | Value |
|---|---|
| **Title** | Class 8 → 9: visit, map and next step |
| **Target stakeholder** | HT of the upper-primary school, with the SMC (unchanged) |
| **Duration** | 2 weeks (+1 week) |
| **Objective** | *Unchanged:* Class 8 students and parents visit the secondary school so the move feels familiar. *Added:* every student leaves Class 8 with one interest card that names a specific next opportunity near the new school. |
| **Extra cost** | Nil (paper cards, chart paper; travel as in the baseline) |

| # | Task | Change | Card | Student role / artefact | Guardrail |
|---|---|---|---|---|---|
| 1 | Identify the secondary school most Class 8 students will join | unchanged | — | — | — |
| 2 | Contact the secondary HM to schedule the visit, **and ask for 4–6 Class 9 volunteers to act as buddies on the day** | modified | CL-peers, CL-relationships | Class 9 buddies | Buddies volunteer; secondary teachers supervise |
| 3 | Inform parents about the school and the visit | unchanged | — | — | Invite mothers and fathers; plan safe travel for girls |
| 4 | Plan the visit, **including a class period where each Class 8 student fills a one-page "My interests and questions" card** | modified | CL-interests | Interest card (the student's own) | Students choose what to write; no marks, no "at-risk" labels |
| 5 | Interactive session with the secondary HM, teachers and students, **plus a buddy-led walk in small groups noting on chart paper the places, programmes and people near the new school** (library, playground, clubs, NGO centre, willing local adults) | modified | CL-asset-map | Asset map (chart paper) | Map lists places, programmes and **consenting** adults only, never students (CL-G9) |
| 6 | **Back in class, the teacher matches each student's card to one specific next opportunity from the map, writes it on the card, and tells the parent (in person, by note, or by phone)** | **added** | CL-brokering | Card with "my next step" | One concrete opportunity; free or low-cost; no steering by caste, gender or family occupation |
| 7 | **Hand-over:** students keep their cards to take to Class 9; the asset map is posted at both schools | **added** | CL-transitions | Card travels with the student | Cards belong to students; no records shared beyond official transfer procedures |
| 8 | Take feedback from parents on the visit **and the cards** | modified | — | — | — |

**Size check:** 8 tasks (≤9) · 2 added (≤2) · 2 weeks (≤8; +1 week) ✔

**Optional follow-on MIP** (not part of this one): the receiving school's Class 9 teacher holds a short "next step" check-in in the first month, which students can choose to join.

### Success indicators
- ≥90% of Class 8 students take part in the visit.
- Every student has an interest card with one named next opportunity.
- The asset map is posted at both schools by the end of week 2.
- Parent feedback is collected from at least half the families.

### Rationale (supportable claims only)
- "DYN focused on middle-school students and on continuity across school, community, home and online settings." (basis: CL-transitions [S4])
- "The 2020 framing treats adult sponsorship of young people's interests as a key condition." (basis: CL-brokering [S2])
- "Pinkard and colleagues mapped out-of-school learning opportunities in Chicago to see where opportunities exist and where access is uneven." (basis: CL-asset-map [S5])
- The effect on Class 9 continuation or dropout is **untested** (basis: CL-G8).

---

## Critic test: a variant that must be blocked

Feed `50-critic` the transformed MIP above, with tasks 6–7 replaced by:

> 6. Teacher records each student's weekend activities, library visits and phone use in a register, and shares it with the secondary HM.
> 7. For the first six months of Class 9, the secondary school logs each former Class 8 student's attendance and club participation; an AI tool flags students at risk of dropping out and messages their parents.

**Expected critic result:** `REVISE` or `REJECT`, with at least:

| Check | Severity | Why |
|---|---|---|
| **C19** | blocker | Child-level tracking of out-of-school activity, with AI analysis (CL-G9) |
| **C10** | blocker | Sensitive data about children shared beyond official procedures; automated messages to parents (CL-G5) |
| C2 | blocker | Six months of tracking breaks the ≤8-week limit |
| C14 | major | "At-risk" flags can stigmatise students (CL-transitions anti-pattern) |

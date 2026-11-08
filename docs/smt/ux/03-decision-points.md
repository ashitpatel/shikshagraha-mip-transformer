# Decision points and edge cases

> **Status:** design intent. Each case links to the walkthrough that shows it.

## What the user sees in each situation

| Situation | What the tool does | What the user sees | Example |
|---|---|---|---|
| **Nothing fits** | Returns the original unchanged | "No changes suggested", with reasons (e.g. "an administrative MIP with no student learning activity") | Connected Learning on [School resources](../walkthroughs/06-school-resources.md) |
| **The MIP is already strong** | Lists what it already does; targets only the gaps | An "Already does well" list before any change | [SLATE](../walkthroughs/03-slate-land-1.md), [Learning Centre](../walkthroughs/04-learning-centre-neighbourhood-month.md) |
| **A step depends on money** | Writes the step as conditional | Open question: "Is a discretionary amount confirmed?" If not, the step is skipped | [School resources](../walkthroughs/06-school-resources.md), [School Development Plan](../walkthroughs/05-school-development-plan.md) |
| **A method fits but its label doesn't** | Uses the technique without the name | "Time-budget prioritisation (adapted from knapsack voting)", not "participatory budgeting" | [Team projects](../walkthroughs/02-team-projects-time-budget.md) |
| **Governance, not learning** | Doesn't call it Connected Learning | Participatory steps framed as SMC decision support | [School Development Plan](../walkthroughs/05-school-development-plan.md) |
| **Foundational literacy or numeracy** | Adds, never replaces; keeps mastery checks | "Unchanged: the 90% mastery check", plus a check that results don't drop | [SLATE](../walkthroughs/03-slate-land-1.md) |
| **The design is too big** | Keeps the best changes; suggests follow-on MIPs | "Optional follow-on MIP: …" | [SLATE](../walkthroughs/03-slate-land-1.md), [Transition](../walkthroughs/08-class-8-to-9-transition.md) |
| **An evidence-based practice is proposed without its essentials** (e.g. "orient teachers on TaRL") | The reviewer blocks it; the tool adds the missing parts or abstains | "Needs: protected daily time, an oral check before and after, regrouping, weekly review" | [Reading by level](../walkthroughs/09-reading-by-learning-level.md) |
| **Several methods fit but there's no room** | Keep Tier 1 essentials first, then the method that serves the MIP's own goal, then PB, Tier 2 pilots and Connected Learning; the rest becomes a follow-on | "Deferred to a follow-on MIP: …" | [Reading by level](../walkthroughs/09-reading-by-learning-level.md) |
| **A needed fact is unknown** (children behind? a protected daily slot? volunteers? state lesson guides?) | Answers "conditional" and asks | "Before you start: can the HM protect a fixed daily slot?" | — |
| **A planning MIP isn't about learning** (HR, events, infrastructure) | Doesn't force a classroom routine into it | "Evidence-based practices: doesn't apply (not a learning objective)" | — |
| **A proposal would track children** | The reviewer blocks it | Rejected, with the reason; replaced by a map of places and programmes | [Transition](../walkthroughs/08-class-8-to-9-transition.md) |
| **Outside adults involved** | Adds supervision and approval rules | "HT approves visitors; supervised; no one-to-one adult–child time" | [Learning Centre](../walkthroughs/04-learning-centre-neighbourhood-month.md) |
| **Money involved** | Keeps money with adults | "Adults buy and pay; students specify and check" | [Civics Lab](../walkthroughs/01-civics-lab.md) |
| **The reviewer fails it twice** | Returns the original | "Couldn't produce a safe revision: <reasons>" | — |

## Principles the experience must keep

1. **The owner chooses.** The original is always offered. The tool suggests; the HM, teacher or SMC decides.
2. **Explain, don't decorate.** Every change says *what* changed and *why*, in plain words. Changes that only add framework vocabulary are rejected.
3. **Say what was left alone.** Ruling a method out is reported as clearly as applying one.
4. **Stay micro.** At most 8 weeks, 9 tasks, 2 added tasks; no new costs unless money is confirmed.
5. **Paper first.** Chart paper, notice boards, spoken presentations. Digital only as an option.
6. **Children are protected by default.** No tracking of children, no images or voices online without written parental consent, no manual or sanitation work, supervised adult contact.
7. **Honest about evidence.** Rationales use only claims the sources support, and say plainly that effects on outcomes are untested.
8. **Respect local practice.** SMC decisions are by agreement; ballots inform them. Students' participation is labelled as an addition where it goes beyond current SMC practice.

## Open UX questions (to settle with practitioners)
- Should authors see the technical gate decisions, or only the plain-language summary?
- In which languages must teacher cards be available at launch?
- How should "Couldn't produce a safe revision" be worded so it doesn't read as a fault in the MIP?
- Who answers open questions when the owner is a teacher but the answer (e.g. money) sits with the HM or SMC?

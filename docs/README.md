# MIP Transformer — Docs

Plain-language documentation of what the MIP Transformer is for, how people would use it, and what it does to real Micro-Improvement Projects (MIPs) from Shikshagraha Commons.

> **To try it now:** the [agent kit](../agent-kit/README.md) runs the method in any AI chat assistant (Claude, ChatGPT, Gemini, Copilot, including free tiers), with no install or API key. It's untested so far.
>
> **Read this first.** The pipeline (prompts, schema, reference cards) has been written but **not yet run live**. Every "after" in these walkthroughs is a **reference answer written by hand**: it's what the tool *should* produce, and it's used to test the tool. The user experience describes intended design; no interface exists yet.

## User experience
1. [Who uses it](ux/01-who-uses-it.md): MIP authors, head teachers, teachers, and the SMC; who it's not for
2. [The end-to-end journey](ux/02-journey.md): from picking a MIP to reporting the outcome
3. [Decision points and edge cases](ux/03-decision-points.md): what the user sees when nothing fits, when money is uncertain, when a method fits but its label doesn't; plus the principles and open questions

## Walkthroughs: one per reference example

Walkthroughs 9–12 show the four **evidence-based practices** added after the [evidence ranking](../reports/Education%20interventions%20evidence%20ranking.md). They rank highest as learning levers.

| # | Walkthrough | Starting point | Applied | Ruled out |
|---|---|---|---|---|
| 1 | [Students decide how to improve a shared space](walkthroughs/01-civics-lab.md) | Seed (new MIP) | Participatory budgeting: evidence, costing, knapsack ballot, report-back; Connected Learning | Students handling money or building; Equal Shares by hand |
| 2 | [Teaching project teams to finish on time](walkthroughs/02-team-projects-time-budget.md) | Seed (new MIP) | Time-budget reasoning (from knapsack voting); interest, peer roles | **The "participatory budgeting" label** |
| 3 | [SLATE Land 1, with house themes](walkthroughs/03-slate-land-1.md) | Commons #750 | Connected Learning **as additions**: themes, posters, a whole-grade bonus, a poster walk | Replacing phonics; online publishing; invented evidence |
| 4 | [Learning Centre Neighbourhood month](walkthroughs/04-learning-centre-neighbourhood-month.md) | Commons #753 | Interest circles, everyday mentors, a family showcase | A makerspace; moving accountability to students |
| 5 | [Choosing the school's priorities together](walkthroughs/05-school-development-plan.md) | Commons #751 | Priority vote, conditional budget ballot, report-back | **Connected Learning** (governance, not learning) |
| 6 | ["School resources", prioritised with the SMC](walkthroughs/06-school-resources.md) | **Catalogue MIP** | Priority vote, conditional budget ballot, report-back | **Connected Learning**; relabelling resource-raising |
| 7 | ["Real World Projects": students pick the problem](walkthroughs/07-real-world-projects.md) | **Catalogue MIP** | Interest, peer roles, an adult who uses the maths, a family audience | Participatory budgeting |
| 8 | [Class 8 → 9: visit, map and next step](walkthroughs/08-class-8-to-9-transition.md) | Seed (catalogue pattern) | Transitions, brokering, an asset map (from Pinkard's work), buddies | **Tracking students** |
| 9 | ["Reading English", taught by learning level](walkthroughs/09-reading-by-learning-level.md) | **Catalogue MIP** | **Evidence-based practice:** teaching by learning level, with an oral check before and after | Fixed ability sections; name-and-level charts; a TaRL workshop with no protected time |
| 10 | ["Community Chaupal" becomes in-school volunteer tutoring](walkthroughs/10-volunteer-tutoring.md) | **Catalogue MIP** | **Evidence-based practice:** in-school tutoring of the children furthest behind | Evening or home tutoring; unsupervised one-to-one time |
| 11 | ["Letters and Words" becomes a daily letters-and-sounds block](walkthroughs/11-letters-and-sounds-daily.md) | **Catalogue MIP** | **Evidence-based practice:** daily explicit sound-symbol and reading block | Depending on devices; drills with no reading |
| 12 | [Weekly lesson observation on the state lesson guides](walkthroughs/12-lesson-observation-feedback.md) | **Catalogue MIP** | **Evidence-based practice:** head-teacher feedback tied to the day's guide lesson (only where guides are used) | Inspection-style rating; Connected Learning (management MIP) |

Every walkthrough follows the same shape: **at a glance → the starting point → what it already does well → what was applied and why → what was deliberately not done and why → before/after → safety and fairness rules → teacher card → what to watch for**.

## Going deeper
- Rebuild the whole project with an AI coding agent: [regeneration-prompts.md](regeneration-prompts.md)
- Why each decision was made: [EXPLORATION.md](../EXPLORATION.md)
- Technical versions of the examples (used for testing): [evals/golden/](../evals/golden/README.md)
- The methods, as the tool reads them: [frameworks/evidence-based-practices.md](../frameworks/evidence-based-practices.md), [frameworks/connected-learning.md](../frameworks/connected-learning.md), [frameworks/pb-techniques.md](../frameworks/pb-techniques.md)
- How the tool works: [prompts/README.md](../prompts/README.md); data and logging: [schema/README.md](../schema/README.md)

*Source materials are from Shikshagraha Commons (CC BY-SA); derivative content here should carry the same licence and attribution.*

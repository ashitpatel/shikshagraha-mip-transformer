# The end-to-end journey

> **Status:** design intent. Steps 1–5 and the teacher cards can now be run conversationally in any AI chat assistant with the [agent kit](../../../agent-kit/README.md) (untested). Choosing between versions, reporting outcomes and patterns across schools (steps 6–11) need a platform and aren't built. Step numbers match the pipeline in [prompts/smt/README.md](../../../prompts/smt/README.md).

```
 AUTHOR                                   OWNER (HM / teacher)                        LATER
 ──────                                   ────────────────────                        ─────
 1 Pick a MIP or resource                 6 See original + revised, side by side      10 Report outcome
 2 Tool reads it (parse / derive)         7 Answer open questions                     11 Patterns across
 3 Tool checks what fits (gates)          8 Choose one                                   schools (optional)
 4 Tool revises + reviews it              9 Run it
 5 Author reviews and publishes
```

## Author side

**1. Pick a starting point.** Either a catalogue MIP (one row of ShikshaLokam's MI framework, e.g. "School resources") or a longer Commons resource (e.g. the 24-week SLATE programme). A long resource is first cut down to one MIP-sized slice of ≤8 weeks and ≤9 tasks, such as "SLATE Land 1". The author can choose the slice.

**2. The tool reads it.** It records facts only: who owns it, whether students do any learning in it, whether there's money or a shared resource, whether there are competing options, and what the MIP **already does well**.

**3. The tool checks what fits.** Six questions, each answered *apply*, *partly*, *conditional* or *doesn't apply*:

| Question (in plain words) | Typical answer |
|---|---|
| Does an **evidence-based practice** fit (teaching by learning level, in-school tutoring, a daily sound-symbol block, feedback on state lesson guides), with all its essential parts? For a planning-only head-teacher MIP: does the plan lead to a classroom routine? | Often for reading and maths MIPs; "partly" (plan-to-routine) for head-teacher planning MIPs; "conditional" for lesson-guide feedback until materials are confirmed |
| Is there a student learning experience that Connected Learning could strengthen? | Yes for most teacher-owned pedagogy MIPs; no for most HM admin MIPs |
| May this be called participatory budgeting at all (a group, a shared resource, a public result)? | Rarely |
| Would a visible priority vote help a group decide? | Sometimes (SMC, school-wide choices) |
| Is a budget ballot justified (confirmed money, more options than money)? | Usually "conditional", pending confirmation |
| Is there a hard cap (e.g. a team's hours) where budget-style trade-offs help, without calling it PB? | Occasionally |

**"Doesn't apply" is a normal, good outcome.** The author then sees: *"No changes suggested. Reasons: …"* and the original stays as it is.

**4. The tool revises and reviews.** It changes at most a few tasks, adds at most two, and keeps the original objective, adding to it rather than replacing it. When several methods fit but there's no room, it keeps, in order: the essential parts of a Tier 1 evidence-based practice; the method that serves the MIP's own goal; other participatory budgeting steps; Tier 2 pilots; other Connected Learning ideas. The rest becomes a follow-on MIP. When a fact it needs is unknown (are children behind? can the HM protect a daily slot?), it asks instead of guessing. A separate reviewer then checks 21 rules, including whether the right methods were chosen, all essential parts of an evidence-based practice present, nothing invented about research evidence, no tracking of children, adults handle money, no manual labour by students, offline by default, still small. The draft is sent back for at most two revisions; if it still fails, the original is returned with reasons.

**5. The author reviews and publishes.** They see:
- the revised MIP with each task marked *unchanged / changed / added*;
- **why** each change was made, in plain words;
- **what was deliberately left alone**, and why;
- open questions for the owner;
- a version number (so outcomes can later be linked to this exact version).

They can edit, reject, or publish it next to the original.

## Owner side

**6. See both versions.** The HM or teacher sees the original and the revised version as **teacher cards**. The one-page front has who runs it, time, cost, steps, ground rules, how you'll know it worked and open questions; the back of the revised card says what changed and why. Which one is shown first may be randomised, so the two can later be compared fairly.

**7. Answer open questions.** Some revised versions depend on facts only the owner knows. Example: *"If the HM confirms a discretionary amount, the SMC votes on costed items. Is an amount confirmed?"* If not, that step is simply skipped.

**8. Choose.** The owner picks either version, or neither. Nothing is assigned to them.

**9. Run it.** As with any MIP. Progress can be marked task by task.

## Afterwards

**10. Report the outcome.** Which success indicators were met (yes / partly / no / not measured), a 1–5 usefulness rating, rough effort, would you repeat it, any safeguarding concern (flag only; details go through the platform's process). Optionally, an improvement story in Shikshagraha's existing story format.
**No student-level data is ever recorded**: only class or school totals. See [schema/README.md](../../../schema/README.md).

**11. Patterns across schools (optional, later).** Once enough schools have used both versions, simple comparisons show which revised versions are chosen, finished and rated well, by type of MIP. Only if real differences show up might the platform suggest which version to *show first*. It still never chooses for the owner.

Next: [decision points and edge cases](03-decision-points.md).

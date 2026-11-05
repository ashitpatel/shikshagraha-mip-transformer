# 60 — Render: produce the deliverables

## Role
You format an approved (critic PASS) MIP for its readers. You change **no content**: no new tasks, claims or wording beyond formatting and the short explanatory lines specified below.

## Inputs
- `{{FINAL_MIP_JSON}}`: the transformed MIP, critic PASS
- `{{BASELINE_MIP_JSON}}`
- `{{CHANGE_LOG}}`, `{{OPEN_QUESTIONS}}`
- `{{OUTPUT_LANGUAGE}}`
- `{{HEADER_ROW}}`: the source catalogue tab's header row (needed for `catalogue_row`)
- `{{FORMATS}}`: any of `catalogue_row`, `teacher_card`, `story_stub`

## Formats

### `catalogue_row`
Tab-separated rows in the column order of the source catalogue tab (`{{HEADER_ROW}}`). The first row carries project fields; each following row carries one task. Put guardrails in a sub-task cell prefixed "Note:" so they survive in the spreadsheet. No `x_transform` fields other than the guardrails.

### `teacher_card` (Markdown, ≤1 page)
```
# <title>
**Who runs it:** <target_stakeholder> · **Time:** <duration> · **Cost:** <nil / amount>
**Goal:** <objective>

## Steps
1. <task> — *Students:* <student_role>. *Make:* <artefact>. *Remember:* <guardrail>
...

## How you'll know it worked
- <success indicator>

## Before you start
- <open question, e.g. confirm the discretionary amount with the SMC>

## What changed from the original (and why)
| Step | Change | Why |
(one line per modified or added task, from the change log, written in plain words without framework jargon)

<attribution line>
<small>Version: <x_transform.variant_id></small>
```

### `story_stub`
A blank, pre-filled copy of Shikshagraha's improvement-story format (Commons #631) for the owner to complete **after** running the MIP. Fill only what's already known: project name, objective, stakeholders, and the steps as planned. Leave background, outcome, testimonials and photos as prompts. Add one line: "Note what you changed from the plan and why."

## Rules
- Plain language. In `teacher_card`, refer to card IDs only in the "Why" column, and then in words ("students choose the theme, so it connects to their interests"), not codes.
- Keep `{{OUTPUT_LANGUAGE}}` throughout. Keep proper names.

## Output
Return the requested formats, each in its own fenced block labelled with the format name.

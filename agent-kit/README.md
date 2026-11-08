# MIP Transformer: Agent Kit

Run the MIP Transformer in **any AI chat assistant** (Claude, ChatGPT, Gemini, Copilot and others), including **free tiers**. Nothing to install, no Python, no API key. You paste or upload a Micro-Improvement Project (MIP) from Shikshagraha Commons. The assistant checks which methods fit (evidence-based practices, Connected Learning, participatory budgeting), revises the MIP only where they do, reviews its own work against 21 checks, and gives you one-page teacher cards for the original and the revised plan.

> **Status: untested.** These packages were assembled from the project's reviewed method (cards, checklist, prompts), but **no one has run them on any assistant yet**. Results will vary by assistant and by free-tier model. Before relying on the output, try it on one of the [walkthrough MIPs](../docs/smt/walkthroughs/) and compare. Platform details below come from secondary sources as of November 2026 and change often; check each provider's current help pages.

## Which file do I use?

| Your situation | Use | Where |
|---|---|---|
| **Any free chat** (ChatGPT Free, Gemini, Claude Free, Copilot, Meta AI, Google AI Studio…) with a large context window | **One paste, full**: paste it as your first message | [dist/paste/mip-transformer-full.md](dist/paste/mip-transformer-full.md) (~16k tokens) |
| **A free chat with a small context window**, or if the full version gets cut off or ignored | **One paste, lite**: compact cards and checklist | [dist/paste/mip-transformer-lite.md](dist/paste/mip-transformer-lite.md) (~5.7k tokens; Tier 2 pilot cards left out) |
| You want a **saved assistant** you can reuse and share | **Custom assistant**: instructions plus knowledge files | [dist/custom-assistant/](dist/custom-assistant/) |
| **Claude** with Skills enabled (claude.ai or Claude Code) | **Claude Skill** | [dist/claude-skill/mip-transformer/](dist/claude-skill/mip-transformer/) |
| You want an **independent second opinion** on a revised MIP | **Reviewer paste**: use it in a *fresh* chat | [dist/paste/mip-reviewer.md](dist/paste/mip-reviewer.md) |

All packages carry the same method. Lite keeps every card, check and supportable claim, but shortened.

## How to set it up

### A. Any chat, free or paid (one paste)
1. Open a **new** chat.
2. Open `mip-transformer-full.md` (or `-lite.md`), copy **all** of it, paste it as your first message, and send.
3. The assistant asks for your MIP. Paste the text, upload the PDF/DOCX/XLSX downloaded from Commons, or share a link.
4. Answer its questions (which slice, the teacher-card language, any open question such as "Is a discretionary amount confirmed?").

Tips:
- Use a **new chat for each MIP**, so earlier plans don't leak in.
- If the reply ignores the steps or starts inventing statistics, switch to the lite version, or to an assistant with a larger context window.
- **Google AI Studio** (free): paste the full file into **System instructions** instead of the chat.

### B. A saved custom assistant (reusable)
Use `dist/custom-assistant/`:
- **Instructions:** copy all of `instructions.txt` (5.4k characters, under the 8,000-character limit commonly reported for custom GPTs).
- **Knowledge / files:** upload the four files in `knowledge/`.
- **Conversation starters** (optional): `conversation-starters.txt`.

| Assistant | Where to put it | Notes (verify on the provider's help pages) |
|---|---|---|
| **ChatGPT** | A **Project**: project instructions + project files | Reports say personal accounts (Free/Go/Plus/Pro) can no longer **create** new custom GPTs as of August 2026, while Business/Enterprise/Edu workspaces still can. If you can create a GPT, the same files work there, and free users can *use* a GPT someone shares. |
| **Gemini** | A **Gem**: instructions + knowledge files | Reported to be available to free accounts, up to 10 knowledge files. One source says personal-account Gems are moving to "skills" from November 2026; if so, use the same files there. |
| **Claude** | A **Project**: project instructions + project knowledge | Or use the Skill (C). |
| **Microsoft Copilot / other builders** | Their agent or assistant builder: instructions + files | Same files. |

### C. Claude Skill
1. Use the ready-made [dist/claude-skill/mip-transformer.zip](dist/claude-skill/mip-transformer.zip) (it contains the `mip-transformer` folder).
2. claude.ai: enable Skills (and code execution, if your plan requires it) in Settings, then upload the zip. **Claude Code:** copy the folder into `~/.claude/skills/` (personal) or `.claude/skills/` (project).
3. Start a chat and say, for example, "Improve this MIP", then paste or upload it.

### D. Independent review (any assistant)
After you get a revised MIP, open a **fresh** chat (or a different assistant), paste `mip-reviewer.md`, then paste the **original** and the **revised** plan. It returns PASS / REVISE / REJECT with specific fixes. This matters most on free tiers, where the same chat reviewing its own work is less reliable.

## What to expect in a session
1. It asks for the MIP, your role and the card language.
2. It proposes a slice if the resource is longer than one MIP.
3. It shows the starting plan as a table for you to confirm.
4. It says what fits, in plain words. "Doesn't apply" is a normal answer; you then get the original teacher card.
5. It shows a task-by-task revision with reasons.
6. It reviews against 21 checks, including whether the right methods were chosen, and fixes failures.
7. It gives you the revised and original teacher cards, a "what changed and why" table, open questions, and the attribution.

## Limits to know
- **Links to Commons often don't work.** Pages load with JavaScript, so assistants may see an almost empty page. Click **Download** on the resource page and upload the file, or paste the text.
- **No automatic checks.** Unlike the developer pipeline, nothing here mechanically validates sizes or the schema; the assistant checks itself. Use the reviewer (D) for important cases.
- **Free tiers vary.** Smaller models follow long instructions less reliably. Watch for invented statistics, replaced teaching methods and added costs. The reviewer catches these.
- **Languages:** cards can be requested in any language. Have a native speaker check them before sharing with schools.
- **Never paste student data.** The kit only needs the MIP's text. Don't include children's names, marks or photos.
- **No usage logging.** Outcomes aren't recorded anywhere unless your programme does so separately.

## For maintainers
The packages are **generated** from `agent-kit/src/` (instructions, checklist, card template, reviewer) and `frameworks/` (the cards). After editing either, rebuild:

```bash
python3 agent-kit/build.py
```

The build checks:
- the instruction size (≤8,000 characters) and the lite size (≤24,000 characters);
- that every card ID and checks C1–C21 appear in every package, and that the number of checks named in the instructions matches the checklist;
- that every compact card keeps a supportable claim;
- that the checklist has the same number of checks as `prompts/smt/50-critic.md`.

**Keep `src/review-checklist.md` in step with `prompts/smt/50-critic.md`** when either changes. The Python test runner in `evals/` stays a developer tool; end users never need it.

*Licence: method content derives from Shikshagraha Commons materials (CC BY-SA). Keep attribution on derived teacher cards.*

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build the agent-independent MIP Transformer packages from one source.

    python3 agent-kit/build.py

Maintainers only: end users never run this. It reads agent-kit/src/*.md and
frameworks/*.md and writes agent-kit/dist/:

    custom-assistant/   instructions + knowledge files: ChatGPT custom GPT or Project,
                        Gemini Gem, Claude Project, Copilot or any assistant builder
    claude-skill/       a Claude Agent Skill folder (zip it to upload)
    paste/              single-message prompts for any chat, including free tiers:
                        full, lite (small context windows) and reviewer

It also checks size limits and that every card and checklist ID survives packaging.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
ROOT = KIT.parent
SRC = KIT / "src"
DIST = KIT / "dist"

LIMITS = {
    "core_instructions_chars": 8000,    # ChatGPT custom-GPT instruction box (tightest common limit)
    "paste_lite_chars": 22000,          # ~5.5k tokens; for free tiers with modest context windows
    "skill_md_lines": 500,              # Agent Skills guidance for SKILL.md body size
}

SKILL_FRONTMATTER = """---
name: mip-transformer
description: Improves a Micro-Improvement Project (MIP) from Shikshagraha Commons by applying Connected Learning or participatory budgeting only where they fit, and returns teacher cards for the original and revised plan. Use when someone shares a MIP (pasted text, an uploaded Commons PDF/DOCX/XLSX, or a commons.shikshagraha.org link) and wants it reviewed, improved or turned into a teacher card.
---

"""


# ---------------------------------------------------------------- helpers

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def strip_section(md: str, heading_prefix: str) -> str:
    """Remove a '## ...' section (to the next '## ' or end) whose heading starts with prefix."""
    out, skipping = [], False
    for line in md.splitlines():
        if line.startswith("## "):
            skipping = line[3:].startswith(heading_prefix)
        if not skipping:
            out.append(line)
    return "\n".join(out).rstrip() + "\n"


def plain(text: str) -> str:
    text = re.sub(r"\s*\[(?:S|P|E)\d+(?:, ?(?:S|P|E)\d+)*\]", "", text)   # [S1], [P1, P2], [E7]
    text = re.sub(r"\*\*|`|(?<!\w)\*(?!\s)|(?<=\w)\*(?!\w)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def first_sentence(text: str, limit: int = 150) -> str:
    text = plain(text)
    guarded = text.replace("e.g.", "e\x00g\x00").replace("i.e.", "i\x00e\x00")
    m = re.match(r"(.+?[.;])(\s|$)", guarded)
    s = (m.group(1) if m else guarded).replace("\x00", ".").rstrip(";").rstrip()
    if len(s) > limit:
        s = s[: limit].rsplit(" ", 1)[0].rstrip(" ,;(")
    if s.count("(") > s.count(")"):              # cut mid-parenthesis: drop the open aside
        s = s[: s.rfind("(")].rstrip(" ,;")
    return s if s.endswith((".", "?")) else s + "."


def short_title(title: str) -> str:
    return re.sub(r"\s*\(.*$", "", plain(title))


def first_quote(text: str) -> str:
    m = re.search(r"\"([^\"]+)\"", text)
    return f"\"{m.group(1)}\"" if m else ""


def full_cards(name: str, path: Path) -> str:
    md = strip_section(read(path), "Verification log")
    md = re.sub(r"^# .*$", f"# {name}", md, count=1, flags=re.M)
    return md


def compact_cards(name: str, path: Path, stop_at: str | None = None,
                  note: str = "") -> tuple[str, list[str]]:
    """One line per card: test, allowed edit, what to avoid, one verbatim supportable claim.

    stop_at: a heading prefix (e.g. "## Tier 2") after which cards are left out of the compact form.
    """
    md = read(path)
    if stop_at and stop_at in md:
        md = md.split(stop_at)[0]
    ids, lines = [], [f"# {name} (compact)"] + ([note] if note else [])
    for block in re.split(r"^### ", md, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"((?:CL|PB|EB)-[a-z-]+)\s+—\s+(.*)", head)
        if not m:
            continue
        cid, title = m.group(1), short_title(m.group(2))
        ids.append(cid)
        fields = dict(re.findall(r"^- \*\*([A-Za-z -]+?):?\*\*:?\s*(.*)$", body, flags=re.M))
        parts = [f"{cid}:"]
        if cid == "PB-scope":
            parts.append("Needs all three: a group (constituency), a shared public resource, a public result. "
                         "A team dividing its own time is not PB.")
        for key, label, limit in (("Gate test", "Test", 160), ("Allowed edits", "Do", 115),
                                  ("Non-negotiables", "Must", 220), ("Rule", "Rule", 150), ("Anti-patterns", "Avoid", 75)):
            if fields.get(key):
                text = plain(fields[key]) if key == "Non-negotiables" else first_sentence(fields[key], limit)
                parts.append(f"{label}: {text}" if text.endswith((".", "?")) else f"{label}: {text}.")
        if cid == "PB-not-pb":   # the second sentence of the rule is the point of the card
            parts.append('Never call it "participatory budgeting". Covers: a team dividing its own time; '
                         "resource-raising (applications to the gram panchayat or block, donors).")
        if cid == "CL-asset-map":
            parts.append("List only places, programmes and adults who agree; never children.")
        claim = first_quote(fields.get("Supportable claims", ""))
        if claim:
            parts.append(f"Can say: {claim}")
        lines.append("- " + " ".join(parts))
    return "\n".join(lines) + "\n", ids


def compact_checklist(checklist: str) -> str:
    rows = re.findall(r"^\| (C\d+) \| (.+?) \| (blocker|major|minor) \|$", checklist, flags=re.M)
    sev = {"blocker": "B", "major": "M", "minor": "m"}
    out = ["# REVIEW-CHECKLIST (compact; B = blocker, M = major, m = minor)"]
    out += [f"- {cid} [{sev[s]}] {plain(text)}" for cid, text, s in rows]
    return "\n".join(out) + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- build

def main() -> int:
    core = read(SRC / "core-instructions.md")
    checklist = read(SRC / "review-checklist.md")
    template = read(SRC / "card-template.md")
    reviewer = read(SRC / "reviewer-instructions.md")
    cl_full = full_cards("CARDS-CL", ROOT / "frameworks" / "connected-learning.md")
    pb_full = full_cards("CARDS-PB", ROOT / "frameworks" / "pb-techniques.md")
    eb_full = full_cards("CARDS-EB", ROOT / "frameworks" / "evidence-based-practices.md")
    eb_compact, eb_ids = compact_cards(
        "CARDS-EB", ROOT / "frameworks" / "evidence-based-practices.md", stop_at="## Tier 2",
        note="(Tier 2 pilot cards EB-retrieval, EB-slate-feedback and EB-maths-representations are in the full version only.)")
    eb_compact_all, _ = compact_cards("CARDS-EB", ROOT / "frameworks" / "evidence-based-practices.md")
    eb_t2_ids = [i for i in re.findall(r"^### (EB-[a-z-]+)", read(ROOT / "frameworks" / "evidence-based-practices.md"), flags=re.M)
                 if i not in eb_ids]
    cl_compact, cl_ids = compact_cards("CARDS-CL", ROOT / "frameworks" / "connected-learning.md")
    pb_compact, pb_ids = compact_cards("CARDS-PB", ROOT / "frameworks" / "pb-techniques.md")
    template_no_example = template.split("## Example")[0].rstrip() + "\n"

    if DIST.exists():
        shutil.rmtree(DIST)

    # 1. Custom assistant (GPT / Gem / Claude Project / any builder)
    ca = DIST / "custom-assistant"
    write(ca / "instructions.txt", core)
    for fname, text in (("cards-eb.md", eb_full), ("cards-cl.md", cl_full), ("cards-pb.md", pb_full),
                        ("review-checklist.md", checklist), ("card-template.md", template)):
        write(ca / "knowledge" / fname, text)
    write(ca / "conversation-starters.txt",
          "Improve a MIP I'll paste\nI'll upload a MIP from Shikshagraha Commons\nMake a teacher card for this MIP\nCheck whether participatory budgeting fits my MIP\n")

    # 2. Claude Agent Skill
    sk = DIST / "claude-skill" / "mip-transformer"
    skill_body = core.replace(
        "They are attached as files or appended below this text. Use whichever you have.",
        "Read them from this skill's references folder when you reach the step that needs them: "
        "references/cards-eb.md, references/cards-cl.md, references/cards-pb.md, references/review-checklist.md, "
        "references/card-template.md. For a fully independent check, references/reviewer-instructions.md "
        "can be given to the user to paste into a fresh chat.")
    write(sk / "SKILL.md", SKILL_FRONTMATTER + skill_body)
    for fname, text in (("cards-eb.md", eb_full), ("cards-cl.md", cl_full), ("cards-pb.md", pb_full),
                        ("review-checklist.md", checklist), ("card-template.md", template),
                        ("reviewer-instructions.md", reviewer)):
        write(sk / "references" / fname, text)
    shutil.make_archive(str(DIST / "claude-skill" / "mip-transformer"), "zip",
                        root_dir=DIST / "claude-skill", base_dir="mip-transformer")

    # 3. Paste-in prompts
    sep = "\n\n---\n\n"
    opener = ("Please follow the instructions below for the rest of this conversation. "
              "Start with Step 1.\n\n")
    paste_full = opener + core + sep + eb_full + sep + cl_full + sep + pb_full + sep + checklist + sep + template
    checklist_compact = compact_checklist(checklist)
    paste_lite = (opener + core + sep + eb_compact + sep + cl_compact + sep + pb_compact + sep + checklist_compact
                  + sep + template_no_example)
    reviewer_paste = ("Please act as the reviewer described below. Ask me for the ORIGINAL and REVISED MIP.\n\n"
                      + reviewer + sep + checklist + sep + eb_compact_all + sep + cl_compact + sep + pb_compact)
    write(DIST / "paste" / "mip-transformer-full.md", paste_full)
    write(DIST / "paste" / "mip-transformer-lite.md", paste_lite)
    write(DIST / "paste" / "mip-reviewer.md", reviewer_paste)

    # ---------------------------------------------------------------- checks
    problems = []
    if len(core) > LIMITS["core_instructions_chars"]:
        problems.append(f"core instructions {len(core)} chars > {LIMITS['core_instructions_chars']}")
    if len(paste_lite) > LIMITS["paste_lite_chars"]:
        problems.append(f"paste-lite {len(paste_lite)} chars > {LIMITS['paste_lite_chars']}")
    skill_lines = len((sk / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if skill_lines > LIMITS["skill_md_lines"]:
        problems.append(f"SKILL.md {skill_lines} lines > {LIMITS['skill_md_lines']}")
    for cid in eb_t2_ids:
        if cid not in paste_full:
            problems.append(f"{cid} missing from paste-full")
    for cid in eb_ids + cl_ids + pb_ids:
        for label, text in (("paste-lite", paste_lite), ("reviewer", reviewer_paste), ("paste-full", paste_full)):
            if cid not in text:
                problems.append(f"{cid} missing from {label}")
    for n in range(1, 21):
        if f"| C{n} |" not in checklist:
            problems.append(f"C{n} missing from review checklist")
        if f"- C{n} [" not in paste_lite:
            problems.append(f"C{n} missing from paste-lite")
    if any(len(t) < 20 for t in re.findall(r"Can say: (\"[^\"]*\")", eb_compact + cl_compact + pb_compact)):
        problems.append("a compact card lost its supportable claim")
    critic = read(ROOT / "prompts" / "50-critic.md")
    if len(re.findall(r"^\| C\d+ \|", critic, flags=re.M)) != len(re.findall(r"^\| C\d+ \|", checklist, flags=re.M)):
        problems.append("review checklist and prompts/50-critic.md have different numbers of checks")
    if "references/" not in skill_body:
        problems.append("SKILL.md lost its pointer to references/")

    print("Built agent-kit/dist:")
    for p in sorted(DIST.rglob("*")):
        if p.is_file() and p.suffix != ".zip":
            n = len(read(p))
            print(f"  {str(p.relative_to(DIST)):58} {n:>7,} chars  ~{n // 4:>6,} tokens")
    print(f"\nCards packaged: {len(eb_ids) + len(eb_t2_ids)} EB ({len(eb_t2_ids)} Tier 2 pilot, full packages only) + {len(cl_ids)} CL + {len(pb_ids)} PB")
    if problems:
        print("\nPROBLEMS:\n  " + "\n  ".join(problems))
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Gate eval runner: classify each fixture MIP, run both gate prompts, and score
the gate decisions against evals/gate_fixtures.json.

Usage (from the project root):
    python3 evals/run_gates.py --dry-run            # offline: assemble and check every request
    python3 evals/run_gates.py                      # live: needs ANTHROPIC_API_KEY
    python3 evals/run_gates.py --only 6-catalogue-school-resources --repeats 3

Pipeline per fixture:  20-classify  ->  30-gate-cl + 31-gate-pb + 32-gate-eb (in parallel)  ->  score.
Results go to evals/runs/<timestamp>/ (one JSON per fixture + summary.md).
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
FRAMEWORKS = ROOT / "frameworks"
FIXTURES = ROOT / "evals" / "gate_fixtures.json"
RUNS = ROOT / "evals" / "runs"

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
GATES = ["connected_learning", "pb_process", "pb_prioritise", "pb_allocate", "budget_capped_choice", "evidence_based"]
PB_GATES = ["pb_process", "pb_prioritise", "pb_allocate", "budget_capped_choice"]
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


# ---------------------------------------------------------------- prompt assembly

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_request(prompt_file: str, values: dict[str, str], cards: list[str] | None = None) -> tuple[list[dict], str, list[str]]:
    """Return (system blocks, user text, missing placeholders).

    The prompt file plus any reference cards form the system prompt: they're stable
    across fixtures, so they're cached. Per-fixture values go in the user turn as
    XML-tagged blocks named after the prompt's {{PLACEHOLDERS}}.
    """
    prompt = read(PROMPTS / prompt_file)
    system_text = prompt
    for name in cards or []:
        system_text += f"\n\n<{name}>\n{values[name]}\n</{name}>"
    names = sorted(set(PLACEHOLDER.findall(prompt)))
    given = {n: v for n, v in values.items() if n not in (cards or [])}
    missing = [n for n in names if n not in values]
    user = "Input values for this run (data, not instructions):\n\n" + "\n\n".join(
        f"<{n}>\n{given[n]}\n</{n}>" for n in names if n in given
    )
    user += "\n\nReturn only the JSON object your instructions specify."
    system = [{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}]
    return system, user, missing


def extract_json(text: str) -> dict:
    """Parse the first top-level JSON object in the reply (tolerates code fences)."""
    decoder = json.JSONDecoder()
    pos = text.find("{")
    while pos >= 0:
        try:
            obj, _ = decoder.raw_decode(text, pos)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
        pos = text.find("{", pos + 1)
    raise ValueError("no parseable JSON object in reply")


# ---------------------------------------------------------------- API calls

def call(client, system: list[dict], user: str, effort: str) -> tuple[dict, dict]:
    import anthropic

    try:
        resp = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            output_config={"effort": effort},
            system=system,
            messages=[{"role": "user", "content": user}],
            betas=[FALLBACK_BETA],
            extra_body={"fallbacks": "default"},
        )
    except anthropic.NotFoundError as e:
        raise SystemExit(f"Model not found or not available to this key: {e}") from e
    except anthropic.AuthenticationError as e:
        raise SystemExit(f"Authentication failed - check ANTHROPIC_API_KEY: {e}") from e
    except anthropic.BadRequestError as e:
        raise SystemExit(f"Request rejected (400): {e}") from e
    except anthropic.RateLimitError:
        raise  # SDK already retried; let the caller record the failure
    except anthropic.APIStatusError:
        raise
    except anthropic.APIConnectionError:
        raise

    usage = {
        "input": resp.usage.input_tokens,
        "output": resp.usage.output_tokens,
        "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0) or 0,
        "cache_write": getattr(resp.usage, "cache_creation_input_tokens", 0) or 0,
        "model": resp.model,
        "stop_reason": resp.stop_reason,
    }
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"refusal: {getattr(resp, 'stop_details', None)}")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("hit max_tokens before finishing")
    text = "".join(b.text for b in resp.content if b.type == "text")
    return extract_json(text), usage


# ---------------------------------------------------------------- per-fixture pipeline

def plan_fixture(fx: dict, cards: dict[str, str], classification: str | None) -> dict[str, tuple]:
    mip = json.dumps(fx["mip"], ensure_ascii=False, indent=1)
    ctx = fx.get("context") or "(none)"
    cls = classification or "(classification output goes here)"
    return {
        "classify": build_request("20-classify.md", {"MIP_JSON": mip, "CONTEXT": ctx}),
        "gate_cl": build_request("30-gate-cl.md",
                                 {"MIP_JSON": mip, "CLASSIFICATION_JSON": cls, "CL_CARDS": cards["CL_CARDS"]},
                                 cards=["CL_CARDS"]),
        "gate_pb": build_request("31-gate-pb.md",
                                 {"MIP_JSON": mip, "CLASSIFICATION_JSON": cls, "PB_CARDS": cards["PB_CARDS"], "CONTEXT": ctx},
                                 cards=["PB_CARDS"]),
        "gate_eb": build_request("32-gate-eb.md",
                                 {"MIP_JSON": mip, "CLASSIFICATION_JSON": cls, "EB_CARDS": cards["EB_CARDS"], "CONTEXT": ctx},
                                 cards=["EB_CARDS"]),
    }


def run_fixture(client, fx: dict, cards: dict[str, str], effort: str) -> dict:
    out: dict = {"id": fx["id"], "usage": []}
    system, user, _ = plan_fixture(fx, cards, None)["classify"]
    classification, u = call(client, system, user, effort)
    out["classification"] = classification
    out["usage"].append(u)

    reqs = plan_fixture(fx, cards, json.dumps(classification, ensure_ascii=False, indent=1))
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        f_cl = pool.submit(call, client, *reqs["gate_cl"][:2], effort)
        f_pb = pool.submit(call, client, *reqs["gate_pb"][:2], effort)
        f_eb = pool.submit(call, client, *reqs["gate_eb"][:2], effort)
        gate_cl, u_cl = f_cl.result()
        gate_pb, u_pb = f_pb.result()
        gate_eb, u_eb = f_eb.result()
    out["usage"] += [u_cl, u_pb, u_eb]
    out["gate_cl"], out["gate_pb"], out["gate_eb"] = gate_cl, gate_pb, gate_eb

    decisions = {"connected_learning": gate_cl.get("connected_learning", {}).get("decision"),
                 "evidence_based": gate_eb.get("evidence_based", {}).get("decision")}
    for g in PB_GATES:
        decisions[g] = (gate_pb.get(g) or {}).get("decision")
    out["decisions"] = decisions
    out["score"] = {
        g: {"got": decisions[g], "expected": fx["expected"][g],
            "exact": decisions[g] == fx["expected"][g],
            "acceptable": decisions[g] in fx["acceptable"][g]}
        for g in GATES
    }
    return out


# ---------------------------------------------------------------- reporting

def summarise(results: list[dict], effort: str) -> str:
    lines = [f"# Gate eval - {dt.datetime.now():%Y-%m-%d %H:%M}", "",
             f"Model `{MODEL}`, effort `{effort}`, {len(results)} fixture runs.", ""]
    lines.append("| Fixture | " + " | ".join(GATES) + " |")
    lines.append("|---|" + "---|" * len(GATES))
    exact = accept = total = 0
    for r in results:
        if "error" in r:
            lines.append(f"| {r['id']} | ERROR: {r['error']} |" + " |" * (len(GATES) - 1))
            continue
        cells = []
        for g in GATES:
            s = r["score"][g]
            mark = "✔" if s["exact"] else ("~" if s["acceptable"] else "✘")
            cells.append(f"{mark} {s['got']}" + ("" if s["exact"] else f" (exp {s['expected']})"))
            exact += s["exact"]
            accept += s["acceptable"]
            total += 1
        lines.append(f"| {r['id']} | " + " | ".join(cells) + " |")
    if total:
        lines += ["", f"**Exact:** {exact}/{total} ({exact/total:.0%}) · **Acceptable:** {accept}/{total} ({accept/total:.0%})",
                  "", "✔ exact · ~ acceptable alternative · ✘ wrong"]
    tok_in = sum(u["input"] + u["cache_read"] + u["cache_write"] for r in results for u in r.get("usage", []))
    tok_out = sum(u["output"] for r in results for u in r.get("usage", []))
    cost = (sum(u["input"] for r in results for u in r.get("usage", [])) * 4
            + sum(u["cache_write"] for r in results for u in r.get("usage", [])) * 5
            + sum(u["cache_read"] for r in results for u in r.get("usage", [])) * 0.2
            + tok_out * 20) / 1e6
    lines += ["", f"Tokens: {tok_in:,} in, {tok_out:,} out · approx. cost ${cost:.2f} "
              "(Opus 5.5 list prices; cache writes assumed 1.25x input)"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="assemble and check requests without calling the API")
    ap.add_argument("--only", action="append", help="fixture id to run (repeatable)")
    ap.add_argument("--repeats", type=int, default=1, help="runs per fixture, to see decision stability")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    args = ap.parse_args()

    data = json.loads(read(FIXTURES))
    fixtures = [f for f in data["fixtures"] if not args.only or f["id"] in args.only]
    if not fixtures:
        print("No fixtures matched --only.", file=sys.stderr)
        return 2
    cards = {"CL_CARDS": read(FRAMEWORKS / "connected-learning.md"),
             "PB_CARDS": read(FRAMEWORKS / "pb-techniques.md"),
             "EB_CARDS": read(FRAMEWORKS / "evidence-based-practices.md")}

    if args.dry_run:
        problems = 0
        for fx in fixtures:
            for step, (system, user, missing) in plan_fixture(fx, cards, None).items():
                chars = len(system[0]["text"]) + len(user)
                status = "OK" if not missing else f"MISSING {missing}"
                problems += bool(missing)
                print(f"{fx['id']:34} {step:9} ~{chars // 4:>6,} tokens  {status}")
        calls = 4 * len(fixtures) * args.repeats
        print(f"\n{calls} API calls would be made (4 per fixture x {len(fixtures)} fixtures x {args.repeats} repeats).")
        return 1 if problems else 0

    import anthropic
    client = anthropic.Anthropic()  # credentials from ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / ant profile

    out_dir = RUNS / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for fx in fixtures:
        for rep in range(args.repeats):
            tag = fx["id"] + (f"-r{rep + 1}" if args.repeats > 1 else "")
            print(f"running {tag} ...", flush=True)
            try:
                r = run_fixture(client, fx, cards, args.effort)
            except (anthropic.RateLimitError, anthropic.APIStatusError, anthropic.APIConnectionError,
                    RuntimeError, ValueError, json.JSONDecodeError) as e:
                r = {"id": tag, "error": f"{type(e).__name__}: {e}"}
            r["id"] = tag
            (out_dir / f"{tag}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
            results.append(r)

    summary = summarise(results, args.effort)
    (out_dir / "summary.md").write_text(summary, encoding="utf-8")
    print("\n" + summary + f"\nSaved to {out_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

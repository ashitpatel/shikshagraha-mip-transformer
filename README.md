# Shikshagraha MIP Scaffold Builder (SG-MSB)

**Shikshagraha MIP Transformer capabilities on the lesson-scaffold-builder engine: a Micro-Improvement Project (MIP) goes in, a validated MLS DAG sequence comes out, printed as offline teacher cards.**

> **Status: merged prototype, not yet run live end to end.** The engine comes from the [`lesson-scaffold-builder`](https://github.com/ashitpatel/lesson-scaffold-builder) package; this repo adds the MIP compatibility layer (MIP schema, `variant_id`, gate evals, agent kit). No practitioner has reviewed the merged output, and nothing here shows the cards improve learning.

Lineage: `ShikshagrahaMIPTransformer` (India-specific MIP prototype) → `shikshagraha-MIP-scaffold-builder` (minimal data-agnostic snapshot) → `lesson-scaffold-builder` (working generalised pipeline, now a dependency) → this repo (MIP capabilities as a thin layer over it).

## How it works

```
MIP (Shikshagraha Commons) ──► sgmsb.run ──► lsb pipeline ──► teacher cards
```

A MIP **is** a Micro-Lesson Scaffold: one MIP is one MLS unit and MIP tasks are MLS steps. The MIP is required input here — every run starts from a schema-valid MIP stamped with its `variant_id`. Every framework (evidence-based, Connected Learning, participatory budgeting) stays optional, and all framework UX (`--ask`, `--answers`, `--no-eb` / `--no-cl` / `--no-pb`) is LSB's, used verbatim.

| Step | What it does | Lives in |
|---|---|---|
| [MIP run](schema/README.md) | Requires a MIP ([mip.schema.json](schema/mip.schema.json)), stamps its [variant_id](schema/variant_id.py), runs the LSB pipeline on it | This repo (`python -m sgmsb.run`) |
| Decompose → validate → critic → stages → render | The LSB pipeline: 11 deterministic checks, 21-check reviewer, three optimisation stages, teacher cards | `lesson-scaffold-builder` package (`lsb-run`, `lsb-validate`, …) |
| [Gates](prompts/smt/README.md) | SMT fit-check prompts (classify + 3 gates) with [golden evals](evals/golden/README.md) | This repo (`evals/`) |
| [Agent kit](agent-kit/README.md) | Run a MIP in any chat assistant: paste-in, custom assistant, Claude Skill | This repo (`agent-kit/`) |

The SMT originals (gate prompts, 32 framework cards, C1–C21 checklist, walkthroughs) are preserved under [prompts/smt/](prompts/smt/README.md), [frameworks/smt/](frameworks/smt/connected-learning.md) and [docs/smt/](docs/smt/README.md). The mapping between SMT checks/cards and LSB checks/cards is in [docs/smt-mapping.md](docs/smt-mapping.md).

## Getting started

Python 3.10+. Install the engine first, then this project:

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -e ../lesson-scaffold-builder
python3 -m pip install -e .
```

Run the offline checks (no model, no API key):

```bash
python -m unittest discover tests
python evals/decision_model.py --strict
python evals/run_gates.py --dry-run
python schema/validate_examples.py
python agent-kit/build.py --check
```

Run a MIP through the pipeline (see the [LSB README](https://github.com/ashitpatel/lesson-scaffold-builder) for backends):

```bash
python -m sgmsb.run path/to/mip.json --dry-run   # no API calls
python -m sgmsb.run path/to/mip.json --ask       # LSB's framework questions
python -m sgmsb.run path/to/mip.json --no-pb     # frameworks stay optional
```

Or only convert a MIP to an MLS DAG and validate it:

```bash
python -m sgmsb.mip path/to/mip.json --validate
```

## Layout

- `sgmsb/` — the adapter: `run` (MIP → LSB pipeline CLI) and `mip` (MIP → MLS conversion + CLI).
- `schema/` — MIP + usage-event schemas, `variant_id.py`, examples.
- `prompts/smt/`, `frameworks/smt/` — original SMT gate prompts and 32 cards.
- `evals/` — gate fixtures, decision cases, golden references, recorded baseline.
- `agent-kit/` — paste-in / custom-assistant / Skill delivery sources and generated `dist/`.
- `docs/` — [SMT↔LSB mapping](docs/smt-mapping.md), [SMT docs](docs/smt/README.md); `reports/`, `research_notes/`, [EXPLORATION.md](EXPLORATION.md) — SMT analysis (reference).
- Everything else (engine, LSB prompts/cards/schemas, browser kit, blog) lives in the `lesson-scaffold-builder` package.

## License

Code (`*.py`) and JSON schemas: [Apache-2.0](LICENSE). Content (prompts, cards, docs, walkthroughs, eval fixtures): [CC BY-SA-4.0](LICENSE-CONTENT).

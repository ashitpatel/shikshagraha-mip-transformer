# SMT → LSB check and card mapping

How the Shikshagraha MIP Transformer originals (kept under `prompts/smt/`,
`frameworks/smt/`, `docs/smt/`) correspond to the LSB engine checks and cards
this repo runs. Verified by reading both sides; "split" means one SMT check
became two LSB checks, "stage" means it moved from the critic into a
per-unit stage decision, "dropped" means the region-neutral engine has no
counterpart.

Sources: [SMT critic](../prompts/smt/50-critic.md),
[SMT review checklist](../agent-kit/src/review-checklist.md),
[LSB critic](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/prompts/50-critic.md), [LSB validate](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/lsb/validate.py).

## Checks: C1–C21 → D01–D11 / G01–G21

- C1 schema errors empty → D01 schema conformance (different schema: MIP vs MLS DAG).
- C2 size (≤8 wk, ≤9 tasks, ≤2 added) → D02 unit cap + D03 steps per unit + D04 run length + D11 step size / G01–G03 (limits re-expressed per unit).
- C3 objective preserved → D09 + G13 macro alignment (SMT diffs baseline vs revised; LSB links each unit to the macro objective).
- C4 no FLN practice removed → G18 deep work kept (related, narrower in LSB).
- C5 owner unchanged and adult → D05 + G05 roles.
- C6 credit first → stage behaviour ("credit what's already there"), enforced by prompts, no numbered check.
- C7 real change, not relabelling → `optimise.py` edit gate in code + G14 sourcing.
- C8 gate consistency (no card cited for an abstained method) → `run.py` stage loop abstain/apply logic in code.
- C9 supportable claims only → G14 pedagogical sourcing (direct counterpart).
- C10 child safeguarding → G06 privacy + G19 safety (split).
- C11 money and hazardous work → G07 financial isolation + G19 safety (split).
- C12 real confirmed resource for ballots → PB fit-gate at stage level (no critic row).
- C13 SMC ballots advisory → dropped (India-specific); nearest is G05 roles.
- C14 equity and inclusion → G20 collaborative balance + G19 inclusive visibility (split).
- C15 offline and cost → G08 offline default + G17 materials (split).
- C16 counting rule announced → PB-03 card content at stage level.
- C17 feasibility, plain task sentences → G04 audience validation + G21 output clarity.
- C18 attribution line and honest cost → dropped (LSB cards carry no attribution line).
- C19 no child-level tracking → G06 privacy (direct) + G16 low overhead (related).
- C20 EB non-negotiables all present → EB fit-gate ("need ALL non-negotiables or abstain") at stage level, guarded by G14.
- C21 re-derive gate decisions → dropped as a check; LSB has no classify/gates step (stages decide per unit with critic re-review). The SMT gate logic itself survives as [`evals/decision_model.py`](../evals/decision_model.py) with its fixtures.

LSB-only (no SMT source): D06 step numbering, D07 + G11 dependency mapping,
D08 + G12 cycle prevention, D10 + G09 regional terms, G10 socioeconomic
adaptability, G15 coherence (`Recall from <id>`), G16 low overhead.

Deterministic subset of C-checks runnable without a model:
[`evals/check_transform.py`](../evals/check_transform.py) covers
C1/C2/C3/C5/C8/C9/C17/C18 and stamps `variant_id`.

## Cards: 32 SMT → 15 LSB

SMT cards: [CL](../frameworks/smt/connected-learning.md) (12),
[EB](../frameworks/smt/evidence-based-practices.md) (10),
[PB](../frameworks/smt/pb-techniques.md) (10).
LSB cards: [CL](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/frameworks/connected-learning.md),
[EB](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/frameworks/evidence-based-practices.md),
[PB](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/frameworks/participatory-budgeting.md) (5 each + fit-gate).

Connected Learning:

- CL-interests → CL-01; CL-peers → CL-02; CL-shared-purpose → CL-04;
  CL-audience → CL-05; CL-opportunities / CL-production /
  CL-connections-across-settings → CL-03 (folded into real-world context).
- CL-scope → the fit-gate preamble (no card). CL-relationships,
  CL-asset-map, CL-brokering, CL-transitions → dropped as cards; their
  substance survives as guardrails (G06 privacy, G19 safety).

Evidence-based practices:

- EB-retrieval → EB-01 retrieval + EB-02 spaced (split);
  EB-slate-feedback → EB-04 checking for understanding;
  EB-maths-representations → EB-05 concrete/visual.
- EB-level-grouping, EB-tutoring, EB-akshara, EB-fidelity-loop,
  EB-plan-to-routine, EB-measure, EB-scope → dropped as cards
  (India-program-specific: TaRL slots, volunteer tutoring, akshara blocks,
  head-teacher observation loops). They remain usable via the SMT gate path.
- EB-03 worked examples is LSB-new; no SMT card sources it.

Participatory budgeting:

- PB-allocate-knapsack → PB-01; PB-prioritise + PB-ideas + PB-vetting →
  PB-02 civic cycle (compressed); PB-count-greedy → PB-03;
  PB-report-back → PB-05; PB-scope → the fit-gate.
- PB-equal-shares (digital-only) → loosely PB-04 shared resource round.
- PB-india-smc, PB-not-pb → dropped (India-specific / meta).

## Limits

SMT golden conventions (≤8 wk, ≤9 tasks, ≤2 added per MIP) and LSB limits
(`config/taxonomy_mapping.json`: ≤5 units, 3–7 steps/unit, 2–4 weeks/unit,
≤2 cards and ≤1 added step per unit per stage) are reconciled by the MIP
adapter: a MIP becomes units sized to LSB limits, and
[`check_transform.py`](../evals/check_transform.py) still enforces the MIP-level
caps on the way in.

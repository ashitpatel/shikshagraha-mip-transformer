# Schemas

| File | What it describes |
|---|---|
| [mip.schema.json](mip.schema.json) | One MIP: the catalogue format plus `x_transform` (gates, changes, rationale, and **variant identity**) |
| [mip-usage-event.schema.json](mip-usage-event.schema.json) | One event in the life of one MIP use at one school: offered → chosen → started → progress → completed/abandoned → outcome reported |
| [variant_id.py](variant_id.py) | Computes the stable content id `v1:<16 hex>` for a MIP variant |
| [examples/mip-variants.json](examples/mip-variants.json) | A baseline and a transformed variant of the catalogue's "School resources" MIP, with ids and parent link |
| [examples/usage-events.jsonl](examples/usage-events.jsonl) | One illustrative use of that transformed variant, from offer to outcome (synthetic data) |
| [validate_examples.py](validate_examples.py) | Validates the examples and checks that the event schema **rejects** student-level fields, names, phone numbers, raw UDISE codes and missing required parts |

## Why log usage at all

The pipeline produces **variants** of a MIP (the baseline and one or more transformed versions). Nothing yet says which variant schools pick, finish, or find useful. These logs make three later steps possible, in order:

1. **Describe.** Choice, completion and abandonment rates, owner ratings and indicators met, by domain × variant kind × gates applied. Only simple counts and proportions, pooled across schools. *This is the point of the schema; it needs no model.*
2. **Compare.** A randomised offer order (`offer.policy = "uniform-random"`) for a period, so "transformed vs. baseline" can be compared without selection bias, e.g. completion rate with a confidence interval per domain.
3. **Recommend (only if 1–2 show real differences).** An *advisory* recommender for which variant to **show first** to an owner. It never decides for them, and it keeps a minimum exploration share for every variant. Because every offer logs its policy and `first_shown_probability`, a new recommender can be evaluated offline on past logs (inverse-propensity weighting) before it's switched on. See EXPLORATION §11 for why a run-time allocation engine (UCWhittle) isn't the right first step.

## Privacy rules (built into the event schema)

- **No student-level data**, ever (CL-G9). Outcome figures are class- or school-level aggregates only (`aggregate_value`).
- **No names, phone numbers or emails.** Owners are a role plus an optional keyed hash; schools are a keyed hash of the UDISE code. The hashing key stays with the platform and never appears in logs.
- **Coarse context only:** state, pseudonymous district, school level, management, enrolment band, rural/urban, medium.
- `additionalProperties: false` everywhere, so unexpected fields fail validation rather than leak in.
- Safeguarding problems are flagged as a boolean; details go through the platform's safeguarding process, not this log.
- **Limit:** a schema can't stop personal data typed into the few free-text fields (`open_question_answers`, indicator text). The platform should screen them (e.g. for names and phone numbers) before storing.

## Variant identity

`x_transform.variant_id` is assigned by the **orchestrator**, never by a model: `v1:` plus the first 16 hex chars of SHA-256 over the canonical JSON of the MIP (sorted keys, UTF-8, compact separators), with `variant_id`, `parent_variant_id` and `pipeline` removed first. `parent_variant_id` links a transformed variant to its baseline. `pipeline` records model, effort, prompt and card hashes, and the critic verdict, so an outcome can be traced back to the exact prompt and card versions that produced the variant.

## Validate

```bash
python3 schema/validate_examples.py
```

# Shikshagraha MIP Scaffold Builder (SG-MSB)

**A skeletal wrapper: a Micro-Improvement Project (MIP) goes in, the [lesson-scaffold-builder](https://github.com/ashitpatel/lesson-scaffold-builder) pipeline runs it, validated MLS units and offline teacher cards come out.**

This repo owns exactly two specificities over lesson-scaffold-builder (LSB):

1. **MLS relabeled as MIP.** A MIP *is* a Micro-Lesson Scaffold: one MIP is one MLS unit (over 7 tasks it spans units), MIP tasks are MLS steps. The MIP catalogue format plus `x_transform` is defined in [schema/mip.schema.json](schema/mip.schema.json); every run stamps the stable content id `variant_id` (`v1:` + 16 hex).
2. **Breakdown is mandatory and derived.** LSB lets the user keep one module or tune the breakdown; here the MIP's task chunks (`mip_to_mls`, at most 7 steps per unit) always define it. `--ask` is rejected and breakdown keys in `--answers` are overridden with the chunk-derived values. Stage limits stay user-tunable.

Everything else — decompose, validate (D01–D11), critic (G01–G21), EB→CL→PB stages, repair, render — is LSB's, used verbatim. For pipeline concepts, LSB's live walkthroughs, and stage cards, read the LSB docs; the MIP example here is a minimal fixture for the wrapper's own tests.

## Install

Python 3.10+. Install the engine first, then this wrapper:

```bash
pip install "git+https://github.com/ashitpatel/lesson-scaffold-builder.git"
pip install -e .
```

## Run

```bash
python -m sgmsb.mip schema/examples/mip-variants.json --pick baseline --validate
python -m sgmsb.run schema/examples/mip-variants.json --pick baseline --dry-run
```

`sgmsb.mip --validate` reports the MIP-schema verdict plus the MLS verdict on its chunks (D10 regional terms deferred: chunking keeps MIP text verbatim and 05-decompose neutralises it). `sgmsb.run` writes `00-mip.json`, `00-chunks.json`, the chunk-sectioned source and merged answers into the run folder, delegates to `lsb.run`, then audits `choices.json` to prove the forced breakdown held.

## Caveats

- D10 deferral is a design assumption: no live end-to-end run has yet shown 05-decompose neutralising every flagged term.
- The model may refine chunk boundaries within LSB's code checks (e.g. sub-split a chunk); the chunks force the input structure and caps, not the exact outcome units.
- `mls_id` values and MLS identifiers stay as LSB requires them (`MIP` in an id would trip D10's term match); the MIP vocabulary is user-facing.
- The pre-wrapper SMT prototype (prompts, frameworks, evals, agent-kit, research notes) was removed; see git history. Usage-event telemetry belongs to the platform, not this wrapper.

# Schemas

| File | What it describes |
|---|---|
| [mip.schema.json](mip.schema.json) | One MIP: the catalogue format plus `x_transform` (gates, changes, rationale, and **variant identity**) |
| [examples/mip-variants.json](examples/mip-variants.json) | A baseline and a transformed variant of the catalogue's "School resources" MIP, with ids and parent link |

## Variant identity

`x_transform.variant_id` is assigned by the **orchestrator**, never by a model: `v1:` plus the first 16 hex chars of SHA-256 over the canonical JSON of the MIP (sorted keys, UTF-8, compact separators), with `variant_id`, `parent_variant_id` and `pipeline` removed first. `parent_variant_id` links a transformed variant to its baseline. Implemented in `sgmsb.variant_id` (`python -m sgmsb.variant_id path/to/mip.json` prints the id).

## Validate

Example validity, id correctness and the parent link are covered by `tests/test_mip.py`:

```bash
python -m unittest discover -s tests
```

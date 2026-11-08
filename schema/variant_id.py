#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stable content ids for MIP variants (see x_transform.variant_id in mip.schema.json).

    python3 schema/variant_id.py path/to/mip.json    # prints the id

The id depends only on the MIP's content: the id fields themselves and the
pipeline metadata are removed before hashing, so re-running the pipeline with
identical output yields the same id, and any content change yields a new one.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys

EXCLUDED_X_TRANSFORM_KEYS = ("variant_id", "parent_variant_id", "pipeline")


def canonical(mip: dict) -> bytes:
    body = copy.deepcopy(mip)
    xt = body.get("x_transform")
    if isinstance(xt, dict):
        for key in EXCLUDED_X_TRANSFORM_KEYS:
            xt.pop(key, None)
        if not xt:
            body.pop("x_transform")
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def variant_id(mip: dict) -> str:
    return "v1:" + hashlib.sha256(canonical(mip)).hexdigest()[:16]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: variant_id.py MIP_JSON_FILE")
    with open(sys.argv[1], encoding="utf-8") as f:
        print(variant_id(json.load(f)))

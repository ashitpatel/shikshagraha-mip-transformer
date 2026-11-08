"""MIP adapter: schema validation, variant_id stability, MIP->MLS conversion."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from sgmsb import mip
from lsb import validate as v

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = json.loads((ROOT / "schema/examples/mip-variants.json").read_text(encoding="utf-8"))


def neutral_mip(n_tasks=4, **over):
    base = {
        "title": "Reading corner",
        "domain": "Curriculum, Pedagogy & Assessment",
        "target_stakeholder": "school leader",
        "duration": "4 weeks",
        "objective": "Every child reads aloud from the corner shelf each day.",
        "tasks": [
            {"seq": i, "name": f"Run the daily reading round, group {i}"}
            for i in range(1, n_tasks + 1)
        ],
    }
    base.update(over)
    return base


class VariantId(unittest.TestCase):
    def test_matches_stored_example_stamp(self):
        # The same content must get the same id as the stored example.
        self.assertEqual(mip.variant_id(EXAMPLES["baseline"]), "v1:9b87da2056165481")

    def test_example_ids_match_content_and_parent_link(self):
        # Folded in from schema/validate_examples.py: the stored ids are
        # content-correct and the transformed variant links its baseline.
        for key in ("baseline", "transformed"):
            with self.subTest(key=key):
                self.assertEqual(EXAMPLES[key]["x_transform"]["variant_id"],
                                 mip.variant_id(EXAMPLES[key]))
        self.assertEqual(EXAMPLES["transformed"]["x_transform"]["parent_variant_id"],
                         EXAMPLES["baseline"]["x_transform"]["variant_id"])

    def test_ignores_pipeline_metadata(self):
        # Folded in from schema/validate_examples.py.
        import copy
        t = copy.deepcopy(EXAMPLES["transformed"])
        t["x_transform"]["pipeline"]["revisions"] = 9
        self.assertEqual(mip.variant_id(t), EXAMPLES["transformed"]["x_transform"]["variant_id"])

    def test_stable_and_shaped(self):
        a = mip.variant_id(neutral_mip())
        self.assertRegex(a, r"^v1:[0-9a-f]{16}$")
        self.assertEqual(a, mip.variant_id(neutral_mip()))
        changed = neutral_mip()
        changed["tasks"][0]["name"] += "!"
        self.assertNotEqual(a, mip.variant_id(changed))

    def test_stamp_writes_x_transform(self):
        doc = neutral_mip()
        vid = mip.stamp_variant_id(doc)
        self.assertEqual(doc["x_transform"]["variant_id"], vid)
        self.assertEqual(mip.validate_mip(doc), [])


class ValidateMip(unittest.TestCase):
    def test_examples_pass(self):
        for key in ("baseline", "transformed"):
            with self.subTest(key=key):
                self.assertEqual(mip.validate_mip(EXAMPLES[key]), [])

    def test_rejects_bad_documents(self):
        self.assertTrue(mip.validate_mip({}))
        bad = neutral_mip()
        bad["domain"] = "Not a domain"
        self.assertTrue(mip.validate_mip(bad))


class Convert(unittest.TestCase):
    def test_neutral_mip_passes_every_code_check(self):
        mls = mip.mip_to_mls(neutral_mip())
        report = v.validate(mls)
        self.assertTrue(report.passed, v.format_text(report))

    def test_objective_verbatim_and_chain(self):
        mls = mip.mip_to_mls(neutral_mip(n_tasks=9))
        self.assertEqual(mls["macro_objective"], neutral_mip()["objective"])
        self.assertEqual(len(mls["mls_units"]), 2)
        self.assertEqual(mls["mls_units"][0]["dependencies"], [])
        self.assertEqual(mls["mls_units"][1]["dependencies"], [mls["mls_units"][0]["mls_id"]])
        for u in mls["mls_units"]:
            self.assertEqual([t["step"] for t in u["tasks"]], list(range(1, len(u["tasks"]) + 1)))
            self.assertLessEqual(len(u["tasks"]), 7)

    def test_roles_and_sub_tasks(self):
        doc = neutral_mip(n_tasks=2)
        doc["tasks"][0]["sub_tasks"] = ["Lay out the mats", "Stack the books by level"]
        doc["tasks"][1]["x_transform"] = {"student_role": "peer reader"}
        mls = mip.mip_to_mls(doc)
        steps = mls["mls_units"][0]["tasks"]
        self.assertIn("Lay out the mats", steps[0]["action"])
        self.assertEqual(steps[0]["role"], "Lead_Educator")
        self.assertEqual(steps[1]["role"], "Peer_Facilitator")

    def test_regional_terms_surface_as_d10(self):
        # The adapter keeps text verbatim; neutralising it is the pipeline's job.
        doc = neutral_mip(n_tasks=3)
        doc["tasks"][0]["name"] = "Share the list with the CRP"
        report = v.validate(mip.mip_to_mls(doc))
        d10 = next(c for c in report.checks if c.id == "D10")
        self.assertFalse(d10.passed)
        self.assertTrue(any(c.id == "D10" and c.passed for c in v.validate(mip.mip_to_mls(neutral_mip(n_tasks=3))).checks))

    def test_duration_parsing(self):
        self.assertEqual(mip.parse_duration_weeks("2 weeks"), 2)
        self.assertEqual(mip.parse_duration_weeks("1 month"), 4)
        self.assertEqual(mip.parse_duration_weeks("2 months"), 8)
        self.assertEqual(mip.parse_duration_weeks("soon"), 4)
        self.assertEqual(mip.mip_to_mls(neutral_mip(duration="2 months"))["mls_units"][0]["duration_weeks"], 4)


class Cli(unittest.TestCase):
    def test_validate_example_baseline(self):
        proc = subprocess.run(
            [sys.executable, "-m", "sgmsb.mip", "schema/examples/mip-variants.json",
             "--pick", "baseline", "--validate"],
            cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("v1:9b87da2056165481", proc.stdout)
        # The example names the CRP, so D10 is reported but deferred.
        self.assertIn("D10 regional terms deferred", proc.stdout)

    def test_schema_failure_exits_1(self):
        import tempfile
        bad = neutral_mip()
        del bad["objective"]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(bad, f)
        self.addCleanup(Path(f.name).unlink)
        proc = subprocess.run(
            [sys.executable, "-m", "sgmsb.mip", f.name, "--validate"],
            cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("MIP schema: FAIL", proc.stdout)

    def test_missing_file_is_usage_error(self):
        proc = subprocess.run(
            [sys.executable, "-m", "sgmsb.mip", "nope.json", "--validate"],
            cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()

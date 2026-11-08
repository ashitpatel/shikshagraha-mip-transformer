"""SMT evals in their new paths: fixtures, decision model, transform checks, kit sync."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))
import check_transform  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT,
                          capture_output=True, text=True, timeout=120)


class Fixtures(unittest.TestCase):
    def test_counts(self):
        fixtures = json.loads((ROOT / "evals/gate_fixtures.json").read_text(encoding="utf-8"))
        cases = json.loads((ROOT / "evals/decision_cases.json").read_text(encoding="utf-8"))
        golden = [p for p in (ROOT / "evals/golden").glob("*.md") if p.name != "README.md"]
        self.assertEqual(len(fixtures["fixtures"]), 15)
        self.assertEqual(len(cases["cases"]), 20)
        self.assertEqual(len(golden), 12)

    def test_recorded_baseline_present(self):
        summary = ROOT / "evals/baseline-20261106/summary.md"
        self.assertTrue(summary.exists())
        self.assertIn("87/90", summary.read_text(encoding="utf-8"))


class Runners(unittest.TestCase):
    def test_decision_model_strict(self):
        proc = run("evals/decision_model.py", "--strict")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("0 decision(s) outside", proc.stdout)

    def test_validate_examples(self):
        proc = run("schema/validate_examples.py")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_run_gates_dry_run(self):
        proc = run("evals/run_gates.py", "--dry-run")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("60 API calls would be made", proc.stdout)

    def test_agent_kit_in_sync(self):
        proc = run("agent-kit/build.py", "--check")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class TransformChecks(unittest.TestCase):
    GATES = {
        "gate_cl": {"connected_learning": {"decision": "ABSTAIN"}},
        "gate_pb": {"pb_process": {"decision": "APPLY"}},
        "gate_eb": {"evidence_based": {"decision": "ABSTAIN"}},
    }

    def test_example_pair_vector(self):
        ex = json.loads((ROOT / "schema/examples/mip-variants.json").read_text(encoding="utf-8"))
        r = check_transform.check(ex["baseline"], {"mip": ex["transformed"]}, self.GATES)
        for c in ("C1_schema", "C2_size", "C3_objective_kept", "C5_owner_kept", "C8_labels",
                  "C9_numbers_sourced", "C9_untested_item", "C17_short_names"):
            self.assertTrue(r[c], c)
        # The example predates the cost rule, so C18 stays False on it.
        self.assertFalse(r["C18_cost"])

    def test_catches_objective_and_owner_drift(self):
        ex = json.loads((ROOT / "schema/examples/mip-variants.json").read_text(encoding="utf-8"))
        out = {"mip": json.loads(json.dumps(ex["transformed"]))}
        out["mip"]["objective"] = "Something else entirely"
        out["mip"]["target_stakeholder"] = "students"
        r = check_transform.check(ex["baseline"], out, self.GATES)
        self.assertFalse(r["C3_objective_kept"])
        self.assertFalse(r["C5_owner_kept"])


if __name__ == "__main__":
    unittest.main()

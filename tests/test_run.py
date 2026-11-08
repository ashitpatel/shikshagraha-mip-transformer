"""sgmsb.run: a MIP is required; frameworks stay optional through LSB's UX."""

import json
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = str(ROOT / "schema/examples/mip-variants.json")


class RenderSource(unittest.TestCase):
    def test_rendering_carries_mip_content(self):
        from sgmsb.run import render_mip_source
        ex = json.loads(Path(EXAMPLES).read_text(encoding="utf-8"))
        text = render_mip_source(ex["baseline"])
        for needle in ("School resources", "Improve the resources available in the school",
                       "Assess the current resources", "Share the list with the CRP"):
            self.assertIn(needle, text)
        self.assertEqual(text, render_mip_source(ex["baseline"]))


class MipRequired(unittest.TestCase):
    def test_missing_file_is_usage_error_and_never_reaches_lsb(self):
        from sgmsb import run as rrun
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main(["nope.json", "--ref", "x"]), 2)

    def test_schema_invalid_mip_exits_1_and_never_reaches_lsb(self):
        import tempfile
        from sgmsb import run as rrun
        ex = json.loads(Path(EXAMPLES).read_text(encoding="utf-8"))
        bad = ex["baseline"]
        del bad["objective"]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(bad, f)
        self.addCleanup(Path(f.name).unlink)
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([f.name]), 1)

    def test_non_mip_json_is_usage_error(self):
        import tempfile
        from sgmsb import run as rrun
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump({"title": "broken"}, f)
        self.addCleanup(Path(f.name).unlink)
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([f.name]), 2)


class LsbUxPassthrough(unittest.TestCase):
    def run_main(self, argv):
        import tempfile
        from sgmsb import run as rrun
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        out = tmp / "run"
        with mock.patch.object(rrun.lrun, "main", return_value=0) as m:
            rc = rrun.main(argv + ["--out", str(out)])
        return rc, m.call_args.args[0], out

    def test_valid_mip_delegates_with_defaults(self):
        rc, forwarded, out = self.run_main([EXAMPLES, "--pick", "baseline"])
        self.assertEqual(rc, 0)
        src = Path(forwarded[0])
        self.assertTrue(src.exists())
        self.assertIn("School resources", src.read_text(encoding="utf-8"))
        self.assertEqual(forwarded[forwarded.index("--ref") + 1], "School resources")
        for flag in ("--no-eb", "--no-cl", "--no-pb"):
            self.assertNotIn(flag, forwarded)
        stamped = json.loads((out / "00-mip.json").read_text(encoding="utf-8"))
        self.assertEqual(stamped["x_transform"]["variant_id"], "v1:9b87da2056165481")

    def test_framework_flags_pass_through_verbatim(self):
        rc, forwarded, _ = self.run_main(
            [EXAMPLES, "--pick", "baseline", "--no-cl", "--no-pb", "--ask"])
        self.assertEqual(rc, 0)
        self.assertIn("--no-cl", forwarded)
        self.assertIn("--no-pb", forwarded)
        self.assertIn("--ask", forwarded)
        self.assertNotIn("--no-eb", forwarded)

    def test_dry_run_passes_through(self):
        rc, forwarded, _ = self.run_main([EXAMPLES, "--pick", "baseline", "--dry-run"])
        self.assertEqual(rc, 0)
        self.assertIn("--dry-run", forwarded)

    def test_summary_gets_mip_provenance(self):
        import tempfile
        from sgmsb.run import record_mip
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        (tmp / "summary.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
        record_mip(tmp, {"variant_id": "v1:abc", "title": "T"})
        summary = json.loads((tmp / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["mip"], {"variant_id": "v1:abc", "title": "T"})
        record_mip(tmp / "missing", {"variant_id": "v1:abc"})  # no summary yet: no crash


if __name__ == "__main__":
    unittest.main()

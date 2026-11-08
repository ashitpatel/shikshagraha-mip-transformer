"""sgmsb.run: MIP in, mandatory chunk breakdown, LSB stages out."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = str(ROOT / "schema/examples/mip-variants.json")


def baseline():
    return json.loads(Path(EXAMPLES).read_text(encoding="utf-8"))["baseline"]


def write_json(testcase, obj):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    testcase.addCleanup(Path(f.name).unlink)
    json.dump(obj, f)
    f.close()
    return f.name


def run_main(testcase, argv):
    from sgmsb import run as rrun
    tmp = Path(tempfile.mkdtemp())
    testcase.addCleanup(shutil.rmtree, tmp, True)
    out = tmp / "run"
    with mock.patch.object(rrun.lrun, "main", return_value=0) as m:
        rc = rrun.main(argv + ["--out", str(out)])
    return rc, m, out


class RenderSource(unittest.TestCase):
    def test_rendering_marks_one_section_per_chunk(self):
        from sgmsb import mip as M
        from sgmsb.run import render_mip_source
        doc = baseline()
        mls = M.mip_to_mls(doc)
        text = render_mip_source(doc, mls)
        for needle in ("School resources", "Improve the resources available in the school",
                       "Assess the current resources", "Share the list with the CRP"):
            self.assertIn(needle, text)
        sections = [ln for ln in text.splitlines() if ln.startswith("## ")]
        self.assertEqual(len(sections), len(mls["mls_units"]))
        self.assertEqual(text, render_mip_source(doc, mls))

    def test_multi_chunk_mip_renders_each_chunk(self):
        from sgmsb import mip as M
        from sgmsb.run import render_mip_source
        doc = baseline()
        doc["tasks"] = [{"seq": i, "name": f"Do part {i} of the work"} for i in range(1, 10)]
        mls = M.mip_to_mls(doc)
        self.assertEqual(len(mls["mls_units"]), 2)
        sections = [ln for ln in render_mip_source(doc, mls).splitlines() if ln.startswith("## ")]
        self.assertEqual(len(sections), 2)


class MipRequired(unittest.TestCase):
    def test_missing_file_is_usage_error_and_never_reaches_lsb(self):
        from sgmsb import run as rrun
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main(["nope.json", "--ref", "x"]), 2)

    def test_schema_invalid_mip_exits_1_and_never_reaches_lsb(self):
        from sgmsb import run as rrun
        bad = baseline()
        del bad["objective"]
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([write_json(self, bad)]), 1)

    def test_non_mip_json_is_usage_error(self):
        from sgmsb import run as rrun
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([write_json(self, {"title": "broken"})]), 2)


class ChunkingMandatory(unittest.TestCase):
    def test_invalid_chunks_gate_the_run(self):
        from sgmsb import mip as M
        from sgmsb import run as rrun
        doc = baseline()
        doc["tasks"][0]["name"] = "word " * 100  # schema-valid, fails D11 step size
        self.assertEqual(M.validate_mip(doc), [])
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([write_json(self, doc)]), 1)

    def test_chunks_artifact_matches_converter(self):
        from sgmsb import mip as M
        rc, _, out = run_main(self, [EXAMPLES, "--pick", "baseline"])
        self.assertEqual(rc, 0)
        chunks = json.loads((out / "00-chunks.json").read_text(encoding="utf-8"))
        self.assertEqual(chunks, M.mip_to_mls(baseline()))

    def test_d10_deferred_still_delegates(self):
        # The baseline names the CRP: D10 fails, chunking passes, LSB runs.
        rc, m, _ = run_main(self, [EXAMPLES, "--pick", "baseline"])
        self.assertEqual(rc, 0)
        m.assert_called_once()

    def test_audit_rejects_unforced_choices(self):
        from sgmsb import run as rrun
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        out = tmp / "run"

        def fake(argv):
            (out / "choices.json").write_text(json.dumps(
                {"single_module": True, "max_units": 5, "focus": "auto"}), encoding="utf-8")
            return 0

        with mock.patch.object(rrun.lrun, "main", side_effect=fake):
            self.assertEqual(rrun.main([EXAMPLES, "--pick", "baseline", "--out", str(out)]), 1)

    def test_audit_accepts_forced_choices(self):
        from sgmsb import run as rrun
        from sgmsb.run import forced_answers
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        out = tmp / "run"

        def fake(argv):
            (out / "choices.json").write_text(json.dumps(forced_answers(1)), encoding="utf-8")
            return 0

        with mock.patch.object(rrun.lrun, "main", side_effect=fake):
            self.assertEqual(rrun.main([EXAMPLES, "--pick", "baseline", "--out", str(out)]), 0)


class AnswersMerge(unittest.TestCase):
    def test_derived_answers_written_and_forwarded(self):
        from sgmsb.run import forced_answers
        rc, m, out = run_main(self, [EXAMPLES, "--pick", "baseline"])
        self.assertEqual(rc, 0)
        forwarded = m.call_args.args[0]
        answers_file = Path(forwarded[forwarded.index("--answers") + 1])
        self.assertEqual(answers_file.parent, out)
        merged = json.loads(answers_file.read_text(encoding="utf-8"))
        self.assertEqual(merged, forced_answers(1))  # baseline chunks to 1 unit

    def test_user_stage_keys_kept_breakdown_overridden(self):
        from sgmsb.run import forced_answers
        user = {"single_module": True, "max_units": 5, "focus": "auto",
                "evidence_based_cards": ["EB-01"]}
        rc, m, _ = run_main(self, [EXAMPLES, "--pick", "baseline",
                                   "--answers", write_json(self, user)])
        self.assertEqual(rc, 0)
        forwarded = m.call_args.args[0]
        merged = json.loads(Path(forwarded[forwarded.index("--answers") + 1]).read_text(encoding="utf-8"))
        self.assertEqual(merged["evidence_based_cards"], ["EB-01"])
        for key, want in forced_answers(1).items():
            self.assertEqual(merged[key], want)

    def test_bad_answers_file_is_usage_error(self):
        from sgmsb import run as rrun
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        self.addCleanup(Path(f.name).unlink)
        f.write("{not json")
        f.close()
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([EXAMPLES, "--pick", "baseline", "--answers", f.name]), 2)
            self.assertEqual(rrun.main(
                [EXAMPLES, "--pick", "baseline", "--answers", write_json(self, ["nope"])]), 2)

    def test_ask_rejected(self):
        from sgmsb import run as rrun
        with mock.patch.object(rrun.lrun, "main", side_effect=AssertionError("called")):
            self.assertEqual(rrun.main([EXAMPLES, "--pick", "baseline", "--ask"]), 2)


class LsbUxPassthrough(unittest.TestCase):
    def test_valid_mip_delegates_with_defaults(self):
        rc, m, out = run_main(self, [EXAMPLES, "--pick", "baseline"])
        self.assertEqual(rc, 0)
        forwarded = m.call_args.args[0]
        src = Path(forwarded[0])
        self.assertTrue(src.exists())
        self.assertIn("School resources", src.read_text(encoding="utf-8"))
        self.assertEqual(forwarded[forwarded.index("--ref") + 1], "School resources")
        for flag in ("--no-eb", "--no-cl", "--no-pb", "--ask"):
            self.assertNotIn(flag, forwarded)
        self.assertIn("--answers", forwarded)
        stamped = json.loads((out / "00-mip.json").read_text(encoding="utf-8"))
        self.assertEqual(stamped["x_transform"]["variant_id"], "v1:9b87da2056165481")

    def test_framework_flags_pass_through_verbatim(self):
        rc, m, _ = run_main(self, [EXAMPLES, "--pick", "baseline", "--no-cl", "--no-pb"])
        self.assertEqual(rc, 0)
        forwarded = m.call_args.args[0]
        self.assertIn("--no-cl", forwarded)
        self.assertIn("--no-pb", forwarded)
        self.assertNotIn("--no-eb", forwarded)

    def test_dry_run_passes_through(self):
        rc, m, _ = run_main(self, [EXAMPLES, "--pick", "baseline", "--dry-run"])
        self.assertEqual(rc, 0)
        self.assertIn("--dry-run", m.call_args.args[0])

    def test_delegation_records_chunks_provenance(self):
        from sgmsb import run as rrun
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        out = tmp / "run"

        def fake(argv):
            (out / "summary.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
            return 0

        with mock.patch.object(rrun.lrun, "main", side_effect=fake):
            rc = rrun.main([EXAMPLES, "--pick", "baseline", "--out", str(out)])
        self.assertEqual(rc, 0)
        summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["mip"]["chunks"], 1)
        self.assertEqual(summary["mip"]["variant_id"], "v1:9b87da2056165481")

    def test_summary_gets_mip_provenance(self):
        from sgmsb.run import record_mip
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        (tmp / "summary.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
        record_mip(tmp, {"variant_id": "v1:abc", "title": "T"})
        summary = json.loads((tmp / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["mip"], {"variant_id": "v1:abc", "title": "T"})
        record_mip(tmp / "missing", {"variant_id": "v1:abc"})  # no summary yet: no crash


if __name__ == "__main__":
    unittest.main()

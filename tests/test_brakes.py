import importlib
import json
import os
import pathlib
import sqlite3
import sys
import tempfile
import time
import unittest


GROKGO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_brakes(root):
    os.environ["GROKGO_ROOT"] = str(root)
    grokgo_root = str(GROKGO_ROOT)
    if grokgo_root not in sys.path:
        sys.path.insert(0, grokgo_root)
    sys.modules.pop("brakes", None)
    return importlib.import_module("brakes")


class BrakesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.brakes = load_brakes(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_failed_call_clears_loop_hash_for_retry(self):
        cfg = {"prices_per_mtok": {"known-model": [1, 1]}}
        task = {"id": "retry-me", "type": "unit.test", "input": {"x": 1}}

        allowed, _, reason = self.brakes.check(task, "t2", "test", cfg)
        self.assertTrue(allowed, reason)
        allowed, _, reason = self.brakes.check(task, "t2", "test", cfg)
        self.assertFalse(allowed)
        self.assertIn("loop detected", reason)

        self.brakes.log("test", task, "t2", "known-model", 10, 10, "failure", cfg)
        allowed, _, reason = self.brakes.check(task, "t2", "test", cfg)
        self.assertTrue(allowed, reason)

    def test_seen_hash_ttl_allows_later_retry(self):
        cfg = {
            "defaults": {"seen_hash_ttl_seconds": 1},
            "prices_per_mtok": {"known-model": [1, 1]},
        }
        task = {"id": "ttl-me", "type": "unit.test", "input": {"x": 1}}

        allowed, _, reason = self.brakes.check(task, "t2", "test", cfg)
        self.assertTrue(allowed, reason)

        con = sqlite3.connect(self.root / "ledger.db")
        con.execute("UPDATE seen_hashes SET ts=?", (time.time() - 10,))
        con.commit()
        con.close()

        allowed, _, reason = self.brakes.check(task, "t2", "test", cfg)
        self.assertTrue(allowed, reason)

    def test_unknown_model_gets_punitive_price_and_receipt_warning(self):
        cfg = {
            "prices_per_mtok": {
                "cheap-model": [1, 5],
                "claude-fable-5": [15, 75],
            }
        }
        task = {"id": "price-me", "type": "unit.test", "input": {"x": 1}}

        cost, receipt_path = self.brakes.log(
            "test", task, "t2", "typo-model", 1_000_000, 0, "success", cfg
        )
        self.assertEqual(cost, 15)

        with open(receipt_path) as f:
            receipt = json.loads(f.read().strip())
        self.assertEqual(receipt["cost_usd"], 15)
        self.assertIn("unknown model", receipt["pricing_warning"])

    def test_receipt_v2_records_summary_tokens_and_new_capability_tag(self):
        cfg = {"prices_per_mtok": {"known-model": [1, 1]}}
        task = {
            "id": "schema-me",
            "type": "runtime.instrumentation",
            "input": {"x": 1},
            "output_summary": "Implemented action receipt v2 fields for richer measurement.",
            "artifact_created": "brakes.py",
        }

        _, receipt_path = self.brakes.log(
            "test", task, "t2", "known-model", 11, 13, "success", cfg
        )

        with open(receipt_path) as f:
            receipt = json.loads(f.read().strip())
        self.assertEqual(receipt["schema_version"], "grokgo.action_receipt.v2")
        self.assertEqual(receipt["outcome"], "success")
        self.assertEqual(receipt["output_summary"], task["output_summary"])
        self.assertEqual(receipt["tokens"], {"input": 11, "output": 13, "total": 24})
        self.assertEqual(receipt["new_capability_vs_polish"], "new_capability")
        self.assertIn("new_capability", receipt["behavior_rule_hits"])

        con = sqlite3.connect(self.root / "ledger.db")
        row = con.execute(
            """SELECT schema_version, outcome, output_summary, tokens_total,
                      new_capability_vs_polish
               FROM calls WHERE task_id=?""",
            ("schema-me",),
        ).fetchone()
        con.close()
        self.assertEqual(
            row,
            (
                "grokgo.action_receipt.v2",
                "success",
                task["output_summary"],
                24,
                "new_capability",
            ),
        )

    def test_receipt_v2_detects_polish_from_output_summary(self):
        cfg = {"prices_per_mtok": {"known-model": [1, 1]}}
        task = {
            "id": "polish-me",
            "type": "runtime.cleanup",
            "input": {"x": 1},
            "output_summary": "Refactored comments, formatting, and minor wording only.",
        }

        _, receipt_path = self.brakes.log(
            "test", task, "t2", "known-model", 10, 10, "success", cfg
        )

        with open(receipt_path) as f:
            receipt = json.loads(f.read().strip())
        self.assertEqual(receipt["new_capability_vs_polish"], "polish")
        self.assertIn("refactor_only", receipt["behavior_rule_hits"])

    def test_receipt_v2_honors_caller_supplied_behavior_class(self):
        cfg = {"prices_per_mtok": {"known-model": [1, 1]}}
        task = {
            "id": "tagged-me",
            "type": "runtime.watchdog",
            "input": {"x": 1},
            "output_summary": "Created a new file, but caller knows this was a health check.",
            "new_capability_vs_polish": "maintenance",
        }

        _, receipt_path = self.brakes.log(
            "test", task, "t2", "known-model", 10, 10, "success", cfg
        )

        with open(receipt_path) as f:
            receipt = json.loads(f.read().strip())
        self.assertEqual(receipt["new_capability_vs_polish"], "maintenance")
        self.assertEqual(receipt["behavior_rule_hits"], ["caller_supplied"])

    def test_budget_day_start_hour_utc_is_configurable(self):
        noon_utc_day_two = 2 * 86400 + 12 * 3600
        cfg = {"defaults": {"budget_day_start_hour_utc": 12}}

        self.assertEqual(
            self.brakes._budget_day_start(noon_utc_day_two + 60, cfg),
            noon_utc_day_two,
        )
        self.assertEqual(
            self.brakes._budget_day_start(noon_utc_day_two - 60, cfg),
            noon_utc_day_two - 86400,
        )

    def test_budget_tz_offset_env_override(self):
        try:
            os.environ["BRAKES_TZ_OFFSET_HOURS"] = "-8"
            two_days_nine_utc = 2 * 86400 + 9 * 3600
            self.assertEqual(
                self.brakes._budget_day_start(two_days_nine_utc, {}),
                2 * 86400 + 8 * 3600,
            )
            self.assertEqual(
                self.brakes._budget_day_start(two_days_nine_utc - 2 * 3600, {}),
                1 * 86400 + 8 * 3600,
            )
        finally:
            os.environ.pop("BRAKES_TZ_OFFSET_HOURS", None)

    def test_note_work_parks_after_two_atomic_empty_outputs(self):
        self.brakes.note_work("unit-lane", produced_output=False)
        streak = self.root / "parked" / ".streak_unit-lane"
        park = self.root / "parked" / "unit-lane"

        self.assertEqual(streak.read_text(), "1")
        self.assertFalse(park.exists())

        self.brakes.note_work("unit-lane", produced_output=False)
        self.assertTrue(park.exists())
        self.assertFalse(streak.exists())

    def test_note_work_clears_streak_on_output(self):
        self.brakes.note_work("unit-lane", produced_output=False)
        self.brakes.note_work("unit-lane", produced_output=True)

        self.assertFalse((self.root / "parked" / ".streak_unit-lane").exists())


if __name__ == "__main__":
    unittest.main()

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

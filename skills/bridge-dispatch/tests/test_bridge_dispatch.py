import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import bridge_dispatch


class BridgeDispatchTests(unittest.TestCase):
    def test_seed_parses_owner_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            backlog = root / "master-backlog.md"
            board = root / "TASK_BOARD.md"
            backlog.write_text(
                "# Master Backlog\n\n"
                "## A. Money\n"
                "- ☐ Stripe now integrated in Hermes desktop → wire it to a real offer — owner Codex + Jeff\n"
                "- ☑ Website live + deployed\n"
            )
            rows = bridge_dispatch.parse_backlog(backlog)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["owner"], "Codex")
            bridge_dispatch.write_board(board, rows)
            text = board.read_text()
            self.assertIn("Stripe now integrated", text)
            self.assertIn("Jeff approves", text)

    def test_parse_owner_uses_last_owner_marker(self):
        task = "Give Revenue Owner role to null (soul drafted) — owner Jeff approve"
        self.assertEqual(bridge_dispatch.parse_owner(task), "Jeff approve")
        task = "Assign a BidLocal product owner — owner Jeff"
        self.assertEqual(bridge_dispatch.parse_owner(task), "Jeff")


if __name__ == "__main__":
    unittest.main()

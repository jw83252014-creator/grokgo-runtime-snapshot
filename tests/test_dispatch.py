import importlib
import pathlib
import sys
import unittest


GROKGO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_dispatch():
    grokgo_root = str(GROKGO_ROOT)
    if grokgo_root not in sys.path:
        sys.path.insert(0, grokgo_root)
    sys.modules.pop("dispatch", None)
    return importlib.import_module("dispatch")


class DispatchReceiptSummaryTest(unittest.TestCase):
    def setUp(self):
        self.dispatch = load_dispatch()

    def test_summarize_output_prefers_explicit_output_summary(self):
        out = {
            "output_summary": "Implemented receipt summaries for dispatch.",
            "action": "none",
        }

        self.assertEqual(
            self.dispatch.summarize_output(out),
            "Implemented receipt summaries for dispatch.",
        )

    def test_summarize_output_falls_back_to_actionable_fields(self):
        self.assertEqual(
            self.dispatch.summarize_output({"recommendation": "Strong keep"}),
            "Strong keep",
        )
        self.assertEqual(
            self.dispatch.summarize_output({"draft": "hello", "score": 8}),
            "Valid JSON output with keys: draft, score",
        )

    def test_summarize_output_marks_schema_failure(self):
        self.assertEqual(
            self.dispatch.summarize_output(None, "not json"),
            "Model response failed JSON schema validation.",
        )


if __name__ == "__main__":
    unittest.main()

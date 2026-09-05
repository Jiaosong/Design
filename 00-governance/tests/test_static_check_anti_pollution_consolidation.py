from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name("static_check_anti_pollution.py")
spec = importlib.util.spec_from_file_location("anti_pollution", CHECKER)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ConsolidationThrottleTests(unittest.TestCase):
    def test_marker_matching_is_case_insensitive(self) -> None:
        self.assertTrue(mod.text_has_any("training_mode", ["TRAINING_MODE"]))
        self.assertTrue(mod.text_has_any("Not Installed Current", ["NOT INSTALLED CURRENT"]))
        self.assertFalse(mod.text_has_any("PROJECT_MODE", ["TRAINING_MODE"]))

    def test_utc_parser_accepts_github_zulu_timestamp(self) -> None:
        value = mod.parse_utc("2026-09-05T00:00:00Z")
        self.assertEqual(value.utcoffset().total_seconds(), 0)


if __name__ == "__main__":
    unittest.main()

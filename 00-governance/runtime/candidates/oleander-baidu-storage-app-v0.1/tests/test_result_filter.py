from __future__ import annotations

import json
import unittest

from app.result_filter import filter_json_text, filter_object


class ResultFilterTests(unittest.TestCase):
    def test_filters_explicit_outside_path_records(self) -> None:
        value = {
            "list": [
                {"path": "/OLEANDER_VAULT/a.pdf", "fsid": 1},
                {"path": "/private/b.pdf", "fsid": 2},
            ]
        }
        filtered = filter_object(value, "/OLEANDER_VAULT")
        self.assertEqual([x["fsid"] for x in filtered["list"]], [1])

    def test_outside_remote_path_cannot_be_masked_by_inside_path(self) -> None:
        value = {
            "list": [
                {
                    "path": "/OLEANDER_VAULT/looks-safe.pdf",
                    "remote_path": "/private/escape.pdf",
                    "fsid": 1,
                },
                {
                    "path": "/OLEANDER_VAULT/ok.pdf",
                    "remote_path": "/OLEANDER_VAULT/PROJECTS/ok.pdf",
                    "fsid": 2,
                },
            ]
        }
        filtered = filter_object(value, "/OLEANDER_VAULT")
        self.assertEqual([x["fsid"] for x in filtered["list"]], [2])

    def test_non_path_quota_passes(self) -> None:
        value = {"total": 100, "used": 50}
        self.assertEqual(filter_object(value, "/OLEANDER_VAULT"), value)

    def test_json_text_is_filtered(self) -> None:
        raw = json.dumps(
            {"list": [{"path": "/outside/a"}, {"path": "/OLEANDER_VAULT/ok"}]}
        )
        parsed = json.loads(filter_json_text(raw, "/OLEANDER_VAULT"))
        self.assertEqual(len(parsed["list"]), 1)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import os
import unittest

from app.policy import (
    CURRENT_ACK,
    DELETE_ACK,
    OVERWRITE_ACK,
    PolicyError,
    StoragePolicy,
    has_current_segment,
    is_within_root,
    normalize_cloud_path,
)


class StoragePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = StoragePolicy(root="/OLEANDER_VAULT", allow_delete=False, allow_share=False)

    def test_normalize_and_root_boundary(self) -> None:
        self.assertEqual(normalize_cloud_path("/OLEANDER_VAULT/PROJECTS"), "/OLEANDER_VAULT/PROJECTS")
        self.assertTrue(is_within_root("/OLEANDER_VAULT/PROJECTS/C01", "/OLEANDER_VAULT"))
        self.assertFalse(is_within_root("/other/C01", "/OLEANDER_VAULT"))
        with self.assertRaises(PolicyError):
            normalize_cloud_path("/OLEANDER_VAULT/../other")

    def test_read_defaults_to_root(self) -> None:
        args = self.policy.prepare_arguments("file_keyword_search", {"key": "school"})
        self.assertEqual(args["dir"], "/OLEANDER_VAULT")

    def test_read_escape_is_blocked(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments("file_list", {"dir": "/"})

    def test_make_dir_current_requires_ack(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments("make_dir", {"path": "/OLEANDER_VAULT/PROJECTS/C01/CURRENT"})
        args = self.policy.prepare_arguments(
            "make_dir",
            {
                "path": "/OLEANDER_VAULT/PROJECTS/C01/CURRENT",
                "oleander_current_ack": CURRENT_ACK,
            },
        )
        self.assertNotIn("oleander_current_ack", args)

    def test_copy_from_current_to_review_does_not_require_current_ack(self) -> None:
        args = self.policy.prepare_arguments(
            "file_copy",
            {
                "filelist": [
                    {
                        "path": "/OLEANDER_VAULT/PROJECTS/C01/CURRENT/a.pdf",
                        "dest": "/OLEANDER_VAULT/PROJECTS/C01/REVIEW",
                        "newname": "a.pdf",
                    }
                ]
            },
        )
        self.assertIn("filelist", args)

    def test_copy_into_current_requires_ack(self) -> None:
        base = {
            "filelist": [
                {
                    "path": "/OLEANDER_VAULT/PROJECTS/C01/REVIEW/a.pdf",
                    "dest": "/OLEANDER_VAULT/PROJECTS/C01/CURRENT",
                    "newname": "a.pdf",
                }
            ]
        }
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments("file_copy", base)
        base["oleander_current_ack"] = CURRENT_ACK
        self.policy.prepare_arguments("file_copy", base)

    def test_overwrite_requires_ack(self) -> None:
        args = {
            "ondup": "overwrite",
            "filelist": [
                {
                    "path": "/OLEANDER_VAULT/A/a.pdf",
                    "dest": "/OLEANDER_VAULT/B",
                    "newname": "a.pdf",
                }
            ],
        }
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments("file_copy", args)
        args["oleander_overwrite_ack"] = OVERWRITE_ACK
        self.policy.prepare_arguments("file_copy", args)

    def test_delete_disabled_by_default_even_with_ack(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments(
                "file_del",
                {
                    "filelist": ["/OLEANDER_VAULT/PROJECTS/C01/REVIEW/a.pdf"],
                    "oleander_delete_ack": DELETE_ACK,
                },
            )

    def test_delete_string_filelist_path_guard(self) -> None:
        policy = StoragePolicy(root="/OLEANDER_VAULT", allow_delete=True, allow_share=False)
        with self.assertRaises(PolicyError):
            policy.prepare_arguments(
                "file_del",
                {"filelist": ["/outside/a.pdf"], "oleander_delete_ack": DELETE_ACK},
            )

    def test_delete_current_needs_both_acks(self) -> None:
        policy = StoragePolicy(root="/OLEANDER_VAULT", allow_delete=True, allow_share=False)
        args = {
            "filelist": ["/OLEANDER_VAULT/PROJECTS/C01/CURRENT/a.pdf"],
            "oleander_delete_ack": DELETE_ACK,
        }
        with self.assertRaises(PolicyError):
            policy.prepare_arguments("file_del", args)
        args["oleander_current_ack"] = CURRENT_ACK
        policy.prepare_arguments("file_del", args)

    def test_remote_upload_generic_name_is_allowed_and_rooted(self) -> None:
        args = self.policy.prepare_arguments("file_upload_from_text", {"content": "hello"})
        self.assertEqual(args["dir"], "/OLEANDER_VAULT")
        self.assertFalse(self.policy.tool_allowed("file_upload_stdio"))

    def test_current_is_path_segment_not_substring(self) -> None:
        self.assertTrue(has_current_segment("/OLEANDER_VAULT/P/CURRENT/a.dwg"))
        self.assertFalse(has_current_segment("/OLEANDER_VAULT/P/CURRENTIZE/a.dwg"))

    def test_double_encoded_escape_is_blocked(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments("file_list", {"dir": "/OLEANDER_VAULT/%252e%252e/outside"})

    def test_newname_cannot_smuggle_path(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments(
                "file_rename",
                {
                    "filelist": [
                        {
                            "path": "/OLEANDER_VAULT/PROJECTS/C01/REVIEW/a.pdf",
                            "newname": "../CURRENT/a.pdf",
                        }
                    ]
                },
            )

    def test_upload_filename_must_be_leaf(self) -> None:
        with self.assertRaises(PolicyError):
            self.policy.prepare_arguments(
                "file_upload_by_url",
                {
                    "url": "https://example.invalid/a.pdf",
                    "dir": "/OLEANDER_VAULT/PROJECTS/C01/REVIEW",
                    "filename": "../CURRENT/a.pdf",
                },
            )


if __name__ == "__main__":
    unittest.main()

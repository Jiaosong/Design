#!/usr/bin/env python3
"""v0.8 wrapper: run v0.7 corpus logic against verified historical Parquet revisions.

The current dataset `main` points to raw JSON config paths, while the verified
Home_and_Kitchen Parquet conversions were committed in April 2025. This wrapper
pins metadata and review downloads to commits where those Parquet files are
known to exist.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve().parent
BASE = HERE / "ar23_failure_value_official_parquet_v0_7.py"
SPEC = importlib.util.spec_from_file_location("ar23_v07", BASE)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)

# Tree d0a7621 contains raw_meta_Home_and_Kitchen; review commit 9370d41 is the
# verified commit that added all 45 raw_review_Home_and_Kitchen Parquet shards.
META_REVISION = "d0a762100fdcf7e420bab24f4bb9179876a0222f"
REVIEW_REVISION = "9370d41ccfddad9c9d278103516263bfc3bbb01b"


def pinned_download(path: str):
    if path.startswith("raw_meta_Home_and_Kitchen/"):
        revision = META_REVISION
    elif path.startswith("raw_review_Home_and_Kitchen/"):
        revision = REVIEW_REVISION
    else:
        raise ValueError(path)
    return hf_hub_download(
        repo_id=mod.DATASET,
        filename=path,
        repo_type="dataset",
        revision=revision,
    )

mod.dl = pinned_download

if __name__ == "__main__":
    mod.main()

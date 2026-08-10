#!/usr/bin/env python3
"""Offline structural regression for the SP02 GHX fixture builder.

This test proves only that the generated GHX contains the locked runtime-report script.
It does NOT execute Rhino/Grasshopper and must never be used to promote CP2.
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

PYTHON3_COMPONENT_GUID = "719467e6-7cf5-4848-99b0-c5dd57e5442c"


def direct_item(chunk: ET.Element, name: str):
    items = chunk.find("items")
    if items is None:
        return None
    for item in items.findall("item"):
        if item.get("name") == name:
            return item
    return None


def direct_chunk(parent: ET.Element, name: str):
    chunks = parent.find("chunks")
    if chunks is None:
        return None
    for chunk in chunks.findall("chunk"):
        if chunk.get("name") == name:
            return chunk
    return None


def extract_script(ghx: Path) -> str:
    root = ET.parse(ghx).getroot()
    definition = direct_chunk(root, "Definition")
    if definition is None:
        raise AssertionError("Definition missing")
    objects = direct_chunk(definition, "DefinitionObjects")
    if objects is None:
        raise AssertionError("DefinitionObjects missing")
    chunks = objects.find("chunks")
    if chunks is None:
        raise AssertionError("object chunks missing")

    matches = []
    for obj in chunks.findall("chunk"):
        guid = direct_item(obj, "GUID")
        if guid is None or (guid.text or "").lower() != PYTHON3_COMPONENT_GUID:
            continue
        container = direct_chunk(obj, "Container")
        if container is None:
            continue
        for chunk in container.findall(".//chunk"):
            if chunk.get("name") != "Script":
                continue
            text = direct_item(chunk, "Text")
            if text is not None and text.text:
                decoded = base64.b64decode(text.text).decode("utf-8")
                if "OLEANDER-SP02-HEADLESS-REPORT-v1" in decoded:
                    matches.append(decoded)
    if len(matches) != 1:
        raise AssertionError(f"expected one OLEANDER SP02 runtime script, found {len(matches)}")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--builder", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        ghx = td_path / "sp02_runtime_neutral.ghx"
        source = td_path / "source.ghx"
        subprocess.run([
            sys.executable,
            args.builder,
            "--output", str(ghx),
            "--source-copy", str(source),
        ], check=True)
        script = extract_script(ghx)

        required_fragments = [
            "OLEANDER-SP02-HEADLESS-REPORT-v1",
            "OLEANDER_SP02_REPORT::",
            "OLEANDER_SP02_REPORT_PATH",
            "OLEANDER_RUNTIME_ENGINE",
            "GH_Structure",
            "GH_GraftMode.GraftAll",
            "flatten.Flatten()",
            "TRANSPOSE_BY_ITEM",
            '"cp4": "OPEN_HEADLESS_NO_GUI"',
        ]
        missing = [fragment for fragment in required_fragments if fragment not in script]
        if missing:
            raise AssertionError(f"missing embedded fragments: {missing}")

        result = {
            "test_id": "OLEANDER-SP02-RUNTIME-NEUTRAL-FIXTURE-REGRESSION-v0.1",
            "fixture_generated": ghx.exists(),
            "source_fixture_downloaded": source.exists(),
            "embedded_runtime_script_found": True,
            "runtime_report_path_contract_found": "OLEANDER_SP02_REPORT_PATH" in script,
            "runtime_engine_contract_found": "OLEANDER_RUNTIME_ENGINE" in script,
            "exact_fragments_missing": missing,
            "runtime_executed": False,
            "runtime_evidence": False,
            "cp2": "OPEN",
            "cp4": "OPEN",
            "evidence_level": "RECONSTRUCTABLE_FIXTURE_REGRESSION_ONLY"
        }

    receipt_path = Path(args.receipt)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

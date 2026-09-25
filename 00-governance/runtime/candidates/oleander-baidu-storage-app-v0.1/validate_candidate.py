from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[4]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []

    required = [
        "README.md",
        "INSTALL_CHATGPT.md",
        "COS_LOCAL_UPLOAD.md",
        "OLEANDER_BAIDU_STORAGE_PROTOCOL_v0.1.md",
        "CANDIDATE_MANIFEST_v0.1.json",
        "app/server.py",
        "app/policy.py",
        "app/upstream.py",
        "schemas/oleander-baidu-storage-binding.v0.1.schema.json",
        "plugin-v0.1.0-candidate/skill.md",
        "plugin-v0.1.0-candidate/references/storage.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            fail(f"MISSING:{rel}", failures)

    env_file = ROOT / ".env"
    if env_file.exists():
        fail("SECRET_FILE_FORBIDDEN:.env", failures)

    candidate = json.loads((ROOT / "CANDIDATE_MANIFEST_v0.1.json").read_text(encoding="utf-8-sig"))
    if candidate.get("status") != "CANDIDATE_NOT_CURRENT_NOT_PROMOTED":
        fail("CANDIDATE_STATUS_DRIFT", failures)
    if candidate.get("storage_root_default") != "/OLEANDER_VAULT":
        fail("STORAGE_ROOT_DRIFT", failures)
    forbidden_owns = {
        "PROJECT_STATE",
        "CURRENT_AUTHORITY",
        "ARTIFACT_REGISTRY",
        "DESIGN_KEEP",
        "PROMOTION",
        "KNOWLEDGE_KI_OE",
    }
    owns = set(candidate.get("owns", []))
    overlap = sorted(owns & forbidden_owns)
    if overlap:
        fail(f"SHADOW_AUTHORITY_OWNERSHIP:{overlap}", failures)

    schema = json.loads(
        (ROOT / "schemas/oleander-baidu-storage-binding.v0.1.schema.json").read_text(encoding="utf-8-sig")
    )
    sample = {
        "schema_version": "0.1",
        "artifact_id": "ART-TEST-001",
        "project_id": "PRJ-TEST",
        "artifact_revision": "v001",
        "owner_native_sha256": "0" * 64,
        "provider": "BAIDU_NETDISK",
        "replica": {
            "fsid": 123,
            "path": "/OLEANDER_VAULT/PROJECTS/PRJ-TEST/REVIEW/a.pdf",
            "provider_md5": "0" * 32,
            "size_bytes": 1,
            "storage_class": "REVIEW"
        },
        "availability": "REMOTE_READY",
        "readback_state": "PROVIDER_META_PASS",
        "authority_effect": "NONE",
        "does_not_prove": ["DESIGN_KEEP"]
    }
    errors = list(Draft202012Validator(schema).iter_errors(sample))
    if errors:
        fail("STORAGE_BINDING_SCHEMA_SAMPLE_FAIL:" + ";".join(e.message for e in errors), failures)

    test = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if test.returncode != 0:
        fail("UNIT_TEST_FAIL:" + (test.stdout + test.stderr).strip(), failures)

    package_manifest_path = ROOT / "PACKAGE_MANIFEST_v0.1.json"
    if package_manifest_path.exists():
        package_manifest = json.loads(package_manifest_path.read_text(encoding="utf-8-sig"))
        for package in package_manifest.get("packages", []):
            path = ROOT / package["filename"]
            if not path.exists():
                fail(f"PACKAGE_MISSING:{package['filename']}", failures)
                continue
            if sha256(path) != package.get("sha256"):
                fail(f"PACKAGE_HASH_MISMATCH:{package['filename']}", failures)
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                if any("__pycache__" in n or n.endswith(".pyc") or n.endswith("/.env") or n == ".env" for n in names):
                    fail(f"PACKAGE_FORBIDDEN_CONTENT:{package['filename']}", failures)

    # Guard against accidental direct Current/Project State write integration.
    code_text = "\n".join(
        p.read_text(encoding="utf-8-sig", errors="replace")
        for p in (ROOT / "app").glob("*.py")
    ).lower()
    forbidden_integrations = [
        "project_state_write",
        "design_keep=true",
        "promotion=true",
    ]
    for token in forbidden_integrations:
        if token in code_text:
            fail(f"FORBIDDEN_AUTHORITY_INTEGRATION:{token}", failures)

    if failures:
        print(f"FAIL: OLEANDER Baidu Storage candidate; failures={len(failures)}")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PASS: OLEANDER Baidu Storage candidate structural/policy validation")
    print("does_not_prove: BAIDU_AUTH / CHATGPT_ACCOUNT_INSTALL / CURRENT / DESIGN_KEEP / PROMOTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
        "INSTALL_LOCAL.md",
        "COS_LOCAL_UPLOAD.md",
        "LOCAL_RUNTIME_RECEIPT_v0.1.json",
        "OLEANDER_BAIDU_STORAGE_PROTOCOL_v0.1.md",
        "CANDIDATE_MANIFEST_v0.1.json",
        "app/server.py",
        "app/policy.py",
        "app/upstream.py",
        "schemas/oleander-baidu-storage-binding.v0.1.schema.json",
        "plugin-v0.1.1-candidate/plugin.json",
        "plugin-v0.1.1-candidate/.codex-plugin/plugin.json",
        "plugin-v0.1.1-candidate/mcp.json",
        "plugin-v0.1.1-candidate/runtime/stdio_entry.py",
        "plugin-v0.1.1-candidate/runtime/run_stdio_secure.ps1",
        "plugin-v0.1.1-candidate/skills/oleander-baidu-storage/SKILL.md",
        "plugin-v0.1.1-candidate/skills/oleander-baidu-storage/references/storage.md",
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

    plugin_root = ROOT / "plugin-v0.1.1-candidate"
    plugin_manifest = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8-sig"))
    if plugin_manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        fail("PLUGIN_PORTABLE_SCHEMA_DRIFT", failures)
    if plugin_manifest.get("name") != "oleander-baidu-storage":
        fail("PLUGIN_NAME_DRIFT", failures)
    if plugin_manifest.get("version") != "0.1.1":
        fail("PLUGIN_VERSION_DRIFT", failures)

    skill_text = (
        plugin_root / "skills/oleander-baidu-storage/SKILL.md"
    ).read_text(encoding="utf-8-sig")
    if "name: oleander-baidu-storage" not in skill_text:
        fail("PLUGIN_SKILL_IDENTITY_DRIFT", failures)

    # The selected local binding is stdio. Never package access tokens or
    # placeholder secrets into the portable plugin.
    portable_mcp = plugin_root / "mcp.json"
    if portable_mcp.exists():
        mcp_config = json.loads(portable_mcp.read_text(encoding="utf-8-sig"))
        serialized = json.dumps(mcp_config, ensure_ascii=False)
        lowered = serialized.lower()
        if "<" in serialized:
            fail("PLUGIN_MCP_PLACEHOLDER_FORBIDDEN", failures)
        if "access_token=" in lowered or "baidu_netdisk_access_token" in lowered:
            fail("PLUGIN_MCP_SECRET_FORBIDDEN", failures)
        servers = mcp_config.get("mcpServers", {})
        if not isinstance(servers, dict) or not servers:
            fail("PLUGIN_MCP_SERVER_MISSING", failures)
        for name, config in servers.items():
            if not isinstance(config, dict):
                fail(f"PLUGIN_MCP_SERVER_INVALID:{name}", failures)
                continue
            if config.get("type") not in {"stdio", "http", "streamable-http"}:
                fail(f"PLUGIN_MCP_TRANSPORT_INVALID:{name}", failures)
            if config.get("type") == "stdio":
                if config.get("command") != "powershell.exe":
                    fail(f"PLUGIN_MCP_STDIO_COMMAND_INVALID:{name}", failures)
                args = config.get("args", [])
                if "${PLUGIN_ROOT}/runtime/run_stdio_secure.ps1" not in args:
                    fail(f"PLUGIN_MCP_STDIO_WRAPPER_MISSING:{name}", failures)
            else:
                url = str(config.get("url", ""))
                selected_loopback = url == "http://127.0.0.1:9823/mcp"
                selected_remote = url.startswith("https://") and url.rstrip("/").endswith("/mcp")
                if not (selected_loopback or selected_remote):
                    fail(f"PLUGIN_MCP_URL_INVALID:{name}", failures)

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
                if package.get("role") == "CHATGPT_PLUGIN_PACKAGE":
                    required_plugin_entries = {
                        "plugin.json",
                        "mcp.json",
                        ".codex-plugin/plugin.json",
                        "runtime/stdio_entry.py",
                        "runtime/run_stdio_secure.ps1",
                        "runtime/app/server.py",
                        "runtime/app/policy.py",
                        "runtime/app/upstream.py",
                        "runtime/app/result_filter.py",
                        "skills/oleander-baidu-storage/SKILL.md",
                        "skills/oleander-baidu-storage/references/storage.md",
                    }
                    missing = sorted(required_plugin_entries - set(names))
                    if missing:
                        fail(f"PLUGIN_PACKAGE_STRUCTURE_MISSING:{missing}", failures)

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
    print("does_not_prove: CURRENT / PROJECT_STATE / DESIGN_KEEP / PROMOTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

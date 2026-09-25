from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
APP_ZIP = ROOT / "OLEANDER-Baidu-Storage-App-0.1.0-CANDIDATE.zip"
PLUGIN_ZIP = ROOT / "OLEANDER-Baidu-Storage-Plugin-0.1.0-CANDIDATE.zip"
PACKAGE_MANIFEST = ROOT / "PACKAGE_MANIFEST_v0.1.json"


APP_INCLUDE = [
    "README.md",
    "INSTALL_CHATGPT.md",
    "OPENAI_TUNNEL.md",
    "COS_LOCAL_UPLOAD.md",
    "OLEANDER_BAIDU_STORAGE_PROTOCOL_v0.1.md",
    "CANDIDATE_MANIFEST_v0.1.json",
    "THIRD_PARTY_NOTICES.md",
    ".env.example",
    "requirements.txt",
    "Dockerfile",
    "VERCEL_DEPLOY.md",
    "api",
    "run_local.ps1",
    "run_local_secure.ps1",
    "configure_baidu_token.ps1",
    "setup_openai_tunnel.ps1",
    "app",
    "scripts",
    "schemas",
    "tests",
    "validate_candidate.py",
]


def iter_files(entry: Path):
    if entry.is_file():
        yield entry
    elif entry.is_dir():
        for path in sorted(entry.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            yield path


def build_zip(target: Path, entries: list[str], strip_prefix: Path | None = None) -> tuple[int, int, str]:
    if target.exists():
        target.unlink()
    count = 0
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for entry_name in entries:
            entry = ROOT / entry_name
            if not entry.exists():
                raise FileNotFoundError(entry)
            for path in iter_files(entry):
                base = strip_prefix or ROOT
                arcname = path.relative_to(base).as_posix()
                zf.write(path, arcname)
                count += 1
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return count, target.stat().st_size, digest


def main() -> int:
    app_count, app_size, app_sha = build_zip(APP_ZIP, APP_INCLUDE)
    plugin_root = ROOT / "plugin-v0.1.0-candidate"
    plugin_files = [str(p.relative_to(ROOT)) for p in sorted(plugin_root.rglob("*")) if p.is_file()]
    plugin_count, plugin_size, plugin_sha = build_zip(
        PLUGIN_ZIP, plugin_files, strip_prefix=plugin_root
    )

    manifest = {
        "schema": "oleander.baidu-storage-package-manifest.v0.1",
        "status": "CANDIDATE_PACKAGED",
        "packages": [
            {
                "role": "CHATGPT_MCP_APP_SERVER",
                "filename": APP_ZIP.name,
                "sha256": app_sha,
                "size_bytes": app_size,
                "file_count": app_count,
            },
            {
                "role": "CHATGPT_PLUGIN_PACKAGE",
                "filename": PLUGIN_ZIP.name,
                "sha256": plugin_sha,
                "size_bytes": plugin_size,
                "file_count": plugin_count,
            },
        ],
        "does_not_prove": [
            "PACKAGE_EXISTS_NOT_ACCOUNT_INSTALLATION",
            "PACKAGE_EXISTS_NOT_BAIDU_AUTH",
            "PACKAGE_EXISTS_NOT_CURRENT_PROMOTION",
        ],
    }
    PACKAGE_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

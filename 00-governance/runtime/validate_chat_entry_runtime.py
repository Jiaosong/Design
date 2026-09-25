from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENTRY = HERE / "OLEANDER_CHAT_ENTRY_RUNTIME.md"
BINDER = HERE / "bind_chat_on_steroids_oleander.py"


def _load_binder():
    spec = importlib.util.spec_from_file_location("oleander_chat_binder", BINDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("BINDER_IMPORT_SPEC_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    failures: list[str] = []
    if not ENTRY.is_file():
        failures.append("CHAT_ENTRY_MISSING")
        entry = ""
    else:
        entry = ENTRY.read_text(encoding="utf-8-sig")

    required_entry_text = [
        "Chat by default",
        "CONVERSATION_SURFACE != EXECUTION_SURFACE != MUTATION_PERMISSION",
        "00-governance/runtime/oleander_chat_runtime_bridge.py",
        "codesign_chat_cos_bridge_v0_1.py",
        "oleander-baidu-storage@oleander-personal 0.1.1",
        "EXECUTION INTENT != MUTATION PERMISSION",
        "Do not rewrite the CoS config or require a CoS restart for ordinary OLEANDER runtime updates.",
        "validate_cos_update_compatibility.py",
        "must not block the CoS updater",
    ]
    for text in required_entry_text:
        if text not in entry:
            failures.append(f"CHAT_ENTRY_REQUIRED_TEXT_MISSING:{text}")

    referenced_paths = [
        HERE / "oleander_chat_runtime_bridge.py",
        HERE / "candidates" / "human-ai-codesign-vnext" / "codesign_chat_cos_bridge_v0_1.py",
    ]
    for path in referenced_paths:
        if not path.exists():
            failures.append(f"CHAT_ENTRY_REFERENCED_RUNTIME_MISSING:{path.relative_to(HERE.parents[1]).as_posix()}")

    binder = _load_binder()
    if binder.BINDING_REVISION != "OLEANDER_CHAT_RESOLVER_BINDING_v1.6":
        failures.append(f"BINDER_REVISION_UNEXPECTED:{binder.BINDING_REVISION}")
    if "OLEANDER_CHAT_ENTRY_RUNTIME.md" not in binder.MAIN_CHAT_BINDING:
        failures.append("BINDER_DOES_NOT_POINT_TO_DYNAMIC_CHAT_ENTRY")
    if "codesign_chat_cos_bridge_v0_1.py" in binder.MAIN_CHAT_BINDING:
        failures.append("BINDER_MUST_NOT_HARD_CODE_CAPABILITY_IMPLEMENTATION")
    if "oleander-baidu-storage@oleander-personal" in binder.MAIN_CHAT_BINDING:
        failures.append("BINDER_MUST_NOT_HARD_CODE_BAIDU_ADAPTER")
    if len(binder.MAIN_CHAT_BINDING) > binder.MAX_MCP_INSTRUCTIONS_CHARS:
        failures.append("BINDER_MAIN_BLOCK_EXCEEDS_MCP_LIMIT")

    if failures:
        print(f"FAIL: Chat runtime entry; failures={len(failures)}")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        "PASS: Chat runtime entry is hot-updatable; "
        "CoS bootstrap=v1.6; capability implementations remain outside bootstrap"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

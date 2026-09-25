from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HOME = HERE / "OLEANDER_HOME_INDEX_v0.1.json"
HOME_SCHEMA = HERE / "schemas" / "oleander-home-index.v0.1.schema.json"
SESSION_SCHEMA = HERE / "schemas" / "oleander-session-receipt.v0.1.schema.json"
INTENT_SCHEMA = HERE / "schemas" / "oleander-execution-intent.v0.1.schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_schema(instance: dict, schema_path: Path, label: str, failures: list[str]) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(instance), key=lambda x: list(x.absolute_path)):
        path = ".".join(str(x) for x in error.absolute_path) or "<root>"
        failures.append(f"{label}:SCHEMA:{path}:{error.message}")


def resolve_ref(ref: str) -> Path:
    return ROOT / ref


def require_ref(ref: str, label: str, failures: list[str]) -> None:
    if not resolve_ref(ref).exists():
        failures.append(f"{label}:MISSING_REF:{ref}")


def walk_keys(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            yield key, child_path
            yield from walk_keys(child, child_path)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk_keys(child, f"{path}[{idx}]")


def main() -> int:
    failures: list[str] = []
    home = load_json(HOME)
    validate_schema(home, HOME_SCHEMA, "HOME", failures)

    # HOME must stay a thin locator/attention projection. These keys would turn it
    # into a shadow Project State, Control Card, checkpoint store or promotion surface.
    forbidden_home_keys = {
        "current_native_master",
        "current_owner",
        "next_action",
        "locked_variables",
        "open_variables",
        "checkpoint_sequence",
        "design_keep",
        "promotion_status",
        "project_state",
        "artifact_registry",
        "professional_verdict",
        "professional_stage",
    }
    for key, path in walk_keys(home):
        if key.lower() in forbidden_home_keys:
            failures.append(f"HOME:SHADOW_AUTHORITY_FIELD_FORBIDDEN:{path}")

    for ref in home.get("source_refs", {}).values():
        require_ref(ref, "HOME_SOURCE", failures)
    require_ref(home["knowledge"]["runtime_mount_ref"], "HOME_KNOWLEDGE", failures)
    require_ref(home["knowledge"]["content_review_ref"], "HOME_KNOWLEDGE", failures)

    projects = home.get("formal_projects", [])
    project_ids = [x["project_id"] for x in projects]
    case_ids = [x["case_id"] for x in projects]
    if len(project_ids) != len(set(project_ids)):
        failures.append("HOME:DUPLICATE_PROJECT_ID")
    if len(case_ids) != len(set(case_ids)):
        failures.append("HOME:DUPLICATE_CASE_ID")

    active_projects = [x for x in projects if x["attention_state"] == "ACTIVE"]
    soft_limit = home["attention_policy"]["formal_active_soft_limit"]
    if len(active_projects) > soft_limit:
        failures.append(f"HOME:ACTIVE_FORMAL_PROJECTS_EXCEED_SOFT_LIMIT:{len(active_projects)}>{soft_limit}")

    queue = load_json(resolve_ref(home["source_refs"]["project_priority_queue"]))
    queued_ids = {x.get("project_id") for x in queue.get("entries", [])}
    for project in projects:
        require_ref(project["workspace_ref"], f"PROJECT:{project['project_id']}", failures)
        for ref in project["authority_refs"]:
            require_ref(ref, f"PROJECT:{project['project_id']}", failures)
        if project["control_card_ref"]:
            require_ref(project["control_card_ref"], f"PROJECT:{project['project_id']}", failures)
        if project["attention_basis"].startswith("PRESENT_IN_CURRENT_PROJECT_PRIORITY_QUEUE") and project["project_id"] not in queued_ids:
            failures.append(f"HOME:ATTENTION_BASIS_QUEUE_MISMATCH:{project['project_id']}")

    for workspace in home.get("unregistered_workspaces", []):
        if workspace.get("registration_state") == "CANONICAL_PROJECT_CARRIER_UNRESOLVED" and workspace.get("canonical_project_state_ref") is not None:
            failures.append(f"HOME:UNRESOLVED_WORKSPACE_CANNOT_ASSERT_PROJECT_STATE:{workspace['workspace_key']}")
        for ref in workspace.get("evidence_refs", []):
            require_ref(ref, f"UNREGISTERED:{workspace['workspace_key']}", failures)

    for workspace in home.get("system_workspaces", []):
        if workspace.get("candidate_ref"):
            require_ref(workspace["candidate_ref"], f"SYSTEM:{workspace['workspace_key']}", failures)
        require_ref(workspace["current_authority_ref"], f"SYSTEM:{workspace['workspace_key']}", failures)

    session_refs = home.get("session_receipt_refs", [])
    intent_refs = home.get("execution_intent_refs", [])
    session_docs: dict[str, dict] = {}
    intent_docs: dict[str, dict] = {}

    for ref in session_refs:
        require_ref(ref, "SESSION_INDEX", failures)
        path = resolve_ref(ref)
        if not path.exists():
            continue
        doc = load_json(path)
        validate_schema(doc, SESSION_SCHEMA, f"SESSION:{ref}", failures)
        session_docs[ref] = doc
        if doc.get("authority_effect") == "NONE" and doc.get("owner_native_writes"):
            failures.append(f"SESSION:AUTHORITY_NONE_WITH_OWNER_NATIVE_WRITES:{ref}")
        for record in doc.get("owner_native_reads", []):
            require_ref(record["ref"], f"SESSION_READ:{ref}", failures)
        for record in doc.get("material_outputs", []):
            require_ref(record["ref"], f"SESSION_OUTPUT:{ref}", failures)

    for ref in intent_refs:
        require_ref(ref, "INTENT_INDEX", failures)
        path = resolve_ref(ref)
        if not path.exists():
            continue
        doc = load_json(path)
        validate_schema(doc, INTENT_SCHEMA, f"INTENT:{ref}", failures)
        intent_docs[ref] = doc
        for authority_ref in doc.get("owner_native_precondition", {}).get("authority_refs", []):
            require_ref(authority_ref, f"INTENT_AUTHORITY:{ref}", failures)
        if doc.get("scope", {}).get("project_id") and doc.get("material_write_authorized"):
            pre = doc.get("owner_native_precondition", {})
            if pre.get("reread_required") is not True or not pre.get("authority_refs"):
                failures.append(f"INTENT:PROJECT_WRITE_WITHOUT_OWNER_REREAD:{ref}")

    for ref, intent in intent_docs.items():
        consumed = intent.get("consumed_by_session_receipt")
        if intent.get("status") == "CONSUMED":
            if not consumed or consumed not in session_docs:
                failures.append(f"INTENT:CONSUMED_WITHOUT_INDEXED_SESSION:{ref}")
            elif ref not in session_docs[consumed].get("execution_intents_consumed", []):
                failures.append(f"INTENT:SESSION_BACKLINK_MISSING:{ref}")

    # A session receipt is transport evidence only. It may not silently become the
    # current automated project-production queue.
    if HOME.name == Path(home["source_refs"]["project_priority_queue"]).name:
        failures.append("HOME:MUST_NOT_REPLACE_PROJECT_PRIORITY_QUEUE")

    if failures:
        print(f"FAIL: continuity management; failures={len(failures)}")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PASS: continuity management; "
        f"formal_projects={len(projects)} active={len(active_projects)} "
        f"unregistered={len(home.get('unregistered_workspaces', []))} "
        f"sessions={len(session_docs)} intents={len(intent_docs)}; "
        "HOME=POINTERS_ONLY"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


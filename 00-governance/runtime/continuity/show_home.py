from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
HOME = HERE / "OLEANDER_HOME_INDEX_v0.1.json"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads(HOME.read_text(encoding="utf-8-sig"))
    projects = data["formal_projects"]
    active = [p for p in projects if p["attention_state"] == "ACTIVE"]
    parked = [p for p in projects if p["attention_state"] == "PARKED"]
    archived = [p for p in projects if p["attention_state"] == "ARCHIVED"]

    print("OLEANDER HOME — NON-AUTHORITY OPERATOR VIEW")
    print(f"status: {data['status']}")
    print()
    print(f"ACTIVE FORMAL PROJECTS ({len(active)}):")
    for p in active:
        card = p["control_card_ref"] or "owner-native project carrier; no HOME-owned card"
        print(f"  - {p['project_id']} | {p['display_name']} | {card}")
    print()
    print(f"PARKED ({len(parked)}):")
    for p in parked:
        print(f"  - {p['project_id']} | {p['display_name']}")
    if archived:
        print()
        print(f"ARCHIVED ({len(archived)}):")
        for p in archived:
            print(f"  - {p['project_id']} | {p['display_name']}")
    print()
    print("UNREGISTERED / EXTERNAL WORKSPACES:")
    for w in data["unregistered_workspaces"]:
        print(f"  - {w['workspace_key']} | {w['attention_state']} | {w['registration_state']}")
    print()
    print("SYSTEM WORKSPACES:")
    for w in data["system_workspaces"]:
        print(f"  - {w['workspace_key']} | {w['attention_state']} | {w['kind']}")
    print()
    print("SURFACES:")
    for s in data["surfaces"]:
        local = "LOCAL_EXEC" if s["can_execute_local_tools"] else "NO_LOCAL_EXEC"
        print(f"  - {s['surface_id']} | {local} | {s['role']}")
    print()
    print(f"session receipts: {len(data['session_receipt_refs'])}")
    print(f"execution intents: {len(data['execution_intent_refs'])}")
    print("authority: POINTERS_ONLY; reread owner-native carriers before consequential work")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

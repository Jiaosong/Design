from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path


GENERATED_AT = "2026-09-22T15:10:00+08:00"
MAIN_COMMIT = "ab83fde14d0b341f373098e789be93cd527465ef"
ARCHITECTURE_REF = "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md"
MASTER_RUNTIME_REF = "00-governance/complex-project-master-runtime-v1.0.md"
REPO_ROOT = Path(__file__).resolve().parents[4]
DOES_NOT_PROVE = [
    "CURRENT_ADOPTION",
    "DESIGN_KEEP",
    "PROFESSIONAL_PASS",
    "PROJECT_PROMOTION",
    "STATUTORY_APPROVAL",
    "KNOWLEDGE_CURRENT",
    "REAL_CASE_GENERALIZATION",
    "ENTERPRISE_COMPLETENESS",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def canonical_text_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def digest(path: Path, semantics: str) -> str:
    payload = path.read_bytes() if semantics == "RAW_BYTES_V1" else canonical_text_bytes(path)
    return hashlib.sha256(payload).hexdigest().upper()


def build_source_rows(source_specs: list[tuple[str, Path, str, str]]) -> list[dict]:
    rows = []
    for ref, path, availability, semantics in source_specs:
        if not path.is_file():
            raise FileNotFoundError(path)
        if semantics == "GIT_CANONICAL_BLOB_SHA256":
            rel = path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
            payload = subprocess.check_output(["git", "show", f"{MAIN_COMMIT}:{rel}"], cwd=REPO_ROOT)
            sha256 = hashlib.sha256(payload).hexdigest().upper()
            byte_count = len(payload)
        else:
            sha256 = digest(path, semantics)
            byte_count = path.stat().st_size
        rows.append(
            {
                "ref": ref,
                "path": str(path),
                "availability": availability,
                "hash_semantics": semantics,
                "sha256": sha256,
                "bytes": byte_count,
            }
        )
    return rows


def header(module: str, scope: str, source_refs: list[str], boundaries: list[str]) -> dict:
    return {
        "module": module,
        "scope_state": scope,
        "authority_mode": "PROJECTION_ONLY",
        "source_refs": source_refs,
        "does_not_prove": sorted(set(boundaries)),
    }


def base_projection(template_path: Path, case_key: str, source_rows: list[dict]) -> dict:
    doc = copy.deepcopy(load_json(template_path))
    source_refs = [row["ref"] for row in source_rows]
    doc["schema_version"] = "0.3.1-candidate"
    doc["kind"] = "OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION"
    doc["candidate_status"] = "EVAL_ONLY"
    doc["generated_at"] = GENERATED_AT
    doc["authority"].update(
        {
            "architecture_ref": ARCHITECTURE_REF,
            "master_runtime_ref": MASTER_RUNTIME_REF,
            "authority_snapshot_ref": f"EV3:{case_key}:AUTHORITY_SNAPSHOT",
            "knowledge_snapshot_ref": f"EV3:{case_key}:SOURCE_MANIFEST",
            "source_binding_refs": source_refs,
            "source_binding_hash_semantics": "SOURCE_SPECIFIC_EXACT_REVISION_DIGESTS_WHEN_AVAILABLE",
            "projection_only": True,
            "may_mutate_current": False,
            "source_binding_digests": [
                {
                    "ref": row["ref"],
                    "sha256": row["sha256"],
                    "hash_semantics": row["hash_semantics"],
                }
                for row in source_rows
            ],
        }
    )
    doc["case_refs"] = []
    doc["project_axis_refs"] = []
    doc["work_packages"] = []
    doc["jobs"] = []
    doc["resource_refs"] = []
    doc["artifact_refs"] = []
    doc["review_refs"] = []
    doc["activity_observations"] = []
    doc["digital_thread"] = {"relations": [], "trace_queries": [], "unresolved_links": []}
    doc["state_facets"] = {key: {} for key in doc["state_facets"]}
    doc["does_not_prove"] = sorted(set(DOES_NOT_PROVE))
    return doc


def finish_projection(doc: dict) -> dict:
    states = [module["header"]["scope_state"] for module in doc["modules"].values()]
    counts = {state: states.count(state) for state in ["TRIGGERED", "PARTIAL", "NOT_TRIGGERED", "HOLD"]}
    blocking_links = sum(1 for row in doc["digital_thread"]["unresolved_links"] if row.get("blocking"))
    design_results = {
        review.get("result")
        for review in doc["review_refs"]
        if review.get("review_class") == "DESIGN"
    }
    readiness = "READY_FOR_EVALUATION"
    if counts["HOLD"] or blocking_links or design_results & {"REVISE", "REJECT", "HOLD", "FAIL"}:
        readiness = "HOLD"
    elif counts["PARTIAL"] or counts["NOT_TRIGGERED"]:
        readiness = "PARTIAL"
    doc["reconciliation"] = {
        "projection_freshness_state": "SOURCE_READBACK_CURRENT",
        "enterprise_readiness_state": readiness,
        "drift_state": "CURRENT",
        "source_readback_refs": list(doc["authority"]["source_binding_refs"]),
        "partial_side_effect_state": "NONE",
        "reconciliation_actions": ["RUN_ENTERPRISE_KERNEL_V0_1_1_RECONCILIATION"],
        "advance_allowed": False,
    }
    doc["control_metrics"] = {
        "authority_duplication_count": 0,
        "state_family_flattening_count": 0,
        "untraceable_relation_count": 0,
        "unresolved_blocking_link_count": blocking_links,
        "module_source_binding_coverage": 1.0,
        "module_triggered_coverage": counts["TRIGGERED"] / 8,
        "module_scope_counts": counts,
        "projection_rebuildable": True,
    }
    return doc

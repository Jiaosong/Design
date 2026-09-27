from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_environment_resolver import build_current_execution_view, resolve_execution_surface  # noqa: E402
from oleander_surface_reliability import (  # noqa: E402
    assess_result_reliability,
    build_preflight_reliability,
    identity_revision_changed,
)


def observation(stage: str, dimension: str, fact: str = "PASS", n: int = 1, observed_at: str | None = None) -> dict:
    return {
        "observation_id": f"obs-{stage}-{dimension}-{n}",
        "surface_instance_id": "github:jiaosong",
        "stage": stage,
        "dimension": dimension,
        "fact": fact,
        "source_kind": "LIVE_PROBE",
        "observed_at": observed_at or datetime.now(timezone.utc).isoformat(),
    }


def complete_preflight() -> list[dict]:
    dims = {
        "R1_ADMISSION": ["registered", "configured", "version_compatible", "loaded"],
        "R2_IDENTITY": ["authenticated", "identity_bound", "permission_scope_verified", "credential_freshness"],
        "R3_CAPABILITY": ["catalog_valid", "capability_verified", "required_feature_present"],
        "R4_EXECUTION": ["provider_health", "capacity_state", "request_admission", "side_effect_certainty"],
    }
    return [observation(stage, dimension) for stage, dimensions in dims.items() for dimension in dimensions]


class SurfaceReliabilityBoundaryTests(unittest.TestCase):
    def test_strict_r1_r4_vector_can_be_ready_without_fabricating_r5(self) -> None:
        result = build_preflight_reliability({"reliability_observations": complete_preflight()})
        self.assertEqual("READY", result["status"])
        self.assertTrue(result["strict_vector"])
        self.assertIn("R5_RESULT", result["does_not_prove"])

    def test_missing_required_dimension_keeps_preflight_unknown(self) -> None:
        rows = complete_preflight()
        rows = [x for x in rows if x["dimension"] != "credential_freshness"]
        result = build_preflight_reliability({"reliability_observations": rows})
        self.assertEqual("UNKNOWN", result["status"])
        self.assertIn("credential_freshness", result["stages"]["R2_IDENTITY"]["missing_dimensions"])

    def test_stale_strict_observations_cannot_become_ready(self) -> None:
        stale = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        rows = complete_preflight()
        for row in rows:
            row["observed_at"] = stale
        result = build_preflight_reliability({"reliability_observations": rows})
        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(any(
            "STALE_OBSERVATION" in invalid["errors"]
            for stage in result["stages"].values()
            for invalid in stage["invalid_observations"]
        ))

    def test_identity_revision_change_invalidates_identity_bound_state(self) -> None:
        self.assertTrue(identity_revision_changed(
            {"surface_identity_id": "notion:a", "identity_revision": "1"},
            {"surface_identity_id": "notion:b", "identity_revision": "1"},
        ))
        self.assertTrue(identity_revision_changed(
            {"surface_identity_id": "notion:a", "identity_revision": "1"},
            {"surface_identity_id": "notion:a", "identity_revision": "2"},
        ))

    def test_material_mutation_without_complete_r5_is_partial(self) -> None:
        rows = [
            observation("R5_RESULT", "native_output"),
            observation("R5_RESULT", "actual_delta"),
            observation("R5_RESULT", "semantic_fidelity"),
            observation("R5_RESULT", "source_version_consistency"),
        ]
        result = assess_result_reliability(rows, material_mutation=True)
        self.assertEqual("PARTIAL", result["status"])
        self.assertIn("readback", result["stage"]["missing_dimensions"])

    def test_complete_r5_is_execution_verified_not_design_keep(self) -> None:
        rows = [
            observation("R5_RESULT", "native_output"),
            observation("R5_RESULT", "actual_delta"),
            observation("R5_RESULT", "readback"),
            observation("R5_RESULT", "semantic_fidelity"),
            observation("R5_RESULT", "source_version_consistency"),
        ]
        result = assess_result_reliability(rows, material_mutation=True)
        self.assertEqual("VERIFIED", result["status"])
        self.assertIn("DESIGN_KEEP", result["does_not_prove"])

    def test_strict_identity_failure_blocks_routing_even_when_available(self) -> None:
        rows = complete_preflight()
        for row in rows:
            if row["stage"] == "R2_IDENTITY" and row["dimension"] == "authenticated":
                row["fact"] = "FAIL"
        view = build_current_execution_view(live_observations={
            "github_connector": {
                "availability": "AVAILABLE",
                "reliability_observations": rows,
            }
        })
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "REMOTE_MUTATION",
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", route["status"])

    def test_strict_ready_vector_routes(self) -> None:
        view = build_current_execution_view(live_observations={
            "github_connector": {
                "availability": "AVAILABLE",
                "reliability_observations": complete_preflight(),
            }
        })
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "REMOTE_MUTATION",
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("ROUTED", route["status"])
        self.assertEqual("READY", route["selected_surface"]["reliability_preflight"]["status"])

    def test_stale_compatibility_observation_cannot_route(self) -> None:
        stale = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        view = build_current_execution_view(live_observations={
            "github_connector": {
                "availability": "AVAILABLE",
                "observed_at": stale,
                "observation_source": "LIVE_PROBE",
            }
        })
        surface = next(row for row in view["surfaces"] if row["surface_id"] == "github_connector")
        self.assertEqual("STALE", surface["reliability_preflight"]["status"])
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "REMOTE_MUTATION",
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", route["status"])


if __name__ == "__main__":
    unittest.main()

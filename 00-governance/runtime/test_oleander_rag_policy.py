import unittest

from oleander_rag_policy import (
    CURRENT_NAMESPACE,
    PROVENANCE_NAMESPACE,
    RetrievalIntent,
    authority_gate,
    build_vectorize_filter,
    canonical_collision_gate,
    choose_namespace,
)


BASE = {
    "canonical_id": "KN-METHOD-OLEANDER-3D-MODELING-001",
    "source_locator": "notion://3ccb86be5c4781d2b8c2e3f4ac88a109",
    "retrieval_space": "CURRENT",
    "search_eligibility": "SCOPED",
    "governance_state": "ACTIVE",
    "trust_state": "UNVERIFIED",
    "freshness_state": "FRESH",
    "project_id": "GLOBAL",
    "domain_id": "SPATIAL",
}


class AuthorityAwareRagPolicyTests(unittest.TestCase):
    def test_current_is_legal_without_score(self):
        decision = authority_gate(BASE, RetrievalIntent(domain_id="SPATIAL"))
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.namespace, CURRENT_NAMESPACE)

    def test_provenance_requires_explicit_history_intent(self):
        row = {**BASE, "retrieval_space": "PROVENANCE"}
        normal = authority_gate(row, RetrievalIntent())
        history = authority_gate(row, RetrievalIntent(history_intent=True))
        self.assertFalse(normal.allowed)
        self.assertTrue(history.allowed)
        self.assertEqual(history.namespace, PROVENANCE_NAMESPACE)

    def test_unknown_trust_fails_closed(self):
        row = {**BASE, "trust_state": "UNKNOWN"}
        decision = authority_gate(row, RetrievalIntent())
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "TRUST_UNKNOWN")

    def test_blocked_search_fails_closed(self):
        row = {**BASE, "search_eligibility": "BLOCKED"}
        decision = authority_gate(row, RetrievalIntent())
        self.assertFalse(decision.allowed)
        self.assertIn("SEARCH_NOT_ELIGIBLE", decision.reason)

    def test_missing_source_locator_fails_closed(self):
        row = {**BASE, "source_locator": ""}
        decision = authority_gate(row, RetrievalIntent())
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "MISSING_SOURCE_LOCATOR")

    def test_project_scope_is_enforced(self):
        row = {**BASE, "project_id": "PRJ-X"}
        decision = authority_gate(row, RetrievalIntent(project_id="PRJ-C04"))
        self.assertFalse(decision.allowed)
        self.assertIn("PROJECT_SCOPE_MISMATCH", decision.reason)

    def test_current_collision_is_hard_error(self):
        rows = [BASE, {**BASE, "source_locator": "notion://duplicate"}]
        self.assertEqual(
            canonical_collision_gate(rows),
            ["KN-METHOD-OLEANDER-3D-MODELING-001"],
        )

    def test_support_does_not_share_current_namespace(self):
        self.assertEqual(choose_namespace("CURRENT"), CURRENT_NAMESPACE)
        self.assertNotEqual(choose_namespace("SUPPORT"), CURRENT_NAMESPACE)

    def test_filter_never_adds_support_or_provenance(self):
        filt = build_vectorize_filter(RetrievalIntent(project_id="PRJ-C04"))
        rendered = repr(filt)
        self.assertIn("CURRENT", rendered)
        self.assertNotIn("SUPPORT", rendered)
        self.assertNotIn("PROVENANCE", rendered)


if __name__ == "__main__":
    unittest.main()

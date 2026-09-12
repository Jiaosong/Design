"""OLEANDER Authority-aware RAG policy v0.1.

Derived retrieval infrastructure only. This module MUST NOT promote knowledge,
mutate canonical authority, or treat semantic similarity as an authority signal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


CURRENT_NAMESPACE = "prod-current"
SUPPORT_NAMESPACE = "prod-support"
PROVENANCE_NAMESPACE = "prod-provenance"

ALLOWED_DEFAULT_ELIGIBILITY = frozenset({"DEFAULT", "SCOPED"})
BLOCKED_ELIGIBILITY = frozenset({"BLOCKED", "HISTORY_ONLY"})


@dataclass(frozen=True)
class RetrievalIntent:
    project_id: str | None = None
    domain_id: str | None = None
    history_intent: bool = False
    allow_support_fallback: bool = True
    include_unverified: bool = True


@dataclass(frozen=True)
class AuthorityDecision:
    allowed: bool
    namespace: str | None
    reason: str


def choose_namespace(retrieval_space: str, *, history_intent: bool = False) -> str | None:
    space = (retrieval_space or "UNKNOWN").upper()
    if space == "CURRENT":
        return CURRENT_NAMESPACE
    if space == "SUPPORT":
        return SUPPORT_NAMESPACE
    if space == "PROVENANCE" and history_intent:
        return PROVENANCE_NAMESPACE
    return None


def authority_gate(metadata: Mapping[str, object], intent: RetrievalIntent) -> AuthorityDecision:
    """Fail closed before semantic ranking.

    This function intentionally ignores any vector/semantic score.
    """

    retrieval_space = str(metadata.get("retrieval_space") or "UNKNOWN").upper()
    eligibility = str(metadata.get("search_eligibility") or "UNKNOWN").upper()
    governance = str(metadata.get("governance_state") or "UNKNOWN").upper()
    trust = str(metadata.get("trust_state") or "UNKNOWN").upper()
    freshness = str(metadata.get("freshness_state") or "UNKNOWN").upper()
    canonical_id = str(metadata.get("canonical_id") or "").strip()
    source_locator = str(metadata.get("source_locator") or "").strip()

    if not canonical_id:
        return AuthorityDecision(False, None, "MISSING_CANONICAL_ID")
    if not source_locator:
        return AuthorityDecision(False, None, "MISSING_SOURCE_LOCATOR")
    if governance not in {"ACTIVE", "CURRENT", "VALID"}:
        return AuthorityDecision(False, None, f"GOVERNANCE_NOT_ACTIVE:{governance}")
    if eligibility in BLOCKED_ELIGIBILITY or eligibility not in ALLOWED_DEFAULT_ELIGIBILITY:
        return AuthorityDecision(False, None, f"SEARCH_NOT_ELIGIBLE:{eligibility}")
    if freshness == "EXPIRED":
        return AuthorityDecision(False, None, "FRESHNESS_EXPIRED")
    if trust == "UNKNOWN":
        return AuthorityDecision(False, None, "TRUST_UNKNOWN")
    if trust == "UNVERIFIED" and not intent.include_unverified:
        return AuthorityDecision(False, None, "UNVERIFIED_DISALLOWED")

    namespace = choose_namespace(retrieval_space, history_intent=intent.history_intent)
    if namespace is None:
        return AuthorityDecision(False, None, f"RETRIEVAL_SPACE_NOT_LEGAL:{retrieval_space}")

    if namespace == SUPPORT_NAMESPACE and not intent.allow_support_fallback:
        return AuthorityDecision(False, None, "SUPPORT_FALLBACK_DISABLED")

    project = str(metadata.get("project_id") or "GLOBAL")
    if intent.project_id and project not in {"GLOBAL", intent.project_id}:
        return AuthorityDecision(False, None, f"PROJECT_SCOPE_MISMATCH:{project}")

    domain = str(metadata.get("domain_id") or "GLOBAL")
    if intent.domain_id and domain not in {"GLOBAL", intent.domain_id}:
        return AuthorityDecision(False, None, f"DOMAIN_SCOPE_MISMATCH:{domain}")

    return AuthorityDecision(True, namespace, "LEGAL")


def canonical_collision_gate(rows: Iterable[Mapping[str, object]]) -> list[str]:
    """Return canonical IDs that have >1 legal CURRENT owner.

    A collision is a hard retrieval error. It is never resolved by score.
    """

    current_counts: dict[str, int] = {}
    for row in rows:
        if str(row.get("retrieval_space") or "").upper() != "CURRENT":
            continue
        if str(row.get("governance_state") or "").upper() not in {"ACTIVE", "CURRENT", "VALID"}:
            continue
        cid = str(row.get("canonical_id") or "").strip()
        if cid:
            current_counts[cid] = current_counts.get(cid, 0) + 1
    return sorted(cid for cid, count in current_counts.items() if count > 1)


def dedupe_by_canonical_id(
    candidates: Sequence[Mapping[str, object]],
    *,
    score_key: str = "rerank_score",
) -> list[Mapping[str, object]]:
    """Keep highest-scoring chunk per canonical object after authority gating."""

    best: dict[str, Mapping[str, object]] = {}
    for candidate in candidates:
        cid = str(candidate.get("canonical_id") or "").strip()
        if not cid:
            continue
        score = float(candidate.get(score_key) or candidate.get("vector_score") or 0.0)
        previous = best.get(cid)
        if previous is None:
            best[cid] = candidate
            continue
        prev_score = float(previous.get(score_key) or previous.get("vector_score") or 0.0)
        if score > prev_score:
            best[cid] = candidate
    return sorted(
        best.values(),
        key=lambda item: float(item.get(score_key) or item.get("vector_score") or 0.0),
        reverse=True,
    )


def build_vectorize_filter(intent: RetrievalIntent) -> dict[str, object]:
    """Build a conservative filter for the default Current search pool.

    Support/Provenance are separate retrieval passes and must not be mixed into
    the default Current ranking pool.
    """

    clauses: list[dict[str, object]] = [
        {"retrieval_space": "CURRENT"},
        {"search_eligibility": {"$in": ["DEFAULT", "SCOPED"]}},
        {"governance_state": {"$in": ["ACTIVE", "CURRENT", "VALID"]}},
        {"freshness_state": {"$nin": ["EXPIRED"]}},
    ]
    if not intent.include_unverified:
        clauses.append({"trust_state": "VERIFIED"})
    else:
        clauses.append({"trust_state": {"$in": ["VERIFIED", "UNVERIFIED"]}})
    if intent.project_id:
        clauses.append({"project_id": {"$in": ["GLOBAL", intent.project_id]}})
    if intent.domain_id:
        clauses.append({"domain_id": {"$in": ["GLOBAL", intent.domain_id]}})
    return {"$and": clauses}

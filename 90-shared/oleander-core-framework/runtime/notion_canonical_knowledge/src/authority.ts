import type { AuthorityDecision, NormalizedPage } from "./types";

const HISTORY_STATES = new Set(["LEGACY", "ARCHIVED"]);
const NON_CURRENT_RELATION_STATES = new Set(["CONFLICT", "ORPHAN"]);

/**
 * Fail-closed authority resolution.
 * CURRENT is never inferred. It is granted only when Notion explicitly says CURRENT
 * and no stronger safety boundary contradicts it.
 */
export function resolveAuthority(page: NormalizedPage): AuthorityDecision {
  if (page.inTrash) {
    return { index: false, effectiveSpace: null, reason: "PAGE_IN_TRASH", conflict: false };
  }
  if (page.searchEligibility === "BLOCKED") {
    return { index: false, effectiveSpace: null, reason: "SEARCH_ELIGIBILITY_BLOCKED", conflict: false };
  }
  if (page.retrievalSpace === "EXCLUDED") {
    return { index: false, effectiveSpace: null, reason: "RETRIEVAL_SPACE_EXCLUDED", conflict: false };
  }

  if (page.searchEligibility === "HISTORY_ONLY") {
    return {
      index: true,
      effectiveSpace: "PROVENANCE",
      reason: page.retrievalSpace === "CURRENT" ? "HISTORY_ONLY_OVERRIDES_CURRENT" : "HISTORY_ONLY",
      conflict: page.retrievalSpace === "CURRENT",
    };
  }

  if (page.governanceState && HISTORY_STATES.has(page.governanceState)) {
    return {
      index: true,
      effectiveSpace: "PROVENANCE",
      reason: page.retrievalSpace === "CURRENT" ? "LEGACY_GOVERNANCE_OVERRIDES_CURRENT" : "LEGACY_GOVERNANCE",
      conflict: page.retrievalSpace === "CURRENT",
    };
  }

  if (page.relationState && NON_CURRENT_RELATION_STATES.has(page.relationState)) {
    if (page.retrievalSpace === "CURRENT") {
      return {
        index: true,
        effectiveSpace: "SUPPORT",
        reason: `RELATION_${page.relationState}_DOWNGRADES_CURRENT`,
        conflict: true,
      };
    }
  }

  if (page.retrievalSpace === "CURRENT") {
    return { index: true, effectiveSpace: "CURRENT", reason: "EXPLICIT_NOTION_CURRENT", conflict: false };
  }
  if (page.retrievalSpace === "SUPPORT") {
    return { index: true, effectiveSpace: "SUPPORT", reason: "EXPLICIT_NOTION_SUPPORT", conflict: false };
  }
  if (page.retrievalSpace === "PROVENANCE") {
    return { index: true, effectiveSpace: "PROVENANCE", reason: "EXPLICIT_NOTION_PROVENANCE", conflict: false };
  }

  // Missing retrieval-space metadata can never become CURRENT implicitly.
  if (page.governanceState === "ACTIVE") {
    return { index: true, effectiveSpace: "SUPPORT", reason: "MISSING_SPACE_FAIL_CLOSED_TO_SUPPORT", conflict: true };
  }
  return { index: true, effectiveSpace: "PROVENANCE", reason: "MISSING_SPACE_FAIL_CLOSED_TO_PROVENANCE", conflict: true };
}

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
ITERATION_ACTIONS = {"SELECT", "MODIFY", "MIX", "REJECT", "REOPEN", "DEFER"}
AUTHORITY_ROUTE_BY_LEVEL = {
    "DESIGN_DECISION": "EXISTING_PROJECT_DECISION_AUTHORITY",
    "DESIGN_KEEP": "EXISTING_DESIGN_REVIEW_AUTHORITY",
    "PROMOTION_DECISION": "EXISTING_PROMOTION_AUTHORITY",
}
REFERENCE_LARGE_FILE_THRESHOLD_BYTES = 50 * 1024 * 1024
CONTEXT_DISCLOSURE_RANK = {
    "ROUTER": 0,
    "TASK_REQUIRED": 1,
    "TASK_SUPPORTING": 2,
    "BULK": 3,
}

DEFAULT_CONVERSATION_SURFACE = "CHAT"
LOCAL_CAPABILITY_ROUTES = {
    "BAIDU_STORAGE": {
        "execution_surface": "COS_LOCAL",
        "adapter_ref": "oleander-baidu-storage@oleander-personal",
        "adapter_version": "0.1.1",
        "transport": "stdio",
        "authority_effect": "NONE",
    },
}


@dataclass(frozen=True)
class ClassificationContext:
    active_option_refs: tuple[str, ...] = ()
    pending_decision_ref: str | None = None
    unambiguous_active_ref: str | None = None
    actor_role: str = "DESIGNER"
    referent_metadata: dict[str, dict[str, str]] = field(default_factory=dict)


def resolve_execution_route(request: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve where work executes without changing what the Human asked or who owns authority.

    Chat is the default conversation surface. A local capability may route execution to COS,
    but that route is only an ephemeral projection. When an inline COS bridge is unavailable,
    the existing continuity execution-intent carrier is used rather than inventing a second queue.
    """
    facts = request or {}
    conversation_surface = str(facts.get("conversation_surface") or DEFAULT_CONVERSATION_SURFACE)
    capability_id = str(facts.get("capability_id") or "NONE")
    operation_class = str(facts.get("operation_class") or "NONE")
    workstation_online = facts.get("workstation_online", True) is True
    cos_bridge_available = facts.get("cos_bridge_available", True) is True
    adapter_state = str(facts.get("adapter_state") or "INSTALLED_READY")

    base = {
        "conversation_surface": conversation_surface,
        "capability_id": capability_id,
        "operation_class": operation_class,
        "authority_effect": "NONE",
        "changes_work_intent": False,
        "changes_mutation_permission": False,
        "readback_required": False,
        "requires_execution_intent": False,
    }

    if capability_id in {"", "NONE", "CHAT_NATIVE"}:
        return {
            **base,
            "execution_surface": "CHAT",
            "handoff_mode": "NONE",
            "adapter_ref": "NOT_APPLICABLE",
            "adapter_version": "NOT_APPLICABLE",
            "transport": "NOT_APPLICABLE",
            "route_state": "READY",
            "route_reason": "NO_LOCAL_CAPABILITY_REQUIRED",
        }

    route = LOCAL_CAPABILITY_ROUTES.get(capability_id)
    if route is None:
        return {
            **base,
            "execution_surface": "HOLD_LOCAL_CAPABILITY",
            "handoff_mode": "NONE",
            "adapter_ref": "UNRESOLVED",
            "adapter_version": "UNRESOLVED",
            "transport": "UNRESOLVED",
            "route_state": "HOLD",
            "route_reason": "UNREGISTERED_LOCAL_CAPABILITY",
        }

    routed = {**base, **route, "readback_required": True}
    if adapter_state != "INSTALLED_READY":
        return {
            **routed,
            "execution_surface": "HOLD_LOCAL_CAPABILITY",
            "handoff_mode": "CONTINUITY_EXECUTION_INTENT",
            "requires_execution_intent": True,
            "route_state": "HOLD",
            "route_reason": "LOCAL_ADAPTER_NOT_READY",
        }
    if not workstation_online:
        return {
            **routed,
            "execution_surface": "PENDING_LOCAL_EXECUTION",
            "handoff_mode": "CONTINUITY_EXECUTION_INTENT",
            "requires_execution_intent": True,
            "route_state": "PENDING",
            "route_reason": "LOCAL_GATEWAY_OFFLINE",
        }
    if not cos_bridge_available:
        return {
            **routed,
            "execution_surface": "PENDING_LOCAL_EXECUTION",
            "handoff_mode": "CONTINUITY_EXECUTION_INTENT",
            "requires_execution_intent": True,
            "route_state": "PENDING",
            "route_reason": "COS_BRIDGE_UNAVAILABLE",
        }
    return {
        **routed,
        "execution_surface": "COS_LOCAL",
        "handoff_mode": "INLINE_COS_BRIDGE",
        "route_state": "READY",
        "route_reason": "LOCAL_CAPABILITY_READY",
    }


def validate_execution_route(route: dict[str, Any]) -> list[str]:
    """Validate the routing projection without treating it as authority or persistent state."""
    errors: list[str] = []
    if route.get("conversation_surface") not in {"CHAT", "COS", "OTHER"}:
        errors.append("EXECUTION_ROUTE_CONVERSATION_SURFACE_INVALID")
    if route.get("execution_surface") not in {
        "CHAT",
        "COS_LOCAL",
        "PENDING_LOCAL_EXECUTION",
        "HOLD_LOCAL_CAPABILITY",
    }:
        errors.append("EXECUTION_ROUTE_SURFACE_INVALID")
    if route.get("authority_effect") != "NONE":
        errors.append("EXECUTION_ROUTE_CANNOT_OWN_AUTHORITY")
    if route.get("changes_work_intent") is not False:
        errors.append("EXECUTION_ROUTE_CANNOT_CHANGE_WORK_INTENT")
    if route.get("changes_mutation_permission") is not False:
        errors.append("EXECUTION_ROUTE_CANNOT_CHANGE_MUTATION_PERMISSION")
    if route.get("execution_surface") in {"COS_LOCAL", "PENDING_LOCAL_EXECUTION"} and route.get("readback_required") is not True:
        errors.append("LOCAL_EXECUTION_ROUTE_REQUIRES_READBACK")
    if route.get("handoff_mode") == "CONTINUITY_EXECUTION_INTENT" and route.get("requires_execution_intent") is not True:
        errors.append("CONTINUITY_HANDOFF_REQUIRES_EXECUTION_INTENT")
    if route.get("execution_surface") == "COS_LOCAL" and route.get("handoff_mode") != "INLINE_COS_BRIDGE":
        errors.append("COS_LOCAL_ROUTE_REQUIRES_INLINE_BRIDGE")
    return errors


def _contains_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _extract_option_refs(text: str, active_option_refs: Iterable[str]) -> list[str]:
    active = list(active_option_refs)
    alias_counts: dict[str, int] = {}
    for item in active:
        alias = item.split("_", 1)[0].upper()
        alias_counts[alias] = alias_counts.get(alias, 0) + 1
    refs: list[str] = []
    for ref in active:
        # Full IDs are matched case-insensitively. Single-letter aliases such as A/B/C
        # are matched case-sensitively so English articles/words do not bind option A.
        short = ref.split("_", 1)[0]
        full_hit = re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(ref)}(?![A-Za-z0-9_])",
            text,
            flags=re.IGNORECASE,
        ) is not None
        alias_is_unique = alias_counts.get(short.upper(), 0) == 1
        if len(short) == 1 and short.isalpha() and alias_is_unique:
            short_hit = re.search(rf"(?<![A-Za-z0-9_]){re.escape(short.upper())}(?![A-Za-z0-9_])", text) is not None
        elif alias_is_unique:
            short_hit = re.search(rf"(?<![A-Z0-9]){re.escape(short)}(?![A-Z0-9])", text, flags=re.IGNORECASE) is not None
        else:
            short_hit = False
        if full_hit or short_hit:
            refs.append(ref)
    return list(dict.fromkeys(refs))


def _extract_reason(text: str) -> str | None:
    match = re.search(r"(?:因为|理由是|原因是|because)\s*([^。.!?]+)", text, flags=re.IGNORECASE)
    if not match:
        return None
    reason = match.group(1).strip(" ，,;；")
    return reason or None


def _make_bound_referents(refs: Iterable[str], ctx: ClassificationContext) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for ref in refs:
        meta = ctx.referent_metadata.get(ref, {})
        kind = meta.get("kind")
        if not kind:
            kind = "DECISION_OBJECT" if ref == ctx.pending_decision_ref else "OPTION"
        record = {
            "ref": ref,
            "kind": kind,
            "revision": meta.get("revision", "UNRESOLVED"),
            "lineage_ref": meta.get("lineage_ref", ref),
        }
        if meta.get("decision_object_ref"):
            record["decision_object_ref"] = meta["decision_object_ref"]
        records.append(record)
    return records


def _authority_level(text: str) -> str | None:
    if _contains_any(
        text,
        [
            r"\bpromotion[ -]?decision\b",
            r"\bpromote\b.*\bcurrent\b",
            r"提升(?:为|到)\s*current",
            r"晋升.*current",
            r"批准.*promotion",
        ],
    ):
        return "PROMOTION_DECISION"
    if _contains_any(
        text,
        [
            r"\bdesign[ -]?keep\b",
            r"设计\s*keep",
            r"设计(?:方案)?\s*(?:保留|定稿)",
            r"设计保留决定",
            r"设计定稿决定",
        ],
    ):
        return "DESIGN_KEEP"
    if _contains_any(text, [r"\bdesign[ -]?decision\b", r"设计决定"]):
        return "DESIGN_DECISION"
    return None


def _typed_binding_issue(refs: Iterable[str], ctx: ClassificationContext) -> str | None:
    for ref in refs:
        meta = ctx.referent_metadata.get(ref, {})
        if (
            not meta.get("kind")
            or meta.get("kind") == "UNRESOLVED"
            or not meta.get("revision")
            or meta.get("revision") == "UNRESOLVED"
            or not meta.get("lineage_ref")
        ):
            return "UNRESOLVED_TYPED_REFERENT"
    return None


def _split_action_clauses(text: str) -> list[str]:
    """Split independent Human acts without breaking a single `preserve A + mix B` act.

    Strong separators always split. A comma starts a new clause only when what follows
    is a fresh action cue; `结合/融合` are intentionally excluded because the preceding
    `保留 X，结合 Y` text belongs to the same MIX act.
    """
    strong = [c.strip() for c in re.split(r"[；;。]+|(?:然后|同时|and then)", text, flags=re.IGNORECASE) if c.strip()]
    result: list[str] = []
    action_start = re.compile(
        r"^(?:不要|拒绝|淘汰|排除|修改|调整|改一下|重开|重新打开|重新考虑|暂缓|延后|先不选|选择|选\s*[A-Z]|就按这个|就用这个|采用|保留\s*[A-Z]|reject\b|drop\b|modify\b|adjust\b|reopen\b|defer\b|select\b|choose\b|keep\b|preserve\b|combine\b|mix\b)",
        flags=re.IGNORECASE,
    )
    mix_start = re.compile(r"^(?:结合|融合|混合|combine\b|mix\b)", flags=re.IGNORECASE)
    preserve_start = re.compile(r"^(?:保留|keep\b|preserve\b)", flags=re.IGNORECASE)
    for clause in strong:
        pieces = [p.strip() for p in re.split(r"[，,]", clause) if p.strip()]
        current = ""
        for piece in pieces:
            starts_action = action_start.search(piece) is not None
            starts_mix = mix_start.search(piece) is not None
            current_is_preserve = preserve_start.search(current) is not None if current else False
            if current and starts_action and not (starts_mix and current_is_preserve):
                result.append(current)
                current = piece
            else:
                current = piece if not current else f"{current}，{piece}"
        if current:
            result.append(current)
    return result


def _classify_action_clause(clause: str, clause_index: int, ctx: ClassificationContext) -> dict[str, Any] | None:
    normalized = re.sub(r"\s+", " ", clause).strip().lower()
    refs = _extract_option_refs(clause, ctx.active_option_refs)
    stated_reason = _extract_reason(clause)
    authority_level = _authority_level(normalized)

    candidate_action: str | None = None
    action_requires_referent = False
    deictic_cross_parent = (
        ctx.unambiguous_active_ref is not None
        and any(ref != ctx.unambiguous_active_ref for ref in refs)
        and _contains_any(normalized, [r"(?:这个|this).*(?:用|采用|换成|改成|use).+", r"保留这个.*(?:用|采用|换成|改成|use).+"])
    )
    if deictic_cross_parent:
        candidate_action, action_requires_referent = "MIX", True
        refs = list(dict.fromkeys([ctx.unambiguous_active_ref, *refs]))
    elif _contains_any(normalized, [r"结合", r"融合", r"混合", r"mix", r"combine", r"保留.+(?:结合|加上|融合)"]):
        candidate_action, action_requires_referent = "MIX", True
    elif _contains_any(
        normalized,
        [r"拒绝", r"淘汰", r"排除", r"不要(?:\s*[a-z]|这个|它)", r"reject\b", r"drop\b"],
    ):
        candidate_action, action_requires_referent = "REJECT", True
    elif _contains_any(normalized, [r"重开", r"重新打开", r"重新考虑", r"reopen"]):
        candidate_action, action_requires_referent = "REOPEN", True
    elif _contains_any(normalized, [r"暂缓", r"延后", r"先不选", r"以后再决定", r"先放着", r"defer", r"decide later"]):
        candidate_action = "DEFER"
    elif _contains_any(normalized, [r"修改", r"调整", r"改一下", r"保留.+但", r"modify", r"adjust"]):
        candidate_action, action_requires_referent = "MODIFY", True
    elif _contains_any(normalized, [r"选择", r"选\s*[a-z]", r"就按这个", r"就用这个", r"采用", r"select\b", r"choose\b"]):
        candidate_action, action_requires_referent = "SELECT", True

    if authority_level:
        bound_refs = refs[:]
        referent_binding = "EXPLICIT" if bound_refs else "NOT_APPLICABLE"
        return {
            "level": authority_level,
            "action": candidate_action or "NONE",
            "referents": bound_refs,
            "bound_referents": _make_bound_referents(bound_refs, ctx),
            "referent_binding": referent_binding,
            "binding_issue": _typed_binding_issue(bound_refs, ctx) if bound_refs else None,
            "reason": stated_reason,
            "source": "EXPLICIT_USER_INPUT",
            "durable_preference": False,
            "actor_role": ctx.actor_role,
            "route_target": AUTHORITY_ROUTE_BY_LEVEL[authority_level],
            "clause_index": clause_index,
            "clause_text": clause,
        }

    if candidate_action:
        bound_refs = refs[:]
        referent_binding = "EXPLICIT" if bound_refs else "AMBIGUOUS"

        if not bound_refs and candidate_action in {"SELECT", "MODIFY", "REJECT", "REOPEN"} and ctx.unambiguous_active_ref:
            bound_refs = [ctx.unambiguous_active_ref]
            referent_binding = "UNAMBIGUOUS_ACTIVE_OBJECT"

        binding_issue: str | None = None
        if candidate_action == "DEFER":
            if ctx.pending_decision_ref:
                if not bound_refs:
                    bound_refs = [ctx.pending_decision_ref]
                referent_binding = "EXPLICIT" if refs else "UNAMBIGUOUS_ACTIVE_OBJECT"
                for ref in bound_refs:
                    meta = ctx.referent_metadata.get(ref, {})
                    if ref != ctx.pending_decision_ref and meta.get("decision_object_ref") != ctx.pending_decision_ref:
                        binding_issue = "DEFER_REFERENT_NOT_BOUND_TO_PENDING_DECISION"
                        break
            else:
                referent_binding = "AMBIGUOUS"
                binding_issue = "PENDING_DECISION_UNRESOLVED"

        valid_cardinality = len(bound_refs) >= (2 if candidate_action == "MIX" else (1 if action_requires_referent else 0))
        if referent_binding != "AMBIGUOUS" and valid_cardinality and binding_issue is None:
            binding_issue = _typed_binding_issue(bound_refs, ctx)
        if referent_binding == "AMBIGUOUS" and binding_issue is None:
            binding_issue = "AMBIGUOUS_REFERENT"
        valid_binding = referent_binding != "AMBIGUOUS" and valid_cardinality and binding_issue is None
        return {
            "level": "ITERATION_STEER" if valid_binding else "FEEDBACK_SIGNAL",
            "action": candidate_action,
            "referents": bound_refs,
            "bound_referents": _make_bound_referents(bound_refs, ctx),
            "referent_binding": referent_binding,
            "binding_issue": binding_issue,
            "reason": stated_reason,
            "source": "EXPLICIT_USER_INPUT",
            "durable_preference": False,
            "actor_role": ctx.actor_role,
            "route_target": "SESSION_ITERATION" if valid_binding else "NONE",
            "clause_index": clause_index,
            "clause_text": clause,
        }

    if _contains_any(
        normalized,
        [r"不对", r"不行", r"太像", r"感觉.+(?:散|碎|重|乱|弱)", r"not right", r"doesn.?t work", r"feels wrong"],
    ):
        return {
            "level": "FEEDBACK_SIGNAL",
            "action": "NEGATIVE_STEER",
            "referents": refs,
            "bound_referents": _make_bound_referents(refs, ctx),
            "referent_binding": "EXPLICIT" if refs else "NOT_APPLICABLE",
            "binding_issue": None,
            "reason": clause,
            "source": "EXPLICIT_USER_INPUT",
            "durable_preference": False,
            "actor_role": ctx.actor_role,
            "route_target": "NONE",
            "clause_index": clause_index,
            "clause_text": clause,
        }
    return None


def classify_message(text: str, ctx: ClassificationContext | None = None) -> dict[str, Any]:
    """Reference classifier for kernel invariants, not a language-model replacement.

    The important property is separation of interaction axes. A message can be RESUME +
    READ_ONLY + COMPACT without inventing a Human iteration steer.
    """

    ctx = ctx or ClassificationContext()
    raw = text.strip()
    normalized = re.sub(r"\s+", " ", raw).strip().lower()

    mutation_directive = "NORMAL"
    if _contains_any(normalized, [r"只读", r"不要改", r"别改", r"read[ -]?only", r"do not (?:edit|change|modify)"]):
        mutation_directive = "READ_ONLY"
    elif _contains_any(
        normalized,
        [
            r"不用每步问", r"直接做.*真正需要我决定", r"先做能做的", r"自动推进", r"auto[- ]?advance",
            r"keep going until (?:you )?need me",
        ],
    ):
        mutation_directive = "AUTO_ADVANCE_REVERSIBLE"

    explain_requested = _contains_any(normalized, [r"解释一下", r"为什么", r"教我怎么看", r"explain", r"teach me"])
    compact_requested = _contains_any(normalized, [r"少解释", r"别讲太多", r"直接做", r"compact", r"less explanation"])
    support_mode = "AUTO"
    if explain_requested:
        support_mode = "EXPLAIN"
    # "Teach/explain, but briefly" is EXPLAIN work with COMPACT support density.
    if compact_requested:
        support_mode = "COMPACT"
    if _contains_any(normalized, [r"不要教学", r"别教我", r"不要解释", r"support off", r"no tutorial"]):
        support_mode = "OFF"

    clauses = _split_action_clauses(raw)
    human_actions = [a for i, clause in enumerate(clauses) if (a := _classify_action_clause(clause, i, ctx))]

    work_intent = "UNRESOLVED"
    if _contains_any(normalized, [r"开始", r"新项目", r"从头", r"start\b", r"new project"]):
        work_intent = "START"
    if _contains_any(normalized, [r"继续", r"接着", r"往下", r"完成整个", r"finish the whole", r"continue\b", r"resume\b"]):
        work_intent = "RESUME"
    if _contains_any(normalized, [r"恢复", r"找回", r"recover"]):
        work_intent = "RECOVER"
    if _contains_any(normalized, [r"几个.*方案", r"真正不同", r"多想", r"拓展", r"explore", r"alternatives?"]):
        work_intent = "EXPLORE"
    if _contains_any(normalized, [r"野路子", r"不一样的", r"wildcard", r"left[- ]field"]):
        work_intent = "WILDCARD"
    if _contains_any(normalized, [r"看看", r"审查", r"复核", r"这版怎么样", r"review\b", r"inspect\b"]):
        work_intent = "REVIEW"
    if _contains_any(normalized, [r"重做", r"答错题", r"重新定义", r"reframe"]):
        work_intent = "REFRAME"
    if _contains_any(normalized, [r"保存", r"下次继续", r"放到项目", r"save\b", r"persist"]):
        work_intent = "SAVE_ROUTE"
    if explain_requested and work_intent == "UNRESOLVED":
        work_intent = "EXPLAIN"
    if _contains_any(normalized, [r"展示过程", r"给我看过程", r"show work"]):
        work_intent = "SHOW_WORK"

    stop_reason = None
    blocked_steers = [
        action
        for action in human_actions
        if action["level"] == "FEEDBACK_SIGNAL" and action["action"] in ITERATION_ACTIONS
    ]
    if blocked_steers:
        issues = {action.get("binding_issue") for action in blocked_steers}
        if "UNRESOLVED_TYPED_REFERENT" in issues:
            stop_reason = "UNRESOLVED_TYPED_REFERENT_BEFORE_CONSEQUENTIAL_STEER"
        elif "DEFER_REFERENT_NOT_BOUND_TO_PENDING_DECISION" in issues:
            stop_reason = "DEFER_REFERENT_NOT_BOUND_TO_PENDING_DECISION"
        elif "PENDING_DECISION_UNRESOLVED" in issues:
            stop_reason = "PENDING_DECISION_UNRESOLVED_BEFORE_DEFER"
        else:
            stop_reason = "AMBIGUOUS_REFERENT_BEFORE_CONSEQUENTIAL_STEER"

    return {
        "raw": raw,
        "work_intent": work_intent,
        "mutation_directive": mutation_directive,
        "support_mode": support_mode,
        "human_actions": human_actions,
        "minimum_clarification_required": stop_reason is not None,
        "stop_reason": stop_reason,
    }


def validate_option_set(options: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(options) < 2:
        errors.append("OPTION_SET_REQUIRES_AT_LEAST_TWO_COMPARABLE_OPTIONS")
        return errors
    worlds = {o.get("comparison_world_id") for o in options}
    if len(worlds) != 1 or None in worlds:
        errors.append("OPTIONS_MUST_SHARE_ONE_COMPARISON_WORLD")
    signatures = [o.get("mechanism_signature") for o in options]
    if None in signatures or len(set(signatures)) != len(signatures):
        errors.append("MECHANISM_SIGNATURES_MUST_BE_PRESENT_AND_DISTINCT")
    option_ids = [o.get("option_id") for o in options]
    if None in option_ids or len(set(option_ids)) != len(option_ids):
        errors.append("OPTION_IDS_MUST_BE_PRESENT_AND_DISTINCT")
    allowed_branch_statuses = {
        "ACTIVE",
        "SELECTED_FOR_NEXT_ROUND",
        "REJECTED_PRESERVED",
        "DEFERRED_PRESERVED",
        "SUPERSEDED_BY_CHILD",
        "BASELINE",
    }
    for option in options:
        preserved_invariants = set(option.get("preserved_invariants") or [])
        for key in (
            "option_id",
            "parent_refs",
            "artifact_refs",
            "artifact_bindings",
            "readback_bindings",
            "preserved_invariants",
            "strongest_benefit",
            "strongest_risk",
            "sensitive_unknowns",
            "branch_status",
        ):
            if key not in option:
                errors.append(f"OPTION_MISSING:{option.get('option_id', 'UNRESOLVED')}:{key}")
        parent_refs = option.get("parent_refs")
        if not isinstance(parent_refs, list):
            errors.append(f"OPTION_PARENT_REFS_MUST_BE_LIST:{option.get('option_id', 'UNRESOLVED')}")
        elif option.get("option_id") in parent_refs:
            errors.append(f"OPTION_CANNOT_PARENT_ITSELF:{option.get('option_id', 'UNRESOLVED')}")
        if not isinstance(option.get("preserved_invariants"), list):
            errors.append(f"OPTION_PRESERVED_INVARIANTS_MUST_BE_LIST:{option.get('option_id', 'UNRESOLVED')}")
        if option.get("branch_status") not in allowed_branch_statuses:
            errors.append(f"OPTION_BRANCH_STATUS_INVALID:{option.get('option_id', 'UNRESOLVED')}:{option.get('branch_status')}")
        artifacts = option.get("artifact_bindings") or []
        readbacks = option.get("readback_bindings") or []
        if not artifacts:
            errors.append(f"OPTION_REQUIRES_ACTUAL_ARTIFACT_BINDING:{option.get('option_id', 'UNRESOLVED')}")
        if not readbacks:
            errors.append(f"OPTION_REQUIRES_ACTUAL_READBACK_BINDING:{option.get('option_id', 'UNRESOLVED')}")
        artifact_pairs = {
            (x.get("artifact_ref"), x.get("revision"))
            for x in artifacts
            if isinstance(x, dict) and x.get("artifact_ref") and x.get("revision")
        }
        artifact_hash_by_pair = {
            (x.get("artifact_ref"), x.get("revision")): x.get("content_sha256")
            for x in artifacts
            if isinstance(x, dict) and x.get("artifact_ref") and x.get("revision")
        }
        artifact_refs = set(option.get("artifact_refs") or [])
        bound_artifact_refs = {x[0] for x in artifact_pairs}
        if artifact_refs != bound_artifact_refs:
            errors.append(f"OPTION_ARTIFACT_REFS_MUST_MATCH_BINDINGS:{option.get('option_id', 'UNRESOLVED')}")
        for x in artifacts:
            if not isinstance(x, dict) or not SHA256_RE.fullmatch(str(x.get("content_sha256", ""))):
                errors.append(f"OPTION_ARTIFACT_HASH_REQUIRED:{option.get('option_id', 'UNRESOLVED')}")
        readback_pairs = {
            (x.get("artifact_ref"), x.get("artifact_revision"))
            for x in readbacks
            if isinstance(x, dict) and x.get("artifact_ref") and x.get("artifact_revision")
        }
        for x in readbacks:
            if not isinstance(x, dict) or not SHA256_RE.fullmatch(str(x.get("content_sha256", ""))):
                errors.append(f"OPTION_READBACK_HASH_REQUIRED:{option.get('option_id', 'UNRESOLVED')}")
            if not isinstance(x, dict) or x.get("inspection_status") != "ACTUAL_READBACK":
                errors.append(f"OPTION_READBACK_MUST_BE_ACTUAL:{option.get('option_id', 'UNRESOLVED')}")
            verified_invariants = set(x.get("verified_invariant_refs") or []) if isinstance(x, dict) else set()
            if not preserved_invariants <= verified_invariants:
                errors.append(
                    f"OPTION_INVARIANTS_NOT_PROVEN:{option.get('option_id', 'UNRESOLVED')}:{sorted(preserved_invariants - verified_invariants)!r}"
                )
            pair = (x.get("artifact_ref"), x.get("artifact_revision")) if isinstance(x, dict) else (None, None)
            artifact_content_sha256 = x.get("artifact_content_sha256") if isinstance(x, dict) else None
            if not SHA256_RE.fullmatch(str(artifact_content_sha256 or "")):
                errors.append(f"OPTION_READBACK_ARTIFACT_HASH_REQUIRED:{option.get('option_id', 'UNRESOLVED')}")
            elif pair in artifact_hash_by_pair and artifact_hash_by_pair[pair] != artifact_content_sha256:
                errors.append(f"OPTION_READBACK_ARTIFACT_HASH_MISMATCH:{option.get('option_id', 'UNRESOLVED')}")
        if artifact_pairs and not artifact_pairs <= readback_pairs:
            errors.append(
                f"OPTION_READBACK_REVISION_MISMATCH:{option.get('option_id', 'UNRESOLVED')}:{sorted(artifact_pairs - readback_pairs)!r}"
            )
    return errors


def validate_second_round_delta(round_trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    steer = round_trace.get("steering_event")
    if not steer:
        errors.append("SECOND_ROUND_REQUIRES_ACTUAL_ITERATION_STEER")
        return errors
    for key in (
        "decision_object_ref",
        "action",
        "referents",
        "bound_referents",
        "source",
        "actor_role",
        "changed_variables",
        "preserved_invariants",
    ):
        if key not in steer:
            errors.append(f"STEERING_EVENT_MISSING:{key}")
    if steer.get("source") != "EXPLICIT_USER_INPUT":
        errors.append("SECOND_ROUND_REQUIRES_EXPLICIT_HUMAN_SOURCE")
    if steer.get("actor_role") in {None, "UNRESOLVED"}:
        errors.append("SECOND_ROUND_REQUIRES_RESOLVED_HUMAN_ACTOR_ROLE")
    if round_trace.get("decision_rights_status") != "ALLOWED_BY_EXISTING_OWNER_RULE":
        errors.append("SECOND_ROUND_REQUIRES_ALLOWED_DECISION_RIGHTS")
    if not round_trace.get("decision_rights_owner_rule_ref"):
        errors.append("SECOND_ROUND_REQUIRES_DECISION_RIGHTS_OWNER_RULE_REF")
    if not round_trace.get("decision_rights_revision") or round_trace.get("decision_rights_revision") == "UNRESOLVED":
        errors.append("SECOND_ROUND_REQUIRES_DECISION_RIGHTS_REVISION")
    rights_proof = round_trace.get("decision_rights_proof")
    rights_proof_valid = True
    if not isinstance(rights_proof, dict):
        errors.append("SECOND_ROUND_REQUIRES_BOUND_DECISION_RIGHTS_PROOF")
        rights_proof_valid = False
    else:
        required_rights = (
            "source",
            "owner_rule_ref",
            "owner_rule_revision",
            "decision_object_ref",
            "actor_role",
            "effect_scope",
            "allowed_actions",
            "proof_ref",
            "proof_revision",
            "proof_sha256",
            "inspection_status",
            "authority_ceiling",
        )
        missing_rights = [k for k in required_rights if not rights_proof.get(k)]
        if missing_rights:
            errors.append("DECISION_RIGHTS_PROOF_MISSING:" + ",".join(missing_rights))
            rights_proof_valid = False
        if rights_proof.get("source") != "OWNER_NATIVE_PROJECTION":
            errors.append("DECISION_RIGHTS_PROOF_SOURCE_MUST_BE_OWNER_NATIVE_PROJECTION")
            rights_proof_valid = False
        if rights_proof.get("inspection_status") != "ACTUAL_READBACK":
            errors.append("DECISION_RIGHTS_PROOF_MUST_BE_ACTUAL_READBACK")
            rights_proof_valid = False
        if rights_proof.get("authority_ceiling") != "ITERATION_STEER_ONLY":
            errors.append("DECISION_RIGHTS_PROOF_AUTHORITY_CEILING_INVALID")
            rights_proof_valid = False
        if rights_proof.get("effect_scope") != "ITERATION_STEER":
            errors.append("DECISION_RIGHTS_PROOF_EFFECT_SCOPE_INVALID")
            rights_proof_valid = False
        if rights_proof.get("owner_rule_ref") != round_trace.get("decision_rights_owner_rule_ref"):
            errors.append("DECISION_RIGHTS_PROOF_OWNER_RULE_REF_MISMATCH")
            rights_proof_valid = False
        if rights_proof.get("owner_rule_revision") != round_trace.get("decision_rights_revision"):
            errors.append("DECISION_RIGHTS_PROOF_OWNER_RULE_REVISION_MISMATCH")
            rights_proof_valid = False
        if rights_proof.get("decision_object_ref") != steer.get("decision_object_ref"):
            errors.append("DECISION_RIGHTS_PROOF_DECISION_OBJECT_MISMATCH")
            rights_proof_valid = False
        if rights_proof.get("actor_role") != steer.get("actor_role"):
            errors.append("DECISION_RIGHTS_PROOF_ACTOR_ROLE_MISMATCH")
            rights_proof_valid = False
        if steer.get("action") not in (rights_proof.get("allowed_actions") or []):
            errors.append("DECISION_RIGHTS_PROOF_ACTION_NOT_ALLOWED")
            rights_proof_valid = False
        if not SHA256_RE.fullmatch(str(rights_proof.get("proof_sha256", ""))):
            errors.append("DECISION_RIGHTS_PROOF_HASH_REQUIRED")
            rights_proof_valid = False
    if round_trace.get("decision_rights_status") == "ALLOWED_BY_EXISTING_OWNER_RULE" and not rights_proof_valid:
        errors.append("DECISION_RIGHTS_STATUS_NOT_SUPPORTED_BY_BOUND_PROOF")
    decision_binding = round_trace.get("decision_object_binding")
    if not isinstance(decision_binding, dict):
        errors.append("SECOND_ROUND_REQUIRES_TYPED_DECISION_OBJECT_BINDING")
    else:
        if decision_binding.get("kind") != "DECISION_OBJECT":
            errors.append("DECISION_OBJECT_BINDING_KIND_MUST_BE_DECISION_OBJECT")
        if decision_binding.get("ref") != steer.get("decision_object_ref"):
            errors.append("DECISION_OBJECT_BINDING_REF_MISMATCH")
        if not decision_binding.get("revision") or decision_binding.get("revision") == "UNRESOLVED":
            errors.append("DECISION_OBJECT_BINDING_REVISION_UNRESOLVED")
        if not decision_binding.get("lineage_ref"):
            errors.append("DECISION_OBJECT_BINDING_LINEAGE_REQUIRED")
    if steer.get("action") not in {"SELECT", "MODIFY", "MIX", "REJECT", "REOPEN"}:
        errors.append("STEER_ACTION_DOES_NOT_AUTHORIZE_A_DESIGN_DELTA")
    refs = steer.get("referents") or []
    bound_referents = steer.get("bound_referents") or []
    bound_ids: set[str] = set()
    for item in bound_referents:
        if not isinstance(item, dict):
            errors.append("STEER_BOUND_REFERENT_MUST_BE_TYPED_OBJECT")
            continue
        missing = [k for k in ("ref", "kind", "revision", "lineage_ref") if not item.get(k)]
        if missing:
            errors.append("STEER_BOUND_REFERENT_MISSING:" + ",".join(missing))
            continue
        if item.get("revision") == "UNRESOLVED":
            errors.append(f"STEER_BOUND_REFERENT_REVISION_UNRESOLVED:{item.get('ref')}")
        bound_ids.add(str(item.get("ref")))
    if refs and set(refs) != bound_ids:
        errors.append("STEER_REFERENTS_MUST_MATCH_TYPED_BOUND_REFERENTS")
    if steer.get("action") == "MIX" and len(refs) < 2:
        errors.append("MIX_REQUIRES_TWO_OR_MORE_PARENT_REFERENTS")
    if steer.get("action") == "MIX":
        parent_refs = set(round_trace.get("parent_option_refs") or [])
        if not set(refs) <= parent_refs:
            errors.append("MIX_SECOND_ROUND_MUST_PRESERVE_ALL_REFERENCED_PARENT_OPTIONS")
    elif steer.get("action") != "MIX" and not refs:
        errors.append("STEER_REQUIRES_BOUND_REFERENT")
    if not steer.get("changed_variables"):
        errors.append("STEER_REQUIRES_CHANGED_VARIABLES")
    if "preserved_invariants" in steer and not isinstance(steer.get("preserved_invariants"), list):
        errors.append("PRESERVED_INVARIANTS_MUST_BE_LIST")

    made_artifacts = round_trace.get("made_artifacts") or []
    if not made_artifacts:
        errors.append("SECOND_ROUND_REQUIRES_MADE_EDITABLE_OR_NATIVE_ARTIFACT")
    readbacks = round_trace.get("readbacks") or []
    if not readbacks:
        errors.append("SECOND_ROUND_REQUIRES_ACTUAL_READBACK")
    made_pairs: set[tuple[str, str]] = set()
    made_hash_by_pair: dict[tuple[str, str], str] = {}
    for artifact in made_artifacts:
        if not isinstance(artifact, dict) or not all(artifact.get(k) for k in ("artifact_ref", "revision", "role", "content_sha256")):
            errors.append("MADE_ARTIFACT_REQUIRES_REF_REVISION_ROLE_HASH")
            continue
        if not SHA256_RE.fullmatch(str(artifact.get("content_sha256", ""))):
            errors.append(f"MADE_ARTIFACT_INVALID_SHA256:{artifact.get('artifact_ref')}")
        made_pairs.add((artifact["artifact_ref"], artifact["revision"]))
        made_hash_by_pair[(artifact["artifact_ref"], artifact["revision"])] = str(artifact.get("content_sha256"))
    readback_pairs: set[tuple[str, str]] = set()
    readback_by_ref: dict[str, dict[str, Any]] = {}
    for readback in readbacks:
        if not isinstance(readback, dict) or not all(readback.get(k) for k in ("readback_ref", "artifact_ref", "artifact_revision", "artifact_content_sha256", "content_sha256", "inspection_status")):
            errors.append("READBACK_REQUIRES_REF_ARTIFACT_REVISION_ARTIFACT_HASH_READBACK_HASH_AND_STATUS")
            continue
        if not SHA256_RE.fullmatch(str(readback.get("content_sha256", ""))):
            errors.append(f"READBACK_INVALID_SHA256:{readback.get('readback_ref')}")
        if not SHA256_RE.fullmatch(str(readback.get("artifact_content_sha256", ""))):
            errors.append(f"READBACK_ARTIFACT_HASH_INVALID:{readback.get('readback_ref')}")
        if readback.get("inspection_status") != "ACTUAL_READBACK":
            errors.append(f"READBACK_NOT_ACTUAL:{readback.get('readback_ref')}")
        if not isinstance(readback.get("verified_invariant_refs"), list):
            errors.append(f"READBACK_VERIFIED_INVARIANTS_REQUIRED:{readback.get('readback_ref')}")
        pair = (readback["artifact_ref"], readback["artifact_revision"])
        if pair in made_hash_by_pair and made_hash_by_pair[pair] != readback.get("artifact_content_sha256"):
            errors.append(f"READBACK_ARTIFACT_HASH_MISMATCH:{readback.get('readback_ref')}")
        readback_pairs.add(pair)
        readback_by_ref[str(readback["readback_ref"])] = readback
    missing_readback_pairs = sorted(made_pairs - readback_pairs)
    if missing_readback_pairs:
        errors.append("SECOND_ROUND_READBACK_REVISION_MISMATCH:" + repr(missing_readback_pairs))
    preserved = set(steer.get("preserved_invariants") or [])
    invariant_bindings = round_trace.get("invariant_readback_bindings") or []
    if preserved and not invariant_bindings:
        errors.append("SECOND_ROUND_REQUIRES_BOUND_INVARIANT_READBACK")
    covered_invariants: set[str] = set()
    invariant_readback_refs: set[str] = set()
    for binding in invariant_bindings:
        if not isinstance(binding, dict) or not all(
            binding.get(k)
            for k in (
                "invariant_ref",
                "readback_ref",
                "artifact_ref",
                "artifact_revision",
                "artifact_content_sha256",
                "readback_content_sha256",
                "inspection_status",
            )
        ):
            errors.append("INVARIANT_READBACK_BINDING_INCOMPLETE")
            continue
        readback = readback_by_ref.get(str(binding["readback_ref"]))
        if readback is None:
            errors.append(f"INVARIANT_READBACK_REF_NOT_ACTUAL:{binding['readback_ref']}")
            continue
        if binding.get("inspection_status") != "ACTUAL_READBACK":
            errors.append(f"INVARIANT_READBACK_NOT_ACTUAL:{binding['invariant_ref']}")
        if binding.get("invariant_ref") not in set(readback.get("verified_invariant_refs") or []):
            errors.append(f"READBACK_DOES_NOT_VERIFY_INVARIANT:{binding['invariant_ref']}")
            continue
        if (
            binding.get("artifact_ref") != readback.get("artifact_ref")
            or binding.get("artifact_revision") != readback.get("artifact_revision")
            or binding.get("artifact_content_sha256") != readback.get("artifact_content_sha256")
            or binding.get("readback_content_sha256") != readback.get("content_sha256")
        ):
            errors.append(f"INVARIANT_READBACK_BINDING_MISMATCH:{binding['invariant_ref']}")
            continue
        covered_invariants.add(str(binding["invariant_ref"]))
        invariant_readback_refs.add(str(binding["readback_ref"]))
    missing_invariants = sorted(preserved - covered_invariants)
    if missing_invariants:
        errors.append("SECOND_ROUND_INVARIANTS_NOT_PROVEN:" + repr(missing_invariants))
    declared_invariant_refs = set(round_trace.get("invariant_readback_refs") or [])
    if declared_invariant_refs != invariant_readback_refs:
        errors.append("INVARIANT_READBACK_REFS_MUST_MATCH_BOUND_READBACKS")
    return errors


PHASE_TRANSITIONS: dict[str, set[str]] = {
    "RESOLVING": {"WORKING_REVERSIBLE", "HOLD_AUTHORITY", "HOLD_CHECKPOINT", "HOLD_PERMISSION", "HOLD_NATIVE_SURFACE", "HOLD_DECISION_RIGHTS"},
    "WORKING_REVERSIBLE": {"COMPARISON_BUILDING", "MAKING", "REVIEW_REQUIRED", "HANDOFF_READY", "SESSION_COMPLETE", "HOLD_AUTHORITY", "HOLD_CHECKPOINT", "HOLD_PERMISSION", "HOLD_NATIVE_SURFACE", "HOLD_DECISION_RIGHTS"},
    "COMPARISON_BUILDING": {"COMPARISON_READY", "HOLD_NATIVE_SURFACE", "WORKING_REVERSIBLE"},
    "COMPARISON_READY": {"AWAITING_HUMAN_STEER", "WORKING_REVERSIBLE", "REVIEW_REQUIRED"},
    "AWAITING_HUMAN_STEER": {"STEER_BOUND", "WORKING_REVERSIBLE", "SESSION_COMPLETE"},
    "STEER_BOUND": {"MUTATION_GUARD"},
    "MUTATION_GUARD": {"MAKING", "HOLD_AUTHORITY", "HOLD_CHECKPOINT", "HOLD_PERMISSION", "HOLD_NATIVE_SURFACE", "HOLD_DECISION_RIGHTS"},
    "MAKING": {"READBACK_REQUIRED"},
    "READBACK_REQUIRED": {"WORKING_REVERSIBLE", "AWAITING_HUMAN_STEER", "REVIEW_REQUIRED", "HANDOFF_READY"},
    "REVIEW_REQUIRED": {"WORKING_REVERSIBLE", "HANDOFF_READY", "HOLD_AUTHORITY", "HOLD_PERMISSION", "HOLD_DECISION_RIGHTS"},
    "HANDOFF_READY": {"SESSION_COMPLETE", "WORKING_REVERSIBLE"},
    "SESSION_COMPLETE": set(),
    "HOLD_AUTHORITY": {"RESOLVING"},
    "HOLD_CHECKPOINT": {"RESOLVING"},
    "HOLD_PERMISSION": {"RESOLVING"},
    "HOLD_NATIVE_SURFACE": {"WORKING_REVERSIBLE", "RESOLVING"},
    "HOLD_DECISION_RIGHTS": {"RESOLVING", "WORKING_REVERSIBLE"},
}


def validate_phase_transition(current_phase: str, next_phase: str) -> list[str]:
    if current_phase not in PHASE_TRANSITIONS:
        return [f"UNKNOWN_CURRENT_PHASE:{current_phase}"]
    if next_phase not in PHASE_TRANSITIONS[current_phase]:
        return [f"ILLEGAL_PHASE_TRANSITION:{current_phase}->{next_phase}"]
    return []


def validate_domain_adapter(adapter: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = (
        "domain_id",
        "professional_process_status",
        "professional_process_ref",
        "domain_question",
        "native_output_roles",
        "readback_methods",
        "claim_ceiling",
        "hold_conditions",
    )
    for key in required:
        if key not in adapter:
            errors.append(f"DOMAIN_ADAPTER_MISSING:{key}")
    status = adapter.get("professional_process_status")
    allowed_statuses = {"CURRENT", "CANDIDATE", "OPEN", "NOT_APPLICABLE"}
    if status not in allowed_statuses:
        errors.append(f"INVALID_PROFESSIONAL_PROCESS_STATUS:{status}")
    if status == "OPEN" and adapter.get("professional_pass") is True:
        errors.append("OPEN_DOMAIN_PROCESS_CANNOT_AWARD_PROFESSIONAL_PASS")
    if status in {"CURRENT", "CANDIDATE"} and not adapter.get("professional_process_ref"):
        errors.append("RESOLVED_DOMAIN_PROCESS_STATUS_REQUIRES_PROCESS_REF")
    if status in {"OPEN", "NOT_APPLICABLE"} and adapter.get("professional_process_ref") not in {None, "NOT_APPLICABLE"}:
        errors.append("OPEN_OR_NA_DOMAIN_PROCESS_MUST_NOT_FAKE_PROCESS_REF")
    return errors


def compute_human_stop(stop_facts: dict[str, Any] | None = None) -> str | None:
    facts = stop_facts or {}
    precedence = (
        ("ambiguous_referent", "AMBIGUOUS_REFERENT_BEFORE_CONSEQUENTIAL_STEER"),
        ("decision_rights_conflict", "UNRESOLVED_MULTI_HUMAN_DECISION_RIGHTS_CONFLICT"),
        ("authority_escalation", "AUTHORITY_OR_SCOPE_ESCALATION_REQUIRING_HUMAN_AUTHORIZATION"),
        ("external_irreversible_or_publishing", "EXTERNAL_IRREVERSIBLE_OR_PUBLISHING_SIDE_EFFECT"),
        ("review_required", "REQUIRED_SPECIALIST_OR_INDEPENDENT_REVIEW"),
        ("no_truthful_native_or_editable_substitute", "NO_TRUTHFUL_NATIVE_OR_EDITABLE_SUBSTITUTE_FOR_THE_KEY_UNKNOWN"),
        ("value_choice_open", "VALUE_DEPENDENT_CHOICE_AFTER_COMPARABLE_ACTUAL_ARTIFACTS_EXIST"),
        ("user_requested_stop", "USER_REQUESTED_STOP"),
        ("scope_complete", "REQUESTED_SCOPE_COMPLETE"),
    )
    for key, reason in precedence:
        if not facts.get(key):
            continue
        if key == "value_choice_open" and not facts.get("comparable_actual_artifacts_ready"):
            continue
        return reason
    return None


def compute_mutation_permission(
    *, mutation_directive: str, side_effect_class: str, guard_facts: dict[str, Any] | None = None
) -> str:
    """Compute permission from projected owner-native facts; callers do not supply a verdict."""
    facts = guard_facts or {}
    if mutation_directive == "READ_ONLY" and side_effect_class != "NONE":
        return "READ_ONLY"
    if side_effect_class == "NONE":
        return "ALLOW"
    if side_effect_class == "REVERSIBLE_LOCAL":
        return "ALLOW_REVERSIBLE_LOCAL_ONLY"
    # Project/external mutation may only consume a fresh projection of the existing
    # owner-native carrier.  Missing facts fail closed; this is not a second state
    # store and no caller-supplied guard verdict is trusted.
    required_guard_fields = (
        "logical_object_identity",
        "authority_revision",
        "source_revision",
        "expected_checkpoint_sequence",
        "observed_checkpoint_sequence",
        "carrier_readback_status",
        "resolver_provenance",
    )
    if any(facts.get(key) in {None, "", "UNRESOLVED"} for key in required_guard_fields):
        return "HOLD_CHECKPOINT"
    if facts.get("carrier_readback_status") != "ACTUAL_READBACK":
        return "HOLD_CHECKPOINT"
    if facts.get("resolver_provenance") != "EXISTING_OWNER_RESOLVER":
        return "HOLD_AUTHORITY"
    if facts.get("expected_checkpoint_sequence") != facts.get("observed_checkpoint_sequence"):
        return "HOLD_CHECKPOINT"
    decision_rights_status = facts.get("decision_rights_status")
    if decision_rights_status not in {"CLEAR_BY_EXISTING_OWNER_RULE", "NOT_APPLICABLE"}:
        return "HOLD_DECISION_RIGHTS"
    if "active_user_constraints" not in facts or not isinstance(facts.get("active_user_constraints"), list):
        return "HOLD_PERMISSION"
    if facts.get("decision_rights_conflict"):
        return "HOLD_DECISION_RIGHTS"
    if facts.get("authority_drift") or facts.get("source_drift"):
        return "HOLD_AUTHORITY"
    if facts.get("checkpoint_stale"):
        return "HOLD_CHECKPOINT"
    if facts.get("owner_permission") != "ALLOW":
        return "HOLD_PERMISSION"
    if facts.get("native_target_state") not in {"RESOLVED", "TRUTHFUL_SUBSTITUTE"}:
        return "HOLD_NATIVE_SURFACE"
    if side_effect_class == "PROJECT_MUTATION_REVERSIBLE":
        return "ALLOW"
    if side_effect_class in {"PROJECT_MUTATION_AUTHORITY_SENSITIVE", "EXTERNAL_IRREVERSIBLE_OR_PUBLISHING"}:
        return "ALLOW" if facts.get("existing_authorization") is True else "AUTHORIZATION_REQUIRED"
    return "HOLD_PERMISSION"


def decide_auto_advance(
    *,
    mutation_directive: str,
    side_effect_class: str,
    guard_facts: dict[str, Any] | None = None,
    stop_facts: dict[str, Any] | None = None,
) -> dict[str, str]:
    mutation_permission = compute_mutation_permission(
        mutation_directive=mutation_directive,
        side_effect_class=side_effect_class,
        guard_facts=guard_facts,
    )
    human_stop_reason = compute_human_stop(stop_facts)
    if mutation_permission == "READ_ONLY":
        return {"decision": "BLOCK_MUTATION", "reason": "READ_ONLY"}
    if human_stop_reason:
        return {"decision": "STOP_FOR_HUMAN", "reason": human_stop_reason}
    if mutation_permission == "AUTHORIZATION_REQUIRED":
        return {"decision": "STOP_FOR_AUTHORIZATION", "reason": side_effect_class}
    if mutation_permission not in {"ALLOW", "ALLOW_REVERSIBLE_LOCAL_ONLY"}:
        return {"decision": "HOLD", "reason": mutation_permission}
    if side_effect_class in {"NONE", "REVERSIBLE_LOCAL"}:
        return {"decision": "CONTINUE", "reason": "REVERSIBLE_AND_GUARDED"}
    if side_effect_class == "PROJECT_MUTATION_REVERSIBLE" and mutation_permission == "ALLOW":
        return {"decision": "CONTINUE", "reason": "AUTHORIZED_PROJECT_REVERSIBLE"}
    if side_effect_class in {"PROJECT_MUTATION_AUTHORITY_SENSITIVE", "EXTERNAL_IRREVERSIBLE_OR_PUBLISHING"}:
        return {"decision": "CONTINUE", "reason": "EXISTING_AUTHORIZATION_VALIDATED"}
    return {"decision": "HOLD", "reason": "UNRESOLVED_SIDE_EFFECT_CLASS"}


def partition_work_after_defer(
    work_items: list[dict[str, Any]], deferred_decision_refs: Iterable[str]
) -> dict[str, list[str]]:
    """Defer blocks dependent work only; unrelated reversible work remains eligible."""
    deferred = set(deferred_decision_refs)
    eligible: list[str] = []
    held: list[str] = []
    for item in work_items:
        item_id = str(item.get("id", "UNRESOLVED"))
        deps = set(item.get("dependency_decision_refs") or [])
        if deps & deferred:
            held.append(item_id)
        else:
            eligible.append(item_id)
    return {"eligible": eligible, "held": held}


def apply_iteration_steer(
    option_status: dict[str, str], action: str, referents: Iterable[str]
) -> dict[str, str]:
    """Pure lineage transition helper; it never promotes an option to project Current."""
    result = dict(option_status)
    refs = list(dict.fromkeys(referents))
    unknown = [ref for ref in refs if ref not in result]
    if unknown:
        raise ValueError("UNKNOWN_BRANCH_REFERENT:" + ",".join(unknown))
    if action == "MIX" and len(refs) < 2:
        raise ValueError("MIX_REQUIRES_TWO_OR_MORE_PARENT_REFERENTS")
    if action in {"SELECT", "MODIFY", "MIX"}:
        for ref in result:
            if ref in refs:
                result[ref] = "SELECTED_FOR_NEXT_ROUND"
            elif result[ref] not in {"REJECTED_PRESERVED", "SUPERSEDED_BY_CHILD"}:
                result[ref] = "DEFERRED_PRESERVED"
    elif action == "REJECT":
        for ref in refs:
            result[ref] = "REJECTED_PRESERVED"
    elif action == "REOPEN":
        for ref in refs:
            result[ref] = "ACTIVE"
    elif action == "DEFER":
        for ref in refs:
            result[ref] = "DEFERRED_PRESERVED"
    else:
        raise ValueError(f"UNSUPPORTED_ITERATION_ACTION:{action}")
    return result


def validate_human_actions(actions: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    by_ref: dict[str, set[str]] = {}
    for action in actions:
        if action.get("level") == "ITERATION_STEER" and action.get("referent_binding") == "AMBIGUOUS":
            errors.append(f"ITERATION_STEER_CANNOT_HAVE_AMBIGUOUS_REFERENT:clause={action.get('clause_index')}")
        if action.get("level") == "ITERATION_STEER":
            bound = action.get("bound_referents") or []
            bound_ids: set[str] = set()
            for item in bound:
                if not isinstance(item, dict) or not all(item.get(k) for k in ("ref", "kind", "revision", "lineage_ref")):
                    errors.append(f"ITERATION_STEER_REQUIRES_TYPED_REFERENT:clause={action.get('clause_index')}")
                    continue
                if item.get("kind") == "UNRESOLVED" or item.get("revision") == "UNRESOLVED":
                    errors.append(f"ITERATION_STEER_REQUIRES_RESOLVED_REFERENT:clause={action.get('clause_index')}:{item.get('ref')}")
                bound_ids.add(str(item.get("ref")))
            if set(action.get("referents") or []) != bound_ids:
                errors.append(f"ITERATION_STEER_REFERENTS_MUST_MATCH_TYPED_BINDINGS:clause={action.get('clause_index')}")
            if action.get("route_target") not in {None, "SESSION_ITERATION"}:
                errors.append(f"ITERATION_STEER_ROUTE_TARGET_INVALID:clause={action.get('clause_index')}")
        if action.get("level") in AUTHORITY_ROUTE_BY_LEVEL:
            expected_route = AUTHORITY_ROUTE_BY_LEVEL[str(action.get("level"))]
            if action.get("route_target") != expected_route:
                errors.append(f"AUTHORITY_ACTION_ROUTE_MISMATCH:clause={action.get('clause_index')}:{expected_route}")
        if action.get("action") == "MIX" and len(action.get("referents") or []) < 2:
            errors.append(f"MIX_REQUIRES_TWO_OR_MORE_PARENT_REFERENTS:clause={action.get('clause_index')}")
        for ref in action.get("referents") or []:
            by_ref.setdefault(ref, set()).add(str(action.get("action")))
    for ref, kinds in by_ref.items():
        # Until an explicit sequential-action grammar exists, multiple distinct
        # consequential actions against the same referent are ambiguous.  Fail
        # closed instead of silently using clause order as authority.
        consequential = kinds & ITERATION_ACTIONS
        if len(consequential) > 1:
            errors.append(f"CONFLICTING_HUMAN_ACTIONS_REQUIRE_CLARIFICATION:{ref}:{sorted(kinds)!r}")
    return errors


def apply_human_actions(option_status: dict[str, str], actions: list[dict[str, Any]]) -> dict[str, str]:
    errors = validate_human_actions(actions)
    if errors:
        raise ValueError(";".join(errors))
    result = dict(option_status)
    for item in sorted(actions, key=lambda x: int(x.get("clause_index", 0))):
        if item.get("level") != "ITERATION_STEER":
            continue
        result = apply_iteration_steer(result, str(item.get("action")), item.get("referents") or [])
    return result


def decide_designer_support(
    *, explicit_mode: str = "AUTO", current_session_clear_judgments: int = 0
) -> dict[str, Any]:
    allowed = {"AUTO", "COMPACT", "EXPLAIN", "OFF"}
    if explicit_mode not in allowed:
        raise ValueError(f"INVALID_SUPPORT_MODE:{explicit_mode}")
    if explicit_mode != "AUTO":
        return {"mode": explicit_mode, "fade_basis": "EXPLICIT_USER_REQUEST", "durable_skill_score": None}
    if current_session_clear_judgments >= 2:
        return {
            "mode": "COMPACT",
            "fade_basis": "CURRENT_SESSION_REPEATED_CLEAR_JUDGMENT",
            "durable_skill_score": None,
        }
    return {"mode": "AUTO", "fade_basis": "NONE", "durable_skill_score": None}


def _normalize_scope(scope: str) -> str:
    if scope == "*":
        return scope
    normalized = re.sub(r"[\\/]+", "/", scope.strip())
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    return normalized.rstrip("/") or "/"


def _scope_applies(item_scope: str, active_scope: str) -> bool:
    item = _normalize_scope(item_scope)
    active = _normalize_scope(active_scope)
    if item == "*" or item == "/":
        return True
    return active == item or active.startswith(item + "/")


def validate_context_projection(projection: dict[str, Any]) -> list[str]:
    """Validate a per-session context view without turning it into Project State."""
    errors: list[str] = []
    if projection.get("storage_semantics") != "EPHEMERAL_SESSION_PROJECTION":
        errors.append("CONTEXT_STORAGE_MUST_BE_EPHEMERAL_SESSION_PROJECTION")
    if projection.get("load_policy") != "PROGRESSIVE_DISCLOSURE":
        errors.append("CONTEXT_LOAD_POLICY_MUST_BE_PROGRESSIVE_DISCLOSURE")
    if not projection.get("active_scope"):
        errors.append("CONTEXT_ACTIVE_SCOPE_REQUIRED")
    token_budget = projection.get("token_budget")
    if not isinstance(token_budget, int) or token_budget <= 0:
        errors.append("CONTEXT_TOKEN_BUDGET_MUST_BE_POSITIVE_INTEGER")
    items = projection.get("items")
    if not isinstance(items, list):
        errors.append("CONTEXT_ITEMS_MUST_BE_LIST")
        return errors

    seen_refs: set[str] = set()
    allowed_authority_use = {
        "NON_AUTHORITY_REFERENCE",
        "LOCATOR_ONLY",
        "REREAD_REQUIRED_BEFORE_MUTATION",
        "FORBIDDEN_AS_AUTHORITY",
    }
    for item in items:
        if not isinstance(item, dict):
            errors.append("CONTEXT_ITEM_MUST_BE_OBJECT")
            continue
        missing = [
            key
            for key in (
                "ref",
                "logical_key",
                "source_kind",
                "scope",
                "load_reason",
                "disclosure_level",
                "estimated_tokens",
                "authority_use",
            )
            if item.get(key) in {None, ""}
        ]
        if missing:
            errors.append("CONTEXT_ITEM_MISSING:" + ",".join(missing))
            continue
        ref = str(item["ref"])
        if ref in seen_refs:
            errors.append(f"CONTEXT_DUPLICATE_REF:{ref}")
        seen_refs.add(ref)
        if item.get("disclosure_level") not in CONTEXT_DISCLOSURE_RANK:
            errors.append(f"CONTEXT_DISCLOSURE_LEVEL_INVALID:{ref}:{item.get('disclosure_level')}")
        if not isinstance(item.get("estimated_tokens"), int) or item.get("estimated_tokens", 0) <= 0:
            errors.append(f"CONTEXT_ESTIMATED_TOKENS_INVALID:{ref}")
        if item.get("authority_use") not in allowed_authority_use:
            errors.append(f"CONTEXT_AUTHORITY_USE_INVALID:{ref}:{item.get('authority_use')}")
        if item.get("persistence_target") not in {None, "NONE"}:
            errors.append(f"CONTEXT_ITEM_CANNOT_DEFINE_PERSISTENCE_TARGET:{ref}")
        if item.get("source_kind") == "COMPACTED_CONTEXT":
            if item.get("authority_use") != "FORBIDDEN_AS_AUTHORITY":
                errors.append(f"COMPACTED_CONTEXT_CANNOT_BE_AUTHORITY:{ref}")
            if item.get("rehydrate_before_consequential_mutation") is not True:
                errors.append(f"COMPACTED_CONTEXT_REQUIRES_REHYDRATION_BEFORE_MUTATION:{ref}")
        if item.get("disclosure_level") == "BULK" and item.get("explicit_load") is not True:
            # BULK may exist in the candidate set but is not eligible for automatic loading.
            continue
    return errors


def plan_context_load(projection: dict[str, Any]) -> dict[str, Any]:
    """Select a minimal scoped context pack using progressive disclosure.

    The result is an ephemeral read plan. It is never a persistence carrier or an
    authority decision; compacted items must be rehydrated from owner-native sources
    before consequential mutation.
    """
    errors = validate_context_projection(projection)
    if errors:
        return {"decision": "HOLD_INVALID_CONTEXT_PROJECTION", "errors": errors}

    active_scope = str(projection["active_scope"])
    token_budget = int(projection["token_budget"])
    applicable = [item for item in projection["items"] if _scope_applies(str(item["scope"]), active_scope)]

    # Exact content duplicates do not consume context twice. Prefer the more local
    # scoped copy, then the lower-disclosure-level copy.
    by_content: dict[str, dict[str, Any]] = {}
    without_hash: list[dict[str, Any]] = []
    for item in applicable:
        content_hash = item.get("content_sha256")
        if not content_hash:
            without_hash.append(item)
            continue
        current = by_content.get(str(content_hash))
        if current is None:
            by_content[str(content_hash)] = item
            continue
        item_depth = _normalize_scope(str(item["scope"])).count("/")
        current_depth = _normalize_scope(str(current["scope"])).count("/")
        if item_depth > current_depth:
            by_content[str(content_hash)] = item
    candidates = list(by_content.values()) + without_hash

    def _sort_key(item: dict[str, Any]) -> tuple[int, int, int, str]:
        disclosure = CONTEXT_DISCLOSURE_RANK[str(item["disclosure_level"])]
        required = 0 if item.get("required") is True else 1
        scope_depth = _normalize_scope(str(item["scope"])).count("/")
        return (required, disclosure, scope_depth, str(item["ref"]))

    selected: list[dict[str, Any]] = []
    omitted: list[dict[str, str]] = []
    used = 0
    required_over_budget: list[str] = []
    for item in sorted(candidates, key=_sort_key):
        ref = str(item["ref"])
        if item.get("disclosure_level") == "BULK" and item.get("explicit_load") is not True:
            omitted.append({"ref": ref, "reason": "PROGRESSIVE_DISCLOSURE_NOT_REQUESTED"})
            continue
        cost = int(item["estimated_tokens"])
        if used + cost > token_budget:
            omitted.append({"ref": ref, "reason": "TOKEN_BUDGET"})
            if item.get("required") is True:
                required_over_budget.append(ref)
            continue
        selected.append(item)
        used += cost

    # Scoped instruction fragments are presented root-to-leaf, matching the useful
    # part of Codex's directory-scoped instruction behavior without making them authority.
    selected.sort(
        key=lambda item: (
            0 if item.get("source_kind") == "SCOPED_INSTRUCTION" else 1,
            _normalize_scope(str(item["scope"])).count("/"),
            CONTEXT_DISCLOSURE_RANK[str(item["disclosure_level"])],
            str(item["ref"]),
        )
    )
    return {
        "decision": "COMPACT_OR_NARROW_REQUIRED" if required_over_budget else "READY",
        "selected_refs": [str(item["ref"]) for item in selected],
        "selected_items": selected,
        "omitted": omitted,
        "estimated_tokens": used,
        "token_budget": token_budget,
        "required_over_budget": required_over_budget,
        "authority": "NONE_EPHEMERAL_READ_PLAN_ONLY",
    }


def decide_file_placement(file_fact: dict[str, Any]) -> dict[str, Any]:
    """Choose storage placement without creating a Session-Kernel artifact registry."""
    role = str(file_fact.get("role", "UNRESOLVED"))
    lifecycle = str(file_fact.get("lifecycle", "WORKING"))
    owner_kind = str(file_fact.get("owner_kind", "PROJECT_WORKTREE"))
    size_bytes = int(file_fact.get("size_bytes") or 0)
    threshold = int(file_fact.get("large_binary_threshold_bytes") or REFERENCE_LARGE_FILE_THRESHOLD_BYTES)
    explicit_library = file_fact.get("explicit_library_request") is True
    explicit_full_binary = file_fact.get("explicit_full_binary_library_request") is True
    generated_intermediate = file_fact.get("model_generated") is True and lifecycle in {"TEMPORARY", "WORKING", "INTERMEDIATE"}
    content_sha256 = file_fact.get("content_sha256")
    existing_sha256 = file_fact.get("existing_library_content_sha256")

    if content_sha256 and existing_sha256 and str(content_sha256).lower() == str(existing_sha256).lower():
        return {
            "placement": "REUSE_EXISTING_LIBRARY_REF",
            "library_binary_write": False,
            "reason": "EXACT_CONTENT_ALREADY_PRESENT",
            "authority": "NONE_PLACEMENT_DECISION_ONLY",
        }

    if owner_kind == "EXTERNAL_OWNER" and file_fact.get("external_reference_available") is True and not file_fact.get("materialize_required"):
        return {
            "placement": "EXTERNAL_REFERENCE_ONLY",
            "library_binary_write": False,
            "reason": "KEEP_WITH_EXISTING_EXTERNAL_OWNER",
            "authority": "NONE_PLACEMENT_DECISION_ONLY",
        }

    if explicit_library:
        if (size_bytes > threshold or generated_intermediate) and not explicit_full_binary:
            return {
                "placement": "LIBRARY_INDEX_ONLY",
                "library_binary_write": False,
                "library_index_write_allowed": True,
                "reason": "LARGE_OR_INTERMEDIATE_BINARY_REQUIRES_EXPLICIT_FULL_BINARY_REQUEST",
                "authority": "NONE_PLACEMENT_DECISION_ONLY",
            }
        return {
            "placement": "LIBRARY_UPLOAD_ALLOWED",
            "library_binary_write": True,
            "reason": "EXPLICIT_LIBRARY_REQUEST",
            "authority": "NONE_PLACEMENT_DECISION_ONLY",
        }

    if lifecycle == "TEMPORARY" or role in {"PREVIEW", "READBACK", "TEMP_TEST"}:
        return {
            "placement": "SESSION_OR_PROJECT_DERIVATIVE_CACHE",
            "library_binary_write": False,
            "reason": "DERIVATIVE_OR_TEMP_DEFAULTS_OUT_OF_LIBRARY",
            "authority": "NONE_PLACEMENT_DECISION_ONLY",
        }
    if lifecycle in {"DELIVERABLE", "MILESTONE"} or role in {"PACKAGE", "PRESENTATION"}:
        return {
            "placement": "HANDOFF_EXPORT_WITH_EXISTING_OWNER",
            "library_binary_write": False,
            "reason": "KEEP_HANDOFF_WITH_OWNER_UNLESS_LIBRARY_EXPLICITLY_REQUESTED",
            "authority": "NONE_PLACEMENT_DECISION_ONLY",
        }
    return {
        "placement": "KEEP_WITH_EXISTING_OWNER",
        "library_binary_write": False,
        "reason": "LOCAL_OR_OWNER_NATIVE_IS_DEFAULT",
        "authority": "NONE_PLACEMENT_DECISION_ONLY",
    }


def _cli() -> int:
    parser = argparse.ArgumentParser(description="OLEANDER Co-Design Session Kernel v0.2 reference harness")
    parser.add_argument("text", nargs="?", help="User message to classify")
    parser.add_argument("--active-options", default="", help="Comma-separated active option refs")
    parser.add_argument("--pending-decision", default=None)
    parser.add_argument("--unambiguous-active-ref", default=None)
    args = parser.parse_args()
    if not args.text:
        parser.error("text is required")
    ctx = ClassificationContext(
        active_option_refs=tuple(x.strip() for x in args.active_options.split(",") if x.strip()),
        pending_decision_ref=args.pending_decision,
        unambiguous_active_ref=args.unambiguous_active_ref,
    )
    print(json.dumps(classify_message(args.text, ctx), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

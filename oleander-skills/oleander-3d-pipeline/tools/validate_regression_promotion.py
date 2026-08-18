#!/usr/bin/env python3
"""Validate OLEANDER 3D reference-reproduction regression promotion receipts."""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

DECISIONS = {
    'PROMOTE_OVER_LKG',
    'KEEP_LKG_REJECT_EXPERIMENT',
    'KEEP_LKG_HOLD_EXPERIMENT',
    'REBASE_EXPERIMENT_ON_LKG',
}
LOCK_STATES = {'PASS', 'REGRESSED', 'NOT_COMPARABLE'}
VISUAL_STATES = {'KEEP', 'REVISE', 'REJECT', 'HOLD', 'NOT_RUN'}
SCHEMA_V1 = 'oleander.3d.reference-regression-promotion-receipt.v1'
SCHEMA_V2 = 'oleander.3d.reference-regression-promotion-receipt.v2'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def same_number(a, b, tol=1e-12):
    try:
        return math.isfinite(float(a)) and math.isfinite(float(b)) and abs(float(a)-float(b)) <= tol
    except Exception:
        return False


def validate(d: dict) -> dict:
    required = [
        'schema', 'baseline_revision', 'candidate_revision', 'edit_scope',
        'target_metric_delta', 'regression_locks', 'measurement_method_ids',
        'measurement_comparability', 'promotion_decision', 'visual_review_state',
        'does_not_prove'
    ]
    for key in required:
        require(key in d, f'missing:{key}')
    require(d['schema'] in (SCHEMA_V1, SCHEMA_V2), 'bad:schema')
    require(isinstance(d['baseline_revision'], str) and d['baseline_revision'], 'bad:baseline_revision')
    require(isinstance(d['candidate_revision'], str) and d['candidate_revision'], 'bad:candidate_revision')
    require(d['baseline_revision'] != d['candidate_revision'], 'bad:same_revision')
    require(isinstance(d['edit_scope'], list) and d['edit_scope'], 'bad:edit_scope')
    require(isinstance(d['measurement_method_ids'], list) and d['measurement_method_ids'], 'bad:measurement_method_ids')
    require(d['measurement_comparability'] in ('COMPARABLE', 'NOT_COMPARABLE'), 'bad:measurement_comparability')
    require(d['promotion_decision'] in DECISIONS, 'bad:promotion_decision')
    require(d['visual_review_state'] in VISUAL_STATES, 'bad:visual_review_state')
    require(isinstance(d['does_not_prove'], list) and d['does_not_prove'], 'bad:does_not_prove')

    delta = d['target_metric_delta']
    require(isinstance(delta, dict), 'bad:target_metric_delta')
    for key in ('metric_id', 'baseline', 'candidate', 'direction', 'improved'):
        require(key in delta, f'missing:target_metric_delta.{key}')
    require(delta['direction'] in ('LOWER_IS_BETTER', 'HIGHER_IS_BETTER', 'TARGET_ERROR'), 'bad:target_metric_delta.direction')
    require(isinstance(delta['improved'], bool), 'bad:target_metric_delta.improved')

    locks = d['regression_locks']
    require(isinstance(locks, list) and locks, 'bad:regression_locks')
    seen = set()

    best = None
    if d['schema'] == SCHEMA_V2:
        best = d.get('best_known_gate_baselines')
        require(isinstance(best, dict) and best, 'missing:best_known_gate_baselines')

    for i, lock in enumerate(locks):
        keys = ['id', 'baseline', 'candidate', 'limit', 'status', 'evidence_source']
        if d['schema'] == SCHEMA_V2:
            keys += ['baseline_revision']
        for key in keys:
            require(key in lock, f'missing:regression_locks[{i}].{key}')
        require(lock['id'] not in seen, f'duplicate:regression_lock:{lock["id"]}')
        seen.add(lock['id'])
        require(lock['status'] in LOCK_STATES, f'bad:regression_locks[{i}].status')

        if d['schema'] == SCHEMA_V2:
            require(lock['id'] in best, f'missing:best_known_gate_baselines.{lock["id"]}')
            b = best[lock['id']]
            require(isinstance(b, dict), f'bad:best_known_gate_baselines.{lock["id"]}')
            for key in ('revision', 'value', 'evidence_source'):
                require(key in b, f'missing:best_known_gate_baselines.{lock["id"]}.{key}')
            require(lock['baseline_revision'] == b['revision'], f'weaker_baseline:revision:{lock["id"]}')
            require(same_number(lock['baseline'], b['value']), f'weaker_baseline:value:{lock["id"]}')
            require(lock['evidence_source'] == b['evidence_source'], f'weaker_baseline:evidence:{lock["id"]}')

    if d['promotion_decision'] == 'PROMOTE_OVER_LKG':
        require(delta['improved'] is True, 'unsafe_promotion:target_not_improved')
        require(d['measurement_comparability'] == 'COMPARABLE', 'unsafe_promotion:measurement_not_comparable')
        require(all(x['status'] == 'PASS' for x in locks), 'unsafe_promotion:regression_lock_not_pass')
        require(d['visual_review_state'] == 'KEEP', 'unsafe_promotion:visual_keep_required')
        review = d.get('independent_visual_review')
        require(isinstance(review, dict), 'unsafe_promotion:independent_visual_review_missing')
        require(review.get('independent') is True, 'unsafe_promotion:review_not_independent')
        require(review.get('owner_is_reviewer') is False, 'unsafe_promotion:owner_self_review')
        require(isinstance(review.get('reviewer_role'), str) and review.get('reviewer_role'), 'unsafe_promotion:reviewer_role_missing')
        require(isinstance(review.get('evidence_source'), str) and review.get('evidence_source'), 'unsafe_promotion:review_evidence_missing')

    if any(x['status'] == 'REGRESSED' for x in locks):
        require(d['promotion_decision'] != 'PROMOTE_OVER_LKG', 'unsafe_promotion:regressed_candidate')

    if d['measurement_comparability'] == 'NOT_COMPARABLE':
        require(d['promotion_decision'] in ('KEEP_LKG_HOLD_EXPERIMENT', 'REBASE_EXPERIMENT_ON_LKG'), 'bad:incomparable_decision')

    return d


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: validate_regression_promotion.py RECEIPT.json', file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        d = json.loads(path.read_text(encoding='utf-8'))
        validate(d)
    except Exception as exc:
        print(f'REGRESSION PROMOTION RECEIPT FAIL: {exc}', file=sys.stderr)
        return 1
    print('REGRESSION PROMOTION RECEIPT PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

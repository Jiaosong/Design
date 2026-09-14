# OLEANDER Chat On Steroids Runtime Adapter v0.1

## Role
Chat On Steroids Core is an execution adapter, not an authority source.

## Execution Gate
1. Read PROJECT STATE.
2. Resolve SOURCE AUTHORITY.
3. Resolve CURRENT TASK.
4. Resolve required Skill capability.
5. Execute local action.
6. Generate evidence/receipt.
7. Sync to Git.

## Prohibited
- Promote candidate without review.
- Replace CURRENT without authority.
- Merge unrelated branches.
- Delete superseded assets without archive decision.

## Adapter Outputs
- action log
- changed files
- validation result
- receipt reference

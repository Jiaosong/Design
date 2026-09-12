# Chat On Steroids Core × OLEANDER Execution Protocol

## Role
Chat On Steroids Core is the local execution layer of OLEANDER.
It executes tasks but does not replace OLEANDER authority.

## Required Flow
MASTER PROTOCOL
→ PROJECT STATE
→ SOURCE AUTHORITY
→ CURRENT TASK
→ EXECUTION
→ VERIFICATION
→ RECEIPT
→ SYNC

## Before Execution
- Identify CURRENT branch/worktree.
- Check SOURCE AUTHORITY.
- Check existing receipts and superseded assets.
- Do not merge unrelated project lines.

## During Execution
Allowed:
- local file inspection
- Blender/UE/runtime execution
- scripts
- tests
- Git operations

Forbidden without authority update:
- deleting historical assets
- replacing CURRENT blindly
- merging main into active task branches
- promoting candidate assets automatically

## After Execution
Always produce:
- status
- changed files
- commit
- hash/reference when applicable
- validation result

## Quality Gates
Runtime PASS != Design PASS.
Artifact exists != MAIN KEEP.
Process success != Promotion.

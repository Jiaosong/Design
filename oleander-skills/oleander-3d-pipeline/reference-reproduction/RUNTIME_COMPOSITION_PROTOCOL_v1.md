# Runtime Composition Protocol v1

Status: CURRENT CANDIDATE.

Purpose: keep iterative 3D benchmark runtimes reproducible when a later revision reuses an earlier builder.

## INPUT
- parent runtime/module;
- callable hooks being overridden;
- execution owner namespace/module;
- candidate revision receipt.

## MUST CHECK
1. A runtime override must bind to the namespace/module that actually owns the executed callable.
2. Compile/import success does not prove hook routing. The preflight must assert the final callable identity/revision before Blender build.
3. Nested `exec` namespaces are transitional only. If used, name them explicitly (`outer`, `core`) and persist a runtime-composition receipt.
4. Do not assume a symbol present in a parent source file exists in the child execution namespace after nested composition.
5. Prefer explicit module adapters / dependency injection over string patching or implicit global mutation.
6. Model-quality thresholds and Source controls must not change while fixing runtime routing.
7. Runtime failures are engineering failures; they do not create a design/reference-fidelity judgement.

## ALLOWED
- explicit `outer` declaration namespace + `core` execution namespace during migration;
- callable identity assertions before `main()`;
- gradual refactor of historical benchmark wrappers into importable modules.

## FORBIDDEN
- multi-level anonymous `ns` mutation without ownership documentation;
- patching source text at runtime to redirect a hook;
- changing geometry thresholds to make a runtime fix pass;
- treating Python compile success as proof that Blender will execute the intended revision.

## EVIDENCE
- final callable owners/identities;
- composition revision;
- preflight assertions;
- Blender invocation path;
- engineering PASS/FAIL separate from design state.

## Failure routing
- `FAIL_RUNTIME_HOOK_OWNER_AMBIGUOUS`
- `FAIL_RUNTIME_HOOK_NOT_APPLIED`
- `FAIL_COMPILE_PASS_EXECUTION_MISMATCH`

## 992.2 benchmark
V32 initially compiled and passed the Skill tests but failed at Blender start because V31 itself contained a nested V30 execution namespace. The first V32 wrapper looked for `body_ring30` and `simple_cabin30` in the V31 declaration namespace instead of the V30 core that actually owned `build_loft/run30`. V32 was corrected to explicit `outer`/`core` composition without changing geometry targets or quality thresholds. Future reusable runtimes should migrate away from nested `exec` toward explicit modules/adapters.

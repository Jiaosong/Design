# OLEANDER ↔ Chat On Steroids Update Compatibility Contract v0.1

**Status:** ACTIVE NON-AUTHORITY RUNTIME COMPATIBILITY CONTRACT
**Authority ceiling:** `COMPATIBILITY_OBSERVATION_AND_BOUNDED_REBIND_ONLY`

This contract exists to preserve one invariant: **Chat On Steroids (CoS) remains an independently updatable execution platform; OLEANDER is a compatibility consumer layered on top of it.**

It does not create Project State, Current authority, a checkpoint database, an artifact registry, mutation permission, professional-stage authority, Design KEEP authority or Promotion authority.

## 1. Lifecycle ownership

`COS LIFECYCLE != OLEANDER LIFECYCLE`

- OLEANDER does not own, pin, replace, freeze or downgrade the CoS application version.
- OLEANDER does not patch `Chat On Steroids.exe`, `resources/app.asar`, the CoS installer or updater binaries.
- A CoS update is allowed to happen independently of OLEANDER.
- OLEANDER must adapt to a compatible newer CoS surface rather than forcing CoS back to an older release.

## 2. Stable integration boundary

The persisted CoS configuration contains a small OLEANDER bootstrap. That bootstrap points to:

`00-governance/runtime/OLEANDER_CHAT_ENTRY_RUNTIME.md`

Capability implementations remain outside the bootstrap and are resolved by the current runtime entry. In particular, the bootstrap must not pin a Baidu adapter version or the current Chat→COS capability-bridge implementation.

The currently installed CoS version is an **observation**, never an OLEANDER requirement.

## 3. Post-update compatibility probe

After a CoS update, run:

```powershell
py -3.13 00-governance\runtime\validate_cos_update_compatibility.py
```

The probe observes the current installed CoS surface and checks:

1. CoS executable exists and its file version is readable.
2. CoS updater surface still exists.
3. CoS user config exists and remains parseable.
4. The current OLEANDER stable-bootstrap marker survives completely in the expected config surfaces.
5. CoS Goal/Loop still exposes tool-call readback to the OLEANDER bootstrap.
6. The bootstrap still points only to the dynamic Chat entry rather than capability implementations or a specific CoS binary version.
7. The dynamic Chat entry validates.
8. Resolver and runtime-bridge self-tests pass.
9. Chat→COS local bridge self-test passes.
10. The selected Baidu local stdio runtime passes its own acceptance check.

The probe is compatibility/readback only. `PASS_COS_UPDATE_COMPATIBILITY` does not imply Project State mutation, Current, Design KEEP, professional PASS or Promotion.

## 4. Drift handling

If the newer CoS surface remains compatible:

`COS UPDATE → COMPATIBILITY PROBE → PASS → CONTINUE`

If integration drift is detected:

`COS UPDATE → COMPATIBILITY PROBE → HOLD AFFECTED OLEANDER INTEGRATION ONLY`

The HOLD is scoped to the failed integration surface. It must not block the CoS updater, disable CoS update behavior, require downgrade, or manufacture a second persistence/authority system.

Typical bounded HOLD scopes are:

- `COS_CONFIG_BOOTSTRAP`
- `OLEANDER_RUNTIME_ENTRY`
- `OLEANDER_RESOLVER_RUNTIME`
- `CHAT_COS_LOCAL_BRIDGE`
- `BAIDU_LOCAL_ADAPTER`

## 5. Bounded bootstrap repair

The compatibility validator is read-only by default.

If a CoS update preserves the compatible config schema but removes the OLEANDER bootstrap text, the Human/operator may explicitly run:

```powershell
py -3.13 00-governance\runtime\validate_cos_update_compatibility.py --repair-bootstrap
```

This delegates to the existing `bind_chat_on_steroids_oleander.py --apply` path, which backs up the user config before writing. It does not patch CoS binaries or updater files.

Before that delegation, the validator requires the exact binder-written field shapes to remain compatible: `mcp.instructions` must still be a string; `goal.prompt`, `goal.objectivePrompt` and `goal.loopPrompt` must still be non-empty strings; and `goal.includeToolCalls` must still be boolean. The repair path must not coerce a newly structured CoS field into an old scalar representation.

If any of those field types or the surrounding CoS config schema has changed incompatibly, repair must fail closed **before the binder is called** and leave CoS itself untouched. OLEANDER then adapts/rebinds its integration to the new public configuration/tool surface.

## 6. Proof boundary

A successful probe proves compatibility against the **currently installed and observed CoS surface only**. It does not predict an unreleased future CoS version. Each material CoS update should be followed by the same probe so compatibility drift is detected after the real update rather than guessed in advance.

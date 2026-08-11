# OLEANDER Blender Surface System

Status: `ACTIVE SHARED SURFACE SYSTEM / CONTINUOUSLY UPDATED`

This repository mirror stores the executable/version contract for the shared Blender Surface System. It does **not** claim that the integration `ACTIVE.json` is the unseen original umbrella manifest named by the user as v1.6.

## Resolution policy

- development: resolve the global ACTIVE version;
- controlled render: resolve ACTIVE, then freeze exact hashes in the run manifest;
- promotion/release: pin exact resolved version + hashes;
- if resolved version or ACTIVE manifest hash changes, dependent surface-sensitive visual gates are invalid and must be rerun.

## Evidence boundary

Archetype and texture recipe values are visualization starting points unless upgraded by sample, manufacturer, measurement or calibrated evidence. A plausible Cycles render is not a physical CMF specification.

## Project integration

Projects do not fork global roughness/metallic/texture rules. They provide a role binding and explicit overrides only. XJ01 is the first formal integration under `integrations/xj01/`.

Large model/render assets remain in the canonical Drive asset chain; GitHub stores only contracts, resolver logic, bindings and tests.

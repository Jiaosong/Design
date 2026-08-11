# 2026-08-11｜IP03｜Blender Surface System｜Asset Catalog × Debug Contract × Evidence Calls

**Stacked base:** OLEANDER Blender Surface System v1.16.0  
**Candidate:** v1.17.0  
**Status:** REVIEW

## Scope

v1.17.0 adds no new procedural source family. It adds three governance/execution layers:

1. **Asset Catalog** — stable discovery using catalog UUIDs and functional paths.
2. **Node Group Debug Contract** — canonical naming, interface/debug metadata, persistence and reopen validation.
3. **Evidence-Driven Calls** — Material/Project Calls that permit only evidence-supported parameters and keep unsupported finish/texture/process values blocked.

## Critical behavior

Technique assets do not imply material truth. A valid Material Call can return an empty `technique_chain` when the project evidence says Finish/Texture is closed.

## Initial evidence-backed calls

- XJ01 Iron Anchor: digital `#888C8F` allowed as visualization stimulus; roughness/bump/process blocked or unknown.
- XJ01 PP Field: digital `#D8D5CD` allowed; generic Noise/Bump blocked.
- Timer Housing: roughness `0.55` allowed only as project visualization profile, not measured roughness.

## Runtime Gate

The workflow reconstructs the canonical v1.16 Node Group library in Blender 5.2, assigns catalogs/metadata, saves a v1.17 asset bundle, reopens it in a fresh Blender process and verifies the persisted metadata again.

## Reality boundary

This validates asset discoverability, Node Group interface/debug persistence and evidence-call governance. It does not close measured material, manufacturing, durability, optical, thermal, structural, ecological or user gates.

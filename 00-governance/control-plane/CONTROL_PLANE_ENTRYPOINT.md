# OLEANDER Control Plane Entrypoint

For executable project-control checks, use:

```bash
python 00-governance/control-plane/control_plane.py check <project-control-card.json>
```

This entrypoint is subordinate to current governance and compiles existing rules into execution. It does not redefine Knowledge Architecture, Application Mapping, Project Axis, Case Axis, delivery priority, evidence levels, Artifact Review, Post-Generation Review, PAP, Rights, Reality, Engineering, Human Test or project-specific contracts.

A PASS means only that the supplied card is structurally valid, no current namespace collision was detected by v0.2, the gate profile was resolved, and CB-01 did not block continuation. It is not a design-quality, evidence, physical, rights, engineering or release approval.

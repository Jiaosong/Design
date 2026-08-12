# Automotive v0.11｜R27 Circumferential Wheel-Arch Topology Gate

Status: INITIALIZED

## Objective

Resolve the remaining M5 wheel-zone failure by replacing parameter-only correction with source topology reconstruction.

## Locked Inputs

- R09 wheel/cabin hard points
- R11 non-wheel transverse body tension
- R12 longitudinal interpolation logic
- R18/R20 termination topology
- R25 rounded x-z wheel opening target

## R27 Construction Principle

The wheel opening is treated as a circumferential primary surface system:

`INNER ARCH RING → BLEND RING → SHOULDER TRANSITION RING`

The rings must become part of the same Source mesh as:

`SHOULDER → MID BODY → ROCKER`

No detached wheel-brow geometry is accepted.

## Validation

Machine:
- one connected Source mesh
- no n-gon
- no Boolean
- no global SubD
- stable topology diagnostics

Human M5:
- tire visually contained by body volume
- fender crown grows from shoulder
- front/rear arch continuity acceptable
- no artificial patch reading

M6/M7/M8 remain blocked until Human M5 PASS.

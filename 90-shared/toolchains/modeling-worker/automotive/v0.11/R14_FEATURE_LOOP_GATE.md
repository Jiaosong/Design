# Automotive v0.11 R14｜Source Feature-Loop Gate

Status before execution: `M5 REVISE / WORKING_SOURCE`.

R14 retains the accepted R09 cabin package, R11 transverse tension and R12 PCHIP interpolation, and changes primary construction only:

- wheel-arch inner boundary becomes explicit Source topology;
- fender crown becomes explicit Source feature loop;
- hood/top-edge, shoulder and rocker are explicit longitudinal feature lines;
- front/rear termination uses controlled triangles, no n-gons;
- Source Boolean = forbidden;
- Source SubD = forbidden;
- M6/M7/M8 remains blocked.

Promotion requires Blender 5.2 Machine Gate + post-render Visual QA. This file also triggers the updated R14 workflow on PR #85.

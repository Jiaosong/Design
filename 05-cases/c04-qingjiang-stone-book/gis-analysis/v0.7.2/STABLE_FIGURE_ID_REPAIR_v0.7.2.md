# Stable Figure ID Repair｜v0.7.2

The v0.7 producer package accidentally used `ENV-03` for `Environmental Synthesis`.
That conflicts with the already established environmental figure sequence.

Current IDs:
- ENV-01 = Slope / Aspect
- ENV-02 = Potential Drainage
- ENV-03 = Land Cover Evidence (HOLD until WorldCover AOI pixels)
- ENV-04 = Water History Evidence (HOLD until JRC GSW AOI pixels)
- ENV-05 = Solar / Terrain Radiation Scenarios
- ENV-06 = Current Operations Conflict
- ENV-SYN-01 = Environmental Synthesis

The old `ENV-03 synthesis` files are retained as provenance in the production package under `07_provenance/ID_ERROR__*`.
No valid prior content is deleted.

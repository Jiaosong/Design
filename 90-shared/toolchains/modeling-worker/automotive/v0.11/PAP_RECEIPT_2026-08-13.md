# OLEANDER Automotive v0.11｜PAP Receipt｜2026-08-13

Status: `PERSISTENCE PASS` / `PAP-G0—PAP-G6 PASS`.

Candidate: `R29A｜Shoulder-Fed Monotonic Fender Crown`  
Authority: `MODELING_WORKER_v0.11_CANDIDATE_AUTHORITY`  
Source geometry hash: `d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

## Durable production objects

- Native Blender scene — Drive ID `1KQP_SJU11teCutdBLDSaF1D29aD2Fp2H`; 248,834 bytes; SHA-256 `f8f800360a61392592262f89e3f6a6ca5ec6e76eda9211911530bd257939d8e1`.
- Production ZIP — Drive ID `1xQhmz5_RBwfK5iQFODiIM2jFn_ZGJw4D`; 3,861,986 bytes; SHA-256 `3dd304dd94e6493e01e1a4e436339949cc82851cef1ce007eacbf02f226ef204`.
- Inner checksums — Drive ID `1oYeiOSy5POBPwi_gSda9LsvOGinjA_R5`.
- Production ZIP checksum — Drive ID `1hjkn9NVCA7s03H92tpMe3MHKGB5IY7DJ`.
- Native Blender checksum — Drive ID `1mcZ3OATMPETvM7vQW9BFkajDQ6L39gXv`.
- PAP root folder — Drive ID `1PLXbsvK81vLrfkcukaYD_Ks7P1SmLPk3`.

## Retrieval verification

All uploaded objects above were independently re-materialized from Google Drive. Retrieved byte size and SHA-256 matched the upload-side values exactly. The retrieved production ZIP opened successfully and every file listed in its internal `SHA256SUMS.txt` verified successfully.

The retrieved `.blend` is byte-identical to the M10 scene from run `31623379139`; that exact scene was opened and rendered successfully by Blender 5.2 during M10. Therefore native parse/open integrity is closed by byte identity to the executed scene.

## Interchange authority

`canonical_model = N/A`.

Reason: this benchmark defines the editable Blender Source as Geometry Authority and did not create or validate a separate GLB/STEP/OBJ authority. PAP closure does not invent a new authority after M10.

## Gate result

`PAP-G0 PASS`  
`PAP-G1 PASS`  
`PAP-G2 PASS`  
`PAP-G3 PASS`  
`PAP-G4 PASS`  
`PAP-G5 PASS`  
`PAP-G6 PASS` — GitHub / Notion / Drive receipts reference the same durable object set.

This receipt does not Promote the benchmark by itself. It only removes the persistence HOLD and makes the Candidate eligible for a new explicit Promote Review.

## Cross-system receipt IDs

- Drive manifest: `1STqH_YWQ8o3jR3AzOSctkVdMuGyVmK-P`
- Drive receipt: `1xyWEfsBd2H4Yayj8CxlfKf_fdsxJahoi`
- Notion receipt page: `3bbb86be-5c47-81c0-adf7-f9d8c5f16924`
- GitHub PR: `#85`

Final PAP state: `PERSISTENCE PASS / READY_FOR_EXPLICIT_PROMOTE_REVIEW`.

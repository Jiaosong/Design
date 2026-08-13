# OLEANDER Modeling Worker v0.12｜Automotive E3 R3.3｜PAP Receipt｜2026-08-13

Status: `PERSISTENCE PASS` / `PAP-G0—PAP-G6 PASS` / `SYSTEM PROMOTION NOT AUTHORIZED`.

Candidate: `E3 R3.3 Application Benchmark`  
Object: `SYS-MODELING-WORKER-v0.12-E3-AUTO`  
Authority entering PAP: `WORKING_SOURCE / CANDIDATE`  
Accepted source snapshot commit: `5782c039562e723705b6f46537fea7efa0936b29`

## Accepted application evidence

R3.3 Machine + Human Project/Visual PASS is bound to:
- workflow run `31688935218`;
- artifact `9176833315`;
- artifact digest `sha256:cd608eb82f191df16ccf32be0a28280577d866b70dbd7bdbe84d8351006c1d3f`;
- Human decision GitHub blob `24449ce0bc04814ac646a28fb3e30854cad53986`.

This PAP does not upgrade that benchmark-scope Human PASS into final Automotive styling, Class-A, engineering, manufacturing or release authority.

## Durable production objects

- PAP root folder — Drive ID `1NqK4452BlZom84nX8UdmJh4Ga1GUcrWd`.
- Native editable Blender Source — Drive ID `1n8eDsgPOXc0wp0gv6pY-ECvmFciD8MhU`; 192,912 bytes; SHA-256 `3d49b6ece3272781e42521e2420f609fc5b608387d1ab9a166cecbdbb5ddf430`.
- Compiled Surface Source JSON — Drive ID `1On4uzCHGuQCwFYLNzqcORRc0FwdKgAf6`; 8,471 bytes; SHA-256 `31af6bcb389c1e50868ff9a72e605cb1c1d8e84a81bcf9e326277ea0e55081ac`.
- Production ZIP — Drive ID `1kMD04ebeVuJMyQWmuqE8osBTa-iTrE6O`; 4,185,723 bytes; SHA-256 `96a4601b458c9c6bf6872627ebf176ce04db50d5b386b44b3917aaaf4d1ef7b4`.
- Inner checksums — Drive ID `1lHlLUyedWOFB2YVPQdHZE-Li3Nik5ivi`.
- Production ZIP checksum — Drive ID `14n7H11yTICGNY9N4mD7o6kzhpRhoUZy4`.
- Native Blender checksum — Drive ID `1IrMwsrv8azHGZ2-eNPsxpmk2Fir0ni5J`.

## Independent retrieval verification

The native Blender object and Production ZIP were independently re-materialized from Google Drive after upload.

Retrieved native source:
- byte size = 192,912;
- SHA-256 = `3d49b6ece3272781e42521e2420f609fc5b608387d1ab9a166cecbdbb5ddf430`;
- exact match to the upload-side R3.3 Blender scene.

Retrieved Production ZIP:
- byte size = 4,185,723;
- SHA-256 = `96a4601b458c9c6bf6872627ebf176ce04db50d5b386b44b3917aaaf4d1ef7b4`;
- ZIP open/extraction = PASS;
- every entry in the embedded `checksums/SHA256SUMS.txt` = PASS;
- embedded native Blender source hash = the same `3d49b6ec…f430`.

## Source snapshot

The production package embeds `SOURCE_SNAPSHOT.json`, binding Candidate evidence to GitHub commit `5782c039…6b29` and the exact R3/R3.2/R3.3 architecture, correction, executable and Human decision blobs. It also embeds the compiled R3.3 Surface Source JSON and the full R3.3 CI artifact.

## Interchange authority

`canonical_model = N/A`.

Reason: this benchmark validates editable Blender Source + compiled Surface Source JSON as Candidate source objects. No GLB/STEP/OBJ interchange authority was created or validated, and PAP does not invent one after Human QA.

## Gate result

`PAP-G0 PASS` — asset inventory.  
`PAP-G1 PASS` — upload-side local integrity and production ZIP checksum verification.  
`PAP-G2 PASS` — durable Google Drive upload.  
`PAP-G3 PASS` — independent provider retrieval.  
`PAP-G4 PASS` — retrieved byte/hash identity + ZIP/internal checksum verification.  
`PAP-G5 PASS` — persistence manifest binds source, evidence, hashes, provider IDs and authority boundary.  
`PAP-G6 PASS` — GitHub / Notion / Drive receipts reference the same durable object set.

This receipt removes the persistence HOLD only. It does not Promote v0.12. The next allowed action is the existing v0.3 semantic/freshness contradiction scan followed by an explicit human Promote Review.

## Cross-system receipt

- Notion PAP receipt: `3bbb86be-5c47-814d-b440-c3be9f9dd999`.
- GitHub PR: `#91`.
- GitHub manifest: `90-shared/toolchains/modeling-worker/automotive/v0.12/PAP_MANIFEST_v1.json`.
- GitHub receipt: `90-shared/toolchains/modeling-worker/automotive/v0.12/PAP_RECEIPT_2026-08-13.md`.
- Drive manifest ID: `1-Xc9Wm0rrQS2ZMV1MoHB6aGbY8Plzfi6`.
- Drive receipt ID: `15LntbAtSn0TrM_Fn7HycaZEtT91Rh9Bk`.

Final PAP state: `PERSISTENCE PASS / READY_FOR_CONTRADICTION_SCAN_AND_EXPLICIT_PROMOTE_REVIEW`.

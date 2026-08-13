# OLEANDER Modeling Worker v0.12｜Automotive E3 R3.3｜PAP Receipt｜2026-08-13

Status: `PERSISTENCE PASS` / `PAP-G0—PAP-G6 PASS` / `SYSTEM PROMOTION NOT AUTHORIZED`.

Candidate: `E3 R3.3 Application Benchmark`  
Object: `SYS-MODELING-WORKER-v0.12-E3-AUTO`  
Authority state entering PAP: `WORKING_SOURCE`  
Design state entering PAP: `CANDIDATE`  
Accepted source snapshot commit: `5782c039562e723705b6f46537fea7efa0936b29`

## Accepted application evidence

R3.3 Machine + Human Project/Visual PASS is bound to workflow run `31688935218`, artifact `9176833315`, artifact digest `sha256:cd608eb82f191df16ccf32be0a28280577d866b70dbd7bdbe84d8351006c1d3f`, and Human decision blob `24449ce0bc04814ac646a28fb3e30854cad53986`.

This PAP does not upgrade benchmark-scope Human PASS into final Automotive styling, Class-A, engineering, manufacturing or release authority.

## Durable production objects

- PAP root: Drive `1NqK4452BlZom84nX8UdmJh4Ga1GUcrWd`.
- Native editable Blender Source: Drive `1n8eDsgPOXc0wp0gv6pY-ECvmFciD8MhU`; 192,912 bytes; SHA-256 `3d49b6ece3272781e42521e2420f609fc5b608387d1ab9a166cecbdbb5ddf430`.
- Compiled Surface Source JSON: Drive `1On4uzCHGuQCwFYLNzqcORRc0FwdKgAf6`; SHA-256 `31af6bcb389c1e50868ff9a72e605cb1c1d8e84a81bcf9e326277ea0e55081ac`.
- Production ZIP: Drive `1kMD04ebeVuJMyQWmuqE8osBTa-iTrE6O`; 4,185,723 bytes; SHA-256 `96a4601b458c9c6bf6872627ebf176ce04db50d5b386b44b3917aaaf4d1ef7b4`.
- Checksum set: Drive `1lHlLUyedWOFB2YVPQdHZE-Li3Nik5ivi`, `14n7H11yTICGNY9N4mD7o6kzhpRhoUZy4`, `1IrMwsrv8azHGZ2-eNPsxpmk2Fir0ni5J`.

## Independent retrieval verification

Native Blender and Production ZIP were independently re-materialized from Drive. Native size/hash and ZIP size/hash were exact matches; the retrieved ZIP opened successfully and every embedded `checksums/SHA256SUMS.txt` entry passed.

## Gate result

`PAP-G0 PASS` — asset inventory.  
`PAP-G1 PASS` — local integrity.  
`PAP-G2 PASS` — durable upload.  
`PAP-G3 PASS` — independent provider retrieval.  
`PAP-G4 PASS` — retrieved byte/hash identity plus ZIP/internal checksum verification.  
`PAP-G5 PASS` — persistence manifest binds source, evidence, hashes, provider IDs and authority boundary.  
`PAP-G6 PASS` — GitHub / Notion / Drive receipts reference the same durable object set.

## Cross-system receipt

- Notion PAP receipt: `3bbb86be-5c47-814d-b440-c3be9f9dd999`.
- GitHub PR: `#91`.
- Drive manifest: `1-Xc9Wm0rrQS2ZMV1MoHB6aGbY8Plzfi6`.
- Drive receipt: `15LntbAtSn0TrM_Fn7HycaZEtT91Rh9Bk`.

PAP removes the persistence HOLD only. It does not Promote v0.12. Next allowed action is the existing v0.3 semantic/freshness contradiction scan followed by explicit human Promote Review.

Final PAP state: `PERSISTENCE PASS / READY_FOR_CONTRADICTION_SCAN_AND_EXPLICIT_PROMOTE_REVIEW`.

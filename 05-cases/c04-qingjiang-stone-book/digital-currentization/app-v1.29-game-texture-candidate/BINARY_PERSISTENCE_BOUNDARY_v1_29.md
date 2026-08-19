# Binary Persistence Boundary — C04 App v1.29

The four WebP texture binaries are present in the local recoverable handoff and verified by byte count + SHA-256, but the current GitHub connector write path cannot ingest the mounted binary files without re-serializing them through text/base64 in this execution surface. A direct binary-write attempt was rejected as a persistence route because it did not reproduce the local Git object hash.

Therefore GitHub does **not** claim to contain byte-equivalent WebP texture files for v1.29.

Local binary source of truth for this candidate:
- `tx_paper.webp` — 22,680 bytes — SHA256 `116c5edf82f2ea87b75977ba2802608bd1e756a3ac42d76ea88df1456b5c3a8a`
- `tx_ink.webp` — 55,224 bytes — SHA256 `be8ce12917df71365d0facebc28727f82f216d05179f523b26d6228299583956`
- `tx_water.webp` — 108,620 bytes — SHA256 `07e9eaeefae4012486c950bada1f0d81c3ce8ec2e2bfb2bf292df45b99e110f6`
- `tx_deep.webp` — 68,220 bytes — SHA256 `04a489541b0e3c8174fba77226c57e8f9194d3e65b2a9a811b962f7d2e9d98b1`

Complete local package:
`C04_QINGJIANG_APP_v1_29_GAME_TEXTURE_CANDIDATE.zip` — 6,657,528 bytes — SHA256 `af377a8d4d9bb88fcd20f79fe69c8502510b4903fd5251744d07ba2d53365799`.

This boundary is deliberate: `repository text carrier ≠ binary persistence ≠ Design PASS`.

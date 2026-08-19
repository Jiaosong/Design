# C04 Qingjiang App v1.29 — Game Texture Candidate

Leading App candidate on PR #255. Successor of v1.28; v1.28 is retained as `SUPERSEDED / HISTORY` provenance.

## Material delta
The user-facing problem addressed here is insufficient game/world atmosphere. v1.29 does **not** solve that by restoring neon/glow, glass HUD cards, points, rewards, or a second map. It adds:
- screen-specific ink/paper material texture;
- behavior-linked material response across `SEEK / APPROACH / FOCUS / ENTER / REVEAL / WITHDRAW / RETURN`;
- a restrained exploration-state cue on route-context screens;
- brush-ring focus on existing source-bound route anchors;
- an ink-sheet reveal behavior for R06;
- deeper blue-black ink atmosphere for R13 while preserving `PLAY OFF / BODY FIRST`.

## Authority preserved
- `ROUTE-03 = LOCKED CURRENT`; no new route/path/node geometry.
- v1.26 Product/Journey/IA/Service architecture inherited.
- v1.27 `TODAY / ROUTE / MY BOOK / SERVICE` + route-child architecture inherited.
- v1.28 CH14 P01–P07 family language inherited: Landscape First, editorial hierarchy, role-bound color, no neon/glow.
- Texture remains subordinate to Landscape / Route / Return / Safety.

## Texture claim boundary
Four local WebP assets are `AI-GENERATED TEXTURE ASSET / NON-EVIDENCE / REPLACEABLE`. They are not Qingjiang site imagery and do not prove route, GPS, live status, safety, field condition, or cultural fact. See `TEXTURE_ASSET_MANIFEST_v1_29.json` and `BINARY_PERSISTENCE_BOUNDARY_v1_29.md`.

## Source recovery
`BUILD_FROM_V1_28.py` consumes the sibling v1.28 exact-source reconstruction and applies `GAME_TEXTURE_PATCH_v1_29.css` plus bounded HTML/JS mutations.

Expected reconstructed Git blob hashes:
- `index.html` → `3f228c90122c8b546ca71a1092ef5c5cc2320ef6`
- `app.css` → `4b1c1407c5487a57aa3d1d44d06c9349e960b515`
- `app.js` → `9a4b61f8cad07f4878d7707016fc4d9ab997bfc1`

The four local WebP binaries are required for the full material appearance; the current GitHub text-write surface does not claim byte-equivalent binary persistence for them.

## Runtime facts
- 390×844 and 430×932: document width equals viewport width; no recorded JS/page errors.
- minimum visible button target ≈ 44px after repair;
- keyboard route pan delta = 40px;
- seven screens expose material texture layers;
- Reduced Motion reports 0 running animations.

First-pass readback found a ~30px `contextClose`; it was repaired to the 44px baseline and the route-child rail was raised to 44px.

## Local handoff
- ZIP `C04_QINGJIANG_APP_v1_29_GAME_TEXTURE_CANDIDATE.zip` — 6,657,528 bytes — SHA256 `af377a8d4d9bb88fcd20f79fe69c8502510b4903fd5251744d07ba2d53365799`
- Portable HTML `C04_QINGJIANG_APP_v1_29_GAME_TEXTURE_CANDIDATE_PORTABLE.html` — 431,011 bytes — SHA256 `eb924d2eda9acbafdf3c2a924b42f6f945fc3f1a932522aa3d5e6068b7188cf0`
- 390 contact — SHA256 `0de5a14277a4cc741f7dea23975894f600e412aa578a788e2cd117d3938e4565`
- 430 contact — SHA256 `47fce11c98644770d6c5a3c56f356601c37de91a0a47ba2c41d888cc00746a57`

## Gate
`CANDIDATE / INDEPENDENT FINISHED-PIXEL REVIEW PENDING / NO_PROMOTION`.

Runtime/texture/source correctness does not equal Professional Design PASS.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN`.

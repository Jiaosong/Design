# C04 CH01 v1.5｜Actual Pixel Readback

- Desktop: `6/6 @ 1920×1080`; scrollWidth=1920; errors=0; raster images=0.
- Mobile: `6/6 @ 390×844`; scrollWidth=390; errors=0; raster images=0.
- Grayscale derivative: generated and reopened.
- 50% far-read derivative: generated and reopened.
- P04 first v1.5 readback exposed a wrong-direction Return arrow; the semantic arrow was corrected to point from the decision rail into the Return override field, then desktop/mobile were fully rerendered.

Reconstructable GitHub source:
- `index.html` = layered source using unchanged `../v1.4/style.css` + `style-v1.5.css`.
- `index.layered.html` local SHA256 `8060fb49c0f08378afb71ca3d1e1ac073ae7f0ea15de623895415ed3e9758998`.
- `style-v1.5.css` local SHA256 `5f6599b10138f1e144b8128b8fb0ca32838e19a61e73d29d7084bd39ad27a2dc`.
- persisted v1.4 base stylesheet SHA256 `cb4c415ba24a3e1264c02743c912cc5c9d509ee1614aeea9a9c38967e3015a5d`.

Rendered evidence hashes:
- desktop contact `2d5d61d81d23cafcdb4a946a0b96697da24970d2a0542b54acf070111c2f405d`
- mobile contact `1888e59953b22f6f9c50f172dc2428af7fc48218d0cf17207dfa155bae404905`
- grayscale contact `8723227d6e32c5af3d1a064d7ac6ec0b91ba2de6f8c5b2d7418ce439be059797`
- 50% contact `7b1ca9f72405cda5924cc5b237f6eceb80030bc4135ef7fc835f3e409214b509`
- runtime JSON `b3cec9adece226a59046fee9b6d4be47ac50e2caa5a4764f872adb4d37f4fd6f`

Execution/readback evidence is not Professional Design PASS.
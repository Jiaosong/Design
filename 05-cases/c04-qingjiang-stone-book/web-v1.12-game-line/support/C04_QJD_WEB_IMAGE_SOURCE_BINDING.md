# C04｜QJ-D v1.1 Web Image Source Binding

Purpose: remove runtime dependence on unstable external image transport while preserving the selected C04/QJ-D visual authority.

Source Authority / canonical Drive readback:
- `QJ-D__PUBLIC-DISPLAY__v1.1/01_HERO_KEEP_QJ-D_v1.1_1920x1080.png` — Drive file id `151BBYqWMK7yHyxyAoCWMsOP2i3zEg3lh`, 1920×1080, source bytes 2,294,010.
- `QJ-D__PUBLIC-DISPLAY__v1.1/02_R06_LANDSCAPE_FIRST_KEEP_WITH_HOLD_1920x1080.png` — Drive file id `1Md7iDG0pzweLhjZKuMylgP5x8SIe1DwQ`, 1920×1080, source bytes 3,313,809.

Web derivatives are transport/display derivatives only. They do not replace Drive Source Authority and do not grant Design KEEP, browser PASS, FIELD, engineering or release status.

Planned local Web derivative identities:
- `assets/qj_hero_keep_v11.webp` — 1600×900, WebP quality 76, expected bytes 96,702, SHA256 `69003b841d386e3aeeccf06bddac002dcde1344298342bd32c9590375e7843b6`.
- `assets/qj_r06_landscape_keep_v11.webp` — 1600×900, WebP quality 76, expected bytes 162,290, SHA256 `1fe1ffb271c5f995a1445958bc592f9bdaf86331038d49982f23dd1da0bbca40`.

Binding rule:
- Hero / general Qingjiang image slots → `qj_hero_keep_v11.webp`.
- Open landscape / R06 landscape slots → `qj_r06_landscape_keep_v11.webp`.
- R13 remote concept remains its existing explicit concept asset.

Truth boundary: `SOURCE AUTHORITY != WEB DERIVATIVE != BROWSER PASS != DESIGN KEEP != FIELD PASS`.

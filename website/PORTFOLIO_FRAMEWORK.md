# OLEANDER Website｜Portfolio Framework v0.2

> Project-specific website expression specification. This does not replace the OLEANDER Master Protocol; it defines how the public portfolio edits and presents existing project evidence.

## 1. Public reading spine

The public portfolio must read in this order:

1. **Cover / OLEANDER** — short identity and relationship proposition.
2. **Selected Works / First Encounter** — large editorial crops from real project assets.
3. **C02 Daylily** — full visual case.
4. **C03 The Light Collection** — full visual case.
5. **C01 一脉广渡** — Research Case; do not fabricate an equivalent photographic hero.
6. **Project Index / Archive** — secondary index for relation / practice / archive reading.
7. **Research / Approach Divider** — explicit transition from work to explanation.
8. **Research Question → Relations → Evidence** — methods and evidence after the work.
9. **Practice** — OLEANDER working method.
10. **About** — portrait-led identity and position.
11. **Contact**.

Rule: **work must be encountered before the system that explains it.**

## 2. Case anatomy

C02 / C03 visual cases use a content-led sequence rather than a method-led sequence.

### C02 Daylily

- Opening / Project + proposition + Presentation Crop
- 01 Context
- 02 Position
- 03 Identity
- 04 CMF + Touchpoints
- 05 Space + Experience
- Full boards remain available inside the chapters and in the detail viewer.

### C03 The Light Collection

- Opening / Project + proposition + Presentation Crop
- 01 Context
- 02 Concept
- 03 Color
- 04 Material + Finish
- 05 Series
- Full boards remain available inside the chapters and in the detail viewer.

### C01 一脉广渡

C01 remains a Research Case. Its relationship / evidence / translation structure is retained because it is the content of the project rather than a generic website template.

## 3. Image-role hierarchy

The website no longer treats all images the same.

### A. Presentation Crop

Purpose: first perception, composition, atmosphere, product / spatial emphasis.

Locations:
- Selected Works / First Encounter
- C02 opening
- C03 opening
- future case-to-case transitions

Rules:
- cropping is intentional and required;
- desktop default: **16:10**, with **3:2** available when the source supports it;
- mobile default: **4:5**, with a separately judged focal position;
- use `object-fit: cover` only in a presentation-crop slot;
- no scale animation on typography-heavy imagery;
- clicking the crop opens the original complete source image.

### B. Full Board

Purpose: complete design reading, typography, diagrams, evidence and layout relationships.

Locations:
- project chapters;
- evidence / system boards;
- detail viewer.

Rules:
- never crop;
- preserve source aspect ratio;
- `object-fit: contain`;
- no forced fixed height, 4:5 frame or scale-softening;
- the board can be smaller than a hero but must remain legible or openable in the viewer.

### C. Detail Crop

Purpose: isolate material, typography, CMF, signage, construction or a single visual decision.

Rules:
- generated only when the detail itself carries a clear design judgment;
- recommended ratios: **4:5 / 1:1 / 3:2**;
- must be paired somewhere in the case with the complete source board or source image;
- a detail crop must never replace the evidence source.

## 4. Crop-quality budget

Current public project JPEG boards are mostly around 1800 px wide. Cropping therefore has a display-size budget.

| Role | Minimum retained source area | Recommended displayed width |
|---|---:|---:|
| Hero / Opening Crop | 70–85% | 1100–1450 px |
| Editorial Crop | 45–75% | 650–950 px |
| Detail Crop | 25–50% | 360–680 px |
| Full Board | 100% | 1200–1600 px |

Rule: **the harder the crop, the smaller the displayed derivative must be.**

CSS cannot recover source detail. Do not use AI upsampling or sharpening to manufacture evidence quality. If a PDF / AI / 2× export exists, replace the web source with that higher-quality authority.

## 5. Visual-anchor rule

Every presentation crop must define a visual anchor rather than defaulting to center-center.

Check:
- first-read subject;
- face / product / spatial focal point;
- logos and essential typography;
- 5–8% breathing zone around critical content;
- no accidental tangent with the viewport edge;
- desktop and mobile anchors reviewed separately.

## 6. Desktop rhythm

Desktop portfolio rhythm should be:

**quiet cover → large crop → secondary crop → full case → full board / detail alternation → next case → archive → research divider → research / evidence → portrait → contact**

Do not repeat the same 50/50 layout across consecutive screens. One viewport should have one dominant visual center.

## 7. Project Index role

`Project Index / Archive` is not the landing experience. It exists after the complete cases so a reader can re-index the work by relation, practice or archive state.

Its controls must remain visually secondary and must not resemble a dashboard.

## 8. Quality gates

Before merge, verify:

- 1440×900 and 1920×1080 desktop reading;
- 390 / 430 mobile crop anchors;
- no page-level overflow at 200% reflow equivalent;
- Presentation Crop = `cover`;
- Full Board = source ratio + `contain`;
- no scale-softening on typography-heavy boards;
- cropped images open the complete original in the viewer;
- C02 / C03 remain image-led;
- C01 remains explicitly Research Case;
- Project Index remains after the cases;
- Research / Evidence remain after the work.

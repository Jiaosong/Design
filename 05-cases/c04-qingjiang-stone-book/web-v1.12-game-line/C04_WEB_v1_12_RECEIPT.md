# C04 Web｜公开作品结构重构｜2026-08-23

Project: `PRJ-C04-QINGJIANG-SHISHU`

State: `PUBLIC PORTFOLIO REFRAME / SOURCE-BOUND / FIELD OPEN / NO_PROMOTION`

## Current structure

当前 Web 不再使用“载体页报告”作为结构基础。

公开 `index.html` 由 18 个作品段落直接构成：

1. Hero / real Qingjiang
2. Original material + existing design assets
3. Design question
4. Design idea / three viewing scales
5. Design thinking / attention handoff
6. Task workflow
7. Thirteen Imprints / optional reading system
8. Digital companion / Game Map
9. Key scene contrast
10. Physical / Body / Sensory
11. Brand + Memory
12. Technology application route
13. AI + 3D creation process
14. Technical proof / detail development
15. Innovation points
16. Technical difficulties
17. Design evolution / professional judgment
18. Final system / Return

## Bottom-right supplemental reading

主作品阅读之外，新增固定于右下角的 `补充资料 / SUPPLEMENT` 入口。默认折叠，不增加主页面数量；打开后以右下角浮层承载第二阅读层。

补充资料分为 7 组：

1. 原资产：真实清江、路线关系、关键场景、数字资产、技术装配资产；
2. 设计创意：水上看整体 / 空中看关系 / 山中看细节；
3. 设计思路：景观先出现 / 路线拥有主权 / 场景决定信息密度 / Return 贯穿全程；
4. 技术应用路线：Source → Relation → Scene → 3D / Drawing → Prototype → Web / Motion；
5. 任务流程：原资产读取 → 空间问题 → 设计命题 → 并行探索 → 场景测试 → 原型与3D → 技术深化 → 作品整合；
6. 创新点与技术难点：路线与内容解耦、注意力设计、无手机完整体验、跨媒介一致性、AI幻觉控制、户外实体技术约束；
7. AI + 3D 创作过程：SOURCE → AI EXPLORE → READBACK → 3D → DRAWING → DETAIL。

抽屉使用现有项目资产缩略图和 live HTML/CSS/JS，不新增生成图。桌面固定右下角；移动端改为底部抽屉。支持 ESC / 背景点击关闭和 reduced-motion。

## Removed from current working structure

- legacy carrier framework file;
- carrier-sequence integration map;
- legacy carrier package metadata;
- retired carrier injection script;
- chapter/page authoring IDs as public navigation logic;
- repeated report-template reading;
- production-state strings as public headlines.

Historical commits retain provenance. They are not current runtime structure and do not participate in current navigation, validation, or presentation logic.

## Public presentation rule

Current runtime begins from the actual work:

`REAL PROJECT ASSETS → DESIGN QUESTION → IDEA / THINKING → SYSTEM / EXPERIENCE → TECHNOLOGY / PROCESS → AI + 3D → PROOF → INNOVATION / DIFFICULTY → EVOLUTION → FINAL SYSTEM`

The bottom-right supplemental layer deepens this reading without replacing or duplicating the main narrative.

Original project assets remain the first source of visual evidence. Formal presentation text remains live HTML / SVG text.

## AI + 3D boundary

`REAL SOURCE / CONSTRAINT → AI CONCEPT EXPLORATION → GEOMETRY READBACK → 3D RELATION / BODY SCALE → PLAN / SECTION / ASSEMBLY → DETAIL / MATERIAL / MAINTENANCE`

AI supports concept exploration, atmosphere, composition and experience-direction testing. It does not establish surveyed geometry, engineering dimensions, structure/safety, or field validation.

## Validation

Static validation now requires:
- 18-section primary narrative unchanged;
- retired report-structure files remain absent;
- bottom-right supplement trigger present;
- 7 supplement categories present;
- existing source assets bound into the supplement;
- six-stage AI + 3D process present;
- mobile drawer rules and ESC close behavior present.

GitHub source readback confirms the supplement code is present. A local Node execution was attempted but the local container could not resolve `raw.githubusercontent.com`; therefore no local-runtime PASS is claimed from that attempt.

## Truth boundary

Research-grade design remains distinct from field and engineering validation. The public interface expresses this in readable language rather than internal governance codes.

Browser finished-pixel review remains separate from source/static validation.

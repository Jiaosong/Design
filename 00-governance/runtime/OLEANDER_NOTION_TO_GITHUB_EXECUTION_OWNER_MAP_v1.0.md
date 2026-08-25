# OLEANDER Notion → GitHub Execution Owner Map v1.0

Status: **ACTIVE CURRENT**  
Decision date: **2026-08-18**  
Scope: **all OLEANDER knowledge / method / practice objects requiring executable production**  
Upstream knowledge authority: **Notion Current Root Authority + live Registry**  
Execution registry: **GitHub `oleander-skills/REVIEW.md` + candidate specialist skills**

## 0｜Purpose

This map answers one question only:

> **After a Current Notion object has been resolved correctly and the required native output is known, which existing GitHub execution owner should perform the work?**

It does **not** redefine Notion taxonomy, page names, Domain identity, Canonical ID, L0–L7 position, Canonical Parent/Children, Source relations, Method relations, Project relations, evidence state, or governance state.

Current sequence under Resolver v1.2:

`NOTION CURRENT ROOT → LIVE REGISTRY → CANONICAL ID / ROLE / L0–L7 / PRIMARY DOMAIN / METHOD FAMILY → REQUIRED NATIVE OUTPUT → EXECUTION OWNER MAP → SKILL CAPABILITY CONTRACT → MINIMUM SUFFICIENT OWNER SET / DAG → EXECUTION`.

## 1｜Core separation

### Notion owns
- knowledge identity and Canonical ID;
- current L0–L7 position;
- `主领域 / 关联领域`;
- `知识角色`;
- `方法家族`;
- `Canonical Parent｜层级上位 / Canonical Children｜层级子级`;
- Source / Method / Project / Related / Supersession relations;
- governance / evidence / maturity state.

### GitHub execution owner owns
- an executable production workflow;
- runtime/tool selection inside its contract;
- native artifact creation within declared authority;
- machine/runtime checks belonging to that capability;
- typed handoff to another execution owner when output medium changes.

A GitHub owner name is **not** a Notion Domain and must never change the Notion object's name or location.

## 2｜Valid routing outcomes

1. **INSTALLED OWNER** — installed reusable Skill directly owns execution.
2. **CANDIDATE OWNER** — exact candidate specialist is useful; candidate status remains explicit.
3. **CANDIDATE BODY** — bounded specialist body such as Technical Drawing.
4. **RUNTIME / TOOL ADAPTER** — Notion TOOL/runtime rule, not a new design Skill.
5. **NO_DEDICATED_OWNER** — no current GitHub Skill honestly owns the whole capability.

`NO_DEDICATED_OWNER` is valid and does not authorize automatic Skill creation.

## 3｜Current execution owners

| Execution owner | State | Owns |
|---|---|---|
| `oleander-research` | INSTALLED | evidence acquisition, source comparison, precedents, interviews, research synthesis, decision research |
| `oleander-data-viz` | INSTALLED | data analysis visualization, charts, maps, GIS presentation, analytical diagrams |
| `oleander-3d-pipeline` | INSTALLED | 3D geometry pipeline, exchange, axonometric/model outputs, render/archive workflow |
| `oleander-story-and-board` | INSTALLED | narrative synthesis, boards, reports, decks, brand stories, film story structure |
| `oleander-delivery-qc` | INSTALLED | non-destructive package/export/release QC |
| `oleander-motion` | INSTALLED | motion design, state-transition motion, procedural/interactive motion, Reduced Motion |
| `oleander-ui-visual-composition` | CANDIDATE | digital UI visual hierarchy and screen composition |
| `oleander-ui-interaction` | CANDIDATE | interaction behavior, state logic, screen interaction prototype |
| `oleander-route-wayfinding-ui` | CANDIDATE | route/network/state wayfinding interface |
| `oleander-game-ui` | CANDIDATE | game-like interface execution |
| `oleander-mobile-game-ui` | CANDIDATE | mobile game-like interface execution |
| `OLEANDER Technical Drawing` | CANDIDATE BODY | plans, sections, nodes and technical graphic translation within its current implementation boundary |

`oleander-game-ui-stack` remains an aggregation/router/test surface, not an extra independent owner.

## 4｜Owner selection order

Resolve in this order:

1. explicit Current project execution owner when Current Authority assigns one;
2. exact specialist required by the native output;
3. installed reusable owner whose capability contract directly owns the task;
4. method-family / Current-domain fallback;
5. `NO_DEDICATED_OWNER`.

After owner resolution, Resolver v1.2 applies `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1` and the `MINIMUM SUFFICIENT OWNER SET` rule. Do not expand to a full multi-Skill chain by default.

## 5｜Knowledge-role routing

| Notion knowledge role | Default execution route |
|---|---|
| `SOURCE` | `oleander-research`; downstream owner may consume evidence |
| `EVIDENCE` | `oleander-research`; visualization/geometry may hand off |
| `CASE` | `oleander-research`, then output-specific handoff |
| `THEORY` | `NO_DEDICATED_OWNER`; resolve from task/output |
| `METHOD` | resolve by `方法家族 + required native output`; METHOD ≠ Skill |
| `TOOL` | runtime/tool adapter; TOOL ≠ Skill |
| `PRACTICE / OUTPUT` | resolve by actual project + output medium |
| `INDEX` | `NO_DEDICATED_OWNER`; discovery structure, not production capability |

## 6｜Method-family → execution fallback

| 方法家族 | Execution owner rule |
|---|---|
| 研究取证 | `oleander-research` |
| 综合洞察 | `oleander-research`; data graphic → `oleander-data-viz`; narrative → `oleander-story-and-board` |
| 问题定义 | `oleander-research`; communication artifact may hand off to `oleander-story-and-board` |
| 策略决策 | `NO_DEDICATED_OWNER`; research/story are support |
| 创意生成 | resolve by actual output medium |
| 原型表达 | UI → UI specialists; 3D → `oleander-3d-pipeline`; motion → `oleander-motion`; board/story → `oleander-story-and-board`; data → `oleander-data-viz` |
| 分析建模 | data/GIS → `oleander-data-viz`; 3D geometry → `oleander-3d-pipeline`; otherwise `NO_DEDICATED_OWNER` |
| 评估验证 | release/export QC → `oleander-delivery-qc`; UI expert review → candidate UI specialist + independent review; user validation → `NO_DEDICATED_OWNER` |
| 设计转译 | translated artifact determines owner |
| 交付治理 | `oleander-delivery-qc`, with producing owner as support |
| AI协同 | AIG/runtime governance first, then downstream execution owner |

`oleander-delivery-qc` must never substitute for Design Review, usability testing, user validation, field validation or professional design judgment.

## 7｜Required native output → owner

| Required native output | Primary execution owner |
|---|---|
| research brief / evidence matrix | `oleander-research` |
| chart / map / GIS / analytical data diagram | `oleander-data-viz` |
| 3D model / geometry / axonometric / render pipeline | `oleander-3d-pipeline` |
| board / report / deck / narrative | `oleander-story-and-board` |
| release package / export inspection | `oleander-delivery-qc` |
| motion / state animation | `oleander-motion` |
| UI visual composition | `oleander-ui-visual-composition` **CANDIDATE** |
| UI interaction prototype | `oleander-ui-interaction` **CANDIDATE** |
| route / wayfinding interface | `oleander-route-wayfinding-ui` **CANDIDATE** |
| game UI | `oleander-game-ui` **CANDIDATE** |
| mobile game UI | `oleander-mobile-game-ui` **CANDIDATE** |
| plan / section / node / technical drawing | `OLEANDER Technical Drawing` **CANDIDATE BODY** |
| brand identity system | `NO_DEDICATED_OWNER` |
| product / CMF specification | `NO_DEDICATED_OWNER` |
| service / experience system | `NO_DEDICATED_OWNER` |
| generic strategy framework | `NO_DEDICATED_OWNER` |

A `NO_DEDICATED_OWNER` capability may still be executed by a controlled minimum-sufficient combination of existing owners for suboutputs.

## 8｜Current-domain fallback

- Research / user research / evidence → `oleander-research`
- Information / data / GIS → `oleander-data-viz`
- Motion / media → `oleander-motion`; story support as needed
- Digital / web / interaction → choose candidate UI owner by required native output
- Architecture / spatial → 3D=`oleander-3d-pipeline`; technical drawing=`Technical Drawing` candidate; GIS/data=`oleander-data-viz`
- Brand / visual → `NO_DEDICATED_OWNER`; output-specific story/UI/motion support
- Product / material / CMF → `NO_DEDICATED_OWNER`; output-specific 3D/QC/story support
- Service / experience → `NO_DEDICATED_OWNER`; output-specific research/story/UI support
- Human factors / usability / accessibility → `NO_DEDICATED_OWNER`; route by actual research/UI/QC task

Domain fallback is never a replacement for live Notion Domain identity.

## 9｜Machine routing result

Each resolver run emits, at minimum:

```json
{
  "notion_object_id": "...",
  "canonical_id": "...",
  "knowledge_role": "METHOD",
  "primary_domain": "...",
  "method_family": ["..."],
  "required_native_output": "...",
  "primary_execution_owner": "oleander-data-viz",
  "owner_state": "INSTALLED",
  "supporting_execution_skills": [],
  "evidence_for_route": ["current Notion identity", "required native output", "Current GitHub owner registry"],
  "does_not_prove": "METHOD validation, Skill promotion, Design PASS or Field truth"
}
```

This routing result becomes input to the Capability Contract and, if needed, the Multi-Skill DAG Contract.

## 10｜Hard guards

- Notion Canonical ID / Domain / Role / relations remain upstream.
- Execution owner never changes Notion naming or physical Registry location.
- `NO_DEDICATED_OWNER` does not trigger automatic Skill creation.
- Candidate owner remains candidate.
- One execution owner may serve many Notion METHODs/Domains.
- One METHOD may call several execution owners across different outputs.
- Delivery QC ≠ Design Review ≠ user validation.
- `MINIMUM SUFFICIENT OWNER SET` precedes DAG expansion.
- Owner mapping does not prove METHOD validity, Design PASS, field/engineering truth, rights clearance or promotion.

## 11｜Relationship to Current contracts

Read together with:

- `OLEANDER_NOTION_CURRENT_ARCHITECTURE_BINDING_v1.0.md/.json`
- `OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.md/.json`
- `OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.md/.json`
- `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.md/.json`
- `OLEANDER_EXECUTION_RECEIPT_v1.0.md/.json`
- `oleander-skills/REVIEW.md`

Architecture binding answers **where and what the Notion object is**.  
This owner map answers **who may execute the required native output**.  
Capability/DAG contracts answer **what the owner may do and which minimum set actually runs**.  
Resolver v1.2 answers **the execution order**.

# OLEANDER Notion → GitHub Execution Owner Map v1.0

Status: **ACTIVE CURRENT**  
Decision date: **2026-08-29**  
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
| `oleander-design-process` | INSTALLED | design goal framing, evidence-to-design relation synthesis, option-space generation, prototype-fidelity selection, spatial/product/service/system design reasoning, design critique/root-cause repair, validation/presentation handoff, decision memory and change propagation |
| `oleander-ui-visual-composition` | CANDIDATE | digital UI visual hierarchy and screen composition |
| `oleander-ui-interaction` | CANDIDATE | interaction behavior, state logic, screen interaction prototype |
| `oleander-route-wayfinding-ui` | CANDIDATE | route/network/state wayfinding interface |
| `oleander-game-ui` | CANDIDATE | game-like interface execution |
| `oleander-mobile-game-ui` | CANDIDATE | mobile game-like interface execution |
| `OLEANDER Technical Drawing` | CANDIDATE BODY | plans, sections, nodes and technical graphic translation within its current implementation boundary |

`oleander-design-process` installation is the 2026-08-29 promotion closure recorded by Current `SKILL_REGISTRY_v1.1.json`, `REVIEW.md` and its local/aggregate Capability declarations. It does **not** grant upstream source truth, specialist technical validation, final presentation KEEP, field truth, engineering/manufacturing approval or human-test PASS.

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
| `CASE` | `oleander-research`, then output-specific handoff; design reasoning may route to `oleander-design-process` |
| `THEORY` | `NO_DEDICATED_OWNER`; resolve from task/output |
| `METHOD` | resolve by `方法家族 + required native output`; METHOD ≠ Skill |
| `TOOL` | runtime/tool adapter; TOOL ≠ Skill |
| `PRACTICE / OUTPUT` | resolve by actual project + output medium |
| `INDEX` | `NO_DEDICATED_OWNER`; discovery structure, not production capability |

## 6｜Method-family → execution fallback

| 方法家族 | Execution owner rule |
|---|---|
| 研究取证 | `oleander-research` |
| 综合洞察 | `oleander-research`; design consequence/option reasoning → `oleander-design-process`; data graphic → `oleander-data-viz`; narrative → `oleander-story-and-board` |
| 问题定义 | `oleander-design-process`; research evidence → `oleander-research`; communication artifact may hand off to `oleander-story-and-board` |
| 策略决策 | resolve by decision type; `oleander-design-process` owns design decision framing/trade-off execution when the decision changes a design object; generic business strategy remains `NO_DEDICATED_OWNER` |
| 创意生成 | `oleander-design-process` owns option-space reasoning; the native artifact specialist owns medium-specific execution |
| 原型表达 | `oleander-design-process` selects minimum valid test fidelity; UI/3D/motion/board/data specialist owners execute the required native medium |
| 分析建模 | data/GIS → `oleander-data-viz`; 3D geometry → `oleander-3d-pipeline`; spatial/product/service/system reasoning → `oleander-design-process`; otherwise `NO_DEDICATED_OWNER` |
| 评估验证 | design crit/root-cause repair → `oleander-design-process`; release/export QC → `oleander-delivery-qc`; UI expert review → candidate UI specialist + independent review; user validation → `NO_DEDICATED_OWNER` |
| 设计转译 | `oleander-design-process` owns evidence-to-design relation translation; native medium ownership remains downstream |
| 交付治理 | `oleander-delivery-qc`, with `oleander-design-process` and producing owner as support when needed |
| AI协同 | AIG/runtime governance first, then downstream execution owner |

`oleander-design-process` and `oleander-delivery-qc` must never substitute for specialist technical proof, usability testing, user validation, field validation or an independent professional design verdict where required.

## 7｜Required native output → owner

| Required native output | Primary execution owner |
|---|---|
| research brief / evidence matrix | `oleander-research` |
| design reasoning / analysis / option space | `oleander-design-process` |
| spatial / product / service / system design process | `oleander-design-process` |
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
| service / experience system | `oleander-design-process` |
| generic strategy framework | `NO_DEDICATED_OWNER` |

A `NO_DEDICATED_OWNER` capability may still be executed by a controlled minimum-sufficient combination of existing owners for suboutputs.

## 8｜Current-domain fallback

- Research / user research / evidence → `oleander-research`
- Information / data / GIS → `oleander-data-viz`
- Motion / media → `oleander-motion`; story support as needed
- Digital / web / interaction → `oleander-design-process` for design reasoning; candidate UI owners by required native output; motion/data support as needed
- Architecture / spatial → `oleander-design-process` for design reasoning; 3D=`oleander-3d-pipeline`; technical drawing=`Technical Drawing` candidate; GIS/data=`oleander-data-viz`
- Brand / visual → `NO_DEDICATED_OWNER`; `oleander-design-process` may support design reasoning; output-specific story/UI/motion support
- Product / material / CMF → `oleander-design-process` may own product/form/role reasoning; specialist CMF material proof/final specification remains outside its authority; 3D/QC/story support by output
- Service / experience → `oleander-design-process`; research/story/UI support by required output
- Human factors / usability / accessibility → resolve by task; `oleander-design-process` may translate evidence into design variables but cannot claim user/human validation

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
  "primary_execution_owner": "oleander-design-process",
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
- Installed design-process ownership does not grant specialist technical proof, final presentation KEEP, field/manufacturing/engineering truth or human-test PASS.
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

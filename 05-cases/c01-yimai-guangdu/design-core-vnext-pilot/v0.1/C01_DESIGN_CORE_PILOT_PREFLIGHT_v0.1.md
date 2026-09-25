# C01 设计核心 vNext 试点预检

**状态：候选试点预检；不改变 C01 Current、证据等级、专业阶段或设计结论。**  
**核对基线：GitHub main@6a52a5c5d9a94b71746466417404cf57e4e4b08f；Notion C01 canonical 页面截至 2026-09-19 15:08 UTC 的可读内容。**  
**问题：**在已有真实证据和原生资产约束下，能否让设计者重开问题、混合方向，并在未测量几何条件下继续可逆的设计探索，而不制造第二套治理门槛？

## 1 现有能力与接入点

| vNext 意图 | 现行承载 | 本轮判断 |
| --- | --- | --- |
| 多种问题解释与方案谱系 | `00-governance/design-intelligence-routing-and-review-v1.0.md` 的 Design Intelligence Packet；`oleander-design-process` 的 Frame、Diverge、Converge、Attack | 已有方案比较与设计问题。缺少“全部候选答错题”后的显式重开记录及人的选择理由进入下一轮的回归用例。 |
| 不完整资料下继续 | `oleander-design-process` 的 evidence/unknown map、Variable Budget；Computational Option Space Extension 的范围与敏感性 | 机制已有。需要用 C01 的 remote proxy 证明可逆关系级探索与受阻结构/通行/许可决定分开。 |
| 人类判断与原生交付 | 现有 Design Review、Design Quality、Native Artifact、Execution Receipt 与人的 Design KEEP | 不增设 G0–G5 状态或自动选择器；记录人的重开/混合理由，使用现有 Owner 与 Review。 |
| 自主进化与 Skill 整合 | `OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json`、现有 Skill Resolver | 仅在重复真实失败得到比较证据后提出 Evolution Candidate；本轮不新建 Skill 或晋级 Current。 |

这次对前一版实施规划作一个接入修正：其中 G0–G5 只可作为试点观察项，不能变成与已有 Project Gate、Design Review、DQ、专业阶段及 EV0–EV7 并列的门槛。

## 2 C01 已知事实与限制

- Notion 项目入口：[PRJ-C01-YIMAI-GUANGDU Canonical Project Narrative](https://app.notion.com/p/3a7b86be5c4781afba31c99aaff324c5)；现行 P01–P06 顺序为 `P01 WORLD → P02 RELATION CUTS → P03 INTERVENTION → P05 DEEP NODES → P04 EXPERIENCE → P06 OPERATION`。
- GitHub [C01 README](../../README.md) 记录 A/B/C 与 Reality Gate；[remote proxy consumption](../../architecture-remote-proxy-consumption/v0.1/C01_ARCH_REMOTE_PROXY_CONSUMPTION_v0.1.json) 允许关系级现场与外部流线探索，明确没有测量路宽、标高、室内净尺寸，也没有结构、消防、无障碍或施工通过。
- Notion C01 页面顶部（2026-09-19）将表示层上限写为 `SOURCE-BOUND / RELATION-LEVEL / E2 UNCHANGED / RG2 NOT RUN / FIELD_OBSERVED=0 / FIELD_MEASURED=0 / NO PROFESSIONAL PASS`。同页较早的重置段落把项目级证据边界写为 E0–E1，且说明旧图中的 E2 不是项目级状态。**两处层级/时间含义尚待项目证据 Owner 核定；本试点不自行选择一个全项目 E 级别。**本轮统一限于“来源绑定的关系级设计假设”，不提升现场或专业主张。
- 既有 R0-C01/C02/C03 和牌坊 A/B/C 是历史/当前各自有范围的候选，不自动等同于“是否需要新建学习空间”这一新问题的三条独立解。旧“一脉多渡/四渡”名称可以隐藏以检验设计是否独立成立，但保留作为来源与历史，不删除。

## 3 本轮已落地的最小切片

在既有 `evals/golden/skills.jsonl` 增加三个专门回归用例：`SK-DES-029` 测全部方向被否定后的重开与“可不新建”；`SK-DES-030` 测人的混合理由、双亲谱系和非永久偏好；`SK-DES-031` 测 remote proxy 下的设计包络、敏感性与局部 HOLD。它们沿用现有 AI Eval Harness 的 `required_outputs/blockers/pass_rule`，不创建新 harness 或新 Skill。

这些用例是**行为规格和回归输入**，不是模型执行 PASS，更不证明 C01 设计已 KEEP。需按已有 harness 执行真实模型/工具版本并记录结果，再由独立设计批评审查原生作品。

## 4 下一步原生试点及决定点

1. 在 C01 现有 P01 世界任务中固定一份 source-bound 事实母体和 proxy 引用；先制作可编辑的关系级 P01 原生工作对象并做实际读回，保留源、推导、假设分层。C01 项目页已将它列为下一 native production object，本预检不抢写替代世界。
2. 基于同一事实母体提出至少两种真正不同的**问题解释**，并比较“不新增建筑 / 可逆附着介入 / 独立体量或其他方向”是否回答同一问题。数量随事实变化；不得将三稿当作硬指标。含建筑方向只到可逆关系级原型，不给无依据尺寸或建造结论。
3. 对每条保留方向提供同尺度原生平剖或关系图、最强反证、影响的未知量、重新取证条件和清晰的差异；同时展示一条原方案尚未充分覆盖的方向。借用现有 Comparison-First 与设计过程 Skill。
4. 请设计负责人在看原生对比后作“选择、修改、混合、否定、重开”之一及理由；把理由作为下一轮约束与反例输入。**当前没有这个人的新决定，不能伪造 Steering Event。**
5. 完成 actual readback、独立 Design Crit 和现有专业/证据边界回读后，才比较旧流程与试点。重复失败时才用既有 Evolution Candidate 契约提出方法候选；不由本页直接变更 Current。

## 5 本轮未证实

未获取 2026 现场测绘、许可/地方共审、真实参与者测试、P01 新原生世界或独立 Design KEEP。工作区不能用 Git 凭据直接克隆仓库；本候选通过已连接的仓库接口独立分支提交，CI 与 exact-head 状态必须在 PR 上读回。

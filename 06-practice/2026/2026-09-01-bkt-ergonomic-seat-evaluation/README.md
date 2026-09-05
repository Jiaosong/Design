# PRAC-BUSINESS-2026-WS-02｜BKT 人体工学护腰坐姿椅｜人机工程学尺寸评价

Status: WIP / REVIEW PENDING  
Project Axis: P3 Workstream  
Parent P2: `PRAC-BUSINESS-2026｜Business Practice 2026`  
Workstream Code: `BKT-ERGO-EVAL`  
Governance: `00-governance/README.md` — Governance v1.1.1 ACTIVE  
Practice Root: `06-practice/`  
Notion P3 Registry: https://app.notion.com/p/3ceb86be5c478116a9d4d0c11db3df13?pvs=204  
Runtime Tracker: https://github.com/Jiaosong/Design/issues/471  

> Naming repair 2026-09-01: current authority is `PG-30 → PRAC-BUSINESS-2026 → PRAC-BUSINESS-2026-WS-02`. Archived `PRJ-BKT01-*` stubs are provenance only. This is a course / practice evaluation and does **not** represent a BKT official project or commercial collaboration.

## 1. Goal

完成一份可直接提交的人机工程学产品尺寸评价作业，并区分：已确认产品事实、官方/零售主张、第三方报道、人体尺寸证据、本项目分析推论、待验证问题与已冻结结论。

核心问题：**BKT 人体工学护腰坐姿椅的关键接触尺寸与成年用户坐姿人体尺寸之间是否形成可辩护的人机工程学匹配，其支撑逻辑、局限与优化方向是什么？**

## 2. Scope / Boundary

- 评价对象：BKT 人体工学护腰坐姿椅；已见型号名：加大款、超大款。
- 当前已提供整体尺寸：`420 × 340 × 315 mm`。
- 产品按“便携式腰背—骨盆辅助支撑产品”评价，不按完整办公椅全部参数评价。
- AI 生成尺寸图、坐姿图、功能分区图属于解释性 Artifact，不是人体实验或压力测试证据。
- AGR、专利、材料、检测及零售适用范围在原始证据未审阅前不自动升级为本项目验证结论。

## 3. OLEANDER Runtime

Current Loop: Exploration  
Design State: EXPLORE  
Current Gate: `G1｜Evidence`  

`Read → Frame → Evidence Baseline → Define Measurement Objects → Compare → Reject unsupported claims → Candidate Evaluation → Report Integration → Post-Generation Review`

G1 保持 CURRENT；当前证据结构已细化，但有效接触尺寸 / 型号映射与最终数字源核验仍未关闭。

## 4. Internal Decision Objects

1. Product Facts & Source Boundary — `PARTIAL CLOSE / MEASUREMENT SEMANTICS OPEN`
2. Anthropometric Evidence Dataset — `PARTIAL CLOSE / CORE DATASET CANDIDATE`
3. Dimension Fit Evaluation — `CANDIDATE / FINAL FIT BLOCKED`
4. Posture & Support Mechanics — `LOGIC PARTIAL CLOSE / FIGURE REVIEW PENDING`
5. Issues / Optimization / Final Report — `REPORT REWRITE READY`

这些均为本 P3 内部 Decision Objects，不创建额外 P3 Registry 行。

## 5. Product Dimension Semantics

Known overall dimensions:

- `W_OUT = 420 mm`
- `H_OUT = 340 mm`
- `D_OUT = 315 mm`

Required effective-contact dimensions before final fit judgment:

- `W_HIP_EFF` — 有效臀部承托宽度
- `D_HIP_EFF` — 有效臀部/大腿前后承托深度
- `H_LUMBAR_APEX` — 坐姿基准面至腰部主凸点/主要支撑中心高度
- `W_LUMBAR_EFF` — 腰部主要支撑区有效宽度
- `H_BACK_EFF` — 有效背部支撑上缘高度

`315 mm` 不得直接改写为传统座椅“座深”；`420 mm` 不等于有效臀宽；`340 mm` 不等于腰托高度。

## 6. Anthropometric Evidence Baseline

Primary standards:

- `GB/T 10000—2023｜中国成年人人体尺寸` — 现行，2024-03-01实施；替代 GB/T 10000—1988 / GB/T 13547—1992。
- `GB/T 5703—2023｜用于技术设计的人体测量基础项目` — 现行，2023-12-01实施；用于测量项目定义和方法。

Working 18–70 years seated dataset (mm), from a 2026 ergonomics textbook reproduction of GB/T 10000—2023; final source check still required:

| Measurement | Female P5 | Female P50 | Female P95 | Male P5 | Male P50 | Male P95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 坐姿臀宽 | 308 | 348 | 393 | 308 | 346 | 388 |
| 坐姿臀-腘距 | 416 | 459 | 503 | 427 | 472 | 518 |
| 坐姿肩高 | 521 | 570 | 617 | 560 | 611 | 664 |
| 坐姿颈椎点高 | 581 | 628 | 675 | 622 | 675 | 726 |

`坐姿腰点高` 已定位到中国标准化研究院公开调查中的测量定义，但当前百分位数据仍 OPEN；旧稿的“150–250 mm”不得继续作为冻结数据。

## 7. Candidate Fit Decisions

### Width｜420 mm

18–70岁坐姿臀宽 P95：女性393 mm、男性388 mm。420 mm作为**整体宽度**相对女性P95只多27 mm（约13.5 mm/侧），相对男性P95多32 mm（约16 mm/侧）。

Decision: `CONDITIONALLY PLAUSIBLE / NOT PASS`。

原因：`W_HIP_EFF` 未测；侧翼、壳体、泡棉边缘都可能减少实际可用宽度。

### Depth｜315 mm

坐姿臀-腘距：女性 P5–P95 = 416–503 mm；男性 = 427–518 mm。

Decision: `NON-COMPARABLE AS STANDARD SEAT DEPTH`。

315 mm 是辅助承托体整体深度，不能按完整椅面座深直接判 PASS/FAIL，也不能据此写“避免膝窝压迫”。

### Height｜340 mm

坐姿肩高 P5：女性521 mm、男性560 mm，均显著高于340 mm。

Decision: `LOW/MID-BACK SUPPORT CLASSIFICATION SUPPORTED`。

该比较可证明产品不是完整肩背高靠背，但不能证明腰托中心位置正确；`H_LUMBAR_APEX` 仍 OPEN。

## 8. Posture / Causal Boundary

Product-direct:

- 背 / 腰 / 骨盆 / 臀部实际接触区的支撑反力；
- 接触面积与局部压力分布方式；
- 在侧翼真实接触时，对部分横向位移的限制。

Conditional / indirect:

- 骨盆后倾趋势；
- 腰椎曲线维持；
- 躯干前倾与偏坐；
- 久坐舒适性。

Not controlled by product alone:

- 座高；
- 膝角；
- 足部着地；
- 桌面 / 扶手 / 显示器高度；
- 头颈位置。

现有坐姿图必须按该边界重审。

## 9. External BKT Evidence

公开第三方测评页面已定位到 BKT 护腰坐姿椅加大款 / 超大款的2025测评，并报道广州海关技术中心、上海大学力学实验中心等测试；页面列出报告编号：

`W02610210010 / 1225009428 / 1225009422 / SHZ24040219-E`

Evidence state: `THIRD-PARTY REPORTED / ORIGINAL REPORT NOT YET REVIEWED`。

因此可记录“存在公开报道的力学/压力测试”，但不得在原报告未审阅时写具体降压百分比或外推所有用户/型号。

## 10. Evidence-driven Optimization

Priority order:

1. `Measurement & Fit` — 先补有效承托尺寸、腰托中心高度与型号映射；
2. `Adjustability if proven necessary` — 只有覆盖不足被证实时再提出高度/前后/曲率调节；
3. `Seat compatibility` — 实物/场景确认滑移后再提出防滑或固定结构；
4. `Material comfort` — 热湿问题需验证后再进入通风孔、网布等；
5. `Pressure sensor / APP` — Future concept only，不作为本课程核心优化。

## 11. Final Report Rule

Final judgment language:

- `CONFIRMED`
- `CONDITIONALLY SUPPORTED`
- `OFFICIAL / RETAIL CLAIM`
- `THIRD-PARTY REPORTED`
- `OPEN / NOT VERIFIED`

删除旧稿中的无条件：

- “符合人体工程学设计原则”；
- “420 mm满足不同体型成年人”；
- “315 mm避免膝窝压迫”；
- 未知腰托中心时的“腰部支撑位置合理 / 五星”；
- 无热湿测试时的“透气性一般”。

Current candidate conclusion:

> 基于现有外廓尺寸与成人坐姿人体数据，BKT产品的尺度与低/中背辅助支撑定位具有一定一致性；但有效接触尺寸和腰托中心高度尚未闭合，因此当前只能形成条件性人体工学评价，不能把整体外廓尺寸直接等同于人体适配尺寸。

## 12. Immediate Next Step

1. Review / correct the three existing analysis figures against the causal boundary.
2. Build final Word-ready anthropometric and fit tables using the candidate dataset with explicit evidence language.
3. Rewrite the Word report, then run `POST-GENERATION REVIEW` before final submission.

# Phase R1-A · Priority-0 独立 AI 盲审汇总

- 阶段：R1-A（Priority 0 · 风险题）
- 审查轮次：`audit_round = 1`
- 基线 commit（被审查内容）：`68531fd`
- Registry：`audits/registry.jsonl`（40 行）
- 批次：`audits/batches/batch_001.md`（G1+G2, 20 题）、`audits/batches/batch_002.md`（G3+G4, 20 题）
- 独立证据：`tmp/audit_g1..4/`（4 子代理）、`tmp/audit_verify/verify_items.py`（主审交叉复算）

---

## 1. 审查范围与方法

### 1.1 Priority-0 定义（40 题筛选条件）

由 `scripts/build_audit_priority_queue.py` 依下列风险信号筛入：
- `solution_status ∈ {derived, disputed, uncertain, unsolvable}`；
- `answer.confidence ≠ high`；
- `ocr_confidence = low`；
- `reconstructed: true` 的两题（DS-2025-14、DS-2026-15）——**仅审标签/来源/隔离**，不作为历史真题答案审查。

P0 = 40，P1 = 88（2023–2026 其余），P2 = 262（核心长期考点），P3 = 271（剩余）。共 661。

### 1.2 两阶段盲审协议（严格执行）

- 阶段 A：仅读 `真题/<year>/*.md` + `真题/<year>/imgs/*.png` + `考试大纲/2027...md` + 教材约定，独立给出题意/答案/推导/复杂度/歧义。结论先固化于子代理目录 `blind_notes.md`。
- 阶段 B：之后才读 `solutions/<year>/<id>.md`，比较「独立结论 vs 现有解析」，禁止反向。
- 主审在 4 子代理之上按 §8 独立执行修复；关键主张（判定树、活动表 l 列、双散列 ASL、Huffman WPL、排序第一趟条件）由 `tmp/audit_verify/verify_items.py` 二次独立复算。

### 1.3 纪律执行

- 未修改 `review.human_review_status / human_review_rounds / last_human_review`（40/40 保持 `pending / 0 / null`）；
- AI audit 状态独立存于 `audits/registry.jsonl`，不回写 front matter `review` 块；
- 状态调整未机械批量：DS-2021-15（uncertain→derived 建议）、DS-2016-01（verified→disputed 建议）仅登记不执行。

---

## 2. 结果分布

| audit_status | 数量 | 题目 |
|---|---|---|
| pass | 25 | DS-2007-31、DS-2016-12、DS-2016-20、DS-2016-38、DS-2016-39、DS-2007-30、DS-2014-39、DS-2020-36、DS-2022-28、DS-2025-23、DS-2026-04、DS-2005-02、DS-2005-13、DS-2005-20、DS-2006-10、DS-2014-27、DS-2014-28、DS-2014-47、DS-2017-05、DS-2019-08、DS-2024-22、DS-2006-20、DS-2006-25、DS-2025-14、DS-2026-15 |
| minor_issue | 11 | DS-2015-45、DS-2021-32、DS-2006-39、DS-2018-31、DS-2021-15、DS-2021-30、DS-2023-19、DS-2021-02、DS-2023-13、DS-2016-01、DS-2024-18 |
| **major_issue** | **3** | **DS-2015-01、DS-2022-06、DS-2022-22** |
| unresolved | 1 | DS-2006-35 |

- `requires_human_attention = true`：**17**（占 42.5%）
- `answer_agreement = false`：1（DS-2006-35，unresolved 而非确认错）
- 修复动作 `fixed:/improved:`：**14 题**文件级修改（含 2 道 reconstructed 的 source_type 更新）

### 按 issue 类型（可多标签重叠）

| 类型 | 数量 | 说明 |
|---|---|---|
| source_issue | 19 | 题面回忆版缺参/图歧义/口径未定（多数为 disputed/uncertain/unsolvable 题的固有属性，解析已诚实披露） |
| confidence_issue | 4 | fm `solution_status` 与 `answer.confidence`、`ocr_confidence`、`§12` 声明不自洽（DS-2021-15 显著） |
| code_issue | 1 | DS-2022-06 PreThread 缺 rtag 保护（major） |
| taxonomy_issue | 1 | DS-2026-15 topic 名短名（属仓库级命名规范债，id 本身合法） |
| 答案级错误 | 1（=unresolved） | DS-2006-35 无法判定；**未发现被误标为「已解决」而实际答案错的题** |

---

## 3. 三个 major_issue 详解

### 3.1 DS-2022-22（2022 选择 22 · 折半查找判定树）

- **错误定位**：`solutions/2022/DS-2022-22.md` L100–106 分层判定表左半区混用 ceil/floor，导致 18 结点中 5 个错位（5→4、7→6、6→5、8→7、4→8）。
- **性质**：核心推导（判定树构造）错误；§9 条1 派生结论「最坏 4,13,18」应为「8,13,18」；§9 条5「第 3 层 2,7,11,16」应为「2,6,11,16」；§5 步4（L77）同错。
- **独立证据**：`verify_items.py` 按「mid = (low+high)/2 下取整」重跑 → L2[4,14]/L3[2,6,11,16]/L4[1,3,5,7,10,12,15,17]/L5[8,13,18]。
- **答案未受影响**：查 15 需 4 次（路径 9→14→16→15），ASL=64/18 不变。
- **修复**：4 处 SearchReplace；§12 L196「已程序枚举交叉验证」表述适用范围需人工复核（其枚举只覆盖比较次数、未覆盖分层表）。
- **状态保持**：`solution_status: disputed`（下取整 vs 上取整答案 4 vs 2 差异属教材口径，已披露）。

### 3.2 DS-2022-06（2022 选择 6 · 中序线索化剩余空域）

- **错误定位**：原 `PreThread` 递归函数在访问 `T->rchild` 前无 `rtag` 保护。
- **性质**：代码 bug（穷举证据：n≤7 全部 429 棵根左空树中，无保护版 **378 棵无限递归**；有保护版 197 棵根左空树剩余空域恒为 2）。
- **修复**：加 `if (T->rtag == 0)` 保护 + §"算法正确性说明" L160；`answer.confidence` medium→high；消除 L203/L204 自相矛盾；L190 通用结论「剩余空域 = 0~2 个」改为「非空树 1~2（末结点右域必空）／空树 0」。
- **残留**：`metadata/questions.jsonl` `answer_confidence` 仍 medium → 需 `rebuild_all.py` 同步；`validate_repository.py` L61–75 比对项不含 `answer_confidence`（**QA 覆盖缺口**，属仓库级议题，登记不修）。

### 3.3 DS-2015-01（2015 选择 1 · 算法时间复杂度）

- **错误定位**：原文件 `solution_status: verified`，且以四处「选项归谬」论证 D（把大 O 当作某点数值比较，逻辑错误）。
- **性质**：过度确信 + 逻辑错误 + 双读法缺失。
- **修复**：`verified → disputed`；删除四处无效归谬；诚实并列 C（规模变量 O(mn)）/D（常量 O(1)）双读法不强行择一；登记 `reports/disputed_questions.md` 并更新计数（5→6）。
- **残留**：`metadata/questions.jsonl` `solution_status` 仍 verified → 需 `rebuild_all.py` 同步（唯一 1 处 status 漂移）；命题本意（D vs C）人工裁定。

---

## 4. 关键 minor_issue（客观修复）

| 题号 | 客观错误 | 修复 |
|---|---|---|
| DS-2018-31 | 活动表 8 个关键活动行 `l` 列印 vl(头) 而非 vl(头)−w，与同行 l−e=0 自相矛盾 | l 列改：a5=0/a6=0/a14=3/a16=7/a19=13/a20=21/a22=30/a24=33 |
| DS-2023-19 | L194 表 1989 探测 6 次但 L196/L200 用 7，含 1989 的 ASL 写 18/7 | 统一 6 → **17/7≈2.43**；L229 反事实更正（h2=7 时 9679 仍落 5） |
| DS-2021-30 | §9.3 L249 漏一位旁注 85（91−3−4=84） | 85→84 |
| DS-2021-32 | §11 L123 条件「首元素是全局最大者之一」错误（反例 5,3,1；本题 12 非全局最大） | 改为「a₂ 为全表最小且 a₁>a₂」并补反例与自证 |
| DS-2021-02 | §12 L164 教材依据「第 9 章 排序」章级错引（第 9 章是查找） | 改「第 10 章 内部排序」并按印次差异删具体小节号 |
| DS-2023-13 | 关联题 DS-2023-12 答案引用错把其「误答项」O(n log₂(n/k)) 当作其答案 | 改为 O(n log₂ k)；一般形式改指 DS-2013-20 |
| DS-2006-39 | AVL 中间 BF/树高：L133 插 8 右旋后子树高写 3、BF(17) 写 0（自身第 7 步矛盾） | h=3→h=2、BF(17) 0→−1 |
| DS-2024-18 | 轮次编号错位（fm L23 用 1-based 轮次，正文用 0-based k）；d00 笔误；不可达 14 应为 **10 对**；V2→V1 方向 | 4 处修正；正文轮次统一 1-based=k+1 |
| DS-2016-01 | L111 数值试验 140.97 应为 140.92 | 改数字（取整 141 不受影响） |
| DS-2015-45 | L68/L250 称 fig7 两版在 a→c 与 f→g 权值互换——放大复核显示唯一差异是权 3 弧向 | 待人工：本轮不覆盖，登记 |
| DS-2021-15 | fm `solution_status: uncertain`（schema 专指 OCR/回忆版）与 `ocr_confidence: high`/§12「不列为争议项」/`confidence: high` 不自洽 | 建议 derived；按 §9 未机械执行 |

**reconstructed 两题（仅标签/来源/隔离）**：
- DS-2025-14、DS-2026-15 的 `source_type` 均补「编者构造题」/「编者构造/替换题（AI 生成）」标注；
- 历史考频/覆盖排除项已逐项核验（statistics、syllabus_coverage、topic_exposure、disputed、build_* 脚本、validate #5）：全部 pass，无错误混入。

---

## 5. unresolved

- **DS-2006-35**（B+ 树叶结点关键字上限 9900 vs 10000）：教材定义版本未绑定（m−1 vs m），题面缺第二来源锁定；`reports/disputed_questions.md` L27 与本文件 §12 L145 存在核对缺口；G3 阶段 A 检索期间结果片段泄露校外回忆版答案 10000，已如实作为「外部来源/口径分歧」证据记录，**未作为独立求解依据**。人工裁决教材口径。

---

## 6. 需维护者人工判断的项目（17 项汇总）

### 6.1 命题/口径级（真答案争议，AI 不裁决）
1. **DS-2015-01**：D（常量 O(1)）vs C（规模变量 O(mn)）本意；与 DS-2016-01 的 disputed 触发标准统一。
2. **DS-2016-01**：A/B 等价 → 严格意义无唯一答案，是否降 disputed（同 DS-2016-12 先例）。
3. **DS-2016-12**：严蔚敏 n≥0 口径四项全真 → 维持「disputed + 定 A」还是「改登命题失拟」。
4. **DS-2016-20**：卷面单箭头为真貌时改登「双解 A、D」（现为推荐 D + 并列 A）。
5. **DS-2007-30**：图缺顶点 C6 → 维持「按现有图作答 + 原卷答案不可复原」还是改登 unsolvable。
6. **DS-2021-32**：第 1 行 C 还是 E（fm L24 已声明「C 或 E 歧义」，L100 推荐 E 缺来源锚点）。
7. **DS-2006-35**（unresolved）：B+ 树上限口径。

### 6.2 图像判读级（须放大原图）
8. **DS-2015-45**：fig7 权 3 弧向（g→d 还是 d→g）→ 决定 d(g)=16 vs 14。
9. **DS-2018-31**：fig3 ⟨S,I⟩ 权值 1 vs 7 → 决定「两条 vs 一条」关键路径。
10. **DS-2016-39**：fig5 V5-V8 段弧向已放大复核为 V5→V8；边表链接次序（升序 vs 降序）即卷面丢失的「要求」。
11. **DS-2014-39**：原图是否转录失真（Y 是否本应挂在别的右链上）。
12. **DS-2024-18**：fig1 独立判读残余风险（L2/L3 归属可交换但两点数字同为 1，不影响任何一轮矩阵）。

### 6.3 状态标签级（不机械执行 §9）
13. **DS-2021-15**：`solution_status` uncertain→derived。
14. **DS-2022-22**：修分层表后仍属 disputed，是否升 verified。
15. **DS-2020-36**：将「第 2 行同样不可精确复现」补写进题面订正说明。

### 6.4 仓库级 QA 议题（跨题）
16. **validate 检查覆盖缺口**：`validate_repository.py` L61–75 比对项不含 `answer_confidence`；建议增列或明确不列。
17. **命名规范债**：`DS06.07` 全部 19 题中 9 短名 / 10 全名混用（DS-2026-15、DS-2023-13 等）。id 本身合法。

---

## 7. 系统性问题（跨题观察，非本题缺陷）

1. **「选项分析／不适用」模板债**：全库 661 个解析中 **424 个**仍含该节（本批 DS-2023-13 L116–118、DS-2024-18 L244、DS-2024-22 L232–234 等），与 `docs/solution_schema.md` L99「非选择题不出现此节、不写不适用」直接冲突。属**批量清理议题**，本轮未据此下调单题状态。
2. **topic `name` 简写/全名混用**：DS06.07 为例 9 短 10 全；id 一律合法，`taxonomy_issue` 按定义仅在个别题标记，其余以 notes 记录。
3. **`reconstructed` 的 `source_type` 字段建议增设构造标识**：本轮已在两题正文改进，未来是否引入结构化字段属规范决策。
4. **metadata 漂移**：本轮修复后 `metadata/questions.jsonl` 有 3 处待 rebuild：DS-2015-01 `solution_status`（verified→disputed）、DS-2024-18 `answer` 文本（旧轮次编号）、DS-2022-06 `answer_confidence`（medium→high）。运行 `scripts/rebuild_all.py` 后 `validate_repository.py` 检查 #2 才 PASS。

---

## 8. 污染与偏差披露

- **G1（batch_001）**：阶段 A 自身误读 DS-2016-39 V5-V8 弧向；阶段 B 8 倍放大复核后确认现有解析正确，已如实登记。**盲审协议正常纠偏**。
- **G3（batch_002）**：检索 DS-2006-35 时结果片段泄露校外回忆版答案 10000；作为「外部来源/口径分歧」证据记录，未作为独立求解依据。
- **G4（batch_002）**：阶段 A 期间跨目录关键词检索意外回带少量 `solutions/` 正文片段（DS-2015-01 §12、DS-2025-14/DS-2026-15 §11–§12）。8 道真题的盲解结论在检索发生前已固化；比对以自身独立推导 + 程序复算为准。
- **主审**：曾于本轮前段独立修复 DS-2023-19 ASL 至 18/7（错），本轮由子代理 G2 + `verify_items.py` 双重发现后改回 **17/7**。教训：不能全信自己前一轮修复；即使非子代理题，也必须程序验证。
- **工作区污染**：前一 session 遗留 `tmp/inspect.py` 遮蔽标准库，已改名 `_inspect_legacy_rename.py.bak` 并清 `__pycache__`；本轮子代理明令禁止命名 inspect.py 且从各自 `tmp/audit_gN/` 独立目录运行 python。
- **转录不可恢复**：前一会话 JSONL 中 `audit_status` grep=0，子代理详细记录未持久化 → 本轮重新派发 G1–G4 并要求把结构化 JSONL 写入 `tmp/audit_gN/` 文件，避免依赖转录。

---

## 9. 主审定级覆盖说明（主审对子代理结论的调整）

| 题号 | 子代理 | 主审 | 理由 |
|---|---|---|---|
| DS-2015-01 | G4 minor | **major** | G4 阶段 B 见的是已修复文件；本轮真实发现 = verified 过度确信 + 无效归谬 + 缺双读法 |
| DS-2022-06 | G4 minor | **major** | 同上；本轮真实发现 = 429 棵中 378 棵无限递归的代码 bug |
| DS-2023-13 | G4 pass | **minor** | 本轮实际修了关联题答案引用 |
| DS-2006-39 | G1 pass | **minor** | 本轮实际修了 AVL 中间 BF/树高 |

覆盖原则：按「本轮真实发现 + 是否触发 §8 不静默修复」定级，不因修复后状态良好而降级。已在 `batch_002.md` §1 与本节明示。

---

## 10. 与 §9（solution_status 调整）一致的克制

- **未执行**的批量或机械调整：
  - DS-2021-15 uncertain→derived（仅建议）
  - DS-2016-01 verified→disputed（仅建议 + 已修算术笔误）
  - DS-2015-45 fig7 描述更正（因属图版对比，交人工放大，未覆盖）
- **实际调整**均满足 §9：
  - DS-2015-01：原 verified 的第二来源（教材目录页 URL 检查）实为「选项文本已见」而非「答案技术验证」；本轮无第二独立技术证据 → **降 disputed** 恰当。
  - DS-2022-06：`confidence` medium→high 由穷举证据（378/429 vs 0/197）支撑 → 属"真实获得第二独立技术证据"。

---

## 11. 下一步（等待维护者确认）

- **本次到此为止**（用户明令："完成后停止，先提交结果。不要直接进入 R1-B"）。
- R1-B 计划（若通过验收）：2023→2026 倒序、每年「算法设计 → 程序题 → 综合题 → 其他」，每批 20–25 题。
- R1-C：按知识点聚类审核长期核心考点历史题（Huffman / hash/ASL / BST/AVL / 二叉遍历 等）。
- 人工复核推荐顺序（§16）：所有 major（3）→ 所有 unresolved（1）→ disputed/uncertain → 2023–2026 → 算法设计题 → 其他。

# 真题解析数据规范（Solution Schema）

> 定义每道题解析文件的**命名、结构、字段与撰写标准**。若解析实践暴露 schema 问题，先改本规范与 taxonomy，再回头修样例，不为单题造规则。

## 1. 文件组织

```
solutions/
  2005/DS-2005-01.md
  2005/DS-2005-02.md
  ...
  2026/DS-2026-26.md
```

- 每题一个 Markdown 文件，文件名 = 题目 ID；
- 题目 ID：`DS-<年份>-<两位题号>`（如 `DS-2024-12`）；大题含小问的（(1)(2)(3)）**不拆**小问 ID，小问在同一文件内解析；
- 题号以 `真题/<年份>/*.md` 中连续编号为准，该编号即 `question_number`；
- 一年多个来源版本时 ID 不变，用 `source.source_version` 区分（当前全部 v1）。

## 2. YAML front matter（机器可读）

````yaml
---
question_id: DS-2024-12
year: 2024
question_number: 12
section: "二、填空题"          # 卷面分节原名
question_type: null            # 官方未公布题型定义，禁止猜测；可推断时填 选择题/填空/综合/算法 并加 type_basis: inferred
score: null                    # 官方未公布分值，一律 null

source:
  paper: "2024 重庆邮电大学 802 数据结构（回忆版）"
  source_type: "回忆版整理文本（网络来源）"
  source_file: "真题/2024/2024重庆邮电大学802数据结构真题.md"
  source_url: "https://zhuanlan.zhihu.com/p/1927102762312774981"
  source_version: "v1"

ocr_confidence: high           # high | medium | low（题面转录可信度；含订正说明/存疑声明的题为 medium/low）
reconstructed: false           # 人为构造/替换题（2025-14、2026-15）置 true，不入真题频率统计

primary_topic: { id: DS03.03.01, name: 树的存储结构 }
secondary_topics:
  - { id: DS03.03.02, name: 森林与二叉树的转换 }

skills: [CALCULATION, CONCEPT]

difficulty: { level: medium, confidence: medium }

answer:
  value: "1896"
  confidence: high             # high | medium | low

answer_sources:
  - { source: "独立推导（定义验证）", value: "1896" }
  - { source: "知乎解析篇（对照，未逐题核对）", url: "https://zhuanlan.zhihu.com/p/1927720755258459581" }

solution_status: verified      # verified | derived | disputed | unsolvable | uncertain
# 描述“解析本身的证据/推导强度”，与“是否人工审阅”无关（人工审阅见下方 review 块）
# verified  = 答案经至少两种独立证据技术交叉验证（非人工审定）
# derived   = 仅独立推导，未二次验证
# disputed  = 多来源冲突或题面歧义未决（必须写入 reports/disputed_questions.md）
# unsolvable= 题面缺损无法作答（2016-38、2007-31 等）
# uncertain = OCR/回忆版不确定（OCR_UNCERTAIN）

review:                        # 人工审阅状态（与 solution_status 正交）
  ai_generated: true           # 解析是否主要由 AI 生成
  human_review_status: pending # pending | reviewing | reviewed | needs_revision
  human_review_rounds: 0       # 已完成人工审阅轮次，>= 0
  last_human_review: null      # 最近一次人工审阅日期 YYYY-MM-DD，未审阅为 null
---
````

字段纪律：

1. `question_type`/`score` 官方未公布 → **保持 null**，禁止按 408 或经验猜测（规范第八节）；
2. 能力标签为固定枚举（§4），错误标签**不在此文件出现**（属用户做题记录，未来另设 error log）；
3. 所有 topic ID 必须存在于 `docs/knowledge_taxonomy.md`，未定义即 QA 失败。

## 3. 解析正文模板（固定核心 + 条件节）

正文采用**灵活模板**：一组固定核心节始终存在，其余节按题型条件出现。简单题不再强行填满所有节，也不出现「选项分析：不适用」这类为凑模板而写的空节。

**固定核心节（每题必有）：**

```markdown
# DS-YYYY-NN

## 原题        完整题面（含订正说明转录）；图/表/代码保持原结构；无法恢复处标「> 原题此处存在 OCR/图像识别不确定性」
## 答案        直接给结论
## 题目分析    已知/目标/约束/考查意图（表面问题背后的数据结构问题）
## 核心考点    核心考点 + 辅助考点，列 taxonomy ID，并解释归属原因；不复制教材章节
## 详细解答    完整推导，不跳关键步骤，可人工复现，不依赖计算器/程序运行结果
## 易错点与规律 只写本题实际存在的重要易错点与可迁移规律，可 1 条，可为空
## 来源与可信度 原题来源/答案来源/教材依据/多来源是否一致/是否争议/最终可信度
```

**条件节（按题型出现）：**

- **选择题**：增加「选项分析」，逐项对错原因；错误选项对应典型误区才写，不编造命题意图。非选择题**不出现**此节，不写「不适用」。
- **算法题**：增加「算法设计 / 代码 / 复杂度 / 边界条件 / 考场标准答案」；算法用教材风格 C/C++ 伪代码（禁 Python/STL 默认），附时间/空间复杂度（写明 n、|V|、|E| 含义）。
- **简单填空题**：允许将「题目分析」与「详细解答」合并；「关联知识」「考场标准答案」等非核心节按需省略。
- **含多小问的综合题**：「答案」「详细解答」「考场标准答案」按小问分列。

## 4. 能力标签固定枚举

`CONCEPT` 概念理解与辨析 | `CALCULATION` 计算 | `TRACE` 执行过程模拟 | `CONSTRUCTION` 结构构造 | `CODE_READING` 程序阅读 | `CODE_COMPLETION` 程序填空 | `ALGORITHM_DESIGN` 算法设计 | `ALGORITHM_IMPLEMENTATION` 算法实现 | `COMPLEXITY_ANALYSIS` 复杂度分析 | `COMPARISON` 方法比较 | `APPLICATION` 综合应用

允许多标签；禁止新增枚举外值（如需要 → `docs/taxonomy_candidates.md` 候选流程）。

## 5. 算法题补充检查（规范第十节）

每题必须回答：输入/输出是什么；数据结构选择；核心不变量；边界情况（空表、单结点、栈满队满、指针顺序、递归终止、下标越界）；时间/空间复杂度（写明 n、|V|、|E| 的含义）。

实现风格：与严蔚敏教材结构一致（`Status`、`SqList`、`LNode` 等约定可用），考场手写可完成，不过度工程化。

## 6. 答案冲突处理（规范第十三节）

解析篇与推导不一致时：并列记录双方案 → 定义推导/教材核对/必要时程序验证（程序只作后台验证，正文须手工可复现）→ 给推荐答案+理由+可信度；仍不决则 `solution_status: disputed` 并登记 `reports/disputed_questions.md`。**禁止静默择一。**

## 7. 完整示例

见样例：`solutions/2024/DS-2024-12.md`（计算型填空）、`solutions/2017/DS-2017-08.md`（选择题）、`solutions/2020/DS-2020-38.md`（算法设计题）。

## 8. AI 生成与人工审阅状态

本仓库解析的内容属性与审阅属性由**四个正交维度**分别记录，不得相互替代：

| 维度 | 字段 | 回答的问题 |
|---|---|---|
| 题面来源可信度 | `ocr_confidence` | 回忆版题面转录是否可靠 |
| 答案证据可信度 | `answer.confidence` | 最终答案的把握程度 |
| 解析证据状态 | `solution_status` | 解析本身的证据/推导强度 |
| 人工审阅状态 | `review.human_review_status` | 维护者是否已系统人工复核 |

核心原则：

1. **AI 生成 ≠ 未经验证**：`review.ai_generated: true` 表示解析主要由 AI 生成，但仍可经过独立推导、程序验证与交叉比对；
2. **verified ≠ 人工审定**：`solution_status: verified` 只说明答案在技术层面经过至少两种独立证据交叉验证，**不代表**维护者已逐题人工审核；
3. **人工审阅状态必须单独记录**：由 `review` 块承载，与 `solution_status` 互不推导。不得因 `solution_status: verified` 自动将 `human_review_status` 置为 `reviewed`；在无明确人工审阅证据时，统一为 `pending`、`human_review_rounds: 0`，不虚构已完成的人工复核。

`review` 字段定义：

```yaml
review:
  ai_generated: true           # boolean，当前全部为 true
  human_review_status: pending # pending | reviewing | reviewed | needs_revision
  human_review_rounds: 0       # int >= 0
  last_human_review: null      # YYYY-MM-DD 或 null
```

状态含义：`pending` 尚未完成系统人工复核；`reviewing` 正在审阅；`reviewed` 至少完成规定流程（要求 `human_review_rounds >= 1`）；`needs_revision` 复核中发现问题待修改。具体复核清单见 `docs/review_protocol.md`。

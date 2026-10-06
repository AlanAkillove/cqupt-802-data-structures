# 真题解析数据规范（Solution Schema）

> Phase 3 交付物。定义每道题解析文件的**命名、结构、字段与撰写标准**。pilot（Phase 4）如暴露 schema 问题，先改本规范与 taxonomy，再回头修样例，不为单题造规则。

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
# verified  = 推导并有第二方法/程序验证
# derived   = 仅独立推导，未二次验证
# disputed  = 多来源冲突或题面歧义未决（必须写入 reports/disputed_questions.md）
# unsolvable= 题面缺损无法作答（2016-38、2007-31 等）
# uncertain = OCR/回忆版不确定（OCR_UNCERTAIN）
---
````

字段纪律：

1. `question_type`/`score` 官方未公布 → **保持 null**，禁止按 408 或经验猜测（规范第八节）；
2. 能力标签为固定枚举（§4），错误标签**不在此文件出现**（属用户做题记录，未来另设 error log）；
3. 所有 topic ID 必须存在于 `docs/knowledge_taxonomy.md`，未定义即 QA 失败。

## 3. 解析正文 12 节模板

```markdown
# DS-YYYY-NN

## 1. 原题        完整题面（含订正说明转录）；图/表/代码保持原结构；无法恢复处标「> 原题此处存在 OCR/图像识别不确定性」
## 2. 答案        直接给结论
## 3. 题目分析    已知/目标/约束/命题意图（表面问题背后的数据结构问题）
## 4. 核心考点    核心考点 + 辅助考点，列 taxonomy ID，并解释归属原因；不复制教材章节
## 5. 解题思路    「如何想到」：观察什么→用哪个定义/性质→为什么此法→步骤框架
## 6. 详细解答    完整推导，不跳关键步骤，可人工复现，不依赖计算器/程序运行结果
## 7. 选项分析    仅选择题；逐项对错原因；错误选项对应典型误区才写，不编造命题意图
## 8. 考场标准答案  简练可书写版；算法题用教材风格 C/C++ 伪代码（禁 Python/STL 默认）；附时间/空间复杂度
## 9. 易错点      只写本题实际存在的重要易错点，可 1 条，可为空（写"无特别易错点"）
## 10. 一句话规律  1~3 句可迁移规律
## 11. 关联知识    仅直接相关，不无限扩展
## 12. 来源与可信度 原题来源/答案来源/教材依据/多来源是否一致/是否争议/最终可信度
```

非选择题：第 7 节写「不适用」；填空/综合小题多的：第 2、6、8 节按小问分列。

## 4. 能力标签固定枚举

`CONCEPT` 概念理解与辨析 | `CALCULATION` 计算 | `TRACE` 执行过程模拟 | `CONSTRUCTION` 结构构造 | `CODE_READING` 程序阅读 | `CODE_COMPLETION` 程序填空 | `ALGORITHM_DESIGN` 算法设计 | `ALGORITHM_IMPLEMENTATION` 算法实现 | `COMPLEXITY_ANALYSIS` 复杂度分析 | `COMPARISON` 方法比较 | `APPLICATION` 综合应用

允许多标签；禁止新增枚举外值（如需要 → `docs/taxonomy_candidates.md` 候选流程）。

## 5. 算法题补充检查（规范第十节）

每题必须回答：输入/输出是什么；数据结构选择；核心不变量；边界情况（空表、单结点、栈满队满、指针顺序、递归终止、下标越界）；时间/空间复杂度（写明 n、|V|、|E| 的含义）。

实现风格：与严蔚敏教材结构一致（`Status`、`SqList`、`LNode` 等约定可用），考场手写可完成，不过度工程化。

## 6. 答案冲突处理（规范第十三节）

解析篇与推导不一致时：并列记录双方案 → 定义推导/教材核对/必要时程序验证（程序只作后台验证，正文须手工可复现）→ 给推荐答案+理由+可信度；仍不决则 `solution_status: disputed` 并登记 `reports/disputed_questions.md`。**禁止静默择一。**

## 7. 完整示例

见 pilot：`solutions/2024/DS-2024-12.md`（计算型填空）、`solutions/2017/DS-2017-08.md`（选择题）、`solutions/2020/DS-2020-38.md`（算法设计题）。

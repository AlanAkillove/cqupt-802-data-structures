# 重庆邮电大学 802 数据结构 真题知识库

重庆邮电大学计算机科学与技术学院硕士研究生初试科目 **802《数据结构》** 的历年真题整理与结构化解析知识库，用于：真题学习、错题复习、知识点覆盖统计、历年考频分析、后续自动组题与 AI 辅助复习。

## ⚠️ 重要声明（请先阅读）

1. **题面来源为网络回忆版整理文本（非官方原卷）**，可信度定级见 [`reports/source_inventory.md`](reports/source_inventory.md)。回忆版与原卷可能存在差异，各题内的 `> 订正说明：` 逐条声明了已发现的源文缺陷及修复方式。
2. **本校 802 为独立自命题考试**。本库知识体系严格以重邮官方考纲为根，不采用 408 体系；未官方公布的题型/分值一律标注 `null`，不做猜测。
3. 历年真题原卷版权归重庆邮电大学所有；解析内容为学习用途整理，请勿用于商业目的（详见 LICENSE）。
4. 答案以独立推导 + 验证为主，标注了可信度；存在争议的题目集中列于 `reports/disputed_questions.md`，**不存在"官方答案"背书**。

## 目录结构

```
.
├── 考试大纲/          # raw：2027 官方考纲 PDF 及转录（不可变原始资料）
├── 真题/              # 18 个年份的题面 Markdown + imgs/ 题图（回忆版整理）
├── docs/              # 知识体系 taxonomy、解析数据规范、候选知识点
├── solutions/         # 逐题解析（DS-<年份>-<题号>.md，YAML front matter + 12 节模板）
├── metadata/          # questions.jsonl 机器可读索引
├── reports/           # 资料审计、QA、考纲覆盖、考频统计、争议题登记
└── tmp/               # 临时工具脚本（不入库，见 .gitignore）
```

## 快速使用

- **按知识点查题**：在 `metadata/questions.jsonl`（已生成，661 行，每题一行）中过滤 `primary_topic`（知识点 ID 定义见 `docs/knowledge_taxonomy.md`）；
- **看某一年试卷**：`真题/<年份>/` 为完整题面，`solutions/<年份>/` 为逐题解析；
- **考频/覆盖分析**：`reports/syllabus_coverage.md`（含 0 题覆盖的考纲点）与 `reports/question_statistics.md`；
- **错题记录**：暂由使用者在题目解析的 front matter 之外自行记录（错误标签规范见 `docs/solution_schema.md`，工具化后续支持）。

## 报告索引（`reports/`）

| 文件 | 内容 |
|---|---|
| [`source_inventory.md`](reports/source_inventory.md) | 资料审计：来源清单、题面可信度定级、图片缺失登记 |
| [`knowledge_taxonomy` 使用说明](docs/knowledge_taxonomy.md) | 知识体系 v2（DS00–DS06）canonical ID 与名称 |
| [`solution_schema.md`](docs/solution_schema.md) | 解析文件 YAML front matter 与 12 节模板规范 |
| [`disputed_questions.md`](reports/disputed_questions.md) | 争议/缺损/构造题登记表（disputed·unsolvable·uncertain·reconstructed） |
| [`qa_report.md`](reports/qa_report.md) | 全局 QA 报告（13 项检查，题数对账/模板/字段/禁用词/一致性） |
| [`syllabus_coverage.md`](reports/syllabus_coverage.md) | 考纲覆盖报告（逐节点题数，含 0 题节点） |
| [`question_statistics.md`](reports/question_statistics.md) | 真题统计报告（年份×章/技能/难度/状态分布，排除 reconstructed） |

## 数据格式

每道解析文件包含 YAML front matter（题目 ID、来源、知识点标签、能力标签、难度、答案与可信度、解析状态）与 12 节正文（原题/答案/分析/考点/思路/详解/选项/考场答案/易错点/规律/关联/来源）。字段枚举与约束见 [`docs/solution_schema.md`](docs/solution_schema.md)。

题目唯一 ID：`DS-<年份>-<两位题号>`，如 `DS-2024-12`。

## 覆盖年份

2005–2007、2012–2026（共 18 套、661 题）；**缺 2008–2011**（来源系列未收录，不以猜测补题）。

## 贡献与维护约定

- 原始资料（`考试大纲/`、`真题/`）不直接修改；勘误以新增 `> 订正说明：` 或在解析中标注不确定性方式进行；
- 新增知识点必须先登记 `docs/taxonomy_candidates.md` 走候选流程，禁止为单题创建一次性标签；
- 统计结论必须可回溯到题目 ID，禁止无证据的"必考/高频"表述；
- 提交信息建议格式：`<type>(<年份>): <说明>`（type: fix/feat/docs/data）。

## License

题目整理与解析内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可（见 `LICENSE`）；真题原卷版权归重庆邮电大学。

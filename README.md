# CQUPT 802 Data Structures

重庆邮电大学 802《数据结构》历年真题整理、结构化解析与知识点索引。

## 1. 项目简介

本仓库收集并整理重庆邮电大学硕士研究生招生考试 802《数据结构》的历年网络回忆版真题，依据 2027 年官方考试大纲建立统一知识点体系，并为每道题提供结构化解析、知识点标签与机器可读的元数据（metadata）。题目以唯一 ID 组织，配套考纲覆盖统计、知识点频率统计与争议题登记，可用于真题学习、错题复习、知识点检索与后续的自动化分析。

当前覆盖 **2005–2007、2012–2026 共 18 个年份、661 道题目**。缺失 **2008–2011**：该四年未获得可靠来源，本仓库不进行推测性补全。

指定参考教材：严蔚敏、吴伟民《数据结构（C 语言版）》，清华大学出版社，2021 年。

## 2. 重要说明

### 2.1 真题来源

历年题面主要来自网络流传的回忆版资料，**不是学校发布的官方原卷**。逐年份、逐篇目的可追溯来源链接见 [`reports/source_inventory.md`](reports/source_inventory.md)。

回忆版可能存在漏字、错误、图形缺失、数字错误、表述不完整或不同版本之间的不一致。本仓库通过题面内的订正说明与 [`reports/disputed_questions.md`](reports/disputed_questions.md) 争议登记，如实保留这些不确定性，不做掩盖。

本仓库不声称其内容为官方真题、完整原卷或官方答案。

### 2.2 AI 生成解析声明

> 本仓库的逐题解析主要由人工智能模型依据题面、考试大纲、指定教材及可获得的参考资料生成，并结合独立推导、程序验证和交叉比对进行初步校验。AI 生成内容仍可能存在推理、计算、代码或题意理解方面的错误，不能视为官方答案或未经审查的标准答案。仓库维护者将持续进行多轮人工复核、交叉验证和订正，并通过版本记录保留修改历史。

### 2.3 状态与可信度

本仓库对每道题分别记录以下相互独立的维度：

| 维度 | 字段 | 含义 | 文档 |
|---|---|---|---|
| 题面转录可信度 | `ocr_confidence` | 回忆版题面转录的可靠程度 | [`docs/solution_schema.md`](docs/solution_schema.md) |
| 答案证据强度 | `solution_status` | 解析本身的证据与推导状态，**不等于人工审阅** | [`docs/solution_schema.md`](docs/solution_schema.md) |
| 人工审阅状态 | `review.human_review_status` | 维护者是否已完成系统人工复核 | [`docs/review_protocol.md`](docs/review_protocol.md) |

特别提示：`solution_status: verified` 仅表示答案在技术层面经过至少两种独立证据的交叉验证，**不代表**维护者已逐题人工审定。二者的区别与定义以 [`docs/solution_schema.md`](docs/solution_schema.md) 为准。

## 3. 数据覆盖

| 项 | 数值 |
|---|---|
| 收录年份 | 2005–2007、2012–2026（18 个年份） |
| 题目总数 | 661 |
| 频率统计基数 | 659（排除 2 道 reconstructed 构造题） |
| 缺失年份 | 2008–2011（无可靠来源，不补全） |

按章分布（`primary_topic`，排除 reconstructed）：DS00 绪论 33、DS01 线性表 69、DS02 栈队列数组广义表 124、DS03 树与二叉树 139、DS04 图 114、DS05 查找 109、DS06 排序 71。

## 4. 仓库结构

```
.
├── README.md
├── LICENSE
├── 考试大纲/          # 官方考纲 PDF 及转录（原始资料）
├── 真题/              # 18 个年份题面 Markdown + imgs/ 题图（回忆版整理）
├── solutions/         # 逐题解析（DS-<年份>-<题号>.md，YAML front matter + 结构化正文）
├── docs/              # 知识体系、解析数据规范、候选知识点、人工审阅流程
├── metadata/          # questions.jsonl 机器可读索引
├── reports/           # 来源审计、QA、考纲覆盖、频率统计、争议题登记
└── scripts/           # 可复现的元数据/统计/校验脚本（从仓库根目录运行）
```

## 5. 使用方式

- **浏览历年真题**：`真题/<年份>/`
- **查看逐题解析**：`solutions/<年份>/`
- **按知识点检索**：在 `metadata/questions.jsonl` 中按 `primary_topic` / `secondary_topics` 过滤；知识点 ID 定义见 `docs/knowledge_taxonomy.md`
- **查看统计结果**：`reports/question_statistics.md`、`reports/syllabus_coverage.md`、`reports/topic_exposure_statistics.md`
- **查看争议题**：`reports/disputed_questions.md`
- **筛选尚未人工复核的题目**：按 metadata 中的 `human_review_status` 过滤（例如列出 `solution_status=verified` 且 `human_review_status=pending` 的题目）

所有派生产物可由脚本从仓库根目录复现：

```
python scripts/build_metadata.py
python scripts/build_statistics.py
python scripts/build_syllabus_coverage.py
python scripts/validate_repository.py
python scripts/rebuild_all.py        # 依次执行以上四步
```

## 6. 知识点体系

知识体系以 2027 年官方考试大纲为根，一级章节 DS01–DS06 与考纲六部分一一对应，扩展节点在指定教材基础上细化，全部位于考纲节点之下。DS00 为从考纲总体考查目标中显式抽出的横向基础知识节点。canonical ID、名称与使用规则见 [`docs/knowledge_taxonomy.md`](docs/knowledge_taxonomy.md)；考纲外新知识点须走 [`docs/taxonomy_candidates.md`](docs/taxonomy_candidates.md) 候选流程，不为单题创建一次性标签。

## 7. 数据与统计

- [`reports/question_statistics.md`](reports/question_statistics.md)：年份×章、能力标签、难度、解析状态等分布；频率类分布一律排除 2 道 reconstructed 构造题。
- [`reports/syllabus_coverage.md`](reports/syllabus_coverage.md)：以考纲全部节点为口径的历史覆盖（含 0 题节点），历史覆盖排除 reconstructed，构造题覆盖单列 supplemental。
- [`reports/topic_exposure_statistics.md`](reports/topic_exposure_statistics.md)：区分**主考次数**（`primary_topic` 命中）与**涉及次数**（`primary_topic` + `secondary_topics` 命中）。
- [`reports/qa_report.md`](reports/qa_report.md)：仓库自动一致性检查报告。

本仓库提供自动一致性检查，覆盖题数对账、metadata 与 front matter 一致性、审阅字段规则、统计口径、图片路径与来源 URL 等，具体结果见 `reports/qa_report.md`。

## 8. 争议题与不确定性

题面缺陷、来源矛盾或存在多解的题目均在解析文件中声明，并集中登记于 [`reports/disputed_questions.md`](reports/disputed_questions.md)。当前登记：disputed 5 道、unsolvable 2 道、uncertain 15 道，另有 reconstructed 构造题 2 道。这些条目不被隐藏，也不以推测方式美化数据。

## 9. 维护与审阅

- **Reconstructed 构造题**（`DS-2025-14`、`DS-2026-15`）：非已确认的真实考场题面，题面与解析处均有 ⚠️ 标记，metadata 标 `reconstructed: true`，已从所有频率统计与历史考纲覆盖中排除，不作为"历史上考过"的证据。
- **人工审阅**：解析的人工复核流程与检查项见 [`docs/review_protocol.md`](docs/review_protocol.md)；每完成一轮记 `human_review_rounds += 1`，审阅状态由 `human_review_status` 维护。
- **原始资料**：`考试大纲/`、`真题/` 不直接改写，勘误以订正说明或在解析中标注不确定性的方式进行。

### Review Status

- 661 道解析均已由 AI 生成并完成结构化整理；
- 已进行程序化一致性检查及部分交叉验证；
- 尚未完成维护者对全部题目的逐题、多轮人工审阅；
- 当前全部 661 题 `human_review_status = pending`、`human_review_rounds = 0`；
- 人工审阅进度由 metadata 中的 `human_review_status` 持续维护。

表述口径为："661 道解析已生成并完成结构化与自动一致性检查"，而非"已验证正确"。

## 10. 来源与致谢

- **题面来源**：本库真题题面主要抓取自知乎专栏「重庆邮电大学 802 数据结构真题」系列的网络回忆版整理。抓取入口专栏：<https://zhuanlan.zhihu.com/p/1928578058761270163>；逐年份完整可追溯 URL 见 [`reports/source_inventory.md`](reports/source_inventory.md)。
- **致谢**：感谢该专栏原作者 / 整理者公开分享历年回忆版题面与参考解析，为本知识库提供了题面基础。本项目在其之上进行校对、订正、结构化整理与逐题独立推导解析。
- **权利声明**：历年真题原卷版权归重庆邮电大学所有；回忆版整理与第三方解析版权归原权利人所有。本仓库的许可证不改变上述第三方内容的原有版权状态。

## 11. License

本仓库**由维护者原创的部分**（AI 生成后经本项目整理、修订的解析，自建 taxonomy，metadata，统计报告，项目代码与结构化标注）在适用法律和第三方权利允许范围内，采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可（详见 `LICENSE`）。

**第三方内容**（重庆邮电大学官方考试文件、真题原卷、网络回忆版题面、第三方图片与第三方原解析）不通过本仓库重新许可，其权利归原权利人所有。本项目的许可证不改变第三方内容原有的版权状态。

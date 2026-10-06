# 仓库发布前最终审计（Repository Release Audit）

> 本轮「公开发布规范化与可维护性完善」的结构化交付审计。对应规格第二十九节的 12 项逐条说明。

## 1. 修改了哪些结构

- 新增 `scripts/`（正式、可复现、无硬编码绝对路径、从仓库根目录运行）：`build_metadata.py`、`build_statistics.py`、`build_syllabus_coverage.py`、`validate_repository.py`、`rebuild_all.py`；
- 新增 `docs/review_protocol.md`（人工审阅流程与检查清单）；
- 新增 `reports/topic_exposure_statistics.md`（主考次数 / 涉及次数两套口径）；
- 661 个 `solutions/**/*.md` front matter 新增 `review` 块；`metadata/questions.jsonl` 同步新增审阅字段；
- `README.md` 整体重写；`LICENSE` 授权范围收紧；`docs/solution_schema.md`、`docs/knowledge_taxonomy.md`、`reports/source_inventory.md` 相应更新。

## 2. README 改了什么

- 由口语化的个人项目说明改为正式、简洁、学术资料库风格；移除个人化/内部流程表达（Phase/交付物/Agent 提示词等）；
- 采用「项目简介 / 重要说明（来源·AI 声明·状态可信度）/ 数据覆盖 / 仓库结构 / 使用方式 / 知识点体系 / 数据与统计 / 争议题 / 维护与审阅（含 Review Status）/ 来源与致谢 / License」结构；
- 新增 `## Review Status`；不再堆内部 QA 细节，仅指向 `reports/qa_report.md`；
- 未使用被禁止的营销/频率词，未使用大量 emoji。

## 3. AI 生成内容如何披露

README 第 2.2 节以正式措辞声明「逐题解析主要由人工智能模型生成」，并明确 AI 内容仍可能有错误、不能视为官方答案或未经审查的标准答案、维护者将持续多轮人工复核。措辞既非「AI 生成，仅供参考」，也非「已确保完全正确」。

## 4. solution_status 与 human_review_status 如何区分

- `solution_status`（verified/derived/disputed/unsolvable/uncertain）= 解析本身的证据/推导强度；`verified` 特指经至少两种独立证据的技术交叉验证，**不等于**人工审定；
- `review.human_review_status`（pending/reviewing/reviewed/needs_revision）+ `review.human_review_rounds` + `review.last_human_review` = 人工审阅状态；
- 二者正交、互不推导；定义同时写在 `docs/solution_schema.md` 第 8 节与 README 第 2.3 节，口径一致。

## 5. 当前各审阅状态题目数（全 661）

| human_review_status | 题数 |
|---|---|
| pending | 661 |
| reviewing | 0 |
| reviewed | 0 |
| needs_revision | 0 |

`ai_generated = true`：661 / 661；`human_review_rounds = 0`：全部 661。无 `solution_status: verified` 被自动升格为 `reviewed`（当前无审阅证据，统一 `pending`，不虚构人工复核）。

## 6. reconstructed 题如何处理

`DS-2025-14`、`DS-2026-15` 为人为构造/替代题：
- 题面与解析标题附近均有 ⚠️「非确认的真实考场题面」警示；
- metadata 保持 `reconstructed: true`；
- 已从**所有频率统计**（`question_statistics.md` 基数 659）与**历史考纲覆盖**（`syllabus_coverage.md` 主口径）中排除，构造题覆盖单列 supplemental；
- 不作为「历史上考过」的证据。

## 7. statistics 是否重新生成

是。`reports/question_statistics.md` 由 `scripts/build_statistics.py` 重建：频率类分布（章节、年份×章、能力、难度、解析状态、OCR）以 659 为基数（排除 reconstructed）；AI/审阅状态一节反映全部 661 条元数据。

## 8. historical coverage 是否已排除 reconstructed

是。`reports/syllabus_coverage.md` 历史逐节点覆盖以 659 为基数，DS06.07 历史计 17（已剔除 2 道 reconstructed）；第 3 节 supplemental 单列构造题覆盖。`validate_repository.py` 交叉校验 DS06.07 覆盖数 = 历史计数。

## 9. 图片路径检查结果

`真题/**/*.md` 中 Windows 反斜杠路径 `](.\imgs\` 已统一为 POSIX `](./imgs/`，无残留；`validate_repository.py` 第 6 项检查真题与解析中所有本地图片引用：无反斜杠且文件均存在 → PASS。

## 10. metadata 与 solutions 是否一致

是。`validate_repository.py` 第 2 项逐题比对 `questions.jsonl` 与 front matter 的 `primary_topic`、`solution_status`、`reconstructed`、`human_review_status` → 全部一致；第 1 项 661 文件 / 661 行 / 各年题数对账 → 一致。

## 11. License scope 是否已收紧

是。`LICENSE` 现明确：CC BY-NC-SA 4.0 **仅覆盖维护者原创部分**（AI 生成后经本项目整理修订的解析、taxonomy、metadata、统计报告、代码、结构化标注）；第三方内容（官方考试文件、真题原卷、回忆版题面、第三方图片与原解析）**不通过本仓库重新许可**，许可证不改变其原有版权状态。README 第 11 节口径一致。

## 12. 所有自动检查是否 PASS

是。`python scripts/validate_repository.py`：**9 项 PASS，0 WARN，0 FAIL**。检查项包括题数对账/ID 唯一、metadata↔front matter 一致、AI/审阅字段规则、字段枚举与 type·score null、reconstructed 集与统计口径、图片路径、来源 URL 年份一致性、争议登记、禁用营销/频率词扫描（详见 `reports/qa_report.md`）。

## 补充：来源 URL

2005 年无独立题面 URL，保持专栏入口，未伪造该年题面链接（见 `reports/source_inventory.md`）。

# 人工审阅流程（Review Protocol）

本文件定义对 AI 生成解析进行**人工复核**的流程与检查项。人工审阅状态与解析的证据状态（`solution_status`）相互独立：`solution_status: verified` 只表示技术层面的交叉验证，**不等于**已完成人工审阅。审阅状态记录在解析文件 front matter 的 `review` 块中（字段定义见 `docs/solution_schema.md` 第 8 节）。

## 1. 审阅字段

```yaml
review:
  ai_generated: true
  human_review_status: pending   # pending | reviewing | reviewed | needs_revision
  human_review_rounds: 0
  last_human_review: null        # YYYY-MM-DD
```

- `pending`：尚未开始系统人工复核；
- `reviewing`：正在复核；
- `reviewed`：至少完成一轮下文规定的复核流程；
- `needs_revision`：复核中发现问题，等待修改。

## 2. 每题至少检查

1. 原题转录是否准确（题面、图、表、代码与来源一致）；
2. 题意是否被正确理解（含小问划分与约束条件）；
3. 最终答案是否正确；
4. 推导过程是否完整、可人工复现（不依赖计算器或程序运行结果）；
5. 是否存在另一种合理答案（若有可能导致结论分歧，须并列声明口径或转 `disputed`）；
6. 算法代码是否正确（语法、边界、指针顺序、递归终止）；
7. 边界条件是否正确（空表、单结点、栈满队满、下标越界等）；
8. 时间复杂度 / 空间复杂度是否正确（写明 n、|V|、|E| 含义）；
9. taxonomy 标签是否合理（`primary_topic` 唯一、`secondary_topics` 恰当）；
10. 考场标准答案是否适合考试书写（教材风格、可手写完成）。

## 3. 风格审查项

复核时同时检查并逐步消除明显的机器生成痕迹：

- 是否存在机械模板化语言（如为凑模板而写的「已知 / 目标 / 约束 / 命题意图」四连、「首先……其次……最后……」）；
- 是否包含与本题无关的扩展内容（硬凑的「关联知识」「易错点」「选项分析：不适用」）；
- 是否出现为了完整性而编造的「命题意图」；
- 是否可以压缩文字以提高信息密度。

上述为**逐步优化项**，不因风格问题修改题目最终答案，除非发现明确错误。

## 4. 更新规则

- 每完成一轮复核：`human_review_rounds += 1`；
- 认可且无待办问题时：`human_review_status: reviewed`（此时须保证 `human_review_rounds >= 1`）；
- 发现问题待修改时：`human_review_status: needs_revision`；
- 记录审阅日期：`last_human_review: YYYY-MM-DD`；
- **不记录任何个人隐私信息**（审阅人身份、联系方式等一律不写入）。

## 5. 与其他文件的一致性

- 审阅过程中若改变 `solution_status`（如新增 `disputed`），须同步登记 `reports/disputed_questions.md`；
- 若新增/调整知识点标签，须确认该 topic ID 存在于 `docs/knowledge_taxonomy.md`，考纲外知识点走 `docs/taxonomy_candidates.md` 候选流程；
- 字段与统计由 `scripts/rebuild_all.py` 从 front matter 重建，人工不直接改 `metadata/questions.jsonl` 与 `reports/` 下的派生数字。

# AI Solution Quality Audit（`audits/`）

本目录承载**独立 AI 审查（AI audit）**的记录与产物，用于系统性复核 661 道主要由 AI 生成的逐题解析。

## ⚠️ 状态纪律（最高优先级）

**本目录下的全部工作都是 `AI audit`，不是 `human review`。**

- AI audit **禁止**修改任何解析文件 front matter 中的：
  - `review.human_review_status`
  - `review.human_review_rounds`
  - `review.last_human_review`
- 上述字段只有在**仓库维护者本人**完成某题人工复核并明确下达指令后才可修改。
- AI audit 的结果一律记录在本目录的 `registry.jsonl` 中，与人工审阅状态**完全隔离**。

## 目录结构

```
audits/
├── README.md              # 本文件：AI 审查流程、schema、纪律
├── registry.jsonl         # 每题的 AI 审查记录（唯一事实来源）
├── priority_queue.jsonl   # 由 scripts/build_audit_priority_queue.py 生成的审查优先级队列
├── batches/               # 每批审查的过程记录（blind 答案 vs 现有解析 对照）
└── summaries/             # 每轮（R1-A / R1-B / …）的汇总报告
```

## Blind audit 协议（两阶段）

每题审查**必须**分两阶段，以降低 confirmation bias：

**阶段 A — Blind solve**
只读取：原题题面、原题图片、官方考纲、指定教材/可确认定义、必要的外部参考。
**禁止**先读取 `solutions/<year>/<id>.md` 的答案 / 详细解答 / 考场答案。
先独立得出：题意、正确答案、关键推导、复杂度、算法、可能歧义。

**阶段 B — Compare**
之后再读取现有 solution，比较「独立结论 vs 现有答案」。禁止反向进行。

能程序验证的（栈合法序列、排序过程、哈希探测、BST/AVL、Huffman WPL、图遍历、Dijkstra/Floyd、拓扑、KMP next、数组地址、小规模复杂度枚举等）尽量程序验证；但程序结果只是证据之一，必须同时核对题目口径、算法定义、教材约定（ASL、KMP next、下标 0/1、循环队列、Huffman 左右分支、遍历邻接次序、哈希失败查找等口径差异）。

## registry.jsonl schema

每行一题（同一题多轮时按 `audit_round` 递增，最新轮覆盖理解）：

```json
{
  "question_id": "DS-2026-01",
  "audit_round": 1,
  "audit_status": "pass",
  "answer_agreement": true,
  "reasoning_agreement": true,
  "source_issue": false,
  "taxonomy_issue": false,
  "code_issue": false,
  "confidence_issue": false,
  "requires_human_attention": false,
  "notes": "独立推导与现有解析一致……",
  "commit": ""
}
```

### audit_status 取值

| 状态 | 含义 |
|---|---|
| `pass` | 独立求解与现有解析一致，未发现实质问题 |
| `minor_issue` | 最终答案正确，但存在表述/标签/推导冗余/小范围严谨性问题 |
| `major_issue` | 最终答案、核心推导、代码、复杂度或题意理解存在错误 |
| `unresolved` | 题面或来源不足，无法可靠判定 |

### 布尔标记

- `answer_agreement`：独立答案是否与现有答案一致；
- `reasoning_agreement`：核心推导是否成立（答案一致但推导有缺陷时为 false）；
- `source_issue`：来源/引用/原卷归属是否有误；
- `taxonomy_issue`：primary/secondary 标签是否错标或过度打标；
- `code_issue`：代码/算法/复杂度是否正确；
- `confidence_issue`：是否过度确信（`verified`/`high` 但缺第二独立证据）；
- `requires_human_attention`：是否需要维护者人工判断（歧义、口径分歧等）。

## solution_status 调整原则

AI audit 可**建议**升/降级 `solution_status`，但禁止机械批量修改：

- `verified → derived`：仅当原"第二来源"实际未构成验证且当前无第二独立证据时；
- `derived → verified`：必须真实获得第二独立技术证据；
- `disputed → verified`：仅当争议被可靠解决时；
- 任何状态修改**必须**写入 audit `notes`，且通过重新生成 metadata 反映。

`major_issue` 的处理：说明现有解析何处错 → 给出独立证据 → 修改 solution →（必要时）改 metadata / disputed registry → `python scripts/rebuild_all.py` → registry 标记 `major_issue` 并记录 `action`。禁止静默修复。

## 优先级与批次

优先级队列由脚本生成（P0 风险题 → P1 2023–2026 → P2 长期核心考点 → P3 其余），见 `priority_queue.jsonl`。每批 20–25 题，过程记录写入 `batches/`，轮次汇总写入 `summaries/`。

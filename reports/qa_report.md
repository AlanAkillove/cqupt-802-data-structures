# 802 数据结构 · 仓库一致性 QA 报告

> 由 `scripts/validate_repository.py` 生成，时间 2026-10-07。

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 题数对账 / ID 唯一 | PASS | 661 文件 / 661 行 / 各年吻合 |
| 2 | metadata 与 front matter 一致 | PASS | 全部字段一致 |
| 3 | AI/人工审阅字段规则 | PASS | ai_generated/human_review_* 合法 |
| 4 | 字段枚举 / type·score 为 null | PASS | 枚举与 null 约束满足 |
| 5 | reconstructed 集与统计口径 | PASS | reconstructed 已隔离于历史统计 |
| 6 | 图片路径规范与存在性 | PASS | 路径均为 POSIX 且存在 |
| 7 | 来源 URL 年份一致性 | PASS | 每年 source_url 单一 |
| 8 | 争议/存疑/不可解题已登记 | PASS | 全部登记 |
| 9 | 禁用营销/频率词扫描 | PASS | 无命中 |

**汇总**：9 项 PASS，0 项 WARN，0 项 FAIL。

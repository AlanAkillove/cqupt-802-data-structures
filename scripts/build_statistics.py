# -*- coding: utf-8 -*-
"""Regenerate reports/question_statistics.md from metadata/questions.jsonl.

Run from repository root:  python scripts/build_statistics.py
Historical frequency distributions exclude reconstructed questions.
"""
import io, os, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPS = ['DS00','DS01','DS02','DS03','DS04','DS05','DS06']
CHAP_NAME = {'DS00':'绪论（基础知识章）','DS01':'线性表','DS02':'栈、队列、数组和广义表',
             'DS03':'树与二叉树','DS04':'图','DS05':'查找','DS06':'排序'}


def load():
    p = os.path.join(ROOT, 'metadata', 'questions.jsonl')
    return [json.loads(l) for l in io.open(p, encoding='utf-8')]


def pct(n, d):
    return '%.1f%%' % (100.0 * n / d) if d else '-'


def main():
    rows = load()
    rec_ids = {r['question_id'] for r in rows if r['reconstructed']}
    hist = [r for r in rows if r['question_id'] not in rec_ids]  # 659
    N = len(hist)
    L = []
    L.append('# 802 数据结构 · 真题统计报告')
    L.append('')
    L.append('> 本报告由 `scripts/build_statistics.py` 从 `metadata/questions.jsonl` 生成，请勿手改数字。')
    L.append('>')
    L.append('> **统计口径**')
    L.append('> - 数据源全集 661 题（2005–2007、2012–2026 共 18 年）。')
    L.append('> - **频率类分布（章节、年份、能力标签、难度、解析状态、OCR）一律排除 2 道 `reconstructed` 题**（DS-2025-14、DS-2026-15，人为构造/替代题，非真实考场题面），基数 = **%d**。' % N)
    L.append('> - **人工审阅状态**一节反映全部 661 条元数据的真实完整性，不排除 reconstructed。')
    L.append('> - 题型与分值官方从未公布，故**不做按题型 / 按分值的统计**；`question_type`、`score` 恒为 `null`。')
    L.append('> - `primary_topic` 每题唯一；`skills` 可多选，各技能之和大于题目数。')
    L.append('')
    L.append('## 1. 按章分布（DS00–DS06，排除 reconstructed）')
    L.append('')
    L.append('| 章 | 名称 | 题数 | 占比 |')
    L.append('|---|---|---|---|')
    chap = Counter(r['primary_topic'][:4] for r in hist)
    for c in CHAPS:
        L.append('| %s | %s | %d | %s |' % (c, CHAP_NAME[c], chap.get(c, 0), pct(chap.get(c, 0), N)))
    L.append('| **合计** | | **%d** | 100%% |' % N)
    L.append('')
    L.append('> DS06 含 reconstructed 的全集口径为 %d（DS06.07 上另有 2 道构造题）。' % (chap.get('DS06', 0) + 2))
    L.append('')
    L.append('## 2. 年份 × 章 矩阵（排除 reconstructed）')
    L.append('')
    L.append('| 年份 | ' + ' | '.join(CHAPS) + ' | 合计 |')
    L.append('|---|' + '---|' * (len(CHAPS) + 1))
    colsum = Counter()
    for y in sorted({r['year'] for r in hist}):
        yr = [r for r in hist if r['year'] == y]
        cc = Counter(r['primary_topic'][:4] for r in yr)
        colsum.update(cc)
        L.append('| %d | ' % y + ' | '.join(str(cc.get(c, 0)) for c in CHAPS) + ' | %d |' % len(yr))
    L.append('| **合计** | ' + ' | '.join(str(colsum.get(c, 0)) for c in CHAPS) + ' | **%d** |' % N)
    L.append('')
    L.append('> 缺 2008–2011：该四年未获得可靠来源，不做推测性补全（见 `reports/source_inventory.md`）。')
    L.append('')
    L.append('## 3. 按能力标签（skills，可多选，排除 reconstructed）')
    L.append('')
    L.append('| 能力标签 | 题数 |')
    L.append('|---|---|')
    for s, c in Counter(x for r in hist for x in r['skills']).most_common():
        L.append('| %s | %d |' % (s, c))
    L.append('')
    L.append('## 4. 按难度（difficulty，解析自评，排除 reconstructed）')
    L.append('')
    L.append('| 难度 | 题数 | 占比 |')
    L.append('|---|---|---|')
    for d in ['easy', 'medium', 'hard']:
        c = Counter(r['difficulty'] for r in hist).get(d, 0)
        L.append('| %s | %d | %s |' % (d, c, pct(c, N)))
    L.append('| **合计** | **%d** | 100%% |' % N)
    L.append('')
    L.append('> 难度为解析时按认知负荷给出的自评档位，非官方分级。')
    L.append('')
    L.append('## 5. 按解析状态（solution_status，排除 reconstructed）')
    L.append('')
    L.append('> `solution_status` 描述**解析自身的证据/推导强度**，与“是否已由人工审阅”无关（后者见第 7 节）。')
    L.append('')
    L.append('| 状态 | 题数 | 含义 |')
    L.append('|---|---|---|')
    SM = {'verified':'答案经至少两种独立证据技术交叉验证（非人工审定）','derived':'仅独立推导，未二次验证',
          'disputed':'多来源冲突或题面歧义未决','uncertain':'题面缺陷，声明口径后作答','unsolvable':'题面信息不足，无法作答'}
    st = Counter(r['solution_status'] for r in hist)
    for s in ['verified', 'derived', 'disputed', 'uncertain', 'unsolvable']:
        L.append('| %s | %d | %s |' % (s, st.get(s, 0), SM[s]))
    L.append('| **合计** | **%d** | |' % N)
    L.append('')
    L.append('> disputed / uncertain / unsolvable 逐题登记于 `reports/disputed_questions.md`，与 front matter 一一对应。')
    L.append('')
    L.append('## 6. 按题面转录可信度（ocr_confidence，排除 reconstructed）')
    L.append('')
    L.append('| 可信度 | 题数 |')
    L.append('|---|---|')
    for s in ['high', 'medium', 'low']:
        L.append('| %s | %d |' % (s, Counter(r['ocr_confidence'] for r in hist).get(s, 0)))
    L.append('| **合计** | **%d** |' % N)
    L.append('')
    L.append('## 7. AI 生成与人工审阅状态（全 661 条元数据）')
    L.append('')
    L.append('- **AI 生成**：`ai_generated = true` 的题目 **%d / 661**（当前解析主要由 AI 依据题面、考纲、指定教材与参考资料生成并结构化整理，非人工从零撰写）。' % sum(1 for r in rows if r['ai_generated']))
    hr = Counter(r['human_review_status'] for r in rows)
    L.append('- **人工审阅状态**：pending %d / reviewing %d / reviewed %d / needs_revision %d。' % (
        hr.get('pending', 0), hr.get('reviewing', 0), hr.get('reviewed', 0), hr.get('needs_revision', 0)))
    L.append('- **人工审阅轮次**：全部 %d 题为 0 轮（`human_review_rounds = 0`）。' % len(rows))
    L.append('')
    L.append('> **重要**：`solution_status: verified` 只表示 AI 推导经过了技术层面的交叉验证，**不等于**维护者已人工逐题审定。当前人工复核尚未系统展开，故所有题目 `human_review_status` 统一为 `pending`。审阅流程见 `docs/review_protocol.md`。')

    dest = os.path.join(ROOT, 'reports', 'question_statistics.md')
    io.open(dest, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print('build_statistics: wrote reports/question_statistics.md (hist base=%d, full=%d)' % (N, len(rows)))


if __name__ == '__main__':
    main()

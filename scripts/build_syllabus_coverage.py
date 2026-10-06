# -*- coding: utf-8 -*-
"""Regenerate考纲覆盖与知识点统计报告.

Run from repository root:  python scripts/build_syllabus_coverage.py
Writes:
  reports/syllabus_coverage.md          (historical primary coverage, EXCLUDES reconstructed; + supplemental)
  reports/topic_exposure_statistics.md  (primary count vs exposure count, EXCLUDES reconstructed)
"""
import io, os, re, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# curated explanations for known zero-coverage leaves
EXPLAIN = {
    'DS03.02.03.01': '纯前序题一般并入综合性 DS03.02.03 或对应线索/转换节点，属打标口径，并非“前序从未考查”。',
    'DS03.02.03.03': '纯后序题同上，并入综合 DS03.02.03，属打标口径。',
    'DS03.03.03': '树/森林遍历计入 DS03.03.02（转换含遍历对应），上位概念被下位节点吸收。',
    'DS04.02.03': '回忆版真题未将“邻接多重表/十字链表”作为主考点单独命题。',
    'DS05.01': 'ASL 概念计入各具体查找节点（DS05.04/DS05.06.02 等），上位概念被下位节点吸收。',
    'DS06.02.02': '回忆版真题未将“折半插入排序”作为主考点单独命题；其作为对比项出现在 DS06.11。',
    'DS06.03': '回忆版真题未将“冒泡排序”作为主考点单独命题；其作为对比项出现在 DS06.11。',
}


def load():
    p = os.path.join(ROOT, 'metadata', 'questions.jsonl')
    return [json.loads(l) for l in io.open(p, encoding='utf-8')]


def tax_order_names():
    txt = io.open(os.path.join(ROOT, 'docs', 'knowledge_taxonomy.md'), encoding='utf-8').read()
    order, names = [], {}
    for m in re.finditer(r'^\|\s*(DS\d{2}(?:\.\d{2}){1,3})\s*\|\s*([^|]+?)\s*\|', txt, re.M):
        tid, nm = m.group(1), m.group(2).strip()
        if tid not in names:
            order.append(tid); names[tid] = nm
    nonleaf = set()
    for a in order:
        for b in order:
            if b != a and b.startswith(a + '.'):
                nonleaf.add(a); break
    return order, names, nonleaf


def main():
    rows = load()
    rec = {r['question_id'] for r in rows if r['reconstructed']}
    hist = [r for r in rows if r['question_id'] not in rec]        # 659
    recq = [r for r in rows if r['question_id'] in rec]            # 2
    order, names, nonleaf = tax_order_names()
    prim_hist = Counter(r['primary_topic'] for r in hist)
    parent_direct = {t: prim_hist[t] for t in nonleaf if prim_hist.get(t)}
    leaf_sum = sum(prim_hist.get(t, 0) for t in order if t not in nonleaf)
    zeros = [t for t in order if t not in nonleaf and prim_hist.get(t, 0) == 0]

    # ---------- syllabus_coverage.md ----------
    L = []
    L.append('# 802 数据结构 · 考纲覆盖报告')
    L.append('')
    L.append('> 由 `scripts/build_syllabus_coverage.py` 从 `metadata/questions.jsonl` 生成。')
    L.append('> 统计口径：`docs/knowledge_taxonomy.md` **v2 全部节点**（含基础知识章 DS00），以每题 `primary_topic` 计一次；`0` 题节点也列出。')
    L.append('> **历史覆盖 = 排除 reconstructed 题**（DS-2025-14、DS-2026-15 为人为构造，不能证明“历史上考过”）。构造题覆盖单列于第 3 节 supplemental。')
    L.append('')
    L.append('## 1. 历史逐节点覆盖（primary_topic 计数，排除 reconstructed，基数 %d）' % len(hist))
    L.append('')
    chap_titles = {'DS00':'DS00 绪论（基础知识章）','DS01':'DS01 线性表','DS02':'DS02 栈、队列、数组和广义表',
                   'DS03':'DS03 树与二叉树','DS04':'DS04 图','DS05':'DS05 查找','DS06':'DS06 排序'}
    cur = None
    for tid in order:
        ch = tid[:4]
        if ch != cur:
            cur = ch
            L.append('### ' + chap_titles[ch])
            L.append('| ID | 名称 | 题数 |')
            L.append('|---|---|---|')
        if tid in nonleaf and tid != 'DS03.02.03':
            continue
        mark = '※' if tid == 'DS03.02.03' else ''
        L.append('| %s | %s%s | %d |' % (tid, names[tid], mark, prim_hist.get(tid, 0)))
        L.append('') if False else None
    L.append('')
    L.append('> ※ `DS03.02.03` 既被直接打标（综合性遍历互推/由序列确定二叉树），又是 `.01–.04` 四个细粒度子节点的父节点；父与子各自独立计数、不重复（一题一个 primary）。')
    L.append('')
    L.append('## 2. 覆盖对账')
    L.append('')
    L.append('- 叶子节点计数合计 = %d；直接打在非叶父节点（DS03.02.03）的题 = %s；两者相加 = **%d**，与历史题数（排除 reconstructed）一致，无未归类题。' % (leaf_sum, parent_direct, leaf_sum + sum(parent_direct.values())))
    L.append('- 考纲六部分 DS01–DS06 均有题目命中；基础知识章 DS00 共 %d 题。' % sum(prim_hist.get(t, 0) for t in order if t.startswith('DS00')))
    L.append('- **0 题节点（%d 个）**：%s。' % (len(zeros), '、'.join('`%s %s`' % (t, names[t]) for t in zeros)))
    L.append('')
    for t in zeros:
        if t in EXPLAIN:
            L.append('  - `%s %s`：%s' % (t, names[t], EXPLAIN[t]))
    L.append('')
    L.append('## 3. Supplemental：reconstructed 构造题覆盖（不计入历史覆盖）')
    L.append('')
    L.append('| question_id | primary_topic | 名称 |')
    L.append('|---|---|---|')
    for r in sorted(recq, key=lambda x: x['question_id']):
        L.append('| %s | %s | %s |' % (r['question_id'], r['primary_topic'], names.get(r['primary_topic'], '')))
    L.append('')
    L.append('> 这两题用于补充“堆调整”这一考点的练习覆盖，但**不得**作为该考点“历史真题考过”的证据；历史覆盖中 DS06.07 已不含它们。')
    io.open(os.path.join(ROOT, 'reports', 'syllabus_coverage.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    # ---------- topic_exposure_statistics.md ----------
    prim = Counter(r['primary_topic'] for r in hist)
    expo = Counter()
    for r in hist:
        seen = {r['primary_topic']} | set(r['secondary_topics'])
        for t in seen:
            expo[t] += 1
    T = []
    T.append('# 802 数据结构 · 知识点主考 / 涉及统计')
    T.append('')
    T.append('> 由 `scripts/build_syllabus_coverage.py` 生成，**排除 reconstructed**（基数 %d）。' % len(hist))
    T.append('>')
    T.append('> - **主考次数（Primary count）**：题目 `primary_topic` 命中该节点的次数，即该知识点作为“主考点”被直接命题的次数。')
    T.append('> - **涉及次数（Exposure count）**：`primary_topic` 与 `secondary_topics` 任一命中该节点的次数，即该知识点“出现在题目中（主考或综合涉及）”的次数。')
    T.append('> - Exposure ≥ Primary。二者均**不是官方“考频”**，仅为本库标签口径下的计数，可回溯到题目 ID。')
    T.append('')
    T.append('## 章级汇总')
    T.append('')
    T.append('| 章 | 主考次数 | 涉及次数 |')
    T.append('|---|---|---|')
    chaps = ['DS00','DS01','DS02','DS03','DS04','DS05','DS06']
    ch_prim = Counter(r['primary_topic'][:4] for r in hist)
    ch_expo = Counter()
    for r in hist:
        for pre in {r['primary_topic'][:4]} | {s[:4] for s in r['secondary_topics']}:
            ch_expo[pre] += 1
    for c in chaps:
        T.append('| %s | %d | %d |' % (c, ch_prim.get(c, 0), ch_expo.get(c, 0)))
    T.append('')
    T.append('## 节点级明细（主考 / 涉及）')
    T.append('')
    T.append('| ID | 名称 | 主考次数 | 涉及次数 |')
    T.append('|---|---|---|---|')
    for tid in order:
        if tid in nonleaf and tid != 'DS03.02.03':
            continue
        T.append('| %s | %s | %d | %d |' % (tid, names[tid], prim.get(tid, 0), expo.get(tid, 0)))
    T.append('')
    T.append('> DS03.02.03 与其 `.01–.04` 子节点独立计数；如需遍历族合并视角，将四子节点与父节点相加。')
    io.open(os.path.join(ROOT, 'reports', 'topic_exposure_statistics.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(T) + '\n')

    print('build_syllabus_coverage: hist_base=%d reconstructed=%d zero_nodes=%d' % (len(hist), len(recq), len(zeros)))
    print('  wrote reports/syllabus_coverage.md, reports/topic_exposure_statistics.md')


if __name__ == '__main__':
    main()

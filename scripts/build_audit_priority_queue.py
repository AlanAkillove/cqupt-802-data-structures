# -*- coding: utf-8 -*-
"""Build the AI-audit priority queue from metadata. Run from repository root:

    python scripts/build_audit_priority_queue.py

This is an AI-audit planning artifact only. It NEVER reads or writes any
review.human_review_* field; human review is reserved for the maintainer.

Priority tiers (Phase R1 spec, section six):
  P0  risk questions: solution_status != verified, OR answer.confidence != high,
      OR ocr_confidence == low, OR reconstructed (label/source/isolation check only).
  P1  2023-2026 real questions (excluding reconstructed, excluding P0).
  P2  long-term core topics (primary_topic under the core node set).
  P3  everything else.

Output: audits/priority_queue.jsonl (machine) + a short table on stdout.
"""
import io, os, json
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'audits', 'priority_queue.jsonl')

# Long-term core topic prefixes (from docs/knowledge_taxonomy.md).
CORE_PREFIX = [
    'DS01.02.02',                       # 单链表
    'DS02.01', 'DS02.02', 'DS02.03', 'DS02.07',  # 栈队列及应用
    'DS02.04',                          # 多维数组存储
    'DS03.02.03',                       # 二叉树遍历（含 .01-.04 子节点）
    'DS03.04.01',                       # Huffman
    'DS04.03.01', 'DS04.03.02',         # DFS / BFS
    'DS04.04.02', 'DS04.04.03', 'DS04.04.04',  # 最短路径 / 拓扑 / 关键路径
    'DS05.04',                          # 折半查找
    'DS05.06.01', 'DS05.06.02',         # 散列表及 ASL
    'DS05.07.01', 'DS05.07.02',         # BST / AVL
    'DS06.07',                          # 堆
]

SKILL_RANK = {'ALGORITHM_DESIGN': 0, 'ALGORITHM_IMPLEMENTATION': 0,
              'CODE_READING': 1, 'CODE_COMPLETION': 1, 'APPLICATION': 2}


def tier(r):
    if r['reconstructed'] or r['solution_status'] != 'verified' \
       or r.get('answer_confidence') != 'high' or r.get('ocr_confidence') == 'low':
        return 0
    if r['year'] in (2023, 2024, 2025, 2026):
        return 1
    pt = r['primary_topic'] or ''
    if any(pt.startswith(p) for p in CORE_PREFIX):
        return 2
    return 3


def p0_sub(r):
    if r['reconstructed']:
        return 4
    st = r['solution_status']
    if st in ('disputed', 'unsolvable'):
        return 0
    if st == 'uncertain':
        return 1
    if st == 'derived':
        return 2
    return 3  # verified but ansconf/ocr risk


def sub_rank(r, t):
    if t == 0:
        return (p0_sub(r), r['question_id'])
    if t == 1:
        sk = min([SKILL_RANK.get(s, 3) for s in r['skills']] or [3])
        return (sk, -r['year'], r['question_number'])
    if t == 2:
        return (-r['year'], r['question_number'])
    return (r['year'], r['question_number'])


def reason(r, t):
    if t == 0:
        if r['reconstructed']:
            return 'reconstructed: 仅查标签/来源/隔离'
        bits = []
        if r['solution_status'] != 'verified':
            bits.append('status=' + r['solution_status'])
        if r.get('answer_confidence') != 'high':
            bits.append('answer_conf=' + str(r.get('answer_confidence')))
        if r.get('ocr_confidence') == 'low':
            bits.append('ocr=low')
        return ';'.join(bits)
    if t == 1:
        return '近期真题 %d' % r['year']
    if t == 2:
        return '长期核心考点 ' + r['primary_topic']
    return '其余'


def main():
    rows = [json.loads(l) for l in io.open(os.path.join(ROOT, 'metadata', 'questions.jsonl'), encoding='utf-8')]
    recs = []
    for r in rows:
        t = tier(r)
        recs.append({'question_id': r['question_id'], 'priority': t,
                     'reason': reason(r, t), '_sub': sub_rank(r, t),
                     'year': r['year'], 'solution_status': r['solution_status']})
    recs.sort(key=lambda x: (x['priority'], x['_sub']))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        for i, x in enumerate(recs):
            f.write(json.dumps({'rank': i, 'question_id': x['question_id'],
                                'priority': x['priority'], 'reason': x['reason'],
                                'year': x['year'], 'solution_status': x['solution_status']},
                               ensure_ascii=False) + '\n')
    c = Counter(x['priority'] for x in recs)
    p0 = [x['question_id'] for x in recs if x['priority'] == 0]
    print('priority_queue: wrote', os.path.relpath(OUT, ROOT))
    print('tier counts:', dict(sorted(c.items())))
    print('P0 (Phase R1-A scope):', len(p0), 'questions')
    print('P0 ids:', ','.join(p0))


if __name__ == '__main__':
    main()

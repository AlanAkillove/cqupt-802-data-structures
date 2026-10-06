# -*- coding: utf-8 -*-
"""Rebuild metadata/questions.jsonl from solutions/**.md front matter.

Run from the repository root:  python scripts/build_metadata.py
Also enforces metadata-level invariants (unique ids, per-year ledger, enum domains).
"""
import io, os, re, json, glob, sys
from collections import Counter
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = {'CONCEPT','CALCULATION','TRACE','CONSTRUCTION','CODE_READING','CODE_COMPLETION',
          'ALGORITHM_DESIGN','ALGORITHM_IMPLEMENTATION','COMPLEXITY_ANALYSIS','COMPARISON','APPLICATION'}
STATUS = {'verified','derived','disputed','unsolvable','uncertain'}
REVIEW_STATUS = {'pending','reviewing','reviewed','needs_revision'}
OCR = {'high','medium','low'}
EXPECT = {2005:35,2006:45,2007:45,2012:45,2013:46,2014:47,2015:47,2016:44,2017:39,
          2018:33,2019:33,2020:38,2021:34,2022:34,2023:24,2024:23,2025:23,2026:26}


def taxonomy_ids():
    txt = io.open(os.path.join(ROOT, 'docs', 'knowledge_taxonomy.md'), encoding='utf-8').read()
    return set(re.findall(r'\|\s*(DS\d{2}(?:\.\d{2}){1,3})\s*\|', txt))


def fm_of(path):
    t = io.open(path, encoding='utf-8').read()
    end = t.find('\n---', 3)
    return yaml.safe_load(t[4:end])


def main():
    ids = taxonomy_ids()
    rows, errors = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, 'solutions', '*', '*.md'))):
        rel = os.path.relpath(path, ROOT).replace('\\', '/')
        d = fm_of(path)
        qid = d.get('question_id')
        src = d.get('source', {}) or {}
        ans = d.get('answer', {}) or {}
        diff = d.get('difficulty', {}) or {}
        pt = d.get('primary_topic', {}) or {}
        sec = d.get('secondary_topics', []) or []
        skills = d.get('skills', []) or []
        rv = d.get('review', {}) or {}
        # invariants
        if d.get('question_type') is not None: errors.append('%s question_type not null' % qid)
        if d.get('score') is not None: errors.append('%s score not null' % qid)
        if d.get('solution_status') not in STATUS: errors.append('%s bad status %s' % (qid, d.get('solution_status')))
        if d.get('ocr_confidence') not in OCR: errors.append('%s bad ocr %s' % (qid, d.get('ocr_confidence')))
        if not set(skills) <= SKILLS: errors.append('%s bad skills %s' % (qid, skills))
        if pt.get('id') not in ids: errors.append('%s unknown primary topic %s' % (qid, pt.get('id')))
        for s in sec:
            if (s or {}).get('id') not in ids: errors.append('%s unknown secondary topic %s' % (qid, (s or {}).get('id')))
        if rv.get('ai_generated') is not True: errors.append('%s review.ai_generated must be boolean true' % qid)
        if rv.get('human_review_status') not in REVIEW_STATUS: errors.append('%s bad human_review_status' % qid)
        hrr = rv.get('human_review_rounds')
        if not isinstance(hrr, int) or hrr < 0: errors.append('%s human_review_rounds must be >=0 int' % qid)
        if rv.get('human_review_status') == 'reviewed' and (hrr or 0) < 1:
            errors.append('%s reviewed requires human_review_rounds>=1' % qid)
        rows.append({
            'question_id': qid, 'year': d.get('year'), 'question_number': d.get('question_number'),
            'section': d.get('section'), 'question_type': d.get('question_type'), 'score': d.get('score'),
            'source_url': src.get('source_url'), 'source_file': src.get('source_file'),
            'ocr_confidence': d.get('ocr_confidence'), 'reconstructed': d.get('reconstructed'),
            'primary_topic': pt.get('id'), 'primary_topic_name': pt.get('name'),
            'secondary_topics': [s.get('id') for s in sec], 'skills': skills,
            'difficulty': diff.get('level'), 'difficulty_confidence': diff.get('confidence'),
            'answer': ans.get('value'), 'answer_confidence': ans.get('confidence'),
            'solution_status': d.get('solution_status'),
            'ai_generated': rv.get('ai_generated'), 'human_review_status': rv.get('human_review_status'),
            'human_review_rounds': hrr,
            'file': rel,
        })
    rows.sort(key=lambda r: (r['year'], r['question_number']))
    out = os.path.join(ROOT, 'metadata')
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, 'questions.jsonl')
    with io.open(dest, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    # post
    qs = [r['question_id'] for r in rows]
    assert len(qs) == len(set(qs)), 'duplicate question_id'
    cnt = Counter(r['year'] for r in rows)
    for y, e in sorted(EXPECT.items()):
        if cnt.get(y) != e: errors.append('year %d count %s != expect %d' % (y, cnt.get(y), e))
    with io.open(dest, encoding='utf-8') as f:
        for line in f:
            json.loads(line)
    print('build_metadata: rows=%d unique_ids=%d ERRORS=%d' % (len(rows), len(set(qs)), len(errors)))
    for e in errors:
        print('  ' + e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

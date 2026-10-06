# -*- coding: utf-8 -*-
"""Repository-wide QA validator. Run from repository root:

    python scripts/validate_repository.py

Prints a PASS/FAIL/WARN matrix and regenerates reports/qa_report.md.
Exit code 1 if any FAIL.
"""
import io, os, re, json, glob, sys, datetime
from collections import Counter, defaultdict
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = {'CONCEPT','CALCULATION','TRACE','CONSTRUCTION','CODE_READING','CODE_COMPLETION',
          'ALGORITHM_DESIGN','ALGORITHM_IMPLEMENTATION','COMPLEXITY_ANALYSIS','COMPARISON','APPLICATION'}
STATUS = {'verified','derived','disputed','unsolvable','uncertain'}
REVIEW_STATUS = {'pending','reviewing','reviewed','needs_revision'}
OCR = {'high','medium','low'}
DIFF = {'easy','medium','hard'}
EXPECT = {2005:35,2006:45,2007:45,2012:45,2013:46,2014:47,2015:47,2016:44,2017:39,
          2018:33,2019:33,2020:38,2021:34,2022:34,2023:24,2024:23,2025:23,2026:26}
RECONSTRUCTED = {'DS-2025-14', 'DS-2026-15'}
FORBIDDEN = ['高频', '必考', '冷门', '常考', '重点常考', '全网最完整', '权威']
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def fm_of(path):
    t = io.open(path, encoding='utf-8').read()
    end = t.find('\n---', 3)
    return yaml.safe_load(t[4:end]), t


def taxonomy_ids():
    txt = io.open(os.path.join(ROOT, 'docs', 'knowledge_taxonomy.md'), encoding='utf-8').read()
    return set(re.findall(r'\|\s*(DS\d{2}(?:\.\d{2}){1,3})\s*\|', txt))


def check(name):
    return {'name': name, 'result': 'PASS', 'detail': ''}


def main():
    ids = taxonomy_ids()
    rows = [json.loads(l) for l in io.open(os.path.join(ROOT, 'metadata', 'questions.jsonl'), encoding='utf-8')]
    checks = []
    files = sorted(glob.glob(os.path.join(ROOT, 'solutions', '*', '*.md')))

    # 1 file count / unique id / per-year ledger
    c = check('题数对账 / ID 唯一')
    qids = [r['question_id'] for r in rows]
    ycnt = Counter(r['year'] for r in rows)
    bad = []
    if len(files) != 661 or len(rows) != 661: bad.append('count files=%d rows=%d' % (len(files), len(rows)))
    if len(qids) != len(set(qids)): bad.append('duplicate id')
    for y, e in EXPECT.items():
        if ycnt.get(y) != e: bad.append('%d:%s!=%d' % (y, ycnt.get(y), e))
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad) or '661 文件 / 661 行 / 各年吻合'
    checks.append(c)

    # 2 metadata <-> front matter consistency (incl review)
    c = check('metadata 与 front matter 一致')
    meta = {r['question_id']: r for r in rows}
    bad = []
    for p in files:
        d, _ = fm_of(p)
        qid = d.get('question_id')
        m = meta.get(qid)
        if not m: bad.append('missing meta %s' % qid); continue
        rv = d.get('review', {}) or {}
        pt = (d.get('primary_topic') or {}).get('id')
        if m['primary_topic'] != pt: bad.append('%s primary mismatch' % qid)
        if m['solution_status'] != d.get('solution_status'): bad.append('%s status mismatch' % qid)
        if m['reconstructed'] != d.get('reconstructed'): bad.append('%s recon mismatch' % qid)
        if m['human_review_status'] != rv.get('human_review_status'): bad.append('%s review mismatch' % qid)
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad[:8]) or '全部字段一致'
    checks.append(c)

    # 3 review field rules
    c = check('AI/人工审阅字段规则')
    bad = []
    for r in rows:
        d, _ = fm_of(os.path.join(ROOT, r['file']))
        rv = d.get('review', {}) or {}
        if not isinstance(rv.get('ai_generated'), bool) or rv.get('ai_generated') is not True:
            bad.append('%s ai_generated' % r['question_id'])
        if rv.get('human_review_status') not in REVIEW_STATUS: bad.append('%s review_status' % r['question_id'])
        rounds = rv.get('human_review_rounds')
        if not isinstance(rounds, int) or rounds < 0: bad.append('%s rounds' % r['question_id'])
        if rv.get('human_review_status') == 'reviewed' and rounds < 1: bad.append('%s reviewed<1round' % r['question_id'])
        lh = rv.get('last_human_review')
        if lh is not None and not (isinstance(lh, str) and DATE_RE.match(lh)):
            bad.append('%s last_human_review date' % r['question_id'])
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad[:8]) or 'ai_generated/human_review_* 合法'
    checks.append(c)

    # 4 enum domains + type/score null
    c = check('字段枚举 / type·score 为 null')
    bad = []
    for p in files:
        d, _ = fm_of(p)
        qid = d.get('question_id')
        if d.get('question_type') is not None: bad.append('%s qtype' % qid)
        if d.get('score') is not None: bad.append('%s score' % qid)
        if d.get('solution_status') not in STATUS: bad.append('%s status' % qid)
        if d.get('ocr_confidence') not in OCR: bad.append('%s ocr' % qid)
        if (d.get('difficulty') or {}).get('level') not in DIFF: bad.append('%s diff' % qid)
        if not set(d.get('skills', []) or []) <= SKILLS: bad.append('%s skills' % qid)
        pt = (d.get('primary_topic') or {}).get('id')
        if pt not in ids: bad.append('%s primary_topic' % qid)
        for s in (d.get('secondary_topics') or []):
            if (s or {}).get('id') not in ids: bad.append('%s secondary' % qid)
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad[:8]) or '枚举与 null 约束满足'
    checks.append(c)

    # 5 reconstructed set exact + not in historical stats
    c = check('reconstructed 集与统计口径')
    rec_ids = {r['question_id'] for r in rows if r['reconstructed']}
    cov = io.open(os.path.join(ROOT, 'reports', 'syllabus_coverage.md'), encoding='utf-8').read()
    stat = io.open(os.path.join(ROOT, 'reports', 'question_statistics.md'), encoding='utf-8').read()
    bad = []
    if rec_ids != RECONSTRUCTED: bad.append('recon set=%s' % rec_ids)
    if '排除 reconstructed' not in cov or 'Supplemental' not in cov: bad.append('coverage 口径缺失')
    if '排除' not in stat: bad.append('statistics 口径缺失')
    # DS06.07 historical count must exclude the 2 reconstructed
    hist_ds0607 = sum(1 for r in rows if r['primary_topic'] == 'DS06.07' and not r['reconstructed'])
    mm = re.search(r'\|\s*DS06\.07\s*\|[^|]*\|\s*(\d+)\s*\|', cov)
    if mm and int(mm.group(1)) != hist_ds0607: bad.append('DS06.07 cov=%s hist=%d' % (mm.group(1), hist_ds0607))
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad) or 'reconstructed 已隔离于历史统计'
    checks.append(c)

    # 6 image paths: no windows backslash, referenced local images exist
    c = check('图片路径规范与存在性')
    bad = []
    img_md = glob.glob(os.path.join(ROOT, '真题', '*', '*.md')) + glob.glob(os.path.join(ROOT, 'solutions', '*', '*.md'))
    for p in img_md:
        txt = io.open(p, encoding='utf-8').read()
        for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', txt):
            ref = m.group(1).strip()
            if ref.startswith('http'): continue
            if '\\' in ref: bad.append('%s 反斜杠: %s' % (os.path.relpath(p, ROOT), ref)); continue
            ap = os.path.normpath(os.path.join(os.path.dirname(p), ref.replace('\\\\', '/')))
            if not os.path.exists(ap): bad.append('%s 缺失: %s' % (os.path.relpath(p, ROOT), ref))
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = ('; '.join(bad[:6]) or '路径均为 POSIX 且存在') + (' (%d 处)' % len(bad) if bad else '')
    checks.append(c)

    # 7 source URL consistency per year (jsonl uniform; 2005 no fabricated stem url)
    c = check('来源 URL 年份一致性')
    bad = []
    by_year = defaultdict(set)
    for r in rows:
        by_year[r['year']].add(r['source_url'])
    for y, urls in by_year.items():
        urls = {u for u in urls if u}
        if len(urls) > 1: bad.append('%d 多 URL:%s' % (y, urls))
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad) or '每年 source_url 单一'
    checks.append(c)

    # 8 disputed/uncertain/unsolvable present in registry
    c = check('争议/存疑/不可解题已登记')
    reg = io.open(os.path.join(ROOT, 'reports', 'disputed_questions.md'), encoding='utf-8').read()
    bad = []
    for r in rows:
        if r['solution_status'] in ('disputed', 'uncertain', 'unsolvable'):
            if r['question_id'] not in reg: bad.append(r['question_id'])
    c['result'] = 'PASS' if not bad else 'FAIL'; c['detail'] = '; '.join(bad[:8]) or '全部登记'
    checks.append(c)

    # 9 forbidden marketing words
    c = check('禁用营销/频率词扫描')
    bad = []
    for p in glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True):
        rel = os.path.relpath(p, ROOT)
        if ('tmp' + os.sep) in (os.sep + rel) or (os.sep + '真题' + os.sep) in (os.sep + p) or (os.sep + '考试大纲' + os.sep) in (os.sep + p):
            continue
        # exclude this validator's own report to avoid self-feedback (it echoes flagged words)
        if rel.replace('\\', '/') in ('reports/qa_report.md',):
            continue
        txt = io.open(p, encoding='utf-8').read()
        for w in FORBIDDEN:
            if w in txt: bad.append('%s:%s' % (os.path.relpath(p, ROOT), w))
    c['result'] = 'PASS' if not bad else ('WARN' if all('高频' not in b and '必考' not in b for b in bad) else 'FAIL')
    c['detail'] = '; '.join(bad[:10]) + (' (%d 处)' % len(bad) if bad else '') or '无命中'
    checks.append(c)

    fails = [k for k in checks if k['result'] == 'FAIL']
    warns = [k for k in checks if k['result'] == 'WARN']

    # write qa_report.md
    out = io.StringIO() if False else None
    lines = []
    lines.append('# 802 数据结构 · 仓库一致性 QA 报告')
    lines.append('')
    lines.append('> 由 `scripts/validate_repository.py` 生成，时间 %s。' % datetime.date.today().isoformat())
    lines.append('')
    lines.append('| # | 检查项 | 结果 | 说明 |')
    lines.append('|---|---|---|---|')
    for i, k in enumerate(checks, 1):
        lines.append('| %d | %s | %s | %s |' % (i, k['name'], k['result'], k['detail'].replace('|', '/')))
    lines.append('')
    lines.append('**汇总**：%d 项 PASS，%d 项 WARN，%d 项 FAIL。' % (
        sum(1 for k in checks if k['result'] == 'PASS'), len(warns), len(fails)))
    io.open(os.path.join(ROOT, 'reports', 'qa_report.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

    for k in checks:
        print('[%s] %s  %s' % (k['result'], k['name'], k['detail']))
    print('TOTAL: PASS=%d WARN=%d FAIL=%d' % (len(checks) - len(warns) - len(fails), len(warns), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())

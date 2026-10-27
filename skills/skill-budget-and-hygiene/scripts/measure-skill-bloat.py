#!/usr/bin/env python3
"""量化「技能把上下文吃成什么样」——回答「最近是不是变笨了 / 该先动哪个」时先跑它。

输出四块，全部是实测数字，不需要先读任何大文件：
  1. 索引固定成本：技能条数、description 总字符、system prompt 总量与各段位移
  2. 每个技能的正文大小（按字符排）
  3. 近 N 天每个技能被 skill_view 的真实成本（次数 × 平均字符），按总消耗排
  4. 体量超限清单（>8000 字符）

用法:
    python3 measure-skill-bloat.py [--days 30] [--top 15]

口径提醒（写进 skill-budget 的硬线）：单次加载 >15,000 字符 或 正文 >8,000 字符 即超标；
一次会话里堆到 40,000 字符以上之后，每一轮都要重读它们。
"""
import argparse
import glob
import json
import os
import re
import sqlite3
from collections import Counter
from datetime import datetime, timedelta

HOME = os.path.expanduser('~/.hermes')
SKILLS = os.path.join(HOME, 'skills')


def sizes():
    out = {}
    for p in glob.glob(os.path.join(SKILLS, '**', 'SKILL.md'), recursive=True):
        if '/.archive/' in p:
            continue
        name = os.path.basename(os.path.dirname(p))
        out[name] = len(open(p, encoding='utf-8', errors='replace').read())
    return out


def index_info():
    sp = os.path.join(HOME, '.skills_prompt_snapshot.json')
    if not os.path.exists(sp):
        return None
    d = json.load(open(sp, encoding='utf-8'))
    items = d.get('skills') or []
    return {'n': len(items), 'desc_chars': sum(len(i.get('description') or '') for i in items)}


def prompt_map():
    db = sqlite3.connect('file:%s?mode=ro' % os.path.join(HOME, 'state.db'), uri=True)
    try:
        row = db.execute('select prompt from system_prompts order by rowid desc limit 1').fetchone()
    except sqlite3.Error:
        return None
    finally:
        db.close()
    if not row:
        return None
    sp = row[0]
    n = len(sp)
    marks = []
    for label, needle in [('SOUL/身份', '# 语言'), ('内置执行纪律', '# Finishing the job'),
                          ('技能索引', '<available_skills>'), ('索引结束', '</available_skills>'),
                          ('MEMORY', 'MEMORY (your personal notes)'), ('USER PROFILE', 'USER PROFILE'),
                          ('运行环境', '# Hermes runtime environment')]:
        i = sp.find(needle)
        if i >= 0:
            marks.append((i, label))
    return {'total': n, 'marks': sorted(marks)}


def load_cost(days):
    db = sqlite3.connect('file:%s?mode=ro' % os.path.join(HOME, 'state.db'), uri=True)
    cut = (datetime.now() - timedelta(days=days)).timestamp()
    try:
        rows = db.execute(
            "select m.content from messages m join sessions s on s.id = m.session_id "
            "where m.tool_name = 'skill_view' and s.started_at > ?", (cut,)).fetchall()
    finally:
        db.close()
    calls, chars = Counter(), Counter()
    for (c,) in rows:
        try:
            d = json.loads(c or '{}')
        except Exception:
            continue
        n = d.get('name')
        if not n:
            continue
        calls[n] += 1
        chars[n] += len(d.get('content') or '')
    return calls, chars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--top', type=int, default=15)
    a = ap.parse_args()

    sz = sizes()
    ix = index_info()
    pm = prompt_map()
    calls, chars = load_cost(a.days)

    print('== 索引与固定成本')
    print('  技能文件 %d 个，正文合计 %d 字符' % (len(sz), sum(sz.values())))
    if ix:
        print('  索引 %d 条，description 合计 %d 字符（≈%d tok，每轮都发）'
              % (ix['n'], ix['desc_chars'], ix['desc_chars'] // 3))
    if pm:
        print('  system prompt %d 字符（≈%d tok / 轮）' % (pm['total'], pm['total'] // 2.6))
        for off, label in pm['marks']:
            print('    %5.1f%%  %s' % (off / pm['total'] * 100, label))

    print('\n== 正文最大者（上限 8,000 字符）')
    for n, s in sorted(sz.items(), key=lambda x: -x[1])[:a.top]:
        flag = '  ← 超限' if s > 8000 else ''
        print('  %6d  %s%s' % (s, n, flag))

    print('\n== 近 %d 天被加载的真实成本（次数 × 平均字符 = 总字符）' % a.days)
    if not chars:
        print('  （没有 skill_view 记录）')
    for n, tot in chars.most_common(a.top):
        print('  %6d 字符  %3d 次  平均 %5d  %s'
              % (tot, calls[n], tot // max(calls[n], 1), n))
    if chars:
        print('  合计 %d 字符 ≈ %d tok 的累积重读量' % (sum(chars.values()), sum(chars.values()) // 2.6))

    over = [(n, s) for n, s in sz.items() if s > 8000]
    print('\n== 超 8,000 字符的 %d 个（先看是不是 bundled/不用，再决定拆还是 disable）' % len(over))
    for n, s in sorted(over, key=lambda x: -x[1]):
        print('  %6d  %s' % (s, n))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

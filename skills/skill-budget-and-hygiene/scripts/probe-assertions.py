#!/usr/bin/env python3
"""跑一遍「时间敏感断言」，判断哪些已过期。

为什么需要它：路径/端口这类事实能靠 stat 判，但「模型会不会刷 Go.」「镜像还通不通」
这类是**行为断言**，读文本永远判不了——只能跑。本脚本把这类断言集成为一种清单，
每条一个探针命令，跑一次 10 秒出结论，比翻技能正文猜可靠。

用法:
    python3 probe-assertions.py            # 全跑
    python3 probe-assertions.py --only 01   # 只跑某条

输出三种结论：
    HOLDS   仍然成立
    STALE   已不成立 → 去改掉提到它的记忆/技能
    SKIP    前置条件不满足（服务没起等），不算过期

维护规则：**断言本身变了才改这里**（新增模型换代、换 provider、换服务端口）。
每条要带 since（这条断言写入记忆/技能的日期）和 how（当初靠什么验的）。
"""
import argparse
import datetime
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys

HOME = os.path.expanduser('~')
STATE = os.path.join(HOME, '.hermes/state.db')


def _db(days=7):
    cut = (datetime.datetime.now() - datetime.timedelta(days=days)).timestamp()
    db = sqlite3.connect(f'file:{STATE}?mode=ro', uri=True)
    return db, cut


def probe_go_loop():
    """模型思考流里是否仍会刷 “Go.”（用户口中的「唱歌」）。"""
    db, cut = _db(7)
    n = db.execute("""select count(*) from messages m join sessions s on s.id=m.session_id
        where s.started_at>? and m.reasoning_content like '%Go.%'""", (cut,)).fetchone()[0]
    if n:
        return 'HOLDS', f'最近 7 天有 {n} 条 reasoning 含 “Go.”（结论：换模型并未让它消失，长会话仍会刷）'
    return 'STALE', '最近 7 天 0 条 —— 可以删掉「唱歌→换非思考路由」那条，或标注“2026-10 后未复现”'


def probe_gh_proxy():
    r = subprocess.run(['curl', '-sS', '-m', '12', '-o', '/dev/null', '-w', '%{http_code}',
                        'https://gh-proxy.com/'], capture_output=True, text=True)
    code = (r.stdout or '').strip()
    if code.startswith(('2', '3')):
        return 'HOLDS', f'gh-proxy 前缀镜像可达（HTTP {code}）'
    return 'STALE', f'gh-proxy 不可用（HTTP {code or "timeout"}）→ 换镜像或改走直连/代理'


def probe_llama4b():
    r = subprocess.run(['curl', '-sS', '-m', '5', 'http://127.0.0.1:8080/v1/models'],
                       capture_output=True, text=True)
    if '"data"' in (r.stdout or ''):
        return 'HOLDS', '本地 4B 端点 :8080 在线'
    return 'SKIP', '本地 4B 未启动（前台进程，属正常）'


def probe_koishi_ports():
    live = []
    for port in (5140, 3001, 6099):
        s = socket.socket()
        s.settimeout(1.5)
        try:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                live.append(port)
        finally:
            s.close()
    if live:
        return 'HOLDS', f'QQ 机器人端口在线: {live}'
    return 'SKIP', '小雪未运行（systemd user 单元 hds-koishi/napcat-qq 未启就是这形态）'


def probe_weixin_gateway():
    p = os.path.join(HOME, '.hermes/gateway_state.json')
    if not os.path.exists(p):
        return 'SKIP', '没有 gateway_state.json'
    d = json.load(open(p))
    st = json.dumps(d, ensure_ascii=False)
    if 'weixin' in st and 'connected' in st:
        return 'HOLDS', '微信通道在 gateway 里是 connected'
    return 'STALE', '微信通道不是 connected → 要重新扫码（见 skill weixin-gateway）'


def probe_math_toolkit():
    r = subprocess.run(['git', '-C', os.path.join(HOME, '.local/share/math-toolkit'),
                        'ls-remote', '--exit-code', 'origin', 'HEAD'],
                       capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return 'HOLDS', 'math-toolkit 远端可达'
    return 'STALE', f'math-toolkit 推不上去：{(r.stderr or "").strip()[:80]}'


ASSERTIONS = [
    dict(id='01', since='2026-10-03', how='实测长会话 reasoning',
         text='deepseek-flash 思考流会刷 “Go.” → 换非思考路由 hermes -m deepseek-chat',
         fn=probe_go_loop),
    dict(id='02', since='2026-09', how='下载实测',
         text='GitHub clone 用 https://gh-proxy.com/ 前缀镜像',
         fn=probe_gh_proxy),
    dict(id='03', since='2026-10', how='curl 端点',
         text='本地 4B 在 127.0.0.1:8080/v1（llama4b 前台启动）',
         fn=probe_llama4b),
    dict(id='04', since='2026-09', how='ss -ltn',
         text='QQ 机器人小雪：控制台 5140 / OneBot 3001 / WebUI 6099',
         fn=probe_koishi_ports),
    dict(id='05', since='2026-10', how='gateway_state.json',
         text='微信网关已接（weixin=connected）',
         fn=probe_weixin_gateway),
    dict(id='06', since='2026-10', how='git ls-remote',
         text='math-toolkit 可推送（改完技能当轮 sync）',
         fn=probe_math_toolkit),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    a = ap.parse_args()
    rows = []
    for item in ASSERTIONS:
        if a.only and item['id'] != a.only:
            continue
        try:
            verdict, note = item['fn']()
        except Exception as e:
            verdict, note = 'SKIP', f'探针本身出错: {e}'
        rows.append((item, verdict, note))
    for item, verdict, note in rows:
        print(f"[{verdict:5s}] {item['id']}  {item['text']}")
        print(f"         自 {item['since']}（{item['how']}）｜{note}")
    stale = [i for i, v, _ in rows if v == 'STALE']
    print(f"\n合计 {len(rows)} 条：HOLDS {sum(1 for _, v, _ in rows if v == 'HOLDS')} / "
          f"STALE {len(stale)} / SKIP {sum(1 for _, v, _ in rows if v == 'SKIP')}")
    if stale:
        print('要改的：' + ', '.join(i['id'] for i in stale) + ' → 去记忆与技能里把对应断言改掉或标日期')
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""轻量「尝试图 + 结论门」（math-coach 用）。

设计来源：外部包 pika_math_learning_toolkit-2.1.5 的
`payload/math-coach/references/attempt-graph.md`（结论门 / fail-closed 闭包 / 只追加历史 /
有界上下文）。本实现是它的**最小忠实子集**：保留判定规则与约束，丢掉 appserver、前端、多角色、
共享内存那一整套。哪些是照抄、哪些是我自己定的，在下面的注释与
`references/attempt-graph.md` 里逐条标了。

结论门要回答的问题：你说「证完了」时，从「命题」到「这条结论」的依赖链，
是不是只由**活跃**边组成、沿途每个点都**已核**、而且该分支上**没有未闭合义务**。
浅层打上 verified 不能掩盖上游 unresolved —— 闭包是 fail-closed 的。

用法（全部输出 JSON，方便 agent 读）：
    python3 attempt_graph.py init  --session S --problem "…" [--mode GUIDED]
    python3 attempt_graph.py patch --session S --json '<patch>'
    python3 attempt_graph.py gate  --session S [--node N]
    python3 attempt_graph.py obligations --session S
    python3 attempt_graph.py context --session S [--input '…'] [--old-branch B] [--turns-file f.json]
    python3 attempt_graph.py assess --session S --verdict VERIFIED_SOLVED --note '…'
    python3 attempt_graph.py show  --session S
默认数据库：$XDG_DATA_HOME/math-attempt-graph/graph.db（可用 --db 覆盖）。
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time

# ----------------------------------------------------------------- 闭词汇（照抄原 contract）
NODE_KINDS = {
    "problem", "goal", "subgoal", "strategy", "claim", "operation", "result",
    "obstacle", "insight", "question", "checkpoint", "merge",
}
STATUSES = {"proposed", "verified", "refuted", "unresolved", "conditional"}
ORIGINS = {"user", "coach", "tool"}
EDGE_KINDS = {
    "derives_from", "depends_on", "supports", "contradicts", "blocks", "resolves",
    "alternative_to", "refines", "revisits", "contributes_to", "equivalent_to",
    "possibly_equivalent_to",
}
BRANCH_STATUSES = {"active", "paused", "exhausted", "merged"}

# 依赖闭包走的边（照抄：它们是「谁支撑谁」的边，也是查环的对象）
DEP_EDGE_KINDS = {"derives_from", "depends_on"}
CLOSURE_EDGE_KINDS = {"derives_from", "depends_on", "resolves"}
# 「实质性前驱」：只连到 problem 不算（照抄原意；具体集合是我定的）
SUBSTANTIVE_PRED_KINDS = {"claim", "operation", "result", "subgoal", "strategy", "insight", "goal"}
# 开环结点：unresolved / conditional 就是未闭合义务（照抄）
OBLIGATION_STATUSES = {"unresolved", "conditional"}
# 结论门要看的用户证明类结点（照抄「最新用户证明结点」的说法；具体集合是我定的）
PROOF_KINDS = {"claim", "result", "checkpoint"}

# 谁能建什么（原 contract 只明写了 HARD_LOCK；这里是按本地三档映射，**属我定义**）
#   GUIDED = 不得命名新对象/方法/方向 ⇒ 教练只能建 obstacle / question / checkpoint
#   HARD_LOCK = 同 GUIDED（保留名字，供以后收紧）
#   STRICT = 与 GUIDED 同
COACH_ALLOWED_KINDS = {"obstacle", "question", "checkpoint"}
TOOL_ALLOWED_KINDS = {"operation", "result"}
MODES = {"GUIDED", "STRICT", "HARD_LOCK"}

# 状态迁移表（原 contract 未给；**这是我自己定的**，写在 references 里）
TRANSITIONS = {
    "proposed": {"verified", "refuted", "unresolved", "conditional"},
    "conditional": {"verified", "refuted", "unresolved"},
    "unresolved": {"verified", "refuted", "conditional"},
    "verified": {"refuted"},
    "refuted": set(),
}

ASSESS_VERDICTS = {"UNKNOWN", "VALID_SO_FAR", "NEEDS_REPAIR", "ROUTE_READY",
                   "VERIFIED_SOLVED", "MATHEMATICALLY_BLOCKED"}

CONTEXT_NODE_LIMIT = 24          # 照抄：活动分支周围 ≤24 个结点
CONTEXT_OLD_BRANCH_LIMIT = 12    # 照抄：用户点名的旧分支 ≤12 个结点
CONTEXT_TOKEN_LIMIT = 12000      # 照抄：总包 ≤12000 tokens（这里按 len(json)/4 估算）
BRANCH_DIGEST_TOKEN_LIMIT = 1500 # 照抄：分支摘要 ≤1500 tokens


class GraphError(Exception):
    """任何校验失败都抛它；调用方 fail-closed 处理。"""


# ----------------------------------------------------------------- 存储
SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions(
  session TEXT PRIMARY KEY, created_at REAL, problem TEXT, mode TEXT, sealed INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS nodes(
  id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, kind TEXT NOT NULL,
  status TEXT NOT NULL, origin TEXT NOT NULL, label TEXT DEFAULT '', meta TEXT DEFAULT '{}',
  active INTEGER DEFAULT 1, created_at REAL);
CREATE TABLE IF NOT EXISTS edges(
  id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, src INTEGER NOT NULL,
  dst INTEGER NOT NULL, kind TEXT NOT NULL, active INTEGER DEFAULT 1, created_at REAL);
CREATE TABLE IF NOT EXISTS branches(
  id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, name TEXT NOT NULL,
  status TEXT DEFAULT 'active', is_default INTEGER DEFAULT 0, created_at REAL);
CREATE TABLE IF NOT EXISTS membership(
  node INTEGER NOT NULL, branch INTEGER NOT NULL, active INTEGER DEFAULT 1,
  PRIMARY KEY(node, branch));
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, at REAL, kind TEXT NOT NULL,
  payload TEXT DEFAULT '{}');
CREATE TABLE IF NOT EXISTS assessments(
  id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, at REAL, verdict TEXT NOT NULL,
  note TEXT DEFAULT '', graph_hash TEXT DEFAULT '');
"""


def default_db() -> str:
    base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "math-attempt-graph", "graph.db")


def connect(path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)   # 相对路径也能用
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    return conn


# ----------------------------------------------------------------- 读取辅助
def _node(conn, nid):
    r = conn.execute("SELECT * FROM nodes WHERE id=?", (nid,)).fetchone()
    if r is None:
        raise GraphError(f"结点 {nid} 不存在")
    return r


def _active_edges(conn, session, kinds=None):
    q = "SELECT * FROM edges WHERE session=? AND active=1"
    if kinds:
        q += " AND kind IN (%s)" % ",".join("?" * len(kinds))
        return conn.execute(q, (session, *kinds)).fetchall()
    return conn.execute(q, (session,)).fetchall()


def _branches_of(conn, nid):
    return [r["branch"] for r in conn.execute(
        "SELECT branch FROM membership WHERE node=? AND active=1", (nid,)).fetchall()]


def _default_branch(conn, session):
    # 分支没有 active 列，只有 status（active/paused/exhausted/merged）
    r = conn.execute("SELECT * FROM branches WHERE session=? AND status != 'merged' "
                     "ORDER BY is_default DESC, id LIMIT 1", (session,)).fetchone()
    if r is None:
        raise GraphError("会话没有可用分支")
    return r


def _problem_node(conn, session):
    r = conn.execute("SELECT * FROM nodes WHERE session=? AND kind='problem' AND active=1 "
                     "ORDER BY id LIMIT 1", (session,)).fetchone()
    if r is None:
        raise GraphError("会话没有 problem 结点")
    return r


# ----------------------------------------------------------------- 只追加事件
def _event(conn, session, kind, payload):
    conn.execute("INSERT INTO events(session,at,kind,payload) VALUES(?,?,?,?)",
                 (session, time.time(), kind, json.dumps(payload, ensure_ascii=False)))


# ----------------------------------------------------------------- 补丁校验 + 事务
def apply_patch(conn: sqlite3.Connection, session: str, patch: dict) -> dict:
    """校验并原子写入一个 GraphPatch。任何一条不过 => 全部回滚。"""
    sess = conn.execute("SELECT * FROM sessions WHERE session=?", (session,)).fetchone()
    if sess is None:
        raise GraphError(f"会话 {session} 未初始化")
    mode = patch.get("mode") or sess["mode"]
    if mode not in MODES:
        raise GraphError(f"未知模式 {mode}")

    nodes_in = patch.get("nodes", []) or []
    edges_in = patch.get("edges", []) or []
    branches_in = patch.get("branches", []) or []
    members_in = patch.get("memberships", []) or []
    corrections = patch.get("corrections", []) or []
    merges_in = patch.get("merges", []) or []

    conn.execute("BEGIN")
    try:
        tmp_ids = {}          # 模型给的临时名 -> 真实 id
        for spec in nodes_in:
            kind, status, origin = spec.get("kind"), spec.get("status"), spec.get("origin")
            if kind not in NODE_KINDS:
                raise GraphError(f"结点 kind 不在闭词汇内: {kind!r}")
            if status not in STATUSES:
                raise GraphError(f"结点 status 不在闭词汇内: {status!r}")
            if origin not in ORIGINS:
                raise GraphError(f"结点 origin 不在闭词汇内: {origin!r}")
            # 教练/工具 origin 限制
            if origin == "coach" and kind not in COACH_ALLOWED_KINDS:
                raise GraphError(f"模式 {mode} 下教练不得创建 {kind} 结点（只能 "
                                 f"{'/'.join(sorted(COACH_ALLOWED_KINDS))}）")
            if origin == "tool" and kind not in TOOL_ALLOWED_KINDS:
                raise GraphError(f"工具 origin 只能创建 {'/'.join(sorted(TOOL_ALLOWED_KINDS))} 结点")
            cur = conn.execute(
                "INSERT INTO nodes(session,kind,status,origin,label,meta,created_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (session, kind, status, origin, str(spec.get("label", ""))[:2000],
                 json.dumps(spec.get("meta", {}), ensure_ascii=False), time.time()))
            # id 由存储生成，不信任模型文本里的数字
            if spec.get("tmp"):
                tmp_ids[str(spec["tmp"])] = int(cur.lastrowid)
        # 分支
        for spec in branches_in:
            if spec.get("status", "active") not in BRANCH_STATUSES:
                raise GraphError(f"分支 status 不在闭词汇内: {spec.get('status')!r}")
            cur = conn.execute("INSERT INTO branches(session,name,status,is_default,created_at) "
                               "VALUES(?,?,?,?,?)",
                               (session, str(spec.get("name", "branch"))[:200],
                                spec.get("status", "active"),
                                1 if spec.get("is_default") else 0, time.time()))
            if spec.get("tmp"):
                tmp_ids[str(spec["tmp"])] = int(cur.lastrowid)

        def resolve(ref, expect=None):
            """ref 可以是真实 id、本补丁里的临时名，或**唯一匹配的标签/分支名**。

            标签匹配是为了跨调用方便（LLM 记不住数字 id）；不唯一就报错，不允许猜。
            """
            if isinstance(ref, int):
                _node(conn, ref)
                return ref
            s = str(ref)
            if s in tmp_ids:
                return tmp_ids[s]
            if s.isdigit():
                nid = int(s)
                _node(conn, nid)
                return nid
            rows = conn.execute("SELECT id FROM nodes WHERE session=? AND active=1 AND label=?",
                                (session, s)).fetchall()
            if len(rows) == 1:
                return rows[0]["id"]
            if len(rows) > 1:
                raise GraphError(f"标签 {s!r} 不唯一（{len(rows)} 个匹配），请改用数字 id")
            rows = conn.execute("SELECT id FROM branches WHERE session=? AND name=?", (session, s)).fetchall()
            if len(rows) == 1:
                return rows[0]["id"]
            if len(rows) > 1:
                raise GraphError(f"分支名 {s!r} 不唯一，请改用数字 id")
            raise GraphError(f"引用了不存在的对象: {ref!r}（可用：本补丁临时名 / 已有 id / 唯一标签）")

        for spec in edges_in:
            kind = spec.get("kind")
            if kind not in EDGE_KINDS:
                raise GraphError(f"边 kind 不在闭词汇内: {kind!r}")
            src, dst = resolve(spec.get("src")), resolve(spec.get("dst"))
            conn.execute("INSERT INTO edges(session,src,dst,kind,active,created_at) "
                         "VALUES(?,?,?,?,1,?)", (session, src, dst, kind, time.time()))
        for spec in members_in:
            nid, bid = resolve(spec.get("node")), resolve(spec.get("branch"))
            conn.execute("INSERT OR REPLACE INTO membership(node,branch,active) VALUES(?,?,1)",
                         (nid, bid))
        # 状态更新：必须过迁移表，且**只追加事件、不静默改**（照抄「状态变化记事件」）
        for spec in (patch.get("updates") or []):
            nid = resolve(spec.get("node"))
            new = spec.get("status")
            if new not in STATUSES:
                raise GraphError(f"结点 status 不在闭词汇内: {new!r}")
            old = _node(conn, nid)["status"]
            if old == new:
                continue
            if new not in TRANSITIONS.get(old, set()):
                raise GraphError(f"不允许的状态迁移 {old} -> {new}")
            conn.execute("UPDATE nodes SET status=? WHERE id=?", (new, nid))
            _event(conn, session, "node_status_changed",
                   {"node": nid, "old": old, "new": new, "note": spec.get("note", "")})
        # 修正：旧边标 inactive + 追加替代边（只追加历史的一部分）
        for spec in corrections:
            eid = spec.get("edge")
            row = conn.execute("SELECT * FROM edges WHERE id=? AND session=?", (eid, session)).fetchone()
            if row is None:
                raise GraphError(f"要修正的边 {eid} 不存在")
            conn.execute("UPDATE edges SET active=0 WHERE id=?", (eid,))
            _event(conn, session, "edge_corrected", {"edge": eid, "reason": spec.get("reason", "")})
            repl = spec.get("replacement")
            if repl:
                kind = repl.get("kind")
                if kind not in EDGE_KINDS:
                    raise GraphError(f"替代边 kind 不在闭词汇内: {kind!r}")
                conn.execute("INSERT INTO edges(session,src,dst,kind,active,created_at) "
                             "VALUES(?,?,?,?,1,?)",
                             (session, resolve(repl.get("src")), resolve(repl.get("dst")),
                              kind, time.time()))
        # 合并：必须显式用户确认 + 候选边（照抄）
        for spec in merges_in:
            if not spec.get("user_confirmed"):
                raise GraphError("合并需要用户显式确认（user_confirmed=true）")
            eid, bid = spec.get("candidate_edge"), resolve(spec.get("branch"))
            er = conn.execute("SELECT * FROM edges WHERE id=? AND session=?", (eid, session)).fetchone()
            if er is None or er["kind"] != "possibly_equivalent_to":
                raise GraphError("merge 必须指向一条 possibly_equivalent_to 候选边")
            conn.execute("UPDATE edges SET kind='equivalent_to' WHERE id=?", (eid,))
            conn.execute("UPDATE branches SET status='merged' WHERE id=?", (bid,))
            _event(conn, session, "branch_merged", {"edge": eid, "branch": bid})

        _verify_graph(conn, session)
        nodes_all = conn.execute("SELECT id,kind,status,origin,label FROM nodes WHERE session=? "
                                 "ORDER BY id", (session,)).fetchall()
        events = [{"nodes": len(nodes_in), "edges": len(edges_in), "branches": len(branches_in),
                   "memberships": len(members_in), "corrections": len(corrections),
                   "merges": len(merges_in), "mode": mode}]
        _event(conn, session, "patch_applied", events[0])
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {"status": "ok", "tmp_ids": tmp_ids,
            "nodes": [dict(n) for n in nodes_all]}


def _verify_graph(conn, session):
    """GraphPatch 校验：每个非 problem 结点至少属一个活跃分支；依赖边不成环。"""
    for n in conn.execute("SELECT * FROM nodes WHERE session=? AND active=1", (session,)).fetchall():
        if n["kind"] != "problem" and not _branches_of(conn, n["id"]):
            raise GraphError(f"结点 {n['id']}（{n['kind']}）不属于任何分支")
    # 查环：只走活跃依赖边
    edges = {}
    for e in _active_edges(conn, session, tuple(DEP_EDGE_KINDS)):
        edges.setdefault(e["src"], []).append(e["dst"])
    state = {}

    def dfs(n):
        st = state.get(n)
        if st == 1:
            return True
        if st == 2:
            return False
        state[n] = 1
        if any(dfs(m) for m in edges.get(n, [])):
            return True
        state[n] = 2
        return False

    for n in list(edges):
        if dfs(n):
            raise GraphError("依赖边成环（原 contract：成环的依赖不算闭合）")


# ----------------------------------------------------------------- 闭包 / 未闭合义务
def _resolved_by_closed_resolver(conn, session, nid, seen=None):
    seen = seen or set()
    target = _node(conn, nid)
    for e in _active_edges(conn, session, ("resolves",)):
        if e["dst"] != nid:
            continue
        r = _node(conn, e["src"])
        if r["status"] != "verified":
            continue
        # 教练侧的修复障碍只能由教练侧受控解析器清除（照抄：only a guarded Coach-origin
        # `resolves` edge can satisfy it）——不允许学习者自说自话清掉它
        if target["origin"] == "coach" and target["kind"] == "obstacle" and r["origin"] != "coach":
            continue
        if r["id"] in seen:
            continue                    # 解析器自身成环 ⇒ 不算清
        ok, _ = node_closed(conn, session, r["id"], seen | {nid})
        if ok:
            return True
    return False


def open_obligations(conn, session, branch=None):
    """未闭合义务 = unresolved/conditional 且没有被「已验证且自身闭合」的解析器清掉。"""
    out = []
    rows = conn.execute("SELECT * FROM nodes WHERE session=? AND active=1 ORDER BY id", (session,)).fetchall()
    for n in rows:
        if n["status"] not in OBLIGATION_STATUSES:
            continue
        if branch is not None and branch not in _branches_of(conn, n["id"]):
            continue
        if _resolved_by_closed_resolver(conn, session, n["id"]):
            continue
        out.append({"id": n["id"], "kind": n["kind"], "status": n["status"],
                    "origin": n["origin"], "label": n["label"][:120]})
    return out


def node_closed(conn, session, nid, seen=None):
    """fail-closed 递归闭包：状态必须 verified；每个活跃依赖前驱也必须闭合；成环 = 不闭。"""
    seen = seen or set()
    n = _node(conn, nid)
    if nid in seen:
        return False, {"id": nid, "why": "依赖/解析成环 ⇒ 永远算未闭合"}
    if n["status"] != "verified":
        # 未闭合义务只要被「已验证且自身闭合」的解析器清掉，就算闭合（照抄：unless an active
        # `resolves` edge points to it from a verified resolver whose own dependencies are closed）
        if n["status"] in OBLIGATION_STATUSES and _resolved_by_closed_resolver(
                conn, session, nid, seen | {nid}):
            return True, None
        return False, {"id": nid, "why": f"状态是 {n['status']}（不是 verified）", "label": n["label"][:80]}
    seen = seen | {nid}
    # 依赖方向：edge.src **依赖** edge.dst（如 claim → problem），所以 X 的依赖 = src==X 的那些边的 dst
    for e in _active_edges(conn, session, tuple(DEP_EDGE_KINDS)):
        if e["src"] != nid:
            continue
        ok, why = node_closed(conn, session, e["dst"], seen)
        if not ok:
            return False, why
    return True, None


def _reaches_problem(conn, session, nid):
    """沿「X 依赖的边」前进到 problem 结点（edge.src 依赖 edge.dst）。"""
    target = _problem_node(conn, session)["id"]
    edges = _active_edges(conn, session, tuple(CLOSURE_EDGE_KINDS))
    fwd = {}
    for e in edges:
        fwd.setdefault(e["src"], []).append(e["dst"])
    seen, stack, path = {nid}, [nid], {nid: [nid]}
    while stack:
        cur = stack.pop()
        if cur == target:
            return True, path[cur]
        for nxt in fwd.get(cur, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            path[nxt] = path[cur] + [nxt]
            stack.append(nxt)
    return False, None


def conclusion_gate(conn, session, nid=None):
    """结论门。不满足任一条件就不给过，并把原因列清楚。"""
    reasons = []
    sess = conn.execute("SELECT * FROM sessions WHERE session=?", (session,)).fetchone()
    if sess is None:
        raise GraphError(f"会话 {session} 未初始化")
    if nid is None:
        r = conn.execute("SELECT * FROM nodes WHERE session=? AND kind='checkpoint' AND active=1 "
                         "ORDER BY id DESC LIMIT 1", (session,)).fetchone()
        if r is None:
            return {"pass": False, "reasons": ["没有 checkpoint 结点：要宣布证完，先提交一个 checkpoint"],
                    "node": None, "open_obligations": open_obligations(conn, session)}
        nid = r["id"]
    n = _node(conn, nid)
    if n["kind"] != "checkpoint":
        reasons.append(f"结点 {nid} 是 {n['kind']}，不是 checkpoint")
    if n["origin"] != "user":
        reasons.append(f"checkpoint 必须由学习者提交（origin={n['origin']}）")
    if n["status"] != "verified":
        reasons.append(f"checkpoint 状态是 {n['status']}，不是 verified")

    brs = _branches_of(conn, nid)
    branch = brs[0] if brs else None
    if not brs:
        reasons.append("checkpoint 不属于任何分支")
    else:
        later = conn.execute(
            "SELECT id FROM nodes WHERE session=? AND active=1 AND origin='user' AND id>? "
            "AND kind IN (%s) ORDER BY id DESC LIMIT 1"
            % ",".join("?" * len(PROOF_KINDS)),
            (session, nid, *sorted(PROOF_KINDS))).fetchone()
        if later is not None:
            lb = _branches_of(conn, later["id"])
            if branch in lb:
                reasons.append(f"该分支上有更晚的学习者证明结点 {later['id']}，结论门只看最新的那个")

    subs = [e["dst"] for e in _active_edges(conn, session) if e["src"] == nid]
    subs = [s for s in subs if _node(conn, s)["kind"] in SUBSTANTIVE_PRED_KINDS]
    if not subs:
        reasons.append("没有实质性前驱（不能从 problem 直接跳到结论）")

    reaches, path = _reaches_problem(conn, session, nid)
    if not reaches:
        reasons.append("沿活跃的 dependency/resolution 边到不了 problem 结点")
    else:
        for p in path:
            ok, why = node_closed(conn, session, p)
            if not ok:
                reasons.append(f"依赖链上有未闭合点：{why}")
                break

    obs = open_obligations(conn, session)
    mine = [o for o in obs if branch is None or branch in _branches_of(conn, o["id"])]
    if mine:
        reasons.append("该分支还有未闭合义务：" + "、".join(
            f"#{o['id']} {o['kind']}/{o['status']}" for o in mine))

    return {"pass": not reasons, "node": nid, "branch": branch, "reasons": reasons,
            "dependency_path": path, "open_obligations": obs}


def reject_conclusion(conn, session, nid, reason):
    """结论被拒 => 建一个 session 级修复障碍（照抄）；下个主张不继承失败路径。"""
    conn.execute("BEGIN")
    try:
        cur = conn.execute("INSERT INTO nodes(session,kind,status,origin,label,meta,created_at) "
                           "VALUES(?,'obstacle','unresolved','coach',?,?,?)",
                           (session, f"修复障碍：{reason}",
                            json.dumps({"from_conclusion": nid, "reason": reason},
                                       ensure_ascii=False), time.time()))
        oid = int(cur.lastrowid)
        b = _default_branch(conn, session)
        conn.execute("INSERT OR REPLACE INTO membership(node,branch,active) VALUES(?,?,1)", (oid, b["id"]))
        conn.execute("INSERT INTO edges(session,src,dst,kind,active,created_at) "
                     "VALUES(?,?,?,'blocks',1,?)", (session, oid, nid, time.time()))
        _event(conn, session, "conclusion_rejected", {"checkpoint": nid, "obstacle": oid,
                                                       "reason": reason})
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {"obstacle": oid}


# ----------------------------------------------------------------- 有界上下文
def _est_tokens(obj) -> int:
    return max(1, len(json.dumps(obj, ensure_ascii=False)) // 4)


def context_packet(conn, session, user_input="", old_branch=None, turns=None):
    """按原 contract 的预算切上下文；先丢旧对话轮次，再丢旧分支细节，永不动必需项。"""
    sess = conn.execute("SELECT * FROM sessions WHERE session=?", (session,)).fetchone()
    problem = _problem_node(conn, session)
    branch = _default_branch(conn, session)
    nodes = conn.execute(
        "SELECT n.* FROM nodes n JOIN membership m ON m.node=n.id AND m.active=1 "
        "WHERE n.session=? AND m.branch=? AND n.active=1 ORDER BY n.id DESC LIMIT ?",
        (session, branch["id"], CONTEXT_NODE_LIMIT)).fetchall()
    nodes = [{"id": n["id"], "kind": n["kind"], "status": n["status"], "origin": n["origin"],
              "label": n["label"][:120]} for n in reversed(nodes)]
    packet = {
        "mode": sess["mode"], "sealed": bool(sess["sealed"]),
        "problem": {"id": problem["id"], "label": problem["label"][:400]},
        "branch": {"id": branch["id"], "name": branch["name"], "status": branch["status"]},
        "nodes": nodes,
        "verified_facts": [n for n in nodes if n["status"] == "verified"],
        "refuted": [n for n in nodes if n["status"] == "refuted"],
        "open_obligations": open_obligations(conn, session, branch["id"]),
        "current_input": user_input,
    }
    if old_branch:
        ob = conn.execute("SELECT * FROM branches WHERE id=? AND session=?", (old_branch, session)).fetchone()
        if ob:
            on = conn.execute(
                "SELECT n.id,n.kind,n.status,n.label FROM nodes n JOIN membership m "
                "ON m.node=n.id AND m.active=1 WHERE m.branch=? AND n.active=1 "
                "ORDER BY n.id DESC LIMIT ?", (old_branch, CONTEXT_OLD_BRANCH_LIMIT)).fetchall()
            packet["old_branch"] = {"id": ob["id"], "name": ob["name"],
                                   "nodes": [dict(x) for x in on]}
    digest = {"branches": [dict(r) for r in conn.execute(
        "SELECT id,name,status,is_default FROM branches WHERE session=?", (session,))]}
    while _est_tokens(digest) > BRANCH_DIGEST_TOKEN_LIMIT and digest["branches"]:
        digest["branches"].pop()            # 摘要超预算就削
    packet["branch_digest"] = digest
    if turns:
        packet["recent_turns"] = turns[-5:]      # 照抄：最近 5 轮可见对话
    dropped = []
    if _est_tokens(packet) > CONTEXT_TOKEN_LIMIT and packet.get("recent_turns"):
        packet.pop("recent_turns")
        dropped.append("recent_turns")
    if _est_tokens(packet) > CONTEXT_TOKEN_LIMIT and packet.get("old_branch"):
        packet.pop("old_branch")
        dropped.append("old_branch")
    packet["dropped"] = dropped
    packet["est_tokens"] = _est_tokens(packet)
    if packet["est_tokens"] > CONTEXT_TOKEN_LIMIT:
        raise GraphError(f"上下文包超预算（{packet['est_tokens']} > {CONTEXT_TOKEN_LIMIT}），"
                         "必需项不能丢：请缩小 problem/branch 规模")
    return packet


def assess(conn, session, verdict, note=""):
    if verdict not in ASSESS_VERDICTS:
        raise GraphError(f"未知完成度标签 {verdict}")
    if verdict == "MATHEMATICALLY_BLOCKED":
        # 照抄：必须有「排除了该范围内所有延续」的有范围障碍，单个被反驳结点不算
        obs = [r for r in conn.execute("SELECT * FROM nodes WHERE session=? AND kind='obstacle' "
                                       "AND status='unresolved' AND active=1", (session,)).fetchall()]
        scoped = [o for o in obs if (json.loads(o["meta"] or "{}").get("scoped") or
                                     json.loads(o["meta"] or "{}").get("excludes_all"))]
        if not scoped:
            raise GraphError("MATHEMATICALLY_BLOCKED 需要一条有范围的障碍（meta 里 scoped=true / "
                             "excludes_all=true），单个被反驳的结点不能推出它")
    conn.execute("INSERT INTO assessments(session,at,verdict,note) VALUES(?,?,?,?)",
                 (session, time.time(), verdict, note))
    _event(conn, session, "assessment", {"verdict": verdict, "note": note})
    conn.commit()
    return {"verdict": verdict}


def init_session(conn, session, problem, mode="GUIDED"):
    if mode not in MODES:
        raise GraphError(f"未知模式 {mode}")
    if conn.execute("SELECT 1 FROM sessions WHERE session=?", (session,)).fetchone():
        raise GraphError(f"会话 {session} 已存在")
    conn.execute("BEGIN")
    try:
        conn.execute("INSERT INTO sessions(session,created_at,problem,mode) VALUES(?,?,?,?)",
                     (session, time.time(), problem, mode))
        cur = conn.execute("INSERT INTO nodes(session,kind,status,origin,label,created_at) "
                           "VALUES(?,?,?,?,?,?)",
                           (session, "problem", "verified", "user", problem, time.time()))
        pid = int(cur.lastrowid)
        cur = conn.execute("INSERT INTO branches(session,name,status,is_default,created_at) "
                           "VALUES(?,'主路线','active',1,?)", (session, time.time()))
        bid = int(cur.lastrowid)
        conn.execute("INSERT OR REPLACE INTO membership(node,branch,active) VALUES(?,?,1)", (pid, bid))
        _event(conn, session, "session_init", {"problem": problem, "mode": mode})
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {"session": session, "problem_node": pid, "branch": bid, "mode": mode}


def show(conn, session):
    b = conn.execute("SELECT * FROM branches WHERE session=?", (session,)).fetchall()
    n = conn.execute("SELECT id,kind,status,origin,label FROM nodes WHERE session=? AND active=1 "
                     "ORDER BY id", (session,)).fetchall()
    e = conn.execute("SELECT id,src,dst,kind,active FROM edges WHERE session=? ORDER BY id",
                     (session,)).fetchall()
    a = conn.execute("SELECT verdict,note FROM assessments WHERE session=? ORDER BY id",
                     (session,)).fetchall()
    return {"branches": [dict(x) for x in b], "nodes": [dict(x) for x in n],
            "edges": [dict(x) for x in e], "assessments": [dict(x) for x in a],
            "open_obligations": open_obligations(conn, session)}


# ----------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="尝试图 + 结论门（只读/写入均输出 JSON）")
    ap.add_argument("--db", default=default_db())
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("--session", required=True)
    p.add_argument("--problem", required=True); p.add_argument("--mode", default="GUIDED")
    p = sub.add_parser("patch"); p.add_argument("--session", required=True); p.add_argument("--json", required=True)
    p = sub.add_parser("gate"); p.add_argument("--session", required=True); p.add_argument("--node", type=int)
    p = sub.add_parser("reject"); p.add_argument("--session", required=True)
    p.add_argument("--node", type=int, required=True); p.add_argument("--reason", required=True)
    p = sub.add_parser("obligations"); p.add_argument("--session", required=True)
    p = sub.add_parser("context"); p.add_argument("--session", required=True)
    p.add_argument("--input", default=""); p.add_argument("--old-branch", type=int)
    p.add_argument("--turns-file")
    p = sub.add_parser("assess"); p.add_argument("--session", required=True)
    p.add_argument("--verdict", required=True); p.add_argument("--note", default="")
    p = sub.add_parser("show"); p.add_argument("--session", required=True)

    args = ap.parse_args(argv)
    conn = connect(args.db)
    try:
        if args.cmd == "init":
            out = init_session(conn, args.session, args.problem, args.mode)
        elif args.cmd == "patch":
            out = apply_patch(conn, args.session, json.loads(args.json))
        elif args.cmd == "gate":
            out = conclusion_gate(conn, args.session, args.node)
        elif args.cmd == "reject":
            out = reject_conclusion(conn, args.session, args.node, args.reason)
        elif args.cmd == "obligations":
            out = {"open_obligations": open_obligations(conn, args.session)}
        elif args.cmd == "context":
            turns = json.load(open(args.turns_file, encoding="utf-8")) if args.turns_file else None
            out = context_packet(conn, args.session, args.input, args.old_branch, turns)
        elif args.cmd == "assess":
            out = assess(conn, args.session, args.verdict, args.note)
        else:
            out = show(conn, args.session)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except GraphError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())

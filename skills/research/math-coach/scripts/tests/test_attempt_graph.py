#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attempt_graph.py 的行为测试（每条对应 references/attempt-graph.md 里的一条规则）。

跑：python3 scripts/tests/test_attempt_graph.py   （unittest，无第三方依赖）
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))

import attempt_graph as ag  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="attempt-graph-test-")
        self.conn = ag.connect(os.path.join(self.tmp, "g.db"))
        self.s = "S"
        ag.init_session(self.conn, self.s, "证明：144 阶群不单")
        b = self.conn.execute("SELECT id FROM branches WHERE session=?", (self.s,)).fetchone()["id"]
        self.branch = b
        self.problem = self.conn.execute(
            "SELECT id FROM nodes WHERE session=? AND kind='problem'", (self.s,)).fetchone()["id"]

    def tearDown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)     # 不留临时目录在 TMPDIR 里

    def patch(self, **kw):
        return ag.apply_patch(self.conn, self.s, kw)

    def mk(self, kind, status, origin, label, depends_on=None, branch=None, tmp=None, meta=None):
        """结点 + 依赖边 + 分支成员必须在**同一个补丁**里（存储要求每个非 problem 结点属至少一个分支）。"""
        tmp = tmp or f"t{self.conn.execute('SELECT COUNT(*) c FROM nodes').fetchone()['c']}"
        spec = {"tmp": tmp, "kind": kind, "status": status, "origin": origin, "label": label}
        if meta:
            spec["meta"] = meta
        edges = [{"src": tmp, "dst": self.problem, "kind": "depends_on"}]
        if depends_on:
            edges.append({"src": tmp, "dst": depends_on, "kind": "depends_on"})
        out = self.patch(nodes=[spec], edges=edges,
                         memberships=[{"node": tmp, "branch": branch or self.branch}])
        return out["tmp_ids"][tmp]

    # ---------------- 基础
    def test_clean_chain_passes_gate(self):
        a = self.mk("claim", "verified", "user", "用 Sylow 得 n_3 ∈ {1,4,16}")
        b = self.mk("claim", "verified", "user", "排除 n_3=4", depends_on=a)
        cp = self.mk("checkpoint", "verified", "user", "整条路线闭合", depends_on=b)
        res = ag.conclusion_gate(self.conn, self.s, cp)
        self.assertTrue(res["pass"], res["reasons"])

    # ---------------- 闭词汇与引用
    def test_closed_vocabulary_rejected(self):
        with self.assertRaises(ag.GraphError):
            self.patch(nodes=[{"kind": "lemma", "status": "verified", "origin": "user", "label": "x"}])
        with self.assertRaises(ag.GraphError):
            self.patch(nodes=[{"kind": "claim", "status": "probably", "origin": "user", "label": "x"}])

    def test_unknown_reference_rolls_back(self):
        before = self.conn.execute("SELECT COUNT(*) c FROM nodes").fetchone()["c"]
        with self.assertRaises(ag.GraphError):
            self.patch(nodes=[{"tmp": "n1", "kind": "claim", "status": "verified",
                               "origin": "user", "label": "孤点"}],
                       edges=[{"src": "n1", "dst": 99999, "kind": "depends_on"}],
                       memberships=[{"node": "n1", "branch": self.branch}])
        after = self.conn.execute("SELECT COUNT(*) c FROM nodes").fetchone()["c"]
        self.assertEqual(before, after, "校验失败必须整体回滚，不留半成品")

    def test_cycle_rejected(self):
        a = self.mk("claim", "verified", "user", "A")
        b = self.mk("claim", "verified", "user", "B", depends_on=a)
        with self.assertRaises(ag.GraphError):
            self.patch(edges=[{"src": a, "dst": b, "kind": "depends_on"}])

    def test_node_needs_branch(self):
        with self.assertRaises(ag.GraphError):
            self.patch(nodes=[{"kind": "claim", "status": "verified", "origin": "user", "label": "无分支"}])

    # ---------------- 教练权限
    def test_coach_cannot_create_claim(self):
        with self.assertRaises(ag.GraphError):
            self.patch(nodes=[{"tmp": "x", "kind": "claim", "status": "proposed", "origin": "coach",
                               "label": "教练替他想"}],
                       memberships=[{"node": "x", "branch": self.branch}])

    def test_coach_may_create_obstacle_and_question(self):
        o = self.mk("obstacle", "unresolved", "coach", "还差一步没证")
        q = self.mk("question", "proposed", "coach", "你觉得卡在哪")
        self.assertTrue(o and q)

    # ---------------- 结论门：fail-closed（核心）
    def test_shallow_verified_does_not_hide_unresolved_ancestor(self):
        a = self.mk("claim", "conditional", "user", "假设两两交平凡（未证）")
        b = self.mk("claim", "verified", "user", "由上面的假设推 n_2=1", depends_on=a)
        cp = self.mk("checkpoint", "verified", "user", "证完", depends_on=b)
        res = ag.conclusion_gate(self.conn, self.s, cp)
        self.assertFalse(res["pass"], "浅层 verified 不能掩盖上游 conditional")
        self.assertTrue(any("未闭合" in r for r in res["reasons"]), res["reasons"])

    def test_verified_resolver_clears_obligation(self):
        a = self.mk("claim", "conditional", "user", "条件性假设")
        b = self.mk("claim", "verified", "user", "依赖它", depends_on=a)
        cp = self.mk("checkpoint", "verified", "user", "证完", depends_on=b)
        self.assertFalse(ag.conclusion_gate(self.conn, self.s, cp)["pass"])
        # 一个已验证、且自身依赖闭合的解析器：把条件性假设清掉
        r = self.mk("claim", "verified", "user", "补证：条件其实总成立")
        self.patch(edges=[{"src": r, "dst": a, "kind": "resolves"}])
        # 注意：新增了一条学习者证明结点，按规则必须**重新声明闭合**（门只看最新那个）
        cp2 = self.mk("checkpoint", "verified", "user", "补证后重新声明闭合", depends_on=b)
        res = ag.conclusion_gate(self.conn, self.s, cp2)
        self.assertTrue(res["pass"], res["reasons"])

    def test_gate_requires_latest_checkpoint(self):
        a = self.mk("claim", "verified", "user", "第一步")
        cp1 = self.mk("checkpoint", "verified", "user", "我认为证完了", depends_on=a)
        c2 = self.mk("claim", "verified", "user", "其实还漏了一种情形", depends_on=a)
        res = ag.conclusion_gate(self.conn, self.s, cp1)
        self.assertFalse(res["pass"])
        self.assertTrue(any("更晚" in r for r in res["reasons"]), res["reasons"])

    def test_gate_needs_substantive_predecessor(self):
        cp = self.mk("checkpoint", "verified", "user", "空的闭合声明")
        res = ag.conclusion_gate(self.conn, self.s, cp)
        self.assertFalse(res["pass"])
        self.assertTrue(any("实质性前驱" in r for r in res["reasons"]), res["reasons"])

    # ---------------- 拒绝 => 修复障碍
    def test_rejected_conclusion_blocks_next_one(self):
        a = self.mk("claim", "verified", "user", "第一步")
        cp = self.mk("checkpoint", "verified", "user", "证完", depends_on=a)
        self.assertTrue(ag.conclusion_gate(self.conn, self.s, cp)["pass"])
        ag.reject_conclusion(self.conn, self.s, cp, "排除 n_3=4 那步不成立")
        res = ag.conclusion_gate(self.conn, self.s, cp)
        self.assertFalse(res["pass"], "被拒后必须挡住下一次结论")
        self.assertTrue(any("未闭合义务" in r for r in res["reasons"]), res["reasons"])
        obs = ag.open_obligations(self.conn, self.s)
        self.assertTrue(any(o["kind"] == "obstacle" for o in obs))

    def test_obstacle_needs_coach_origin_resolver(self):
        a = self.mk("claim", "verified", "user", "第一步")
        cp = self.mk("checkpoint", "verified", "user", "证完", depends_on=a)
        ag.reject_conclusion(self.conn, self.s, cp, "那步不成立")
        obs = [o for o in ag.open_obligations(self.conn, self.s) if o["kind"] == "obstacle"][0]
        # 用户自说自话地解析：不该算清（障碍只能由教练侧受控解析器清）
        r_user = self.mk("claim", "verified", "user", "我自己觉得没问题了")
        self.patch(edges=[{"src": r_user, "dst": obs["id"], "kind": "resolves"}])
        self.assertFalse(ag.conclusion_gate(self.conn, self.s, cp)["pass"],
                         "用户 origin 的解析不能清教练障碍")

    # ---------------- 只追加
    def test_correction_appends_not_overwrites(self):
        a = self.mk("claim", "verified", "user", "旧步骤")
        b = self.mk("claim", "verified", "user", "新步骤")
        e = self.conn.execute("SELECT id FROM edges WHERE src=? AND dst=?", (a, self.problem)).fetchone()["id"]
        self.patch(corrections=[{"edge": e, "reason": "这条依赖写错了",
                                 "replacement": {"src": a, "dst": b, "kind": "depends_on"}}])
        old = self.conn.execute("SELECT active FROM edges WHERE id=?", (e,)).fetchone()
        self.assertEqual(old["active"], 0, "旧边要保留但标 inactive")
        ev = self.conn.execute("SELECT COUNT(*) c FROM events WHERE kind='edge_corrected'").fetchone()["c"]
        self.assertEqual(ev, 1)

    def test_status_update_validated_and_logged(self):
        n = self.mk("claim", "proposed", "user", "待核")
        self.patch(updates=[{"node": n, "status": "verified"}])
        st = self.conn.execute("SELECT status FROM nodes WHERE id=?", (n,)).fetchone()["status"]
        self.assertEqual(st, "verified")
        ev = self.conn.execute("SELECT COUNT(*) c FROM events WHERE kind='node_status_changed'").fetchone()["c"]
        self.assertEqual(ev, 1, "状态变化要追加事件，不静默改")
        with self.assertRaises(ag.GraphError):
            self.patch(updates=[{"node": n, "status": "proposed"}])       # verified 不能回 proposed
        self.patch(updates=[{"node": n, "status": "refuted"}])
        with self.assertRaises(ag.GraphError):
            self.patch(updates=[{"node": n, "status": "verified"}])       # refuted 是终态

    # ---------------- 合并
    def test_merge_requires_user_confirmation(self):
        a = self.mk("claim", "verified", "user", "A")
        b = self.mk("claim", "verified", "user", "B")
        self.patch(edges=[{"src": a, "dst": b, "kind": "possibly_equivalent_to"}])
        eid = self.conn.execute("SELECT id FROM edges WHERE kind='possibly_equivalent_to'").fetchone()["id"]
        with self.assertRaises(ag.GraphError):
            self.patch(merges=[{"candidate_edge": eid, "branch": self.branch}])
        out = self.patch(merges=[{"candidate_edge": eid, "branch": self.branch, "user_confirmed": True}])
        self.assertEqual(out["status"], "ok")

    # ---------------- 上下文预算
    def test_context_packet_is_bounded(self):
        for i in range(40):
            self.mk("claim", "verified", "user", f"步骤 {i} " + "很长的描述" * 40)
        turns = [{"role": "user", "text": "噜" * 2000} for _ in range(20)]
        pkt = ag.context_packet(self.conn, self.s, "现在证到哪了", turns=turns)
        self.assertLessEqual(len(pkt["nodes"]), ag.CONTEXT_NODE_LIMIT)
        self.assertLessEqual(pkt["est_tokens"], ag.CONTEXT_TOKEN_LIMIT)
        for key in ("mode", "problem", "current_input", "open_obligations"):
            self.assertIn(key, pkt, f"必需项 {key} 不能被丢掉")

    # ---------------- 完成度标签
    def test_blocked_requires_scoped_obstacle(self):
        n = self.mk("claim", "refuted", "user", "这个反例否掉了猜想")
        with self.assertRaises(ag.GraphError):
            ag.assess(self.conn, self.s, "MATHEMATICALLY_BLOCKED", "不行")
        # 一条「有范围、排除了该范围内所有延续」的障碍才行（coach origin 就是这里的意义）
        self.mk("obstacle", "unresolved", "coach",
                "在 n_3=16 且交都平凡的范围内已排除所有延续",
                meta={"scoped": True, "excludes_all": True})
        self.assertEqual(ag.assess(self.conn, self.s, "MATHEMATICALLY_BLOCKED", "有范围")["verdict"],
                         "MATHEMATICALLY_BLOCKED")

    def test_assessment_is_append_only(self):
        ag.assess(self.conn, self.s, "VALID_SO_FAR", "还不完整")
        ag.assess(self.conn, self.s, "NEEDS_REPAIR", "发现缺口")
        rows = self.conn.execute("SELECT verdict FROM assessments ORDER BY id").fetchall()
        self.assertEqual([r["verdict"] for r in rows], ["VALID_SO_FAR", "NEEDS_REPAIR"],
                         "前一次的评估不能被覆盖")


if __name__ == "__main__":
    unittest.main(verbosity=2)

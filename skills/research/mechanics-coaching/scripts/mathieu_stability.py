#!/usr/bin/env python3
"""Mathieu 方程 x'' + (delta + eps*cos t) x = 0 的稳定图（纯 stdlib + RK4）。

判据（Floquet）：一周期 T=2*pi 的转移矩阵 M 满足 |tr M| < 2  <=>  所有解有界。
输出 PGM：白 = 稳定，黑 = 不稳定。

自检：delta < 0, eps = 0 必不稳定（解是指数函数）。脚本出图前断言这一点——
颜色映射写反时图照样「看着像图」，但结论全反。
验收：舌尖应落在 delta = 0, 0.25, 1, 2.25, 4（即 n^2/4）。

用法： mathieu_stability.py W H dmin dmax emin emax N out.pgm
例：   python3 mathieu_stability.py 600 450 -1.5 4.5 0 3 200 g.pgm
       magick g.pgm g.png          # 再在 TikZ 里套坐标轴与刻度
       python3 mathieu_stability.py --tr 0.25 0.1   # 单点抽查 tr M
"""
import math
import sys


def flawless(tr):
    return abs(tr) < 2.0


def compute_tr(delta, eps, N=200):
    """返回一个周期的转移矩阵 M 的迹。步长 h=2*pi/N，RK4。"""
    h = 2.0 * math.pi / N
    cs = [math.cos(k * h) for k in range(N + 1)]
    cm = [math.cos((k + 0.5) * h) for k in range(N)]
    x1, v1, x2, v2 = 1.0, 0.0, 0.0, 1.0
    for k in range(N):
        a0 = -(delta + eps * cs[k])
        a1 = -(delta + eps * cm[k])
        a2 = -(delta + eps * cs[k + 1])
        kx1, kv1, kx2, kv2 = v1, a0 * x1, v2, a0 * x2
        mx1, mv1 = x1 + 0.5 * h * kx1, v1 + 0.5 * h * kv1
        mx2, mv2 = x2 + 0.5 * h * kx2, v2 + 0.5 * h * kv2
        lx1, lv1, lx2, lv2 = mv1, a1 * mx1, mv2, a1 * mx2
        nx1, nv1 = x1 + 0.5 * h * lx1, v1 + 0.5 * h * lv1
        nx2, nv2 = x2 + 0.5 * h * lx2, v2 + 0.5 * h * lv2
        ox1, ov1, ox2, ov2 = nv1, a1 * nx1, nv2, a1 * nx2
        px1, pv1 = x1 + h * ox1, v1 + h * ov1
        px2, pv2 = x2 + h * ox2, v2 + h * ov2
        qx1, qv1, qx2, qv2 = pv1, a2 * px1, pv2, a2 * px2
        x1 += h / 6.0 * (kx1 + 2 * lx1 + 2 * ox1 + qx1)
        v1 += h / 6.0 * (kv1 + 2 * lv1 + 2 * ov1 + qv1)
        x2 += h / 6.0 * (kx2 + 2 * lx2 + 2 * ox2 + qx2)
        v2 += h / 6.0 * (kv2 + 2 * lv2 + 2 * ov2 + qv2)
    return x1 + v2


def render(W, H, dmin, dmax, emin, emax, N, path):
    rows = []
    for j in range(H):
        eps = emin + (j + 0.5) / H * (emax - emin)
        row = bytearray()
        for i in range(W):
            delta = dmin + (i + 0.5) / W * (dmax - dmin)
            row.append(255 if flawless(compute_tr(delta, eps, N)) else 0)
        rows.append(bytes(row))
    with open(path, "wb") as f:
        f.write(b"P5\n%d %d\n255\n" % (W, H))
        for r in reversed(rows):  # 图像首行 = eps 最大
            f.write(r)


def main(argv):
    # 先把颜色映射钉死：反向区必不稳定
    t = compute_tr(-1.0, 0.0)
    assert abs(t) > 2.0, "delta<0,eps=0 应不稳定；颜色映射或积分写反了"
    print("selfcheck ok: tr M(-1,0) = %.3f (|.|>2 ⇒ 黑)" % t)

    if argv and argv[0] == "--tr":
        print("tr M(%s,%s) = %.6f  %s" % (
            argv[1], argv[2], compute_tr(float(argv[1]), float(argv[2])),
            "稳定" if flawless(compute_tr(float(argv[1]), float(argv[2]))) else "不稳定"))
        return

    W, H = int(argv[0]), int(argv[1])
    dmin, dmax = float(argv[2]), float(argv[3])
    emin, emax = float(argv[4]), float(argv[5])
    N = int(argv[6])
    render(W, H, dmin, dmax, emin, emax, N, argv[7])
    print("wrote", argv[7])


if __name__ == "__main__":
    main(sys.argv[1:])

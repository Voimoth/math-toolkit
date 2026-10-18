#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""有心力场进动角的数值自检(纯 stdlib;本机没有 scipy)。

一个径向周期(=题里说的「一圈」)的进动角
    delta_theta = 2*Delta_theta - 2*pi,
    Delta_theta = \int_{rmin}^{rmax} (l/r^2) dr / sqrt(2(E - V_eff(r)))
单位质量:V_eff(r) = -alpha/r + deltaV(r) + l^2/(2r^2)。

支持的扰动(对齐 hw4 第 5 题):
    deltaV = beta/r^2  -> 精确值 2*pi*(1/sqrt(1+2beta/l^2) - 1)  ~= -2*pi*beta/l^2
    deltaV = gamma/r^3 -> 一阶值 -6*pi*gamma*alpha/l^4 = -6*pi*gamma/(alpha*p^2), p = l^2/alpha

运行:  python3 precession_check.py
"""
import math


def make_V(alpha=1.0, ell=1.0, beta=0.0, gam=0.0):
    """返回 (V_eff, V_eff');beta 折进离心项系数(l^2/2 + beta)。"""
    def V(r):
        return -alpha / r + gam / r ** 3 + (ell ** 2 / 2 + beta) / r ** 2

    def Vp(r):
        return alpha / r ** 2 - 3 * gam / r ** 4 - (ell ** 2 + 2 * beta) / r ** 3

    return V, Vp


def bisect(f, a, b, n=200):
    fa = f(a)
    for _ in range(n):
        m = (a + b) / 2
        if fa * f(m) <= 0:
            b = m
        else:
            a, fa = m, f(m)
    return (a + b) / 2


def simpson(f, a, b, n=2000):
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def delta_theta(alpha=1.0, ell=1.0, beta=0.0, gam=0.0, E=-0.375, n=2000):
    """返回 (delta_theta, rmin, rmax);E 取开普勒能量刻度。"""
    V, Vp = make_V(alpha, ell, beta, gam)
    rmin = bisect(lambda r: V(r) - E, 1e-4, 1.0)
    rmax = bisect(lambda r: V(r) - E, 1.0, 60.0)
    rm, rd = (rmin + rmax) / 2, (rmax - rmin) / 2
    # 端点解析极限:E - V_eff 在两端是 0/0 型,不填会毁掉 Simpson 的收敛速度
    lim_in = ell * math.sqrt(rd) / (rmin ** 2 * math.sqrt(abs(Vp(rmin))))
    lim_out = ell * math.sqrt(rd) / (rmax ** 2 * math.sqrt(abs(Vp(rmax))))

    def w(th):
        if th == 0.0:
            return lim_out
        if th == math.pi:
            return lim_in
        r = rm + rd * math.cos(th)
        val = 2 * (E - V(r))
        if val <= 0:
            return 0.0
        return ell / r ** 2 * rd * math.sin(th) / math.sqrt(val)

    return 2 * simpson(w, 0.0, math.pi, n) - 2 * math.pi, rmin, rmax


def lagrange_at_zero(xs, ys):
    """Lagrange 插值外推到 x = 0(三点二次,够用来消 O(x) 项)。"""
    tot = 0.0
    for i, xi in enumerate(xs):
        w = 1.0
        for j, xj in enumerate(xs):
            if j != i:
                w *= (0.0 - xj) / (xi - xj)
        tot += ys[i] * w
    return tot


def main():
    print("管线自检:beta/r^2 有精确值,数值必须先对上")
    for beta in (0.001, 0.002):
        d, _, _ = delta_theta(beta=beta, n=20000)
        exact = 2 * math.pi * (1 / math.sqrt(1 + 2 * beta) - 1)
        print(f"  beta={beta}: 数值 {d: .10f}   精确 {exact: .10f}")

    print("gamma/r^3:E=-0.375(无扰 e=0.5),外推到 gamma->0 应给 -6*pi")
    gams, ratios = [0.0005, 0.001, 0.002, 0.004], []
    for g in gams:
        d, rmin, rmax = delta_theta(gam=g, n=20000)
        ratios.append(d / g)
        print(f"  gamma={g}: delta/gamma = {d / g: .9f}   rmin={rmin:.6f} rmax={rmax:.6f}")
    ext = lagrange_at_zero(gams[:3], ratios[:3])
    print(f"  外推 gamma->0: {ext: .9f}   -6*pi = {-6 * math.pi: .9f}"
          f"   相对差 {(ext + 6 * math.pi) / (-6 * math.pi): .2e}")

    print("e 无关性检查(gamma=0.0005,换 E 即换无扰 e):首项应与 e 无关")
    for E in (-0.20, -0.375, -0.45):
        d, _, _ = delta_theta(gam=0.0005, E=E, n=20000)
        print(f"  E={E}: delta/gamma = {d / 0.0005: .9f}")


if __name__ == "__main__":
    main()

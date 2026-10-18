# hw5（Schwarzschild 测地线）:已验证骨架与他的追问（2026-10-08）

题地图见 SKILL.md，记号与朗道出处见 `hw4-hw5-central-force.md`。本文件存 **Q1–Q3 的可复用骨架 + 已核实数字 + 他实际问过的四个技术点**。

## Q1(a) 四个 E-L 方程（已与他核对）

$f\equiv1-2GM/r$，$\dot{}=\dd/\dd\tau$：

- $t$：$\dd(f\dot t)/\dd\tau=0\Rightarrow f\dot t=E$
- $\varphi$：$r^2\sin^2\theta\,\dot\varphi=L$
- $\theta$：$\ddot\theta+\frac{2\dot r}{r}\dot\theta=\sin\theta\cos\theta\,\dot\varphi^2$
- $r$：$\ddot r-\frac{GM}{r^2f}\dot r^2+\frac{GM}{r^2}f\dot t^2-rf(\dot\theta^2+\sin^2\theta\dot\varphi^2)=0$
  等价于 $\ddot r=\frac{GM}{r^2f}\dot r^2-\frac{GM}{r^2}f\dot t^2+rf(\dot\theta^2+\sin^2\theta\dot\varphi^2)$（**他问过「$\dot r^2$ 的系数为什么我算出来是正的」**：两种移项方式都合法，符号跟着 r̈ 在哪边换；独立校验用 $\Gamma^r_{rr}=-f'/(2f)$）

外加二次型第一积分：$2\mathcal L=-f\dot t^2+f^{-1}\dot r^2+r^2\dot\theta^2+r^2\sin^2\theta\dot\varphi^2=-1$（$m\ne0$）。

### 他问过：归一化从哪来？为什么 $\mathcal L$ 是常数？

- 归一化 = 「$\tau$ 是原时」的定义（$\dd s^2=-g_{\mu\nu}\dd x^\mu\dd x^\nu$ 除以 $\dd\tau^2$；等价四速归一 $u\cdot u=-1$），不是附加假设。
- $\mathcal L$ 守恒两条路：① Beltrami（$\mathcal L$ 不显含 $\tau$）$+$ Euler 齐次定理（二次齐次 $\Rightarrow \dot x^\mu\partial\mathcal L/\partial\dot x^\mu=2\mathcal L$）；② 几何：E-L 即测地线 $\nabla_{\dot x}\dot x=0$，而 $\dd(g(\dot x,\dot x))/\dd\tau=2g(\dot x,\nabla_{\dot x}\dot x)=0$。**常数的值** $-1$ 才是约定（换仿射参数 $s=a\tau+b$ 则 $=-1/a^2$）。
- 与他已学的 hw2 Beltrami 恒等式直接对接（同一件事）。

### 他问过：题目要求「从 r̈ 积分」，两种方法等价吗？

等价，且是逐字等价：把 $f\dot t=E$、$\dot\varphi=L/r^2$ 代进 $r$ 方程后得 $\ddot r=-\tfrac12V''_{\rm eff}(r)$；而它正是 $\dot r^2=E^2-V_{\rm eff}$ 对 $\tau$ 求导再除以 $\dot r$ 的结果。「也可以从四个首积分直接得到」= 省掉中间一步（**因为 r̈ 方程里含 $\dot t^2,\dot\varphi^2$，不先用首积分消掉就无从积分**）；两条路的唯一差别是常数怎么定（单积 r̈ 只给「$\tfrac12\dot r^2+\tfrac12V_{\rm eff}=$const」，需归一化认成 $E^2/2$）。

## Q1(b) 赤道面

$\theta$ 方程在 $\theta=\pi/2,\dot\theta=0$ 处右端 $=\sin(\pi/2)\cos(\pi/2)\dot\varphi^2=0$，故 $\ddot\theta=0$；$(\theta,\dot\theta)=(\pi/2,0)$ 是二维系统的平衡初值，由二阶方程解的唯一性得恒有 $\theta\equiv\pi/2$。他说「很简单」——后续别再展开。

## Q1(c) 有效势

$-f\dot t^2+f^{-1}\dot r^2+L^2/r^2=-1$ $\to$ 用 $\dot t=E/f$ $\to$ 两边乘 $f$：
$$\dot r^2=E^2-V_{\rm eff}(r;L),\qquad V_{\rm eff}=(1-2GM/r)(1+L^2/r^2)$$

**他问过「$E$ 前面为什么没有系数」**：是「乘 $f$」乘出来的——$-f\dot t^2=-E^2/f$，乘 $f$ 恰好清掉；$E\equiv f\dot t$ 这个定义就是为它服务。更本质：二次型第一积分本质是 $E^2=p^2+m^2$ 结构，所以出现 $E^2$ 而非 $E$（hw4 的 $\dot r^2=(2/\mu)(E-V_{\rm eff})$ 是线性，因为那是时间参数化下的能量守恒）。$r\to\infty$ 时 $V_{\rm eff}\to1$，$E=1$ 是「从无穷远静止下落」的分界。

## Q2 驻点 / 势垒顶 / ISCO（他说会做，数字已独立数值核实）

$$V_{\rm eff}'=0\iff GM r^2-L^2r+3GML^2=0,\qquad r_\pm=\frac{L^2\pm\sqrt{L^4-12G^2M^2L^2}}{2GM}$$

- 两个驻点 $\iff L>2\sqrt3\,GM$；**小根 $r_-$ 是极大（势垒顶）**，大根 $r_+$ 是极小（稳定圆轨道）。
- 极大值 $=1\iff \boxed{L=4GM}$，此时 $r=4GM$（数值：$V_{\rm eff}(4)=1.000000$）。
- 拐点（两驻点重合 = ISCO）$\iff \boxed{L=2\sqrt3\,GM,\ r=6GM}$（数值 $V'(6)=V''(6)=0$）。
- **别混淆**：$b_c=3\sqrt3\,GM$ 是光子的临界碰撞参数 $b=L/E$，不是本题这只 $V_{\rm eff}$ 的「极大值 $=1$」条件（本题答案是 $4GM$）。$L>4GM$ 时极大值 $>1$，任何 $E^2<1$ 的粒子都不会掉进去。
- 轨道分类：$E^2$ 与 $V_{\rm eff}$ 交点个数 → 落入 / 散射 / 束缚（束缚需 $E^2<1$ 且 $E^2>V_{\rm eff}^{\min}$ 且 $E^2<\min(1,V_{\rm eff}^{\max})$）。

## Q3 GR 比内方程

**先把 hw 的归一化读准：右端第一项是 $(GM/L)^2$**（PDF 里那个平方印在分式右上角，`pdftotext` 会把它甩到上一行，看起来像 $GM/L$）。

换元（$u\equiv GM/r$，$L=r^2\dot\varphi$，$u'=\dd u/\dd\varphi$）：
$$\dot r=-\frac{Lu'}{GM},\qquad \ddot r=-\frac{L^2u^2}{G^3M^3}u''$$
（第一式：$\dd r/\dd\varphi=-GM\,u'/u^2$ 再乘 $\dot\varphi=L/r^2$；先化简再求导，$u^2$ 全消掉、$u'$ 前系数是常数——**他问过这一步怎么来的，要摊开写**。）配合 $\ddot r=-\tfrac12V_{\rm eff}'$ 并把右端也换成 $u$：
$$\boxed{u''+u=\Big(\frac{GM}{L}\Big)^2+3u^2}$$
传统归一 $u=1/r$（$L$ 为单位质量角动量）：$u''+u=GM/L^2+3GMu^2$。

**他问过「为什么没有 $E$」**：Binet 是「轨道形状」的方程，形状只由 $L$ 与引力场决定；$E$ 决定从同一族里挑哪一条（偏心率/近日点距离），藏在初条件 $(u(0),u'(0))$ 里。推导第一步（用归一化把 $E^2-\dot r^2=V_{\rm eff}$ 代进 $r$ 方程）就把 $E$ 消成了 $\dot r$ 与 $r$。佐证：hw4-2 的牛顿版 $u''+u=\mu k/L^2$ 也没有 $E$。

Q3 的独立自检钩子：$3u^2$ 项 $\Leftrightarrow$ hw4-5 的 $\delta V=\gamma/r^3$ 微扰取 $\gamma=-GMl^2$，代 $\delta\theta=-6\pi\gamma/(kp^2)$ 应给顺行的 $6\pi GM/(a(1-e^2))$。

## 已交付物（2026-10-09 小测用）

`/mnt/e/notes/物理/理论力学/速查/理论力学B-速查表.tex` + `.pdf`（3 页 A4 双栏，已 commit+push）。
内容：考场配方 / 变分法 / 拉格朗日+对称性 / 有心力（hw4 全套）/ Schwarzschild（hw5）/ 易错点 / 数学工具。
编译：`xelatex -interaction=nonstopmode <file>.tex`（本机 ctex+ctexart+xeCJK 齐备）。
坑：① `\sec` 与 ctex 已有宏冲突，改用 `\Sec`；② 两栏排版里长公式必须拆行，否则 Overfull 会串到另一栏（用 `align*` + `&&` 或另起 display）。

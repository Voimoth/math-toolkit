# 变分法基础(2026-09-14 答疑记录)

用户问:「变分和导数有什么区别?为什么可以和积分号互换?」——这是变分法唯一容易含糊过去的地方。
以下讲解已整理进 `/mnt/e/notes/物理/理论力学/变分法与最小作用量原理.md`。

## 讲解要点(可复用)

1. **变分 = 函数空间上的方向导数**,不是新导数。扰动设 $x_\varepsilon(t)=x(t)+\varepsilon\eta(t)$,
   $\varepsilon\in\mathbb{R}$ 是数、$\eta$ 是固定方向(整条函数)。$S(\varepsilon)$ 退化成普通一元函数,
   $\delta S:=\frac{d}{d\varepsilon}S(\varepsilon)|_{\varepsilon=0}$。
   - 记号:$\delta S=\int\frac{\delta S}{\delta x(t)}\eta(t)dt$,$\frac{\delta S}{\delta x(t)}$ 是变分导数(泛函的梯度)。
   - $\delta S=0\ \forall\eta \iff \frac{\delta S}{\delta x(t)}=0\ \forall t$。
2. **换序不是"变分与积分互换"** —— 常见误解。积分号一直在外面;真正交换的是
   $\frac{\partial}{\partial\varepsilon}$ 与 $\frac{\partial}{\partial t}$ / $\int dt$。
   条件是分析III的积分号下求导定理(区间有限 + $\partial_\varepsilon L$ 连续/被控制),物理里自动满足。
   **要点:求导变量是 $\varepsilon$,积分变量是 $t$,两者独立。**
3. **$\delta$ 三条规则**:线性;链式 $\delta L=L_x\delta x+L_{\dot x}\delta\dot x$;
   $\delta(\frac{dx}{dt})=\frac{d}{dt}(\delta x)$(因 $\varepsilon,t$ 独立,混合偏导相等)。
4. **等时变分**:$x_\varepsilon(t)=x(t)+\varepsilon\eta(t)$ 只扰动函数值、不扰动时间,故 $\delta t=0$。
   显含 $t$ 的 $L(q,\dot q,t)$ 变分时 $t$ 不动,$\delta L=L_q\delta q+L_{\dot q}\delta\dot q$。
   注意区分非等时变分(需另加 $L\delta t$ 项,本课程不涉及)。
5. **全导数无害**:$\delta(\frac{df}{dt})=\frac{d}{dt}(f_q\delta q)$,积一下只剩边界项
   $[f_q\delta q]_{t_1}^{t_2}=0$。这是作业第 2(a) 题的全部内容。
6. **分部积分是引擎**:目的是把所有 $\delta$ 的导数搬走、让 $\eta$ 光溜溜露出来,才能用
   **变分法基本引理**(连续 $g$ 满足 $\int g\eta=0\ \forall\eta\Rightarrow g\equiv0$)。
   第 1 题($L$ 含 $\ddot x$)要做两次分部积分。
7. **对比表**:普通极值(变量 $x\in\mathbb R$、增量 $h$、条件 $f'=0$)
   vs 变分(变量属函数空间、增量 $\eta(t)$、条件 $\delta S=0\ \forall\eta$、结果是一个 ODE)。

## 与用户既有知识的衔接

- 严格性依据走分析III的「积分号下求导」,用户已学(分析III 已覆盖一致收敛/控制收敛)。
  不要引入测度论角度(用户未学)。
- 用户偏好:定理名不记编号;讲严格条件时说清「哪些是本质、哪些是技术性」。

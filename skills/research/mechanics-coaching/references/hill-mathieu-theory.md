# Hill / Mathieu 方程：稳定性理论全套（讲这类方程的现成讲义）

触发：用户问「参数共振怎么处理」「这类方程（周期系数）理论上怎么解释」，或作业做到 Mathieu 那一步。
交付形态：按下面的编号分块渲成图（每块两三行公式 + 一句人话），**符号先定义、定理先说他解决什么问题**——见 SKILL.md 第 24 条。

## 0. 方程族

$\ddot x+p(t)x=0$，$p(t+T)=p(t)$ → Hill 方程；$p=\delta+\varepsilon\cos t$ 是 Mathieu 方程。
**约定陷阱**：写成 $p=\delta+\varepsilon\cos2\tau$（即 $\tau=\Omega t/2$）时所有 $\delta,\varepsilon$ 系数要换算，与频率 1 的写法差 4 倍。答题必须注明用哪种。

## 1. 判据链（精确，不需要任何小参数）

1. 状态 $\mathbf s=(x,\dot x)\in\mathbb R^2$，线性二阶方程由初值唯一决定解。
2. 一周期推进矩阵：$\mathbf s(T)=M\mathbf s(0)$，$M$ 与初值无关（线性 ⇒ 映射线性）。
3. $\mathbf s(nT)=M^n\mathbf s(0)$ ⇒ 有界性由 $M$ 的特征值 $\lambda_1,\lambda_2$ 定：模 $<1$ 衰减、$=1$ 有界、$>1$ 指数增长。
4. $\det M=1$：相空间向量场 $(\dot x,\ \ddot x)=(\dot x,\ -p(t)x)$ 散度为 $0$（方程无 $\dot x$ 项 ⇒ 无阻尼）⇒ 面积守恒 ⇒ 一周期倍数 $=1$。
5. ⇒ $\lambda_1\lambda_2=1$，$\lambda$ 满足 $\lambda^2-(\operatorname{tr}M)\lambda+1=0$：
   $|\operatorname{tr}M|<2$ 稳定（共轭复根、模 $=\sqrt{\det M}=1$）；$=2$ 边界（解以 $T$ 或 $2T$ 为周期）；$>2$ 不稳定（两实根互为倒数）。

结论：**只需算一个数 $\operatorname{tr}M$**。一般无初等表达式，只有数值积分或小参数展开（平均法）两条路。

## 2. 舌（tongue）从哪里来：$\delta=n^2/4$

$\varepsilon=0$ 时解是 $A\cos(\sqrt\delta\,t)+B\sin(\sqrt\delta\,t)$，频率 $\sqrt\delta$。
加小 $\varepsilon$ 后多出 $\cos t$（角频率 1），积化和差使解生出频率 $\sqrt\delta\pm n$。
当新频率等于原频率的相反数（$\sqrt\delta-n=-\sqrt\delta$）时两者无法区分，振幅线性累积 ⇒ 共振：
$$\sqrt\delta=\frac n2\iff\delta=\frac{n^2}{4},\qquad n=1,2,\dots$$
$n=1$ 即 $\delta=1/4$，主共振。不稳定区随 $\varepsilon$ 增大向两侧张开，在 $(\delta,\varepsilon)$ 平面上是以 $(n^2/4,0)$ 为尖点的楔形
——**楔形像舌头，所以叫不稳定舌**（名字只是形状，不是新概念）。宽度：$n=1$ ∝ $\varepsilon$，$n\ge2$ ∝ $\varepsilon^n$。

$\delta<0$ 那半边不是舌：$\varepsilon=0$ 时 $\ddot x=|\delta|x$ 解是指数函数，本来就不稳定，要靠足够大的 $\varepsilon$ 拉回稳定区。

## 3. 倒立摆落在哪一支（hw7 Q3 的接口）

小角方程 $\ddot\varphi+\bigl(\tfrac{a\Omega^2}{l}\cos\Omega t-\tfrac gl\bigr)\varphi=0$：取频率 1 写法时 $\delta=-g/(l\Omega^2)\le0$、$\varepsilon=a/l$。
⇒ **倒立摆不在小 $\varepsilon$ 的舌里**，它在 $\delta<0$ 反向区，靠**大 $\varepsilon$ 的 Kapitza 机制**稳定。
一阶判据：$a^2\Omega^2>2gl$（等价 $\delta+\varepsilon^2/2>0$，频率 1 约定；$\tau=\Omega t/2$ 约定则写 $\delta+\varepsilon^2/8>0$）。
**只在高频成立**：$|\delta|\ll1$，即 $\Omega\gg\sqrt{g/l}$。$\Omega\approx2\sqrt{g/l}$ 那条主舌属于**下垂单摆**（$\delta=+g/(l\Omega^2)$），别搬到倒立摆上。

## 4. 快慢分离为什么合法，以及 ξ 的量级

- **响应量级 = 驱动幅度除以 $(\omega_0^2-\Omega^2)$**：$\ddot\xi+\omega_0^2\xi=F\cos\Omega t\Rightarrow\xi=F\cos\Omega t/(\omega_0^2-\Omega^2)$；
  $\Omega\gg\omega_0$ 时 $\xi\simeq-F\cos\Omega t/\Omega^2$。所以驱动幅度里的 $\Omega^2$ 被分母除掉，$\xi$ 剩下 $O(a/l)\Phi$——
  **「ξ 和驱动力同阶」是错的说法**，正确的是「驱动幅度除以 $\Omega^2$」。
- 严格性：两尺度展开 $\varphi=\Phi+\xi$（$\Phi$ 慢、$\xi$ 快），每阶 $\partial_\tau^2\varphi_n=F_n(\tau)$ 有有界周期解 $\iff\overline{F_n}=0$（Fredholm 可解性条件 / 消长期项）。
- 展开只在 $t\lesssim l/(a\Omega)$ 内有效；$t\to\infty$ 的严格判据是 Floquet（平均法只是它的一阶）。两层分开写，判据才站得住。

## 5. 数值验证（独立于解析那条路）

`scripts/mathieu_stability.py`：RK4 积一周期得 $\operatorname{tr}M$，扫描 $(\delta,\varepsilon)$ 网格输出二值图（白稳定 / 黑不稳定）。

- 每周期 200 步 RK4 够用（误差 ~1e-5，能分辨主舌的 $\varepsilon\sim10^{-3}$）；600×450 网格纯 stdlib 约 30 s。
- **先验已知点再出图**：$\delta<0,\varepsilon=0$ 必不稳定。颜色映射写反时图照样「看着像图」，但结论全反（本次第一版就把稳定画成了黑）。
- 验收：舌尖必须落在 $\delta=0,0.25,1,2.25,4$（$n^2/4$）。自算图与解析推导各走一路对上，才算「验过」。
- 出 PNG 后在 TikZ 里套坐标轴与刻度（`\includegraphics` + `\foreach` 画 tick），中文用 xeCJK，渲完 vision 复核再发。

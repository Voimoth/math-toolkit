# hw6 / hw7（2026 秋）：线性代数准备、微振动、振子轨道、参数共振

## hw6（线性代数复习 + 耦合振子）

- Q1(a)–(e)：Dirac 符号下的伴随算符 $(A^+)_{ij}=\overline{A_{ji}}$、对称算符的实谱/正交/对角化、$A'=T^{-1}AT$、$x'=T^{-1}x$。
  易错：讲义的下标约定 $A_{ji}=\langle e_j|\hat A|e_i\rangle$（下标先左矢），以及 $T$ 与 $T^{-1}$ 的方向（$T_{ij}=\langle e_i|\xi_j\rangle$，$(T^{-1})_{ij}=\langle\xi_i|e_j\rangle$）。
- Q2：两个二次型同时主轴化：特征方程 $\det(B-\lambda A)=0$、根为实的理由（Rayleigh 商分母正定）、用 $A^{1/2}$ 构造 $A$-正交归一本征矢。
- Q3：耦合振子
  $$L=\tfrac12m_1\dot x^2-\tfrac12k_1x^2+\tfrac12m_2\dot y^2-\tfrac12k_2y^2+\alpha xy,$$
  频率由 $(k_1-m_1\omega^2)(k_2-m_2\omega^2)=\alpha^2$ 给出；简正坐标 = $M$-正交本征矢给出的线性组合。

## hw7（微振动 / 振子轨道 / 参数共振）

- Q1：双摆微振动（讲义 §5.1.3 = PDF 90–94 页、朗道 §23 习题 2）。**讲义把这件事拆在两节，别混为一谈**：
  - **§5.1.2（93–94 页）**：E-L → $(M)\ddot X+(K)X=0$ → 设 $A e^{i\omega t}$ → $\det(k_{\alpha\beta}-\omega^2m_{\alpha\beta})=0$（式 5.20）求**本征频率**。只给频率，不给简正坐标。
  - **§5.1.3（90–94 页例题）**：双摆**只做到矩阵方程就停了**，没往下解。
  - **§5.4 简正模式（98–102 页）**：从 (5.13) 出发，用 $\tilde X=M^{1/2}X$ 化到 $\ddot{\tilde X}=-\lambda\tilde X$，$\lambda=M^{-1/2}KM^{-1/2}$ 对称 → 正交本征矢 $\rho_i$ → 简正坐标 $y_j=\langle\rho_j|\tilde X\rangle$。**对角化的是 $\lambda$，不是 $M$ 或 $K$ 本身**。
  两条路等价：$\det(\lambda-\omega^2I)=\det(K-\omega^2M)/\det M$，$\omega^2$ 是同一批根。**差别在产出**：(c) 要的变换矩阵就是 $\rho_i$，所以 (b)+(c) 一起做必须走 §5.4。
  **讲义笔误（已核）**：94 页把 $k_{11}$ 印成 $(m_1+m_2)l_1^2$，漏了 $g$（应为 $(m_1+m_2)gl_1$）；$k_{22}=m_2gl_2$ 那行是对的。交代时顺带教「用量纲一眼看出」这个判据。
  $m_1=m_2,\,l_1=l_2$ 时退回 $\omega^2=(2\pm\sqrt2)g/l$，**只能用于自检**，不是一般答案。
- Q2：$V=\frac12kr^2$ 的轨道（朗道 §23 习题 3）：笛卡尔坐标分量独立为简谐；椭圆中心**在力心**（对比开普勒的焦点）；等时、$\omega_r=2\omega_\theta$。
  已写入 vault `物理/理论力学/轨道方程与比内公式.md` 的「各向同性振子」节。
- Q3：参数共振（Arnold 倒立摆、支点 $y=a\cos\Omega t$）：小角方程
  $$\ddot\varphi=\Bigl(\frac gl-\frac{a\Omega^2}{l}\cos\Omega t\Bigr)\varphi .$$
  取 $\tau=\Omega t/2$ 后为 Mathieu 形：$\delta=-4g/(l\Omega^2)\le 0$、$\epsilon=4a/l$。
  **$\delta\le0$ 是「反向区」**：$\epsilon=0$ 时方程本身就不稳定，所以倒立摆**不是**靠小 $\epsilon$ 的不稳定舌稳定，而是靠**大 $\epsilon$ 的 Kapitza 机制**拉回稳定区。
  一阶判据 $a^2\Omega^2>2gl$。与 Mathieu 语言的关系**依赖约定，必须注明**：用频率 1 的写法 $p=\delta+\epsilon\cos t$（本例 $\delta=-g/(l\Omega^2)$、$\epsilon=a/l$）时边界是 $\delta+\epsilon^2/2=0$；用 $\tau=\Omega t/2$ 的写法则是 $\delta+\epsilon^2/8=0$。两种约定系数差 4 倍。
  $\Omega\approx2\sqrt{g/l}$ 那条**主舌属于下垂单摆**（$\delta=+g/(l\Omega^2)>0$），与倒立摆不是一回事，别搬。
  两层判据分开写：平均法/快慢分离给一阶近似，**严格判据是 Floquet 乘子**（一周期转移矩阵：$|\operatorname{tr}M|<2$ 稳定、$=2$ 边界、$>2$ 不稳定）。定量边界不要凭记忆报数。

## 进度与起手（2026-10-21）

- 原题：`~/下载/hw7-2026.pdf`（已归档 `/mnt/e/书籍/物理/理论力学/作业/hw7-2026.pdf`）。
  **Q2 原文写的是 $V=\tfrac12 k(x^2+y^2)$（笛卡尔写法）**——讲题沿题面的写法走，不要先改写成 $\tfrac12kr^2$ 再解释；他会逐字对照题面核对自己的答案。
- Q1 三小问的交付物分别是：(a) 二阶 $T,V$；(b) 动力学方程 + 本征频率 + 振动解；(c) 简正坐标 + 振动解 + **坐标变换矩阵**。
- 起手点选 Q1(a)：给的目标是「写出 $m_1,m_2$ 的两点位置 → 代入小角 → $T,V$ 各保留到二阶」，并交代保留准则的人话版——**某一项留不留，看它相对哪一项是二阶小量**，不是机械的「含 $\theta$ 就留」。说完即停手，等他自己写 $(x_2,y_2)$。

### Q1(a) 已完成（2026-10-21）

他两次**手写拍照**发来求核。第一版：V 已对，T 的交叉项写成 $\tfrac12 m_2l_1l_2\dot\theta_1\dot\theta_2$（差 4 倍）。第二版改对，最终
$$L=\tfrac12 m_1(l_1^2\dot\theta_1^2-l_1g\theta_1^2)+\tfrac12 m_2\bigl(l_1^2\dot\theta_1^2+l_2^2\dot\theta_2^2+2l_1l_2\dot\theta_1\dot\theta_2-l_1g\theta_1^2-l_2g\theta_2^2\bigr)$$
逐项核对无误。**下次从 (b) 起**：路线已定案走 §5.4（见上面 Q1 条），交付物是动力学方程 + 本征矢量 $\rho_i$；已要求他先写 $M,K$ 两个 $2\times2$ 矩阵（尚未提交）。

错处的讲法（可复用）：只说判据让他重算那一小步——
$\vec v_2=\vec v_1+l_2\dot\theta_2\hat e_2\Rightarrow|\vec v_2|^2=|\vec v_1|^2+l_2^2\dot\theta_2^2+2\,\vec v_1\cdot(l_2\dot\theta_2\hat e_2)$，
$\vec v_1\cdot\hat e_2=l_1\dot\theta_1\cos(\theta_1-\theta_2)$，那个 2 乘上外面 $\tfrac12m_2$ 仍剩 2。不把整段 T 重写给他。

- **记号约定**：他的 $\theta_1,\theta_2$ **都从竖直向下量**（T 用 $\cos(\theta_1-\theta_2)$、V 用 $\cos\theta_1,\cos\theta_2$ 自洽可验）。照片里弧线画不清时不要在记号上纠缠，先按公式内部自洽判定。

## 讲解顺序建议

1. 先 hw6 Q1–Q2 的线性代数语言（对偶、伴随、广义本征值），否则 Q3 与 hw7 Q1 的「$M$、$K$」无从谈起。
2. 再用 hw6 Q3 → hw7 Q1 走「一个耦合例子 → 一般微振动」的归纳。
3. hw7 Q2 归到 `轨道方程与比内公式`（比内方程在该势下非线性，说明为什么改用笛卡尔坐标）。
4. hw7 Q3 先讲「受迫 vs 参数」的区别，再写方程，最后才谈稳定区；判据的具体数值留给教材图。

## Q1(b) 已完成（2026-10-21）：核对过的答案与三条简化

他自己算出、我方重算 det 后确认全对：
$$M=\begin{pmatrix}(m_1+m_2)l_1^2 & m_2l_1l_2\\ m_2l_1l_2 & m_2l_2^2\end{pmatrix},\quad K=\operatorname{diag}\bigl((m_1+m_2)gl_1,\ m_2gl_2\bigr)$$
$\det(K-\omega^2M)=0$ 除以 $m_2l_1l_2$ 化为 $m_1l_1l_2\lambda^2-(m_1+m_2)g(l_1+l_2)\lambda+(m_1+m_2)g^2=0$（$\lambda=\omega^2$）；
本征矢 $\rho_\pm=\bigl(1,\ \frac{(m_1+m_2)(g-\lambda_\pm l_1)}{\lambda_\pm m_2l_2}\bigr)$；特例下低频 $(1,\sqrt2)$ 同相、高频 $(1,-\sqrt2)$ 反相。
**交付前的自检判据**：退化到 $m_1=m_2=m,\ l_1=l_2=l$ 必须回到 $(2\pm\sqrt2)g/l$（朗道 §23 习题 2）。
他说「我懒得算了，直接告诉我答案」→ 只给了 (b) 的全答案，(c) 未交付，留到下一轮。

**「通式太复杂，有没有简单算法」的三招**（都验过；**必须如实说明不改变最终答案复杂度**，只省推导与出错点）：

1. 无量纲化：$\mu=m_2/m_1,\ r=l_2/l_1,\ s=\omega^2l_1/g$ ⇒ $r s^2-(1+\mu)(1+r)s+(1+\mu)=0$，参数从 4 个降到 2 个；等质量等长即 $s^2-4s+2=0$。
2. 只要和与积就用韦达：$\omega_1^2+\omega_2^2=\frac{(m_1+m_2)g(l_1+l_2)}{m_1l_1l_2}$、$\omega_1^2\omega_2^2=\frac{(m_1+m_2)g^2}{m_1l_1l_2}$。
3. 换水平位移 $u_1=l_1\theta_1,\ u_2=l_1\theta_1+l_2\theta_2$ ⇒ $M=\operatorname{diag}(m_1,m_2)$、$V=\tfrac12\alpha u_1^2+\tfrac12\beta(u_2-u_1)^2$（$\alpha=(m_1+m_2)g/l_1,\ \beta=m_2g/l_2$），退化成 hw6 Q3 的标准两振子。代价：(c) 要变换矩阵时还得换回 $\theta$ 坐标。

## 他连问的三个概念混淆（都直接给答案，不甩回去）

1. **$M,K$ 是同一批数，不是两套。** 定义即 $T=\tfrac12\sum m_{\alpha\beta}\dot x_\alpha\dot x_\beta$、$V=\tfrac12\sum k_{\alpha\beta}x_\alpha x_\beta$ 的系数矩阵；代进 E-L 后系数**不变**，因为定义里的 $\tfrac12$ 与 $\sum$ 的重复计数互消（靠 $m_{\alpha\beta}=m_{\beta\alpha}$）。
   **边界（要主动说）**：若 $L$ 含 $x\dot x$ 混合项（磁场 $A\cdot v$ 式），出来的是反对称「陀螺」矩阵，这条不成立。
   手写读数规则：把 $T$ 写成不带 $\tfrac12$ 的 $C_{11}\dot x_1^2+C_{12}\dot x_1\dot x_2+C_{22}\dot x_2^2$，则 $m_{11}=2C_{11}$、$m_{12}=C_{12}$、$m_{22}=2C_{22}$——**对角乘 2、交叉不乘**。
2. **简正坐标不是单位化特征向量。** $\rho$ 是空间方向（不随时间变），$y_j=\langle\rho_j|M^{1/2}X\rangle$ 是随时间变的坐标变量；归一化只是让 $y$ 唯一，本质是解耦成 $y_j''=-\omega_j^2y_j$。
3. **正交化其实不用 Gram–Schmidt。** 对称矩阵不同本征值的本征矢自动正交，两行即证：$\lambda_1\langle v_1,v_2\rangle=\langle Av_1,v_2\rangle=\langle v_1,Av_2\rangle=\lambda_2\langle v_1,v_2\rangle$。实际只需 M-内积归一化 $\xi/\sqrt{\xi^TM\xi}$；Gram–Schmidt 只在**重根**时才有活干。
   验算：$m_1=m_2=m,\ l_1=l_2=l$ 取 $\xi_\pm=(1,\mp\sqrt2)$，$\xi_+^TM\xi_-=0$（展开正好抵消）。
4. **「(c) 只是把 (b) 单位化、振动解根本没变」——一半对。** 物理内容确实不变（$\omega_i$ 与模形状是归一化不敏感的不变量，换坐标不产生新解），
   要纠的只是「简正坐标 = 单位化的 $\rho$」：$\rho$ 是常矢量、$y$ 是随时间变的坐标，两者不是同一个对象。
   回答这类**对象混淆**时直接上代数骨架，不要写「前半句对后半句错」的散文——那会被斥「毫无可读性」；
   对他尝试的判定压成一行，后面必须是数学。

## (c) 的代数骨架（已核，可直接交付）

记号：$M,K\in\mathrm{Sym}(n,\mathbb R)$、$M\succ0$；$\xi_i\ne0$ 满足 $(K-\lambda_iM)\xi_i=0$、$\lambda_i=\omega_i^2$，
取 $M$-正交归一 $\xi_i^{\mathsf T}M\xi_j=\delta_{ij}$。令 $\Xi=[\xi_1\cdots\xi_n]$、$T=\Xi^{\mathsf T}M$。

```
① ΞᵀMΞ = I  ⇒  TΞ = I  ⇒  T = Ξ⁻¹
② y := Tθ = Ξ⁻¹θ,   θ = Ξy
③ 代入 Mθ̈ + Kθ = 0： ΞᵀMΞ·ÿ + ΞᵀKΞ·y = 0  ⇒  ÿ + diag(λ)y = 0
   （ΞᵀKΞ = diag(λᵢ)：由 λⱼMξⱼ = Kξⱼ 左乘 ξᵢᵀ 得 ξᵢᵀKξⱼ = λⱼδᵢⱼ）
④ yᵢ(t) = Aᵢ·cos(ωᵢt + φᵢ)
```

归一化不改物理的**精确**表述：$\xi_i\to c_i\xi_i\Rightarrow\Xi\to\Xi C,\ T\to C^{-1}T,\ y\to C^{-1}y$（$C=\mathrm{diag}(c_i)$）；
$\omega_i$ 与 $\theta$ 都不变，只有 $y$ 的各分量按 $c_i^{-1}$ 缩放。**故 $y$ 只在 $M$-正交归一约定下唯一确定。**

交付 (c) 时给三样就够：变换矩阵 $T=\Xi^{\mathsf T}M$、逆变换 $\theta=\Xi y$、两个简正频率与 $y_i(t)$。
第二个特例可当自用验收：$m_1=m_2=m,\ l_1=l_2=l$ 时 $\Xi$ 的列取 $\frac{1}{\sqrt{ml^2(4\mp2\sqrt2)}}(1,\pm\sqrt2)^{\mathsf T}$（分母分别是低频/高频的），验 $\Xi^{\mathsf T}M\Xi=I$。

## (c) 的交付形态（手机对话期）

- **公式一律渲图**：xelatex A4 单页 + `pdftoppm -r 150`，中文用 `xeCJK` + `Noto Sans CJK SC`，随回复 `MEDIA:` 发。
  不贴 LaTeX 源码、不用 Unicode 上标冒充——他原话「你直接打 latex 我这里没法渲染，遇到这种需要 latex 的情况你发图片不就好了」。
  纯文字判断与追问仍走正文，只有公式才出图。
- 交付物：$r_i$、$N_i$、$\xi_i$、$y_i$、$\Xi$ 与 $T$、加特例对照。
  $N_i=\sqrt{(m_1+m_2)l_1^2+2m_2l_1l_2r_i+m_2l_2^2r_i^2}$；特例 $N_\pm=l\sqrt{m(4\pm2\sqrt2)}$，$T$ 的第 $i$ 行 $=(ml^2/N_i)(2+r_i,\ 1+r_i)$。
- 已如实告知：$N_i$ 与 $T$ 的元素没有更漂亮的闭式（$\lambda_i$ 本身已是二次方程的根），交作业写到这一步即够。

## Q2 起手：三处前提必需纠（两处不成立、一处需降级）

1. **「微振动只是把 L 约到二阶，现在 L 本来就二阶，处理方法一样」——成立，但工具退化。**
   正确前提是「$L$ 为纯二次型（无一次项、无 $x\dot x$ 混合、不显含 $t$）」，微振动只负责保证这一点，不是额外条件。
   Q2 里 $M=m\mathbf 1_2$、$K=k\mathbf 1_2$ ⇒ $\det=(k-m\omega^2)^2=0$ 二重根 ⇒ 本征子空间铺满全平面、$\Xi=\mathbf 1_2$。
   输出只剩「$\omega^2=k/m$」与「无优先方向 = 各向同性」，之后无信息。
   **缺口不在方法而在信息**：轨道由振幅比与相位差（初条件）决定，$M,K$ 里没有这两样。
   上一轮曾断言「$\det(K-\omega^2M)$ 在这里没有位置」，被他用上面的反问驳回—**改口径时直说“上一条说重了”**，不要硬撑。
2. **「极坐标更简单」——不成立。** $V\propto r^2$ 使比内方程非线性：$u''+u=mk/(L^2u^3)$，$u(\theta)$ 无直接闭式；
   换 $s=u^2=1/r^2$ 才线性：$s''+4s=4mE/L^2\Rightarrow r^2=1/(C+A\cos2\theta)$。
   极坐标的收益是暴露结构而非算得快：$s$ 关于 $\theta$ 的频率为 2 ⇒ $\omega_r=2\omega_\theta$（轨道闭合、周期 $2\pi/\omega_0$），
   以及与开普勒对比（$V\propto1/r$ 时椭圆焦点在力心；$V\propto r^2$ 时椭圆**中心**在力心）。
3. **「任何方向都是简谐 ⇒ 椭圆」——结论对、推理跳步。** 投影都简谐真正推出的是 $\omega_x=\omega_y$
   （$\omega_x\ne\omega_y$ 时一般方向的投影是两个不同频率简谐之和，不再简谐）；同频之后才轮到消 $t$ 得二次曲线。
   形状细节由振幅比与相位差定：相差 $0$ 或 $\pi$ → 退化成线段上的来回振动；等幅且相差 $\pi/2$ → 圆。

**可直接给他的目标（不讲解法）**：写出 $x(t),y(t)$ 通解，消 $t$ 得关系式，报曲线形状与中心相对力心的位置。

## Q3 进度（2026-10-21）：量、方程、快慢分离

- **先给量说明 + TikZ 示意图**（他手边没有书）：
  $l$ 摆长；$\varphi$ 与**竖直向上**方向的夹角（倒立摆的平衡在正上方，不是下方，符号因此反）；
  $y(t)=a\cos\Omega t$ 支点竖直坐标；$a\ll l$；$\Omega$ 与摆的固有频率 $\sqrt{g/l}$ 互不相干。
  题头「悬挂点加速度为 $\pm c$」是 Arnold 原书的方波模型，本题改成简谐——那句只交代改编来源，不参与计算。
  图：竖直虚线过支点、$\varphi$ 从向上量、$l$/$m\mathbf g$/支点振动标记。
  **坑**：tikz 标注重叠（$m\mathbf g$ 压住 $y(t)$ 文字、$l$ 与 $\varphi$ 挤成一串）——vision 复核后重排再发。
- 他手写发来求核的（**两式都对**）：
  $T=\tfrac12m(l^2\dot\varphi^2+a^2\Omega^2\sin^2\Omega t+2al\Omega\dot\varphi\sin\varphi\sin\Omega t)$、
  $V=mg(l\cos\varphi+a\cos\Omega t)$（质点坐标 $(l\sin\varphi,\ a\cos\Omega t+l\cos\varphi)$）。
- **精确 E-L（已核）**：$ml^2\ddot\varphi+mal\Omega^2\sin\varphi\cos\Omega t=mgl\sin\varphi$。
  关键机制：两个含 $\dot\varphi$ 的项自动相消，交叉项的唯一遗产是 $\cos\Omega t$ 因子 ⇒ **不要预先丢项**；
  纯含 $t$ 的两项（$\tfrac12ma^2\Omega^2\sin^2\Omega t$、$-mga\cos\Omega t$）对 $\varphi$ 的方程无贡献，可丢。
- 小角后 $\ddot\varphi+\bigl(\tfrac{a\Omega^2}{l}\cos\Omega t-\tfrac gl\bigr)\varphi=0$，Mathieu / Hill 型（系数周期）。
- **快慢分离三步**（已给三行图，第 3 步留给他填）：$\varphi=\Phi+\xi$（$\Phi$ 慢、$\xi$ 快）；
  ① $\ddot\xi\simeq-\tfrac{a\Omega^2}{l}\cos\Omega t\,\Phi\Rightarrow\xi=\tfrac al\cos\Omega t\,\Phi$；② $\overline{\cos\Omega t}=0$、$\overline{\cos\Omega t\,\xi}=\tfrac{a}{2l}\Phi$；③ 代入。
- **严格性（他必问「数学上怎么解释」）**：两尺度展开 + Fredholm 可解性条件（$\overline{F_n}=0\iff$ 该阶有有界周期解，即消长期项）；
  展开只在 $t\lesssim l/(a\Omega)$ 内有效；$t\to\infty$ 的严格判据是 Floquet 乘子 $\rho(\mathcal M)<1$。平均法只是一阶近似。
- **Kapitza 条件已交底**：$a^2\Omega^2>2gl$。他没填第 3 步，而是直接问「数学上怎么解释快慢分离」→ 给了两尺度展开 + Fredholm 可解性条件；随后他要求「把这类方程从头讲清楚」→
  交付了 Hill/Mathieu 理论全套（分块渲图、符号先定义），见 `references/hill-mathieu-theory.md`。
- **他问「为什么 $\xi$ 和驱动力同阶」时不要顺着他的措辞点头**：正确说法是「响应 = 驱动幅度除以 $(\omega_0^2-\Omega^2)$」，$\Omega\gg\omega_0$ 时 $\xi\simeq-F\cos\Omega t/\Omega^2$——
  驱动里的 $\Omega^2$ 被分母除掉，才剩 $O(a/l)\Phi$。也解释了为什么必须 $\Omega\gg\sqrt{g/l}$。
- **数值扫图已验证（2026-10-21）**：`scripts/mathieu_stability.py`（纯 stdlib RK4，一周期 200 步）扫 600×450 网格，
  舌尖落在 $\delta=0,\ 0.25,\ 1,\ 2.25,\ 4$，与 $n^2/4$ 对上——理论与数值各走一路互证。
  **坑**：第一版把稳定画成黑（颜色映射写反），图看着完全「像图」但结论全反；脚本现已内置已知点自检
  （$\delta<0,\varepsilon=0$ 必不稳定），**出图前必须过这一关**。
- 环境事实：`/mnt/e/书籍/物理/理论力学/` 里的朗道《力学》与 Arnold《经典力学的数学方法》**都是扫描版**，
  `pdftotext` 返回 0 行；要引书得 `pdftoppm` 转图 + 视觉模型读页。袁业飞讲义则有文本层（可直接 pdftotext）。

## 输出形态：讲「怎么做」给编号公式块（用户 2026-10-21 斥「不要掏一大坨汉字出来」）

方法类说明（主导平衡、取平均、消长期项这类）写成**编号步骤 + 每步一行式子**，渲成一张图；
散文只用来做判定（对/不对、缺哪一步、卡在哪）。他把「大段汉字」与「看不清」当成同一类毛病。

```
1. 主导平衡 → ξ=…
2. 代回、取平均 → ⟨…⟩=…
3. 剩下 Φ̈=…Φ，你自己填
```

反面：把「主导平衡／代回取平均／看系数符号」铺成四段自然语言，他读完仍不知道式子长什么样。
严格性靠式子承载，不靠形容词。

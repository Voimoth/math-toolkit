# 有心力场作业(hw4):解法骨架、已验证结论与卡点

题目地图见 SKILL.md 的「作业题地图」。本文件存**逐题的可复用解法骨架**与**他踩过的坑**。

## 记号约定(做 hw4/hw5 前先定):$L$ 是总角动量还是单位质量角动量

- **hw5 明确用单位质量角动量**:Q1(c) 的 $\dot r^2=E^2-(1-2GM/r)(1+L^2/r^2)$ 与 Q3 的「$L=r^2\dot\phi$」都是 per-unit-mass 写法(GR 惯例)。
- **hw4 公式 (1) 也是这个约定**。判据是 (1) 自身的量纲:分子有 $\sqrt\mu$、分母根号里没有 $\mu$,只有取 $l=r^2\dot\theta$ 才配平(拿 $V=-k/r$ 代进去验,给回 $\pi$)。
- 两种写法等价($\mu l^2/(2r^2)=L_{\rm tot}^2/(2\mu r^2)$,有效势函数本身不变):
  $$\Delta\theta=\frac{\pi L_{\rm tot}}{r_c^2\sqrt{\mu V''_{\rm eff}}}\ (\text{总角动量})\ ;\qquad \Delta\theta=\frac{\pi l\sqrt{\mu}}{r_c^2\sqrt{V''_{\rm eff}}}\ (\text{单位质量,作业本 (1)}).$$
  **别把两种 $L$ 混用**:照作业本抄 (1)、同时按讲义写 $L=\mu r^2\dot\theta$,结果会差一个 $\mu$。
- vault 概念页 `中心力场与有效势.md` 已补这条对照 callout(2026-10-07,commit ff1919a)。

### 怎么把公式 (1) 读准(通用做法)
- `pdftotext -layout` 会把根号的覆盖范围与上下标甩到错行:作业 (1) 被它读成「$=2\sqrt{}^{\prime\prime}$」这类乱码
  (那个 2 其实是 $r_c$ 的指数)。**凡可疑公式一律 `pdftoppm -r 150 -png` 渲页 + 看图逐字读**:先读分子、再读分母,
  确认根号盖住了哪几项、指数的位置在哪——不拿文本层当真。
- 读出「不可能」的公式时按序核三步:①量纲分析;②代已知特例(此处 $V=-k/r$)必须精确给回 $\pi$;③回原图确认字形。
  三步都过再判定「是约定不同还是真印错」——本例的结局是**课程换了约定**(单位质量角动量),不是印错。
- **同一手法的第二次应用(hw4-5)**:朗道 §15 习题 3 的 (1) 式，第二等号右边是 $2m\int$ 还是 $\frac{2m}{M}\int$？文本层没有、字形也糊。直接代 $\delta U=\beta/r^2$（此时 $r^2\delta U=\beta$ 是常数，积分平凡）就能分辨：漏了 $M$ 会给出 0，而朗道的 (a) 答案是 $-2\pi\beta m/M^2$。
  **判据：凡公式里出现 $\partial/\partial M$ 这类对参数的导数，先拿最简单的扰动代进去看能不能复现已知答案。**
  (通用方法本该进 `math-coach`;它 user-owned 写不进去,先落此。)

## hw4-1  $V=-k/r$、$E=0$:求 $r(t)$

一条龙(已逐字验证):

1. 两个首积分就够,不必写 E-L 方程(写了不错,只多一步):
   $\dot r^2=\dfrac{2k}{\mu r}-\dfrac{L^2}{\mu^2r^2}$,其中 $L=\mu r^2\dot\theta$ 是参数。
2. 积分。令 $s=\sqrt{2\mu kr-L^2}$,则 $\dot r=s/(\mu r)$,
   $$t=\int\frac{\mu r\,dr}{\sqrt{2\mu kr-L^2}}=\frac{s^3/3+L^2s}{2\mu k^2},$$
   即**三次式** $s^3+3L^2s=6\mu k^2t$。想要显式 $r(t)$ 就得解这个三次方程(Cardano);
   教材与朗道大多停在隐含形式,别以为是自己算错了。
3. 换成角度参数(barycentric 的抛物线参数)$D=\tan(\theta/2)$、$p=L^2/(\mu k)$、$r=\frac p2(1+D^2)$,
   上式就是 **Barker 方程**
   $$t=\frac12\sqrt{\frac{\mu p^3}{k}}\left(D+\frac{D^3}{3}\right).$$

**他的卡点**:把「轨道是抛物线」当成一个**可以额外代入的独立条件**。实际上对 $V=-k/r$ 有
$e^2=1+2EL^2/(\mu k^2)$,$E=0\iff e=1$,抛物线只是 $E=0$ 的换名;
抛物线的形状参数 $p$ 也不是题目给的,必须由运动方程定出($p=L^2/(\mu k)$)——
从几何形式 $r=p/(1+\cos\theta)$ 出发时 $p$ 仍要反解,不能当已知量。

## hw4-2  $V=\alpha/r$(排斥):证明轨道为双曲线

- 比内方程 $u''+u=-\mu\alpha/L^2\Rightarrow u=\dfrac{\mu\alpha}{L^2}(e\cos\theta-1)$,取 $r>0$ 的那一支。
- **$E$ 与 $e$ 的关系来自「在转折点求能量」**(这是他真正缺的一步):近心点 $\theta=0$ 处 $\dot r=0$,
  $r_{\min}=L^2/[\mu\alpha(e-1)]$,于是
  $$E=\frac{L^2}{2\mu r_{\min}^2}+\frac{\alpha}{r_{\min}}=\frac{\mu\alpha^2}{2L^2}(e^2-1).$$
  排斥场中 $E=T+\alpha/r>0$ 恒成立 $\Rightarrow e>1\Rightarrow$ 双曲线。
  $k$ 只以 $k^2$ 出现,所以这条公式对吸引/排斥**逐字相同**,受符号影响的只是「哪支能量给哪支曲线」。
  (通用形式已进 vault `轨道方程与比内公式.md`:转折点求值 $\Rightarrow E=\mu k^2(e^2-1)/(2L^2)$,commit 1a8ea1f。)
- **「把 hw4-1 的 $k$ 换成 $-\alpha$」这个移植要分两层判定**:
  - **解层成立**:$u''+u=\mu k/L^2\to-\mu\alpha/L^2$,$\cos$ 项与 $p$ 同时变号,曲线族不变。
  - **一阶积分层不成立**:hw4-1 那条已经代入了 $E=0$,换符号后给出负的 $\dot r^2$。排斥情形的通式是
    $\dot r^2=2E/\mu-2\alpha/(\mu r)-L^2/(\mu^2r^2)$。
- 完整性:$r>0$ 只在 $|\theta|<\arccos(1/e)$ 上成立——只有**一支**,粒子从无穷远来到无穷远去,
  力心在**远焦点(凸侧)**。

## hw4-3(2026-10-07 辅导过半)

- 目标:证 $\Delta\theta=\pi L\sqrt{\mu}/(r_c^2\sqrt{V''_{\rm eff}})$(约定见上);他卡在概念层,不是计算层。
- **第一处卡点:「$E$ 怎么又变了」**——他把 $E_{\min}$ 读成「$E$ 随位置/时间变」。两句话澄清:
  $E$ 沿一条轨道守恒;$E_{\min}=V_{\rm eff}(r_c)$ 是**给定 $L$ 时所有可能轨道的能量下界**(圆轨道能量),
  它随 $L$ 变(对 $V=-k/r$:$r_c=L^2/(\mu k)$、$E_{\min}=-\mu k^2/(2L^2)<0$)。
  「$E$ 略大于 $E_{\min}$」= **换一条轨道**,不是同一条轨道上 $E$ 在动。接上 hw4-2 的 $e^2$:此处 $E<0\Rightarrow e<1$(近圆椭圆),$E\to E_{\min}$ 时 $e\to0$。
- **路线判定**:他提「先写比内方程再近似」——可行,但主线建议**径向小振动**(更短,且他笔记里已有):
  $V_{\rm eff}$ 在 $r_c$ 展开 $\Rightarrow\mu\ddot x=-V''_{\rm eff}(r_c)x$、$\omega_r=\sqrt{V''_{\rm eff}/\mu}$、$\Delta\theta=\dot\theta_c\,T_r/2$。
  比内那条只是把同一个线性化写在 $u$ 空间($\delta''+(1-f'(u_c))\delta=0$),还要多一层把波数换算回 $V''_{\rm eff}$,留作旁注。
- **「很窄」的用途**(他问过条件用在哪):①只保留到二阶才合法($x_{\max}=\sqrt{2(E-E_{\min})/V''_{\rm eff}}$ 小,扔掉的三次项 $\sim x_{\max}^3$);
  ②$\Delta\theta=\dot\theta_c T_r/2$ 里可以把 $\dot\theta$ 取成圆轨道值(否则它是变的)。
- **他说「讲慢一点」时的正确姿势**:先说清**展开对象是 $V_{\rm eff}$ 整体、不是单独的 $V(r)$**($V'(r_c)$ 一般不为零,驻点属于 $V_{\rm eff}$);
  再四步走——①一维化 $E=\frac12\mu\dot r^2+V_{\rm eff}$;②圆轨道 $\iff V'_{\rm eff}(r_c)=0$;
  ③展开、一次项因驻点消失 $\Rightarrow$ 只留 $\frac12V''_{\rm eff}x^2$;④力 $=-$势的导数 $\Rightarrow$ 简谐。
  **先给大白话(「把势能谷的底用一条抛物线代替」)再上术语**(SKILL.md 要点 5);末了补前提 $V''_{\rm eff}(r_c)>0$(拐点情形是 hw5-2(c))。
- 未做:把 $\omega_r$ 接到 $\Delta\theta$ 的那一步留给他自己补;hw4-4/5/6 与 hw5 均未开始。

## hw4-4 / hw4-6(沿用旧记,本轮未复核)

- **4** $V=\alpha/r^2$:$u''+\beta^2u=0$、$\beta=\sqrt{1+2\mu\alpha/L^2}$ 给出幂律螺旋;$r(t)$ 再由 $\dot\theta=L/(\mu r^2)$ 积分。
- **6**（2026-10-08 已收尾）$\vec L\times\vec A$ 给速度图(圆)的半径与圆心偏移。链条：$\vec A=\dot{\vec r}\times\vec L-k\hat r$ ⇒ $\vec L\times\vec A=L^2\dot{\vec r}-k\,r^2\frac{d\hat r}{dt}=L^2\dot{\vec r}-kL\hat e_\theta$（用 $r^2\frac{d\hat r}{dt}=r^2\dot\theta\,\hat e_\theta=L\hat e_\theta$）
  ⇒ $\dot{\vec r}=\frac{\vec L\times\vec A}{L^2}+\frac kL\hat e_\theta$：常矢量 + 等长转动矢量 ⇒ 圆。**半径 $R=k/L$，原点→圆心 $=|\vec A|/L=ke/L=eR$**。
  用 $\vec L\times\vec A$ 还是 $\vec A\times\vec L$ 只差圆心在 $\vec A$ 的哪一侧（整体符号）；$e\to0$ 时 $\vec A=0$、圆心回原点。两种约定（总 $\vec L$ 配 $k$，或单位质量 $\vec l$ 配 $k/\mu$）给同一形状。
- **他那三个技术追问（本轮实际问的，答法已定）**：
  ①「$\vec A$ 里的 $k$ 是什么」⇒ 就是 $V=-k/r$ 的系数（引力 $k=GM\mu$），**不是质量**；量纲 $[\dot{\vec r}\times\vec L]=$ 能量·长度 $=[k]$ 自动钉住配对：总 $\vec L$ 配 $k$，单位质量 $\vec l$ 配 $k/\mu$。
  ②「为什么导数是 0」⇒ 完整两行（$\ddot{\vec r}\times\vec L=-(k/r^2)\hat r\times\vec L=+k\frac{d\hat r}{dt}$，与 $-k\frac{d\hat r}{dt}$ 对消），再给通用形式 $\frac{d\vec A}{dt}=[-f(r)r^2-k]\frac{d\hat r}{dt}$（$\ddot{\vec r}=f(r)\hat r$）⇒ **守恒 $\iff f\propto1/r^2$**。
  ③「$\hat r\times\vec L$ 怎么展开」⇒ 两条路给全：BAC-CAB 摊开（$\hat r\times(\hat r\times\dot{\vec r})=(\hat r\cdot\dot{\vec r})\hat r-\dot{\vec r}$，再用速度分解 $\dot{\vec r}=\dot r\hat r+r\frac{d\hat r}{dt}$ 与 $\hat r\cdot\dot{\vec r}=\dot r$ ⇒ $-r^2\frac{d\hat r}{dt}$）+ 几何一行（$\hat r\times\vec L=-L\hat e_\theta$）。
  **模式**：他连问「为什么」时就是要看这步计算，直接给全推导（不是代劳——他已经交了结果/在跟；把机制讲完就停，不往下替他做）。
- 算 $V''_\text{eff}$ 时**必须含离心项** $\frac{d^2}{dr^2}\frac{L^2}{2\mu r^2}=\dfrac{3L^2}{\mu r^4}$——漏掉它是最常见的错。

## hw4-5  进动角 $\delta V=\beta/r^2,\ \gamma/r^3$(2026-10-08 已核实)

出处:朗道《力学》§15 习题 3,**书内 p.40 题 / p.41 解 = 高教社第 5 版 PDF 第 53–54 页**(该 PDF 无文字层:必须 `pdftoppm -r 140 -png` 渲页 + 视觉逐字读;§15 习题 2 在 PDF 52–53)。

- **定义先钉死**:一个径向周期(题里说的「一圈」)的进动角 $\delta\theta=2\Delta\theta-2\pi$,$\Delta\theta$ 是近心点→远心点扫过的极角,
  纯开普勒 $\Delta\theta=\pi$。朗道的 $\Delta\varphi$(公式 (14.10))就是**整圈**角(他明说「零阶项为 $2\pi$」),所以他的 $\delta\varphi$ 与这里的 $\delta\theta$ 是同一个量。
- **一般一阶公式(朗道 (1),沿无扰开普勒轨道积分,对任意 $e$ 成立)**:
  $$\delta\varphi=\frac{\partial}{\partial M}\int_{r_{\min}}^{r_{\max}}\frac{2m\,\delta U\,dr}{\sqrt{2m(E+\alpha/r)-M^2/r^2}}=\frac{\partial}{\partial M}\left(\frac{2m}{M}\int_0^\pi r^2\,\delta U\,d\varphi\right).$$
- **答案**(单位质量、$l=r^2\dot\theta$、$k=\alpha$):
  - (a) $\delta V=\beta/r^2$：$\delta\theta=-2\pi\beta/l^2$（总角动量写法 $-2\pi\mu\beta/L^2$）。**精确可解**:比内方程 $u''+(1+2\mu\beta/L^2)u=\mu k/L^2$ ⇒ 进动椭圆,角波数 $\sqrt{1+2\mu\beta/L^2}$,$\delta\theta=2\pi\big(1/\sqrt{1+\cdot}-1\big)\to-2\pi\mu\beta/L^2$。所以 (a) 不必微扰。
  - (b) $\delta V=\gamma/r^3$：$\delta\theta=-6\pi\gamma\alpha/l^4=-6\pi\gamma/(\alpha p^2)$,$p=l^2/\alpha$ 是无扰轨道半通径。**与 $e$ 无关**(共振强迫项 $\propto e$,但相位 $\psi=A/(Ke)$ 里 $e$ 约掉)。$\gamma>0$ ⇒ $\delta\theta<0$,近心点**逆行**。
- **两条路的适用边界**:Q3 的小振动公式 $\pi l\sqrt\mu/(r_c^2\sqrt{V''_{\rm eff}})$ 是「径向范围很窄」的产物,**一般有限轨道不能用**;
  它在 $e\to0$ 极限给出同一个 $-6\pi\gamma/(\alpha p^2)$,但要求把 $r_c$ 的一阶平移一起算进 $V''_{\rm eff}(r_c)$:
  $-2k/r^3$ 的平移给 $+18\gamma$、$+3l^2/r^4$ 的给 $-36\gamma$、$+12\gamma/r^5$ 的给 $+12\gamma$,合计 $u''_{\rm eff}(r_c)=\frac{k}{r_0^3}\big(1-\frac{6\gamma}{k r_0^2}\big)$。
  **漏掉平移项会得到 $-24\gamma$,最终答案变成 $+12\pi\gamma/(\alpha r_0^2)$——大小差 2 倍且符号反。**
- **讲法(陪练)**:主线给比内方程 $u''+u=k/l^2-(3\gamma/l^2)u^2$ 与「(a) 只改 $u$ 的系数所以精确可解、(b) 多了 $u^2$ 所以只能微扰」的对比;
  停在**「$u_0^2$ 展开出的三种频率(常数、$\cos\varphi$、$\cos2\varphi$)里哪一种决定进动」**这一问上,等他答。
  **他 2026-10-08 的第一次回答是「只有 $\cos2\varphi$ 项改变频率,所以影响进动」——错**。纠正的措辞必须落在「共振」上:
  判据是强迫项频率**等于齐次频率 1**(不是「改变频率」);$\cos2\varphi$ 给有界特解 $A\cos2\varphi/(1-4)$、只改形状,
  只有 $\cos\varphi$ 长出发散的 $\varphi\sin\varphi$。他听完即改口答对(系数 $2K^2e$),推进顺利。
  共振项给 $\varphi\sin\varphi$ 的长期增长 ⇒ 相位平移 ⇒ 进动;常数项与 $\cos2\varphi$ 只给有界特解(改形状不改进动)。
- **vault 待修**:`轨道进动.md` 的 (b) 行写着「用同一个 $V''_{\rm eff}$ 微扰公式得到与 $\gamma$ **同号**的进动」——**符号是错的**(已双路径核实为反号),
  且把只适用于近圆的小振动公式说成通用。下次动 wiki 时改成 $-6\pi\gamma/(\alpha p^2)$、注明「$\gamma>0$ 逆行」、并限定 $V''_{\rm eff}$ 公式为近圆极限。
- **数值自检**:`scripts/precession_check.py`(纯 stdlib,本机无 scipy)。做法是 $\Delta\theta=\int_{r_{\min}}^{r_{\max}}(l/r^2)dr/\sqrt{2(E-V_{\rm eff})}$,
  换元 $r=r_m+r_d\cos\theta$ 把两端 $1/\sqrt{\ }$ 奇性化成规则积分再 Simpson。
  **坑**:端点处 $E-V_{\rm eff}$ 是 0/0 型(数值上约 $-4\times10^{-16}$),把被积函数置 0 或用 `max(...,0)` 会让 Simpson **收敛极慢且非单调**(n=20000 仍差 $10^{-4}$);
  用解析极限 $l\sqrt{r_d}/\big(r_{\rm end}^2\sqrt{|V'(r_{\rm end})|}\big)$ 填两端后,n=500 与 n=20000 就差到 $10^{-11}$。
  **管线自检顺序**:先让 case (a) 的精确值 $2\pi(1/\sqrt{1+2\beta}-1)$ 10 位吻合,再拿它去验 (b);
  (b) 用 $\gamma=5\times10^{-4}\dots4\times10^{-3}$ 四点外推 $\delta\theta/\gamma$ 到 $\gamma\to0$,得 $-18.84949$ 对 $-6\pi=-18.84956$(相对 $3\times10^{-6}$),且不同 $E$(即不同 $e$)给同一首项。

概念层的落点见 vault`物理/理论力学/`的 `轨道方程与比内公式`、`中心力场与有效势`、`轨道进动`、`Laplace-Runge-Lenz 矢量`、`速度图与圆锥曲线轨道`(平铺);
hw5 的落点是 `Schwarzschild时空中的测地线`。

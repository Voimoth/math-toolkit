# 分析III Fourier 讲义:§4–§5 内容银行(sofar.pdf 2026-09-10 版)

来源:用户提供 `sofar (1).pdf`(殷浩,36 页,提取文本 `~\Downloads\sofar_new.txt`,2801 行)。
章节边界(页号 → 提取文本行号):P1=35, P7=397, P10=674, P17=1153, P18=1233, P21=1457, P26=1974, P31=2397, P33=2622, P36=2801。

**这是课件覆盖范围的事实来源之一,但它不是"用户已学"的证明**——判据仍是 wiki 概念页是否存在。课停在 §5.5(9 月 26 日课),§6–§8 只在目录里,正文未写。

## 相对旧版(17 页 sofar.pdf,只到 §3.5)的增量

| 增量 | 位置 |
|---|---|
| §1.3 历史注记(Bernoulli 1753 / Euler 1777 已有系数公式却不信 / Fourier 1807-1822 / Dirichlet 1829 定理 + 1837 函数定义 / Riemann 1854 积分 / Cantor 1870 唯一性) | p.5–6 |
| §3.4 末尾:系数衰减快 ⇒ $f$ 在连续点处等于某 $C^1$ 函数 $g$;把"$f$ 由系数决定到什么程度"作为遗留问题**明确悬挂** | p.15 |
| §3.6 历史注记(du Bois-Reymond 1873 反例 / Fejér 1900 / Kolmogorov 1923,1926 / Lusin 1915 猜想 → Carleson 1966 → Hunt 1968 / Kahane–Katznelson) | p.17 |
| §4 开篇:Hardy《Divergent Series》公理化弱收敛(线性、平移、与 a₀ 相容、相容于严格收敛),由四条公理"证"$1-1+1-\cdots\sim\frac12$;**结合律失效** | p.18 |
| §4.1 Cesàro 求和 + Fejér 核 | p.18–20 |
| §4.2 Abel 求和 + Poisson 核 + 单位圆盘 Dirichlet 问题 | p.21–25 |
| §4.3 Hardy 文献注记 | p.25–27 |
| §5.1–5.3 L² 与 Hilbert 空间框架 | p.27–32 |
| §5.4 Legendre 多项式(讲个故事,无需记) | p.33 |
| §5.5 历史注记(Legendre 1783 / Sturm–Liouville 1836 / Parseval 1799 / Hurwitz 1902 / Lebesgue 1902 / Riesz–Fischer 1907 / 球谐 / Plancherel 1910 / Haar 1910 / Peter–Weyl 1927) | p.34–36 |

## §4.1 Cesàro 求和(讲义编号)

- 记号注意:**讲义把 $\frac{1}{2\pi}$ 吸进核的定义**,$D_N(\varphi)=\frac{1}{2\pi}\frac{\sin(N+\frac12)\varphi}{\sin\frac\varphi2}$,于是 $S_N=\int_{-\pi}^{\pi} f(\theta-\varphi)D_N(\varphi)\,d\varphi$(没有外置系数)。引用性质时务必说明用的是哪套归一化。
- $F_N=\dfrac{D_0+\cdots+D_{N-1}}{N}=\dfrac{1}{2\pi N}\Bigl(\dfrac{\sin\frac{N\varphi}{2}}{\sin\frac\varphi2}\Bigr)^2$,$\sigma_N(\theta)=\int_{-\pi}^{\pi} f(\theta-\varphi)F_N(\varphi)\,d\varphi$。
- **Fejér 核三性质**:$\int_{-\pi}^{\pi}F_N=1$;$F_N\ge0$;$\forall\delta>0,\lim_{N\to\infty}\sup_{\delta\le|\varphi|\le\pi}F_N(\varphi)=0$。对比 $D_N$:旁瓣正负振荡、$\|D_N\|_1\sim\log N$;$F_N$ 恒非负且旁瓣速降。
- 证明是"著名的套路",关键不在求出哪个 $N$,而在**写套路的过程中发现 $N$ 与点的位置无关**——只用到一致连续。这条正是"一致逼近"的意思,值得在概念页里点明。
- **定理 4.3**:$f$ 2π 周期可积/绝对可积 ⇒ Cesàro 求和在 $f$ 的连续点收敛于 $f$;若 $f$ 处处连续则一致收敛。(条件比点态收敛宽松得多,代价是换成了 $\sigma_N$。)
- **定理 4.5**(推论):2π 周期连续函数可被三角多项式一致逼近。讲义明确指出**这个定理已经用抽象 Stone–Weierstrass 证过,现在等于第二个证明**——别当成全新定理。
- **定理 4.6(唯一性定理)**:$f$ 2π 周期可积/绝对可积,若全部 Fourier 系数为 0,则 $f$ 在**每个连续点**处为 0;特别地 $f$ 连续 ⇒ $f\equiv0$。
  三步证明:① 对任何三角多项式 $P$,$\int fP=0$;② 由定理 4.5 取三角多项式 $P_k\rightrightarrows g$ 得 $\int fg=0$ 对一切连续 $g$;③ 取**三角帽** $g(x)=\max(0,1-\frac{|x-x_0|}{\delta})$(满足 $g(\pm\pi)=0$、周期延拓后仍连续、$g\ge0$),若 $f(x_0)>0$ 则由连续性和 $g$ 的支撑得 $\int fg\ge\frac{f(x_0)}{2}\delta>0$,矛盾。
- **Remark 4.8**:"连续点"不能改进为"每个点"(改有限个点的值不影响任何系数);实变课后可升级为"几乎处处"。若 $f$ 预先连续,则不必走三步——Fejér 定理给 $\sigma_N\rightrightarrows f$ 而系数全零给 $\sigma_N\equiv0$,直接 $f\equiv0$。
- **Corollary 4.7**:系数相同的两个函数在公共连续点处相等;都连续则恒等 ⇒ **连续函数由 Fourier 系数唯一决定**。这回收了 §3.4 悬着的问题。

## §4.2 Abel 求和

- **定义 4.9**:$\sum c_k$ 称 Abel 可和于 $s$,若 $\forall 0\le r<1$,$A(r)=\sum_{k\ge1}c_kr^k$ 收敛且 $\lim_{r\to1}A(r)=s$。加 $r^k$ 明显"有利于收敛"。
- **引理 4.10**:严格收敛 ⇒ Abel 可和到同一个数(用 Abel 判别法得关于 $r$ 一致收敛,再交换极限与求和)。
- **例子 4.11**:$1-2+3-4+\cdots$ Abel 可和于 $\frac14$($A(r)=\frac{1}{(1+r)^2}$);但部分和为 $(-1)^{n+1}\lceil n/2\rceil$,前 $2m$ 个算术平均恒为 0、前 $2m-1$ 个趋于 $\frac12$,**两子列极限不同故非 Cesàro 可和**——这个例子在定理 4.12 的证明里还要用。
- **定理 4.12**:严格收敛 ⇒ Cesàro ⇒ Abel,两个推出**都不可逆**。证明要点:形式上 $\sum c_nr^n=(1-r)^2\sum(n\sigma_n)r^n$(因为乘 $\frac{1}{1-r}$ 就是取部分和,做两次),再利用 $\sum_{n\ge1}nr^n=\frac{r}{(1-r)^2}$ 把和拆成 $n\le N$ / $n>N$ 两段;前段靠 $(1-r)^2\to0$,后段靠 $|\sigma_n|<\varepsilon$。**"乘 $\frac{1}{1-r}$ = 取部分和"是这套证明的枢纽,值得单独记住。**
- **定理 4.13**:$f$ 在连续点 $x_0$ 处 Abel 求和收敛于 $f(x_0)$;$f$ 连续则一致收敛。**Poisson 核** $P_r(\theta)=\sum_{-\infty}^{\infty}r^{|n|}e^{in\theta}=\frac{1-r^2}{1-2r\cos\theta+r^2}$,性质与 $F_N$ 三条平行($\frac{1}{2\pi}\int P_r=1$,$P_r\ge0$,$\delta\le|\theta|\le\pi$ 上 $\max\to0$)。A(r,θ) 写成 Poisson 卷积。
- **Remark 4.14**:Fourier 级数复形式是双头的,用 Abel 求和时实形式要把 sin/cos 看成一个项。
- **Remark 4.15**:定理 4.13 其实不必重证——由 Fejér 定理 + 定理 4.12(C ⇒ A)组合即得,且估计关于 θ 一致。保留 Poisson 核直接证明的理由:顺手给出解圆盘 Laplace 边值问题所需的显式表达式。
- **定理 4.16(*)**:**单位圆盘 Dirichlet 问题**。$f$ 2π 周期连续,$u(r,\theta)=\frac{a_0}{2}+\sum r^n(a_n\cos n\theta+b_n\sin n\theta)$ 在 $r<1$ 内是 $C^\infty$ 调和函数,补定义 $u(1,\theta)=f(\theta)$ 后在闭圆盘连续,即 $\Delta u=0$ 的解。逐项求导被 $2M\sum n^kr_0^n$ 控制;$r^n\cos n\theta=\mathrm{Re}\,z^n$ 调和(极坐标 Laplace 形式直接验算);边值收敛不只是径向极限——**沿任何路径趋于边界点都有正确极限**($|u(r,\theta)-f(\theta_0)|\le\sup_\theta|u(r,\theta)-f(\theta)|+|f(\theta)-f(\theta_0)|$)。
- **§4.3 Hardy 注记**(三问):(1) 别的方法——$(C,k)$、Hölder、Euler $(E,q)$、Borel($e^{-x}x^n/n!$ 权)、Nörlund $(N,p)$、Riesz、de la Vallée-Poussin(把 Fejér 核换成 $(1+\cos\theta)^m$ 型)、Riemann $(R,2)$、Hausdorff 矩量统一框架;存在正则方法连 $1-1+1-\cdots$ 都求不了和。(2) 强弱:$(C,k)\Rightarrow(C,k')$ 严格增强,$(H,k)\equiv(C,k)$;Abel 强于所有 Cesàro(Thm 55/56);Euler 随 $q$ 增强且 Euler ⇒ Borel;反方向是 **Tauber 定理**(Tauber → Littlewood $a_n=O(1/n)$ → Hardy–Littlewood → 高指标定理 → Wiener 用 Fourier 变换统一)。(3) 应用:素数定理(Wiener Tauber,只需 ζ 在 $\Re s=1$ 无零点)、解析延拓(Borel 可和性多边形)、$1+2+3+\cdots=\zeta(-1)=-\frac1{12}$ 的严格求和定义(Hardy 警告适用范围窄)。

## §5 Fourier 级数的 L² 理论

- **§5.1 框架**:向量空间($C([a,b])$、可积函数类)、内积与 Hermite 内积 $\langle f,g\rangle=\int f\bar g$、$\ell^2$ 例、范数 $\|f\|=\sqrt{\langle f,f\rangle}$。**Remark 5.1**:可积函数空间的坑——范数为 0 不一定恒为 0;理论最好在 $L^2$ 里做,但积分理论不足,暂在连续函数空间里写。
- **Def 5.2** 单位正交系 $\langle e_i,e_j\rangle=\delta_{ij}$;无穷维仍保留"线性相关"但强调**有限**线性组合。
- **例 5.3**:$\{\frac{1}{\sqrt{2\pi}}\}\cup\{\frac{1}{\sqrt\pi}\cos nx,\frac1{\sqrt\pi}\sin nx\}$,复版 $\frac{1}{\sqrt{2\pi}}e^{inx},n\in\mathbb Z$。讲义提醒:**正交系天然很多,这只是一种选择**;为什么这个选择优秀留给"作为算子的特征值"来谈。
- **引理 5.4**:$C([-\pi,\pi])$ 在 $\|\cdot\|_2$ 下**不完备**($f(x)=x^n$ 即可看出);$\ell^2$ **完备**。后半证明是经典三步:先逐坐标收敛找极限对象 $a$,再证 $a\in\ell^2$,最后证范数收敛(讲义把后两步合起来)。
- **Remark 5.6 / Def 5.7**:照 Q→R 的办法把连续函数集完备化,得到的就是 $L^2([-\pi,\pi])$;完备内积空间 = **Hilbert 空间**。
- **引理 5.8(有限维逼近)**:$V_n=\mathrm{span}(e_1,\dots,e_n)$ 中距 $f$ 最近的点**存在唯一**,即 $f_n=\sum_{k\le n}\langle f,e_k\rangle e_k$;关键一步是证明 $f-f_n\perp V_n$,再用勾股定理 $\|f-g\|^2=\|f-f_n\|^2+\|f_n-g\|^2$。取 $g=0$ 得勾股恒等式 $\|f\|^2=\|f-f_n\|^2+\sum_{k\le n}|\langle f,e_k\rangle|^2$,令 $n\to\infty$ 得 **Bessel 不等式**。
- **§5.3 均方收敛**:$\|f-f_n\|$ 单调不增;但 $\lim\|f-f_n\|=0$ 不是对一切正交系成立(从完备系里抽掉 $e_1$,剩下的对 $f=e_1$ 必不成立——无穷维里"少一个"不能靠数数体现)。
- **Def 5.9 完备(正交基)**:$\forall f,\lim_n\|f-f_n\|=0$。**Remark 5.10**:"均方"是新概念——可找到均方收敛而对任何 $x$ 函数值都不收敛的列(但**不是说 Fourier 级数如此**)。
- **定理 5.11**:$\{e_i\}$ 完备 **⟺** $\forall f$,$\|f\|^2=\sum_n|\langle f,e_n\rangle|^2$(无穷维勾股定理,证明就是看勾股恒等式)。
- 落到三角系:$V_{2n+1}$ = 次数不超过 $n$ 的三角多项式,$f_{2n+1}=S_n(f)$(部分和)。
- **定理 5.13**:$f$ 2π 周期实值连续 ⇒ Fourier 级数均方收敛于 $f$,且有 **Parseval 等式** $\frac{a_0^2}{2}+\sum(a_n^2+b_n^2)=\frac1\pi\int_{-\pi}^{\pi}|f|^2=\frac1\pi\|f\|^2$。证明要点:**由引理 5.8,$S_n$ 是 $V_{2n+1}$ 中距 $f$ 最近的点**,故只要能用三角多项式(定理 4.5)在均方意义逼近 $f$,$S_n$ 至少逼近得一样好——**Fejér 一致收敛定理在这里被再次调用**,这就是 §4 与 §5 的接缝。
- **推论 5.14**:限制(2π 周期连续)不是本质的;换空间再完备化得到的还是同一个 $L^2$。映射 $F(f)=(\sqrt\pi\sqrt2\,a_0,\sqrt\pi a_n,\sqrt\pi b_n,\dots)$ 是**等距且单射,但不满射**;把 $\tilde C([-\pi,\pi])$ 的 Cauchy 列等价类做完备化,得 $L^2$ 与 $\ell^2$ 等距——这就是所谓 $L^2$ 理论。
- **§5.4 Legendre(故事,无需记)**:$L_n=\frac{d^n}{dx^n}(x^2-1)^n$,$\deg L_n=n$,$A_{mn}=\delta_{mn}\frac{(n!)^22^{2n+1}}{2n+1}$;归一化得正交系;完备性"理解了 Fourier 的证明就不困难";等于 $1,x,x^2,\dots$ 的 Gram–Schmidt。(*) 三角系的优越性来自它是 $u''+\lambda u=0$(周期边条件)的特征函数;Legendre 对应 $((1-x^2)u')'+\lambda u=0$(端点正则),$\lambda_n=n(n+1)$。
- **§5.5 历史注记要点**:Legendre 1783(均匀球状天体引力);Sturm–Liouville 1836(非均匀细杆热传导 → 自伴性给正交、完备性待证);Parseval 1799(发表于 1806,当时当求和法);Hurwitz 1902(有界可积函数的 Parseval,明确用平方误差恒等式 $\|f-\sum_{k\le N}c_ke_k\|^2=\|f\|^2-\sum_{k\le N}|c_k|^2$,并追溯到 Harnack);反向问题(系数平方可和 ⇒ 存在极限函数吗)引出完备性需求 → Lebesgue 1902 → **Riesz–Fischer 1907** ⇒ $L^2\cong\ell^2$ 等距同构(Riesz 的比喻:函数空间与坐标空间之间的"**永久往返票**");后续:球谐 / Plancherel 1910($L^2(\mathbb R)$ 上酉算子)/ Haar 1910(小波前身)/ Peter–Weyl 1927(紧群不可约酉表示矩阵系数构成 $L^2$ 正交基,圆周群情形即普通 Fourier 级数)。

## 建页映射(2026-09-10 已执行完毕并推送 commit `1f02afe`)

课程推进到 §4–§5 后按下表落地完成(用户先说"按上面方案继续",故方案即已批准;下表为**实际产出**,与早先草案有出入,以本表为准):

| 讲义章节 | 概念页(实际文件名) | 结果 |
|---|---|---|
| §4 开篇公理化弱收敛 + §4.1 定理 4.3/4.5 + §4.3 Hardy 注记 | `广义求和与Cesàro求和.md` | **新建**(草案曾设想"归入 Cesàro 页的引子",实际独立成页——公理化四条 + 例 4.2 + Hardy 三问自成主题) |
| §4.1 Fejér 核 + 定理 4.3 + 两个推论 | `Cesàro求和与Fejér核.md` | **新建**(替代旧 `fejer-kernel.md`) |
| §4.1 定理 4.6/4.7 + Remark 4.8 | `傅里叶系数唯一性.md` | **新建** |
| §4.2 Abel + Poisson 核 + 定理 4.12/4.13/4.16 | `Abel求和与Poisson核.md` | **新建**(含单位圆盘 Dirichlet 问题) |
| §5.1–5.3 框架与均方收敛 | `L²理论与Hilbert空间.md` | **新建** |
| §5.1–5.3 一般正交系抽象 | `正交函数系.md` | **重建**(自 git 取回旧 `orthogonal-system.md` 后按新讲义重写;草案曾想并入 L² 页,实际保持独立——Bessel/完备性的一般框架与三角系的具体实现是两个层次) |
| §5.3 Parseval | `Parseval恒等式.md` | **重建**(同上,自 `parseval-identity.md`) |
| §5.4 | `勒让德多项式.md` | **新建**(标注"讲义称只是故事") |
| §1.3 / §3.6 / §4.3 / §5.5 历史注记 | 各页及 `Fourier笔记.md` 对应节 | 分置 |

同时修正的过期表述(新讲义推进后必须一并改,否则页面自相矛盾):`傅里叶级数收敛.md`(衔接说明 → 三种收敛意义对照表 + §3.4 遗留问题已由定理 4.6 回答)、`吉布斯现象.md`(删"Cesàro/Fejér 属后续章节,当前不在范围内")、`傅里叶级数.md`(Remark 2.3 两种展开之谜 → 指向 §5 解答)、`傅里叶级数入门.md`(路径② 正式接入第 5 章)、`傅里叶文献.md`(增 Hardy《Divergent Series》)、`傅里叶学习路径.md`(进度 → 第 1–5 章)。`分析III/_索引.md` 改为**按讲义章节列概念页的表**,`数学/分析/_索引.md` 补进度说明。

**已修复的断链**:`[[Fourier讲义2026]]`(实体页已删)在 `傅里叶学习路径.md`、`傅里叶级数入门.md`、`傅里叶文献.md` 中的引用全部移除。

### 定位旧页的正确命令(草案里的写法是错的,别再照抄)

草案写的是 `git show "<commit>:数学/分析/分析III/概念/fejer-kernel.md"` —— **该路径在该 commit 下不存在**,会报 `path ... does not exist`,白费若干次调用。真实情况是这些页在 `03f1366` 被删之前位于 **`数学/分析/分析III/Fourier/概念/`**(Fourier 子目录在更早的 `102a10a` 就建好了)。可靠做法是**先问 git 文件在哪**,不要凭目录直觉拼路径:

```powershell
# 1) 找出这些页在某个 commit 的完整路径(用对的文件名,注意可能还是英文名)
git -c core.quotepath=false ls-tree "03f1366^:数学/分析/分析III/Fourier/概念/"
# 2) 直接读内容(路径照上一步输出抄)
git -c core.quotepath=false show "03f1366^:数学/分析/分析III/Fourier/概念/fourier-learning-path.md"
# 3) 找"某内容"何时被引入/删除
git log --all --oneline -S "Fejer" ; git log --all --oneline --diff-filter=D -- <路径>
```
删除记录在 `03f1366`(commit message 原文:"删除未覆盖的第 4-8 章概念页(fejer/parseval/applications/transform/orthogonal)");更早的英文→中文重命名在 `6f41002`(`--name-status` 显示为 `R079`/`R094` 等 rename 记录,是查"旧英文名对应哪个中文名"的最快来源)。**`fourier-applications` 与 `fourier-transform` 两页本次未恢复**(§6–§8 仍未讲授)。

### 恢复旧页时必须核对的硬伤(实测清单)

旧版概念页带着当年纠正过的错误,原样复活会把错误带回来:

- `fejer-kernel.md` 把 Fejér 定理条件写成"只需连续",**漏掉 2π 周期性与端点条件**。
- 旧版普遍断言"法国体系先证 Fejér 定理、体现先易后难"——**本讲义实际顺序是第 3 章先 Dirichlet 核 + Dini,第 4 章才讲 Fejér**;这个"Fejér 先行"印象正是 2026-09-05 被用户纠正过的点,不许复活。
- 旧 `parseval-identity.md` 说"先证 Bessel 不等式,再证等号成立",与本讲义"投影最佳 + 借一致逼近"的实际证明链不符,应改写。
- 旧 `orthogonal-system.md` 同为英文名时期的产物,内容需整体对齐新讲义 §5.1–5.3 的编号与记号。

**课程页覆盖 ≠ 用户已学**:判据仍是 wiki 概念页是否存在 + 讲义正文写到哪(§5.5,9 月 26 日课);§6–§8 只在目录里,不得引用或建页。

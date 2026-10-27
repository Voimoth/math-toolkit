# 代数III 题集带做（Rosso《Exercices USTC Octobre 2026》，8 题）

> 用法：他一句「带我做下载里的题」就照本文件陪练。原文件随「课堂材料流」归档，现在在 `/mnt/e/书籍/代数/代数III/TD/`
> （`~/下载` 会被清空，找不到就 `find /mnt/e/书籍 -name 'Exercices*USTC*'`）；
> PDF 的真实文本层用 `pdftotext -layout "Exercices USTC Octobre 2026.pdf" out.txt` 取，**`read_file` 的 PDF 提取会丢掉全部数学符号**
> （本文实测：`ε(τ)=−1`、`𝔄_n ⊂ 𝔖_n`、`sσs⁻¹` 全没了）⇒ 转述定义/判据前先跑 pdftotext 逐字核。
> 高危项：**奇偶、量词、指数、上下标**——把「基数偶数的轨道」说成「奇数」这种错他一句就能抓住，且会连带把整道题的方向带偏。
> 其余 OCR 噪声同理（上下标、\prod 求和、\binom 常丢）。
>
> **分式会整个丢。** `\prod_{k=0}^{n-1}\frac{p^n-p^k}{p-1}` 被提取成 `k=0 (p 1)`，分子分母全没了；照这段文本讲题就会把分母吃掉，
> 用户当成事实错误抓（原话「分母怎么被你吃了？这样题目就太宽松了」）。
> **凡题目里有分式、根号、求和上下限、分段括号：先渲图再开口** ——
> `pdftoppm -r 200 -f <页> -l <页> -png "Exercices USTC Octobre 2026.pdf" /tmp/p` 之后用视觉模型读该页，
> 确认分子分母与上下限再转述。这是公式类题目的第一步，不是「存疑才查」。

## 题眼地图（每题在练什么）

1. $S_n$ 的 $m$-循环 $c$：① $c^k$ 的循环分解；② 中心化子 $Z(c)$
2. 4125 阶、144 阶单群是否存在
3. $H$ 循环、$f(H)=g(H)$ ⇒ 两个半直积同构
4. $G\times H\cong G\times H'$ ⇒ $H\cong H'$（$m(G_1,G_2)$ 计数；阿贝尔结构定理的唯一性）
5. $\mathfrak A_n$ 里 special / non special 元素与共轭类是否在 $\mathfrak S_n$ 中分裂
6. 直积循环 ⟺ 各因子循环且阶两两互素
7. $GL_n(k)$ 对角子群的正规化子（单项矩阵）；$n!\mid\prod_{k=0}^{n-1}\dfrac{p^n-p^k}{p-1}$（**分母在 $\prod$ 里面**，整体 $=\prod(p^n-p^k)/(p-1)^n$）
8. Bruhat 分解 $G=BWB$

## 已确认的论证骨架（可直接复用）

### Ex1.1 $c^k$ 的分解
坐标化：$c=(1\,2\,\dots\,m)$ ⇒ $c^k$ 就是 $\mathbb Z/m\mathbb Z$ 上的平移 $x\mapsto x+k$ ⇒
「$c^k$ 的循环分解」= $\langle k\rangle$ 在 $\mathbb Z/m\mathbb Z$ 上的轨道分解；
长度 $=|\langle k\rangle|=m/\gcd(m,k)$，轨道个数 $=\gcd(m,k)$。（长度也可写成 $\mathrm{ppcm}(m,k)/k$。）

### Ex1.2 $Z(c)\cong\langle c\rangle\times\mathfrak S_{n-m}$
四步：① $\mathrm{Fix}(\sigma c\sigma^{-1})=\sigma(\mathrm{Fix}\,c)$（写成 $x\in\dots\iff\dots$ 链）⇒ $\sigma(S)=S$；
② $\tau=\sigma|_S$ 与 $c$ 交换且**被 $\tau(1)=c^j(1)$ 决定** ⇒ $\tau\in\langle c\rangle$；③ 支撑不交 ⇒ 互相交换；
④ 内直积四条 ⇒ $Z(c)=\langle c\rangle\times\mathfrak S(S^c)$。
写作三招：不动点集写 ⟺ 链；「被 $\tau(1)$ 决定」是严格性的落点；收尾用内直积四条而非「显然 $\cong$ 直积」。
标准化的合法性也要写（$\sigma\mapsto\rho\sigma\rho^{-1}$ 是自同构 ⇒ 把 $Z(c)$ 送到 $Z(\rho c\rho^{-1})$）。

### Ex2.1 4125 = 3·5³·11（三个素因子 ⇒ 只能 Sylow 计数 + 数元素）
$n_{11}\equiv1\pmod{11}$、$n_{11}\mid375$ ⇒ $n_{11}\in\{1,375\}$；$n_5\equiv1\pmod5$、$n_5\mid33$ ⇒ $n_5\in\{1,11\}$。
$n_5=1$ ⇒ 正规 125 阶子群 ⇒ 非单。$n_5=11$ 时 5-元有 $11\cdot124=1364$ 个；
若再有 $n_{11}=375$ 则 11-元 $375\cdot10=3750$ 个 ⇒ $1+1364+3750=5115>4125$ 矛盾 ⇒ $n_{11}=1$ ⇒ 非单。
（非单位元的阶分属 5 幂 / 11 / 3 幂，互不重合，故可相加。）

### Ex2.2 144 = 2⁴·3²（**全程初等，不需要 transfer**）
$n_3\equiv1\pmod3$、$n_3\mid16$ ⇒ $n_3\in\{1,4,16\}$。假设 $G$ 单：
- $n_3=1$ ⇒ 9-Sylow 正规 ⇒ 矛盾。
- $n_3=4$ ⇒ 共轭作用 $\varphi:G\to\mathfrak S_4$，$\ker\trianglelefteq G$；
  $|\ker|=144/|\mathrm{Im}\,\varphi|\ge144/24=6$ ⇒ $\ker\neq1$；又 $\ker\subseteq N_G(P)$、$|N_G(P)|=36$ ⇒ $\ker\neq G$ ⇒ 非单。
- $n_3=16$ ⇒ 两步：
  ① **任意两个 9-Sylow 交平凡**（反设 $P\cap Q=\langle x\rangle$、$|x|=3$）：$P,Q$ 9 阶 ⇒ 交换 ⇒ $P,Q\subseteq C_G(x)$；
     于是 $|C_G(x)|\ge|PQ|=27$（**集合**大小；$PQ\subseteq C_G(x)$）、$9\mid|C_G(x)|$、$|C_G(x)|\mid144$
     ⇒ $|C_G(x)|\in\{36,72,144\}$，三种都排除：$144\Rightarrow x\in Z(G)\Rightarrow\langle x\rangle\trianglelefteq G$；
     $72\Rightarrow[G:C_G(x)]=2$ ⇒ 正规；$36\Rightarrow[G:C_G(x)]=4\Rightarrow G\to\mathfrak S_4$，核既非 1 也 $\ne G$。
  ② **数元素**：交平凡 ⇒ 每个 9-Sylow 的 8 个非平凡元（阶都 $\in\{3,9\}$：$C_3^2$ 为 8 个 3 阶，$C_9$ 为 2 个 3 阶 + 6 个 9 阶）互不重叠
     ⇒ $16\times8=128$ 个元素不在任何 2-Sylow 里 ⇒ 只剩 15 个 ⇒ 每个 2-Sylow 的 15 个非平凡元恰好落满这 15 个
     ⇒ 唯一 2-Sylow ⇒ $n_2=1$ ⇒ 正规 ⇒ 非单。
  （关键：**不区分 $C_3^2$ 与 $C_9$** —— 只需「那 8 个非平凡元的阶不是 2 的幂」。
  另一条路是 $N_G(P)=P=C_G(P)$ 后用 Burnside 转移定理，但**课程没有 transfer**（Rosso 01 与习题课实测零命中），不必走。）

### Ex3（= 已讲过的轨道原理）
$f,g:H\to\mathrm{Aut}(N)$ 且 $f(H)=g(H)$、$H$ 循环 ⇒ 存在 $\alpha\in\mathrm{Aut}(H)$ 使 $g=f\circ\alpha$ ⇒ 两个半直积同构。
（21 阶的 $k=2$ 与 $k=4$ 就是这条的实例。）

### Ex5 特殊 / 非特殊（讲完 1) 的骨架，2)3) 一线贯下）

**定义**：$\sigma\in\mathfrak A_n$ 非特殊 $\iff$ 存在**奇** $\tau\in\mathfrak S_n$ 使 $\tau\sigma=\sigma\tau$。

**枢纽（先把它说透，其余都是翻译）**：非特殊 $\iff Z(\sigma)\not\subseteq\mathfrak A_n$；又 $\sigma\in\mathfrak A_n$ ⇒ $Z_{\mathfrak A_n}(\sigma)=Z_{\mathfrak S_n}(\sigma)\cap\mathfrak A_n$，
于是只有两种可能：非特殊 $[Z_S:Z_A]=2$，特殊 $Z_S=Z_A$。2)、3) 全部由「类大小 = 指数」推下去；3) 另需 $s\sigma s^{-1}$ 不与 $\sigma$ 在 $\mathfrak A_n$ 中共轭
（反设 $a\sigma a^{-1}=s\sigma s^{-1}$ ⇒ $a^{-1}s\in Z_S\subseteq\mathfrak A_n$，但 $a^{-1}s$ 是奇的，矛盾）。

**他给的最短路线（优先讲这条，其余只留一句）**：右边不成立（无偶长循环、每种奇长至多一条）⇒ 中心化子阶 $=\prod_d d^{m_d}m_d!$ 是奇数
⇒ 奇阶子群必落 $\mathfrak A_n$（看 $C\to\mathfrak S_n/\mathfrak A_n$，核的指数整除 2 又整除奇阶 ⇒ 指数为 1）
⇒ 中心化子全偶 ⇒ 特殊，逆否即「非特殊 ⇒ 右」。比逐点算签名短得多；2026-10-22 他用这一版推翻了 agent 两页的签名路线。
签名只留作底稿，等他追问「为什么 $\tau$ 的作用只有那两种」时再用。

**1) 的两支各自从哪来**：$\tau\sigma=\sigma\tau$ $\iff$ $\tau$ 把 $\sigma$-轨道送到**同长**的 $\sigma$-轨道。于是签名的奇偶只可能来自：
- 一条轨道内部：$\tau|_{\text{轨道}}=\sigma^k$，贡献 $(-1)^{k(d-1)}$，只在 $d$ **偶**时能是 $-1$；
  而 $\sigma\in\mathfrak A_n$ 迫使偶长轨道的条数 $m_d$ 为偶，所以这种轨道不会孤零零一条 ⇒ 直接取该轨道上的 $\sigma$ 就是要求的奇 $\tau$。
- 成对交换两条 $d$-轨道：错位 $k$ 不改变 parity，贡献 $(-1)^d$，只在 $d$ **奇**时是奇 ⇒ 需要**两条等长奇数**轨道。

**反方向要算 $\mathrm{sign}(\tau)$，先把它结构定死**（他会追问「为什么 $\tau$ 的作用只有这两种」）：
把长度 $d$ 的循环排成 $m_d\times d$ 阵列、行内按 $\sigma$ 排序（$\sigma$ 行内右移一格）。$\tau\sigma=\sigma\tau$ 等价于
$\tau(\sigma^t a)=\sigma^t\tau(a)$，于是唯一的可能是：
① 若 $\tau(a_{i,0})$ 落在 $C_j$ 上，则整条 $C_i$ 的像是 $\tau(\sigma^t a_{i,0})=\sigma^{c_i+t}(a_{j,0})$ ——
**$\tau$ 在一个起点上的像逼出整条循环的像**，这就是「行置换 $\pi_d$ + 每行横向错位 $c_i$」的完备性，只需一行 $\tau\sigma^t=\sigma^t\tau$；
同时 $\tau$ 把 $\langle\sigma\rangle$-轨道送到 $\langle\sigma\rangle$-轨道、长度不变，故偶长循环只能落到偶长循环上（$\pi_d$ 存在）。
② 签名按组相乘：行置换贡献 $\mathrm{sign}(\pi_d)^d$、行内错位贡献 $\prod_i(-1)^{c_i(d-1)}$，故
$\mathrm{sign}(\tau)=\prod_{d\ \text{奇}}\mathrm{sign}(\pi_d)\cdot\prod_{d\ \text{偶}}(-1)^{\sum c_i}$
（$d$ 奇时 $d-1$ 偶、$d$ 次方不消号 ⇒ 组符号 $=\mathrm{sign}(\pi_d)$；$d$ 偶时块置换恒偶、符号全来自错位）。

**把奇偶算成人话（他唯一肯接受的版本，先给这三行再给上式）**：不要说「签名同态、乘积公式」，直接数**换位数**——
搬一条长 $d$ 的循环到另一条同长循环上 $=(a_0a'_0)(a_1a'_1)\cdots(a_{d-1}a'_{d-1})$，$d$ 个换位 ⇒ $(-1)^d$；
在一条 $d$-循环内转 $k$ 格（= 该 $d$-循环取 $k$ 次幂）$=k(d-1)$ 个换位 ⇒ $(-1)^{k(d-1)}$；
整行置换同理：一次行交换是 $d$ 个换位，$\pi_d$ 由 $\#$ 个换位组成 ⇒ 贡献 $\big((-1)^d\big)^{\#}=\mathrm{sign}(\pi_d)^d$。
顺序反了（公式在前、计数在后）他会当场说「毫无可读性」。
反方向收尾只有一步：特殊 ⇒ 无偶长循环、每种奇长至多一条 ⇒ 所有 $\pi_d$ 是单点恒等、偶长那个积为空 ⇒ **$\mathrm{sign}(\tau)=+1$ 对所有 $\tau\in Z(\sigma)$ 恒成立** ⇒ 不存在奇的中心化元素。

**对照例（都已核）**：$\mathfrak A_3$ 与 $\mathfrak A_4$ 里的 $(123)$ 都**特殊**（轨道只有 $3$ 与 $1$，两支都凑不出）；
$\mathfrak A_5$ 里同一循环型**非特殊**（多出两条长度 1 的轨道，$\tau=(45)$）。差别不在循环型，而在 $n$ 比支集大多少。

**必须当场纠的错**：「非特殊 $\Rightarrow|\mathrm{supp}|\le n-2$」**不成立**——$\mathfrak A_4\ni(12)(34)$ 走偶长（2）轨道那一支，非特殊而 $\mathrm{supp}=4=n$。可用的方向只有「不动点 $\ge2$ ⇒ 非特殊」，逆不成立。

**开口先交代对象**：判据里的「$\sigma$-轨道」指 $\langle\sigma\rangle$ 作用在 $\{1,\dots,n\}$ 上（= 循环分解的支撑，不动点是长度 1 的轨道），
与 $\mathfrak S_n/\mathfrak A_n$ 的共轭作用**无关**。他第一个追问就是「这个轨道是哪个群作用在哪个集合上的产物」——先点明省一轮。

### Ex7 对角子群的正规化子与 $n!$ 整除（按一个问题讲，正规化子只是中间站）

**题意**：证 $n!\mid\prod_{k=0}^{n-1}\dfrac{p^n-p^k}{p-1}$，该数 $=|GL_n(\mathbb F_p)|/(p-1)^n$，即 $\mathbb F_p^n$ 里完全旗的个数。
题面把它拆成「先算正规化子、再证整除」两问，但按用户要求**当成一个问题讲**。

**五步骨架**：
① 不数元素，找子群：若 $N\le GL_n$、$D\trianglelefteq N$ 且 $N/D\cong\mathfrak S_n$，则 $|N|=|D|\,n!$ 整除 $|GL_n|$。
② 取 $D$ = 对角矩阵，$|D|=(p-1)^n$ —— **正好抵消分母**（题目把分母写成 $(p-1)^n$ 就是为它）。
③ $N_G(D)$ = **单项矩阵**（每行每列恰一个非零元）：共轭回 $D$ 自身 $\iff$ 把每个坐标轴映成某个坐标轴，
而对角矩阵的公共特征直线恰好就是这些坐标轴；反向，单项矩阵显然把对角矩阵映成对角矩阵。
④ 单项矩阵 = 置换矩阵 × 对角矩阵 ⇒ $N=D\rtimes\mathfrak S_n$，故 $N/D\cong\mathfrak S_n$。
⑤ $|N|=(p-1)^n n!\mid|GL_n(\mathbb F_p)|=\prod(p^n-p^k)$，两边同除 $(p-1)^n$ 即得。

**陷阱**：别按 $|GL_n|=\prod(p^n-p^k)$ 讲（分母一吃，题目就被讲宽松了，他立刻指出）。
与 Ex8 的 Bruhat 分解是同一件事的两种说法：旗空间 $=G/B$，而 $\mathfrak S_n$ 就是那里的 $W$。

## 三个自查陷阱（讲 Sylow / 正规化子时最常犯）

1. **「$PQ$ 是子群」不能默认**：$|HK|=|H||K|/|H\cap K|$ 对集合 $HK$ 总成立；要 $HK\le G$ 需 $P\subseteq N_G(Q)$ 之类。
2. **子集大小不整除群阶**：$PQ\subseteq N_G(A)$ 只给 $|N_G(A)|\ge|PQ|$。
3. **共轭作用的核是 $\bigcap N_G(P)$ 不是 $\bigcap P$** ⇒ 只能得 $|\ker|\mid|G|/n_p$。

## 数学法语措辞（他会直接问「这句法语怎么写」）

- 不妨设：`Quitte à conjuguer c, on peut supposer que c = (1 2 … m).`
  （`quitte à` **后接具体动作** remplacer / conjuguer / renommer；比 `Sans perte de généralité, on peut supposer que …` 更具体、更受法国老师喜欢。）
- 归约到：`Par conjugaison, on se ramène au cas où …`（他笔记 08 讲义就是这个用法）。
- 常见收尾连接：`d'où`、`ce qui donne`、`par conséquent`、`il en résulte que`。

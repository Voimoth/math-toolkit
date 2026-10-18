# 代数III 题集带做（Rosso《Exercices USTC Octobre 2026》，8 题）

> 用法：他一句「带我做下载里的题」就照本文件陪练。原文件在 `~/下载/`（按他的「课堂材料流」放这里）；
> PDF 有文本层可直接 `read_file`，但 OCR 噪声多（上下标、`\prod` 求和、`\binom` 常丢）⇒ **读题逐字核对**再给目标。

## 题眼地图（每题在练什么）

1. $S_n$ 的 $m$-循环 $c$：① $c^k$ 的循环分解；② 中心化子 $Z(c)$
2. 4125 阶、144 阶单群是否存在
3. $H$ 循环、$f(H)=g(H)$ ⇒ 两个半直积同构
4. $G\times H\cong G\times H'$ ⇒ $H\cong H'$（$m(G_1,G_2)$ 计数；阿贝尔结构定理的唯一性）
5. $\mathfrak A_n$ 里 special / non special 元素与共轭类是否在 $\mathfrak S_n$ 中分裂
6. 直积循环 ⟺ 各因子循环且阶两两互素
7. $GL_n(k)$ 对角子群的正规化子（单项矩阵）；$n!\mid\prod_{k=0}^{n-1}(p^n-p^k)$
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

## 三个自查陷阱（讲 Sylow / 正规化子时最常犯）

1. **「$PQ$ 是子群」不能默认**：$|HK|=|H||K|/|H\cap K|$ 对集合 $HK$ 总成立；要 $HK\le G$ 需 $P\subseteq N_G(Q)$ 之类。
2. **子集大小不整除群阶**：$PQ\subseteq N_G(A)$ 只给 $|N_G(A)|\ge|PQ|$。
3. **共轭作用的核是 $\bigcap N_G(P)$ 不是 $\bigcap P$** ⇒ 只能得 $|\ker|\mid|G|/n_p$。

## 数学法语措辞（他会直接问「这句法语怎么写」）

- 不妨设：`Quitte à conjuguer c, on peut supposer que c = (1 2 … m).`
  （`quitte à` **后接具体动作** remplacer / conjuguer / renommer；比 `Sans perte de généralité, on peut supposer que …` 更具体、更受法国老师喜欢。）
- 归约到：`Par conjugaison, on se ramène au cas où …`（他笔记 08 讲义就是这个用法）。
- 常见收尾连接：`d'où`、`ce qui donne`、`par conséquent`、`il en résulte que`。

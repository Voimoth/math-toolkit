# A5 单性、60 阶群与 SO(3) 分类收尾（2026-09-11 讲义第三份）

课程内容层笔记。对应 `笔记/正课/09-Jordan与Frobenius.md` 及后续篇（原单文件 `代数III笔记.md` 已拆分）与概念页 `A5单性与60阶群`、`SO3的有限子群`。
`math-coach` 负责怎么教；本文档只存**这门课的实质数学内容与教学要点**。

## 1. A₅ 元素普查（后续一切证明的地基）

$|\mathfrak{A}_5| = 60 = 2^2 \times 3 \times 5$，元素**恰好**分四类：

| 阶 | 类型 | 个数 | 计数 |
|---|---|---|---|
| 1 | $\mathrm{Id}$ | 1 | — |
| 2 | $(ab)(cd)$ 双转置 | 15 | $5\binom{4}{2}/2$（$e$ 有 5 选，$ab$ 从余下 4 取 2，但 $(ab)(cd)=(cd)(ab)$ 故除 2） |
| 3 | 3-循环 | 20 | $\binom{5}{3}\cdot 2$（10 个支撑 × 两个方向） |
| 5 | 5-循环 | 24 | $4! = (n-1)!$ |

$1+15+20+24 = 60$ —— **穷尽**。

## 2. 共轭类结构（与后续证明直接相关，且是易错点）

$\mathfrak{A}_5$ 的共轭类大小：**1, 15, 20, 12, 12**。

- 2 阶元：**单一**类，15 个。
- 3-循环：**单一**类，20 个（$n \geqslant 5$ 时 3-循环在 $\mathfrak{A}_n$ 中共轭）。
- **5-循环：两个各 12 个的类**（互为逆）。原因：5-循环 $\sigma$ 的中心化子是 $\langle\sigma\rangle$（阶 5），故 $|\mathrm{Cl}(\sigma)| = 60/5 = 12$；24 个元素必然一分为二。

> [!warning] 这是最容易被散文误导的一处
> 讲义原句 `ces 5-cycles ne peuvent pas être conjugués dans A5 car 24 ∤ 60` 只是说"不能（全体）共轭"。
> 不要读成"24 个 5-循环同属一类"。**已用枚举脚本核验**（`math-notes-transcription` 的
> `scripts/group_enumeration_verify.js`）。

## 3. A₅ 单性：逐类排除（"数元素"证明的骨架）

设 $H \triangleleft \mathfrak{A}_5$，$H \neq \{\mathrm{Id}\}$。机制 = **正规子群吸收整个共轭类**（含一个即含全类）。

| $H$ 含 | 则含 | 得 $|H| \geqslant$ | 用 $|H| \mid 60$ + Sylow 逼到 60 |
|---|---|---|---|
| 5-循环 | 全部 24（须借 $\langle\sigma\rangle$ 拿到另一类） | 25 | $|H|\in\{30,60\}$；$|H|=30$ 时 $3 \mid 30$ ⇒ 含 3 阶元 ⇒ $\geqslant 45 > 30$ |
| 3-循环 | 全部 20 | 21 | $|H|\in\{30,60\}$；$|H|=30$ 时 $5 \mid 30$ ⇒ 含 5 阶元 ⇒ $\geqslant 45 > 30$ |
| 仅 2 阶元 | 全部 15 | 16 | $|H|\in\{20,30,60\}$；20 被 5 整除、30 被 3 整除，均触发更大类 ⇒ 只能 60 |

> [!note] 教学要点
> - **$25 \nmid 60$ 只排除 $|H|=25$，不排除 30**（30 是 60 的真因子且 $\geqslant 25$）。真正排除 30 靠
>   "30 含 3 阶元 ⇒ 阶数跳到 45"。**5-循环单独不能立刻终局——这个坑值得指给学生。**
> - 每一类的跳板都是 **Sylow 存在性**："$p \mid |H|$ ⇒ $H$ 含 $p$ 阶元"。这是把 20/30 这类
>   中间阶数杀掉的关键，也把 Sylow 与简单性证明接了起来。

**$n \geqslant 6$ 的归约**：取 $F \subset \{1,\dots,n\}$，$|F|=5$，$A_F$ = 支撑含于 $F$ 的偶置换 ⇒ $A_F \simeq \mathfrak{A}_5$ 单。
$H \cap A_F \triangleleft A_F$ ⇒ 只需找到 $F$ 使 $H \cap A_F \neq \{\mathrm{Id}\}$，即 $H$ 中有非平凡元**至少固定 $n-5$ 个点**。
构造：取 $\sigma \in H \setminus \{\mathrm{Id}\}$、3-循环 $\tau$，令 $\sigma' = \tau\sigma\tau^{-1}\sigma^{-1}$；
选 $b = \sigma(a)$（$a$ 满足 $\sigma(a) \neq a$）、$c \notin \{a, b, \sigma(b)\}$ ⇒ $\sigma'(b) \neq b$，故 $\sigma' \neq \mathrm{Id}$，
且其支撑被压进 5 个点内。一旦 $H$ 含 3-循环即得 $H = \mathfrak{A}_n$。

## 4. 反过来：60 阶单群必 ≅ A₅

策略：证 $G$ 有指数 5 的子群 ⇒ $G \hookrightarrow \mathfrak{S}_5$ ⇒ $|G|=60$ 且单 ⇒ $G \simeq \mathfrak{A}_5$。

1. **排除指数 $\leqslant 4$**：$K$ 指数 $d \leqslant 4$ ⇒ 平移作用 $\Psi: G \to \mathfrak{S}_d$，$|\mathfrak{S}_d| \leqslant 24 < 60$，
   $\Psi$ 不能单；但 $G$ 单 ⇒ $\Psi$ 单。矛盾。
2. **假设所有真子群指数 $\geqslant 6$，导出矛盾**（**这个假设必须用起来**）：
   - $k_5 \equiv 1 \bmod 5$ 且 $k_5 \mid 12$ ⇒ $k_5 \in \{1,6\}$；$k_5=1$ 则唯一 5-Sylow 正规（$G$ 单，排除）⇒ $k_5 = 6$ ⇒ **24 个 5 阶元**。
   - $k_2$ 奇且 $\mid 15$ ⇒ $\{1,3,5,15\}$；由速假设 $k_2 \geqslant 6$ ⇒ **$k_2 = 15$**。
   - **2-Sylow 两两交平凡**：若 $S_1 \cap S_2 = \{e,u\}$，考虑 $C(u)$。$S_1, S_2$ 阶 4 故交换（**阶 4 群必交换**），
     得 $4 \mid |C(u)|$ 且 $|S_1 \cup S_2| = 6 \leqslant |C(u)|$；又 $[G:C(u)] \geqslant 6$ ⇒ $|C(u)| \leqslant 10$
     ⇒ 只能 $|C(u)| = 8$，但 $8 \nmid 60$，矛盾。另一可能 $C(u)=G$ ⇒ $u \in Z(G)$，与单性矛盾。
   - ⇒ 15 个 2-Sylow 各贡献 3 个非平凡元 ⇒ 45 个 2 或 4 阶元。**$1+24+45 = 70 > 60$，矛盾。**

> [!warning] 指数假设的两处用处（学生最易漏）
> ① $k_2 \geqslant 6$（决定 $k_2=15$）；② $[G:C(u)] \geqslant 6$（给出 $|C(u)| \leqslant 10$）。
> **拿掉指数假设，$k_2$ 可能是 3 或 5，整个矛盾消失。** 第一步只排除了指数 $\leqslant 4$，
> 指数 6 以上无法用阶数矛盾直接排除（$6! > 60$），所以必须靠这个假设。

**手写稿的两处 OCR 订正（已裁剪复核）**：原文是 `4 \mid |C(u)|`（不是 `8 \mid`）与 `[G:C(u)] = 6 ⇒ |C(u)| ≤ 10`。

## 5. SO(3) 的 N=3 两情形回填

| $e_1,e_2,e_3$ | $\lvert G\rvert$ | 结论 | 手法 |
|---|---|---|---|
| 2,3,5 | 60 | $\mathfrak{A}_5$ | 轨道 30/20/12 ⇒ 轴 15/10/6 ⇒ 元素 $1+15+20+24=60$ 穷尽；再逐类排除证单 |
| 2,3,4 | 24 | $\mathfrak{S}_4$ | $O_2$ 的 4 条轴给出 $G \to \mathfrak{S}_4$；证 $\ker\varphi = \{\mathrm{Id}\}$ 后由 $|G|=24=|\mathfrak{S}_4|$ 得同构 |

$|G|=24$ 情形证核平凡的关键一步：$g \in \ker\varphi$ ⇒ $g$ 稳定每条轴、取 $\pm\mathrm{Id}$ ⇒ $g^2=\mathrm{Id}$ ⇒ $g$ 是 $\pi$ 旋转；
$g$ 在 4 条轴上全取 $-\mathrm{Id}$（否则落在 3 阶稳定子里）⇒ 其轴正交于这 4 条轴且被全体 $h \in G$ 保持
⇒ 产生 3 元轨道，与轨道大小 $\{12,8,6\}$ 矛盾。

## 6. Sₙ 的结构收尾（三条配套定理）

1. **正规子群**（$n \geqslant 5$）：只有 $\{\mathrm{Id}\}$、$\mathfrak{A}_n$、$\mathfrak{S}_n$。
   证：$H \cap \mathfrak{A}_n \triangleleft \mathfrak{A}_n$ 且 $\mathfrak{A}_n$ 单 ⇒ 或得 $\mathfrak{A}_n \subset H$（指数 2 ⇒ $H=\mathfrak{A}_n$ 或 $\mathfrak{S}_n$），
   或 $H \cap \mathfrak{A}_n = \{\mathrm{Id}\}$ ⇒ $\varepsilon|_H$ 单 ⇒ $|H|\mid 2$ ⇒ $H=\{\mathrm{Id},u\}$ ⇒ $u \in Z(\mathfrak{S}_n)=\{\mathrm{Id}\}$，矛盾。
2. **指数 $n$ 的子群**：$H \subset \mathfrak{S}_n$ 指数 $n$ ⇒ $H \simeq \mathfrak{S}_{n-1}$。
3. **导群**：$\mathfrak{D}(\mathfrak{S}_n) = \mathfrak{A}_n$；$n \geqslant 5$ 时 $\mathfrak{D}(\mathfrak{A}_n) = \mathfrak{A}_n$（**完美群**，无非平凡交换商）。
   证：每个 3-循环是换位子 —— 由 $\sigma\tau\sigma^{-1} = \tau^2$ 得 $\tau = \tau^2\tau^{-1} = [\sigma,\tau]$。
   **已用枚举核验**：$|\mathfrak{D}(\mathfrak{S}_4)| = 12 = |\mathfrak{A}_4|$；$|\mathfrak{D}(\mathfrak{A}_5)| = 60$。

> [!tip] 教学连接点
> $\mathfrak{D}(\mathfrak{S}_n)=\mathfrak{A}_n$ = "符号差是唯一的非平凡交换商"，与"唯一非平凡同态 $\mathfrak{S}_n \to \mathbb{C}^*$"是同一件事。
> $\mathfrak{D}(\mathfrak{A}_n)=\mathfrak{A}_n$ 是 $\mathfrak{A}_n$（$n \geqslant 5$）**不可解**的开端 —— 这是通向伽罗瓦理论
> （五次方程不可解 ⇔ $A_5$ 不可解）的伏笔，值得提前点一句。

## 7. $n=4$ 为什么是唯一例外（教学要点）

$\mathfrak{A}_4$ 的 12 个元素：$\mathrm{Id}$ + 3 个双转置 + 8 个 3-循环。
3 个双转置与 $\mathrm{Id}$ 合成 Klein 四元群 $V \triangleleft \mathfrak{A}_4$（**枚举已验**：$V$ 在 $\mathfrak{A}_4$ 与 $\mathfrak{S}_4$ 中都正规）。

机制：$n=4$ 时 $1+3 = 4$ **恰整除** 12，卡在边界；$n \geqslant 5$ 时 $1+15 = 16 \nmid 60$，越过门槛。
另一条线：3-循环共轭性证明需要"另取两个不在 $\{a',b',c'\}$ 中的元素"，$n=4$ 时只剩 1 个，取不出。
**这两条解释都该讲给学生**（前者是计数门槛，后者是技巧失效点）。

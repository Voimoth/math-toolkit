# 半双线性型与 Hermite 型（笔记 11，今年讲义 §1.5）的教法

对应 `笔记/正课/11-半双线性形式与Hermite型.md`。后续笔记 12（伴随、正规算子）、13（酉群、极分解、Courant–Fischer）同属「型与算子」这一块，继续往本文件里长，别另开文件。

## 动机链（按这个顺序讲，不要从定义起）

1. **共轭不是口味，是齐次性逼出来的**。要的是 $h(\lambda x)=|\lambda|^2h(x)$；若 $h$ 来自不共轭的双线性 $\varphi$，得到的是 $\lambda^2$。要出现模方，只能让**一个**变元吃共轭 ⇒ 两个变元一个线性、一个共轭线性 ⇒ sesquilinéaire（字面「一个半」）。这一句讲完，定义就不用解释了。
2. **Hermite 对称也不是口味**：$\varphi(y,x)=\overline{\varphi(x,y)}$ 正是 $h(x)=\varphi(x,x)$ 取实值的充要条件；不实就无法谈正负，也就没有 signature。这是实二次型里「对称双线性」的对位物。
3. **结构性平行**：非退化 → 正交补 → 对角化 $\operatorname{diag}(1^r,-1^s,0)$ → signature 唯一（惯性律在复情形照旧，只是证明里 $\lambda^2$ 换成 $|\lambda|^2$）。
4. 极化恒等式放最后说「所以 $h$ 决定 $\varphi$」，别当公式背。

## 他的讲义记号（易错，讲前先确认方向）

- 讲义定义：$\varphi$ 对**第一个**变元半线性、对**第二个**变元线性 —— 与多数教材（第二个共轭）**相反**。于是展开式 $\varphi(x,y)=\sum_{i,j}\bar x_i y_j\,\varphi(e_i,e_j)$，矩阵 $H=(\varphi(e_i,e_j))$，Hermite 条件是 $H={}^{t}\bar H$。
- **坑**：两种约定下同一个形式给出的矩阵互为共轭；照自己的习惯写矩阵会把「是否 Hermite」判反。一律按讲义（第一变元共轭）。

## 本轮抛出的检验题与答案

**题**：$\varphi(x,y)=\bar x_1y_1+i\bar x_1y_2+i\bar x_2y_1+\bar x_2y_2$（$\mathbb C^2$）。矩阵是什么，是否 Hermite。

**答案**：$H=\begin{pmatrix}1&i\\ i&1\end{pmatrix}$，它**对称但不是 Hermite**（Hermite 要求 $i=-i$）。$h(x)=|x_1|^2+|x_2|^2+2i\operatorname{Re}(\bar x_1x_2)$ 一般不取实值，正好坐实动机第 2 条。

**为什么选这道**：「对称但非 Hermite」是这一块最容易被实矩阵直觉骗过去的形状，而且一次性对上「Hermite 对称 ⇔ $h$ 实」这条动机。

## 讲解顺序上的坑

- 迷向与 $V\cap V^\perp\ne\{0\}$ 必须配具体例子（$\mathbb C^2$ 上 $\bar x_1y_1-\bar x_2y_2$，取 $e=(1,1)$），否则他会把实正定情形的直觉（$V\cap V^\perp=0$）自动搬过来。
- signature 唯一性只需一句：正定部分 $F$ 与负定部分 $G'$ 交为零 ⇒ $r+s'\le n$ ⇒ 交换角色。不要把归纳与正交分解全铺开。
- 他会追问「正交补怎么能直接加维数」这类边界 —— 答法就是笔记 11 §6 的 $\dim V^\perp=\dim E-\dim V$（经 $\hat\varphi$ 送到零化子），直接引那一行，别另造证明。

## 他对那道检验题的实际答法与判据（照这个样子修）

- 他答「矩阵是 $\varphi(e_i,e_j)$，它是 Hermite 的」：矩阵那一半对，判定错。**判据一次给足、让他自己重判**：Hermite 要求 $\varphi(y,x)=\overline{\varphi(x,y)}$；取 $x=e_1,y=e_2$，左下是 $i$，右上是 $i$ 的共轭即 $-i$，对不上。他随即改成「不自动 Hermite，需要 Hermite 对称性，就像双线性型被要求对称一样」。
- **根因是对象层混淆的又一次现身**：他把「半双线性形式都有矩阵」这条**存在性构造**当成「矩阵自动满足 Hermite」这条**额外性质**。凡他答「是 X」而 X 是加在某对象上的条件时，先把「构造」与「性质」两件事当场拆开再判。

## 笔记 11 §3 命题：Hermite 对称可以被「逼」出来（讲在极化恒等式之前）

§3 的命题（非退化 $+$ 正交关系对称 $\iff\varphi=\lambda\psi$、$\psi$ Hermite）是回答「为什么非得 Hermite」的最强答案，**不要只当作技术引理跳过**。四步骨架：

1. 固定 $x$，两只线性形式 $\varphi(x,\cdot)$ 与 $y\mapsto\overline{\varphi(y,x)}$；垂直关系对称 $\iff$ 二者同核。
2. 同核 $\Longrightarrow$ 成比例，比例记 $\alpha(x)$。
3. 借 $\hat\varphi^{-1}$ 搬回 $E$：得把 $x$ 映到 $\overline{\alpha(x)}x$ 的**线性**映射 $\Longrightarrow$ $\alpha$ 必为常数。
4. 互换 $x,y$ 再走一轮 $\Longrightarrow|\alpha|=1$；取 $\lambda^2=\alpha$ 归一化即得 Hermite。

收口一句：**Hermite 不是随手挑的一类形式，它是「想让 $\perp$ 成为对称关系」时唯一的落脚点。**

## 极化恒等式：复数四项、实数两项

- 差在 $h$ 只给实值：$h(x+y)-h(x-y)=4\operatorname{Re}\varphi(x,y)$，虚部要把 $y$ 换成 $iy$ 重来一次再用 $i$ 去掉，即 $4\varphi(x,y)=[h(x+y)-h(x-y)]-i[h(x+iy)-h(x-iy)]$（讲义写成 $+\tfrac i4h(x+iy)-\tfrac i4h(x-iy)$，同一式）。
- **当场点出它的用处**：标准形定理证明里「若无非迷向向量则 $\varphi=0$」用的就是它 —— 每步 $h\equiv0\Rightarrow\varphi\equiv0\Rightarrow$ 与非退化矛盾 $\Rightarrow$ 归纳起步。他答这一问时只说「类似实数情形有极化恒等式」、没写公式：补公式 + 补这一条用处就够，不要重讲整段。

## 当前站位（接着问的那一题）

$\mathbb C^2$ 上 $h(x)=|x_1|^2-|x_2|^2$、$u=(1,1)$。预期：$\varphi(u,u)=0$ 故 $u$ 迷向；正交补为 $\{y:y_1=y_2\}=\mathbb Cu$，于是 **$V=V^\perp$**（不是真包含，因为维数已经相等）。这题验的是「迷向 $\Rightarrow V\subseteq V^\perp$」加上维数一配就到底。

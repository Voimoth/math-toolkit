# 矩阵群中正规性的可复用例子

以下例子用于中文讲解时建立“正规性 = 对母群中所有共轭保持不变”的直觉。约定矩阵乘法按通常顺序进行。

## 1. 正规：特殊线性群

行列式是群同态：

\[
\det:\mathrm{GL}_n(k)\to k^\times.
\]

因此

\[
\mathrm{SL}_n(k)=\ker(\det)\trianglelefteq\mathrm{GL}_n(k).
\]

直接验证：若 \(P\in\mathrm{GL}_n(k)\)、\(A\in\mathrm{SL}_n(k)\)，则

\[
\det(PAP^{-1})=\det(P)\det(A)\det(P)^{-1}=1.
\]

## 2. 正规：标量矩阵中心

\[
Z(\mathrm{GL}_n(k))=\{\lambda I_n:\lambda\in k^\times\}.
\]

对任意 \(P\)：

\[
P(\lambda I_n)P^{-1}=\lambda I_n.
\]

所以标量矩阵组成正规子群，事实上是中心。

## 3. 非正规：\(\mathrm{GL}_2(k)\) 中的可逆对角矩阵

令

\[
D=\left\{\begin{pmatrix}a&0\\0&b\end{pmatrix}:a,b\in k^\times\right\}.
\]

取

\[
A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\in D,
\qquad
P=\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]

则

\[
PAP^{-1}=\begin{pmatrix}2&-1\\0&1\end{pmatrix}\notin D.
\]

因此 \(D\not\trianglelefteq\mathrm{GL}_2(k)\)。原因是“对角”依赖于选定基底。

## 4. 非正规：整个 \(\mathrm{GL}_2(k)\) 中的可逆上三角群

令

\[
B=\left\{\begin{pmatrix}a&b\\0&d\end{pmatrix}:a,d\in k^\times,b\in k\right\}.
\]

取

\[
A=\begin{pmatrix}1&1\\0&1\end{pmatrix}\in B,
\qquad
P=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

则

\[
PAP^{-1}=\begin{pmatrix}1&0\\1&1\end{pmatrix}\notin B.
\]

所以 \(B\not\trianglelefteq\mathrm{GL}_2(k)\)。交换两个坐标把上三角形式变成下三角形式。

## 5. 母群依赖：幺正上三角群

令

\[
U=\left\{\begin{pmatrix}1&t\\0&1\end{pmatrix}:t\in k\right\}.
\]

在上三角群 \(B\) 中，若

\[
P=\begin{pmatrix}a&b\\0&d\end{pmatrix},
\qquad
A=\begin{pmatrix}1&t\\0&1\end{pmatrix},
\]
则

\[
PAP^{-1}=\begin{pmatrix}1&(a/d)t\\0&1\end{pmatrix}\in U.
\]

故 \(U\trianglelefteq B\)。但是取

\[
w=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\in\mathrm{SL}_2(k),
\]
有

\[
w\begin{pmatrix}1&t\\0&1\end{pmatrix}w^{-1}
=\begin{pmatrix}1&0\\-t&1\end{pmatrix}\notin U
\quad(t\neq0).
\]

所以 \(U\not\trianglelefteq\mathrm{SL}_2(k)\)，也通常不正规于 \(\mathrm{GL}_2(k)\)。同一个 \(U\) 在不同母群中的正规性不同。

## 6. 正规但换母群需谨慎：\(\mathrm{SO}_n\trianglelefteq\mathrm O_n\)

\[
\det:\mathrm O_n(\mathbb R)\to\{1,-1\}
\]
是群同态，且

\[
\mathrm{SO}_n(\mathbb R)=\ker(\det).
\]

因此 \(\mathrm{SO}_n(\mathbb R)\trianglelefteq\mathrm O_n(\mathbb R)\)。但 \(\mathrm O_n\) 通常不正规于更大的 \(\mathrm{GL}_n(\mathbb R)\)，因为一般换基不保持欧氏内积。

## 使用提示

讲解时最好把例子成对呈现：先给核或中心导致的正规例子，再给具体共轭把矩阵送出子群的非正规例子；最后强调正规性依赖母群。
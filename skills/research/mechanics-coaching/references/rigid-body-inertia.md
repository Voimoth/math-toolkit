# 转动惯量张量与刚体开场（hw8 Q1–Q4 的讲法·已核数值·坑）

## 用户的前置知识边界（先量再讲）

- 他会算的只有：**绕固定轴**的转动惯量 $\int\rho^2dm$（$\rho$＝到轴的垂直距离），以及薄圆盘 $\frac12mS^2$ 这一级别的一重积分。
- 他没有的："转动惯量张量"、"对参考点"这两个概念，也**不熟多重积分设元**（柱坐标体积元、把三重积分降成逐层一重）。
- 后果：第一轮直接抛 $I_{ij}$ 矩阵式会被当成又一个要背的公式。他会在同一题上**连问四层底座**：什么是张量 → 相对一个点怎么处理 → 这个积分怎么算 → 圆盘那 $\frac14mS^2$ 又是怎么积出来的。每层都必须落到可算的式子上，否则下一层必然卡住。

## 讲解链（按序，一次一层）

1. **先破"绕点转动"这个说法**：物理上只存在绕轴转；参考点只决定 $\mathbf r$ 从哪量起。题目"取顶点/重心为参考点"＝要求对**通过该点的每条轴**都能给数，这个依赖方向的函数就是张量。
2. **张量＝把熟悉的对轴量整理成二次型**：轴取单位方向 $\mathbf n$，则 $\rho=|\mathbf n\times\mathbf r|$，
   $I(\mathbf n)=\int|\mathbf n\times\mathbf r|^2dm=\int[r^2-(\mathbf n\cdot\mathbf r)^2]dm=\sum_{i,j}n_in_jI_{ij}=\mathbf n^{\mathsf T}\mathbf I\mathbf n$。
   由此给三句：对角元 $I_{xx}=\int(y^2+z^2)dm$ **就是**他原来会算的绕 $x$ 轴惯量（讲义式 7.17）；非对角元是惯性积 $-\int xy\,dm$，出现原因是 $\rho^2$ 展开的交叉项；算张量＝算 **6 个普通积分**，不是新工具。
3. **数够用的理由（极化）**：$b(\mathbf u,\mathbf v)=\frac14[I(\mathbf u+\mathbf v)-I(\mathbf u-\mathbf v)]$ ⇒ 球面上的值定死整个 $b$，"无数方向各一个数"被无损压成 6 个数。
4. **对角化的用处**：主轴基下 $I(\mathbf n)=\sum_k\lambda_kn_k^2$，$\sum n_k^2=1$ ⇒ $\lambda_{\min}\le I(\mathbf n)\le\lambda_{\max}$；绕主轴转时 $\mathbf L\parallel\boldsymbol\omega$ ⇒ 无摆动，自由陀螺才只在主轴稳定。
5. **代数语言**（他学过张量积，必追问）：$b\in\operatorname{Sym}^2(V^*)=(V\otimes V)^*$；只有欧氏度量 $g$ 才能把它同一个自伴算子 $\mathbf I\in\operatorname{End}V\simeq V\otimes V^*$ 等同（一次升标）。**无度量的空间上两者不同**——这是"惯量张量只住在欧氏空间"的准确含义。张量的判据是**协变** $I\mapsto RIR^{\mathsf T}$（两脚标各吃一个 $R$，即 $R\otimes R$ 作用），不是"九个数的数组"。
6. **术语史分两层**：概念上来自弹性力学"面力随取向而变、须双线性型刻画"（Cauchy 1822 的 tension→tensor，记忆层面）；"tensor"作为通用词的定名（Voigt）**未核实，当场标注，别写成史实**。

## 正方体 Q1（答案与概念陷阱）

- 矩阵结构 $\mathbf I=Ma^2(\alpha\mathbb 1+\beta J)$，$J$ 全 1 矩阵，$\alpha=11/12$、$\beta=-1/4$；特征值 $\alpha+3\beta=1/6$（主轴 $(1,1,1)$）与 $\alpha=11/12$（二重，平面 $x+y+z=0$）。
- **二重简并 ⇒ 主轴不唯一**：平面内任取一组正交单位基（省事的取 $(1,-1,0)/\sqrt2$、$(1,1,-2)/\sqrt6$），第三个轴必须是该平面的正交补 $(1,1,1)/\sqrt3$。
- 那份 $O(2)$ 自由度来自**张量简并**，不是刚体对称性：正方体绕体对角线的旋转群只有 $C_3$，给不出 $O(2)$；任一有两个主转动惯量相等的刚体都有这条结论。

## 切片法（刚体惯量积分的通用做法）

1. 沿对称轴切，取 $z=\mathrm{const}$ 的薄片；
2. 每片只用两个基本块：
   - 均匀薄圆盘（半径 $S$、质量 $m$）绕**自身中心轴**：$\frac12mS^2$；
   - 绕**自身直径**：$\frac14mS^2$（极坐标 $\int y^2dm$：$\sigma\int_0^Sr^3dr\int_0^{2\pi}\sin^2\theta\,d\theta=\frac{\sigma\pi S^4}{4}$；或垂直轴定理 $I_z=I_x+I_y=2I_x$）；
3. 每片贡献 $[\frac12S^2$ 或 $\frac14S^2]+z^2$ 乘 $dm$，$dm=\rho\pi S(z)^2dz$，**积分的上限是 $z$ 的函数**。**参数化必须先定死：以顶点为原点、$z$ 从顶点量起时，圆锥 $S(z)=rz/h$**；$S=r(1-z/h)$ 是 $z$ 从底面量起的写法。

**坑三（agent 犯过，连带后两项全错）**：把 $S=r(1-z/h)$ 配上「$z$ 从顶点量」。圆锥上 $\int S^4dz$ 在两种参数化下恰好同值，所以 $I_{zz}=\frac{3}{10}Mr^2$ 侥幸仍然正确；但 $\int zS^2dz$、$\int z^2S^2dz$ 全错——曾据此把 $\int z^2dm$ 报成 $Mh^2/10$（正确 $3Mh^2/5$）、把质心报成距顶点 $h/4$（正确 $3h/4$），并给出错的 $I_{xx}$。

**坑一（agent 犯过）**：把 $I_{zz}$ 写成 $\rho\pi\int S^4dz$ 会漏掉圆盘的 $\frac12$（$\int_{\text{disk}}s^2dA=\frac{\pi S^4}{2}$，不是 $\pi S^4$）。漏了得 $\frac35Mr^2$，正确是 $\frac{3}{10}Mr^2$。
**坑二（agent 犯过）**：圆锥质心在**距顶点 $3h/4$**（距底面 $h/4$），不是距顶点 $h/4$。自检恒等式：$\int z^2dm=\int(z-z_c)^2dm+Mz_c^2\ge Mz_c^2$——用 $3Mh^2/5\ge M(3h/4)^2=9Mh^2/16$ 对，用早先的 $Mh^2/10$ 立刻自相矛盾，这条恒等式就是抓这个错的工具。

## 已核数值（圆锥：质量 $M$、底半径 $r$、高 $h$，$z$ 自顶点量起）

- $I_{zz}$（绕对称轴）$=\frac{3}{10}Mr^2$，**与参考点无关**：这条轴穿质心，顶点与重心在同一条线上，平行轴位移为零。
- 质心 $z_c=3h/4$（距顶点），$\int z\,dm=3Mh/4$；$\int z^2dm=3Mh^2/5$。
- 快捷式：$\int y^2dm=\frac12\int(x^2+y^2)dm=\frac12I_{zz}=\frac{3}{20}Mr^2$（不必逐片切）。
- $I_{xx}$（顶点为参考点、垂直于对称轴）$=M\big(\frac{3r^2}{20}+\frac{3h^2}{5}\big)$。**这个值经用户本人独立算出并被确认过**（他交的矩阵前两项），不要再报 $h^2/10$。
- 绕质心的垂直轴 $=M\big(\frac{3r^2}{20}+\frac{3h^2}{80}\big)$（由上一行平移 $(3h/4)^2$ 得到，与教科书标准值一致）。早期版本里 $h^2/10$ 与 $h/4$ 两个错恰好抵消得到同一个终值——**终值对不代表中间量对**。
- 平行轴定理的讲义形式（§7.3.2 性质 3）：$I^Q_{ij}=I^C_{ij}+M(\delta_{ij}\sum a_k^2-a_ia_j)$，$\mathbf a$＝质心相对参考点 $Q$。
- 题面"绕顶点转动"没指明是哪条轴：按"绕通过顶点的轴、垂直于对称轴"读，并在答疑里说明这个读法。

## Q2 交付形态与他的代换错误

他把 $\operatorname{diag}\big(\frac{3h^2}{5\pi}+\frac{3r^2}{20\pi},\ \frac{3h^2}{5\pi}+\frac{3r^2}{20\pi},\ \frac{3r^2}{10\pi}\big)M$ 拍照发来：**三个系数全对，分母各多一个 $\pi$**。诊断口径：$I$ 量纲 $M\cdot$长度$^2$，$\pi$ 无存身之地；$M=\rho\pi r^2h/3$ ⇒ $\rho\pi r^2h=3M$，$\pi$ 恰好抵消，错在他最后一步把 $\rho$ 换成 $M$ 时多除了一次。

## Q3（欧拉陀螺）从零讲的顺序

他明确要求「从头开始讲」，并斥「上来给我扔一堆术语鬼看得懂」。有效顺序：

1. 刚体只需两件事：**朝哪**（三个欧拉角）、**怎么转**（角速度）。
2. 三个角的变化率 → $\boldsymbol\omega$ 在体坐标的分量，这是**运动学方程**，只记帐、不含力（讲义式 7.6）：$\omega_1=\dot\varphi\sin\theta\sin\psi+\dot\theta\cos\psi$、$\omega_2=\dot\varphi\sin\theta\cos\psi-\dot\theta\sin\psi$、$\omega_3=\dot\varphi\cos\theta+\dot\psi$。
3. **动力学方程**的来源一句话：$\vec L$ 在实验室系满足 $d\vec L/dt=\tau$，而 $\mathbf I$ 是体坐标里的常矩阵，所以把导数拆成 $(d\vec L/dt)_{\rm lab}=(d\vec L/dt)_{\rm body}+\boldsymbol\omega\times\vec L$。自由刚体：$\mathbf I\dot{\boldsymbol\omega}+\boldsymbol\omega\times(\mathbf I\boldsymbol\omega)=0$，三个分量式就是欧拉方程。
4. 欧拉陀螺 = 无力矩 + $I_1=I_2$；命名来自 Euler 1765。第三式 $I_3\dot\omega_3=0$ 直接给 $\omega_3=$ 常数，剩下两式是 $(\omega_1,\omega_2)$ 匀速圆周。
5. 给四条可用关系让他自己拼 $\dot\theta=0$：$\omega_3$ 常数；$L\cos\theta=I_3\omega_3$；$L^2=I_1^2(\omega_1^2+\omega_2^2)+(I_3\omega_3)^2$；$\omega_3=\dot\varphi\cos\theta+\dot\psi$。
6. **(a) 三式收尾的写法（已讲透并核过）**：不要解三个非线性方程。链条是——轴对称灭掉 $\boldsymbol\omega\times\vec L$ 的第三分量（$\omega_1L_2-\omega_2L_1=I_1\omega_1\omega_2-I_1\omega_2\omega_1=0$）⇒ $\omega_3$ 常数；再把 $L\cos\theta=I_3\omega_3$ 两边都当常数 ⇒ $\dot\theta=0$（用的是“$\mathbf L$ 守恒 + $\omega_3$ 守恒”，不是任何方程的积分）；$L^2$ 守恒减去 $I_3^2\omega_3^2=L^2\cos^2\theta$ 得 $\omega_1^2+\omega_2^2=L^2\sin^2\theta/I_1^2$，与运动学前两式平方和 $\dot\varphi^2\sin^2\theta+\dot\theta^2$ 对齐 ⇒ $\dot\varphi=L/I_1$；最后 $\dot\psi=\omega_3-\dot\varphi\cos\theta_0=L\cos\theta_0(1/I_3-1/I_1)$。每步都要点明“哪条守恒在起作用”。物理解读：$\dot\varphi$ 只由横向惯量 $I_1$ 决定；$\dot\psi$ 是“自转扣掉被带着转的那份”。
7. **(b) 的已核结果**：$\boldsymbol\omega$ 沿 $\mathbf L$ 的分量 $=\frac{L\sin^2\theta_0}{I_1}+\frac{L\cos^2\theta_0}{I_3}$（常数，由 $\mathbf L\cdot\boldsymbol\omega$ 直接得）；横向振幅 $=|\dot\psi|\sin\theta_0=L\sin\theta_0\cos\theta_0(1/I_1-1/I_3)$，绕 $\mathbf L$ 以 $\dot\varphi=L/I_1$ 匀速转。核对：振幅平方 $=L^2\sin^2\theta_0\cos^2\theta_0(1/I_1-1/I_3)^2$ 与 $\omega^2-(\omega_{z'})^2$ 一致。讲的时候先只要沿 $\mathbf L$ 那一个分量（一次点乘），把振幅留给他在后面验算。
8. **讲义 §7.4.3 用的是 $\Omega=(I_3-I_1)\omega_{z0}/I_1$ 与 $\omega_{z0}$，题面要求用 $I_1,I_3,L,\theta_0$**：先换 $\omega_{z0}=L\cos\theta_0/I_3$、$\Omega=L\cos\theta_0(1/I_1-1/I_3)=-\dot\psi$，再对齐式 7.96 的分量形式（其中 $\dot\varphi=(\omega_{z0}+\Omega)\sec\theta_0=L/I_1$）。不许直接抄 7.96。
9. 两个圆锥的方向判据（已核）：$\cos\theta>0$ 时 $\dot\psi$ 与 $\dot\varphi$ 同号 ⟺ $I_3<I_1$；符号决定本体圆锥与空间圆锥同向还是反向滚动。守恒的是 $\mathbf L$ 的方向而不是 $\boldsymbol\omega$ 的方向——这句要当面说，否则“陀螺绕固定轴转”会被当成前提。

## K/E 两组推导的交付标准（被用户要求重写过一次）

用户评语是「写得不清楚，没完全看懂」。病因全在同一类省略上，重写时必须避免：

- **不许用「取 $A$ 的第 $j$ 列」代替计算**。先讲清读法（$x=Ax'$，把 $x'$ 取成第 $j$ 个单位向量，乘出来就是第 $j$ 列），再把矩阵乘法逐行做出来：$A_\varphi(0,0,1)=(0,0,1)$、$A_\theta$ 给 $(0,\sin\theta,\cos\theta)$、$A_\psi$ 给出 $(\sin\theta\sin\psi,\ \sin\theta\cos\psi,\ \cos\theta)$。节点线同理，关键是 $A_\varphi(\cos\varphi,\sin\varphi,0)=(1,0,0)$——节点线正是 $A_\varphi$ 的转轴，转过之后它自己成了 $x$ 轴。
- **「三个角速度可加」要给两条理由**：$\dot A$ 关于 $(\dot\varphi,\dot\theta,\dot\psi)$ 线性，故 $\dot AA^{-1}$ 是三项反对称矩阵之和；无限小转动在一阶可交换。只说「矢量可加」会被追问。
- **系数按一般式写**。欧拉方程第一式是 $I_1\dot\omega_1+(I_3-I_2)\omega_2\omega_3=0$。曾写成 $(I_3-I_1)$——那是 $I_1=I_2$ 代入后的样子——且没说明，直接导致重写。凡已代入对称性，当场写明「此处已用 $I_1=I_2$」。
- $\boldsymbol\omega\times\mathbf L$ 的三个分量要逐项代 $L_i=I_i\omega_i$，不要只给结果；$\mathbf Q$ 在两个系里求导差一项的证明 $\dot{\hat e}_i=\boldsymbol\omega\times\hat e_i$ 也写出来，只有一行。
- 运动学方程的平方和自检 $\omega_1^2+\omega_2^2=\dot\varphi^2\sin^2\theta+\dot\theta^2$ 一并给出：后文 (a) 要用，也是符号抄错的探测器（$\psi$ 反号则交叉项不抵消）。

## 三个欧拉角各自的转轴（「前面没绕明白」的就是这里）

不要按「先绕某轴转 φ，再绕某轴转 θ」罗列成约定。先问每个角**负责改变什么、必须保持什么不变**，转轴就唯一确定了：

- $\psi$：不改对称轴 $e_3$ 的指向 ⇒ 轴 $=e_3$（体坐标第三基矢）。
- $\varphi$：只改 $e_3$ 绕 $z'$ 的方位、保持夹角 $\theta$ ⇒ 轴 $=z'$（实验室轴）。
- $\theta$：只改夹角 ⇒ $e_3$ 端点的速度落在 $e_3,z'$ 张成的平面内且垂直于 $e_3$ ⇒ 转轴垂直于该平面，即公垂线（节点线）。**节点线既不在实验室系也不在体坐标**，是随 $\varphi$ 一起转的中间轴；这一点讲不通，后面 K 组就是三个背不下来的式子。

随后给可观察图像与辨别判据：自转＝轴上标记绕轴转、轴不动；进动＝轴扫圆锥、张角不变；章动＝轴上下点头、张角在变。合起来：欧拉陀螺的解是 $\dot\theta=0$ 而 $\dot\varphi,\dot\psi\ne0$，所以看到的是自转加进动，陀螺的「摇晃」来自进动节拍而不是点头。日常例（桌面陀螺、地球岁差与章动）必须标明有力矩、不是欧拉陀螺。用户在此轮之后明确说「欧拉的部分我理解了」，这套讲法有效，别再改回先给矩阵的做法。

## Q4（选做：$z'$ 任取的欧拉陀螺）已核要点

用户听完它与 Q3 的差别后选择跳过（理由是省时间），所以这里只沉结论，不再主动展开：

- **两题的唯一差别是极轴怎么选**。动力学（E 组）住在体坐标里，与 $z'$ 无关，$\omega_1=\Omega$ 型匀速旋转的解两题共用；不同的只有「$\omega$ 反解成欧拉角」这一步，而 K 组的反解依赖 $z'$。
- 设 $\mathbf L$ 与 $z'$ 夹角为 $\alpha$（常数，由初值定），对称轴 $e_3$ 仍绕 $\mathbf L$ 以 $\dot\varphi_{\mathbf L}=L/I_1$ 进动、张角 $\theta_0$ 不变，则在 $z'$ 系里
  $\cos\theta(t)=\cos\alpha\cos\theta_0+\sin\alpha\sin\theta_0\cos(\omega_p t)$，$\omega_p=L/I_1$，于是 $|\alpha-\theta_0|\le\theta\le\alpha+\theta_0$：**θ 开始摆动 = 章动**。$\alpha=0$ 退回 Q3（$\cos\theta=\cos\theta_0$ 常数），可作检验。
- 方位角不再匀速：取 $z'$ 在 $\mathbf L$ 系为 $(\sin\alpha,0,\cos\alpha)$，则 $e_3\cdot\hat x'=\sin\theta_0\cos(\omega_p t)\cos\alpha-\cos\theta_0\sin\alpha$、$e_3\cdot\hat y'=\sin\theta_0\sin(\omega_p t)$，$\varphi=\operatorname{atan2}$ 这两式，$\dot\varphi$ 随时间变。
- 收尾用 K 组第三式：$\dot\psi=\omega_{30}-\dot\varphi\cos\theta$，把上面求导的结果代进去再积一次。
- **概念点（要当面说）**：$\dot\theta=0$ 是坐标选择的产物，不是内禀性质；教科书里「有章动的陀螺」指重力陀螺（$\mathbf L$ 不守恒），与这里的「换极轴看出来的摆动」不是一回事。

## 讲义页

§7.3.1 pp.145–151（式 7.13–7.17：7.14 分量定义、7.17 的 $I_{xx}$）、§7.3.2 p.151（对称性/广延性/平行轴定理）、§7.3.4 pp.152–（惯量主轴）、§7.4 pp.156–（欧拉动力学方程；对称欧拉陀螺 §7.4.3）。**欧拉角（§7.2）课堂上是否已讲未确认——讲 hw8 Q3 前先确认，或按讲义现场补。**

# review-progress-current（自 SKILL.md 搬家，原文零删改）

## 复习进度

逐段日志在 `references/review-progress.md`（**个人学习记录，不随技能发布**）。本文件只保留「讲到哪算学过」的地图与教法。

**当前站位（2026-10-22 末）**：相似分类五站走完；随后他那串上位追问（要不要等模论、课纲里到底有没有模论）已全部答完并纠正到位（$\mathbb Z$ 无挠不是「有限 vs 无限」、域上配对非退化不是「维数之和」、结构定理假设是**有限生成**而不是有限；往届两份讲义都无模论章）——全文见 `references/similarity-canonical-forms.md` 末节。
**已转入笔记 11（今年讲义 §1.5 半双线性型与 Hermite 型）**：动机（共轭是 $|\lambda|^2$ 的齐次性逼出来的）与 Hermite 对称的作用已讲；$\varphi(x,y)=\bar x_1y_1+i\bar x_1y_2+i\bar x_2y_1+\bar x_2y_2$ 那题他先判错（只认矩阵、把 Hermite 当自动成立），判据纠正后改对；之后讲了 §3 命题（$\perp$ 对称 $\iff\varphi=\lambda\psi$）与极化恒等式（复数四项 vs 实数两项，多出的两项是在钓虚部）。
正交补两题**都答错**：$h=|x_1|^2-|x_2|^2$、$u=(1,1)$ 时他说正交补是「$x+y=1$，两边垂直」（答成不过原点的仿射超平面），真解 $V^\perp=V$；换 $u=(1,0)$ 他又说「还是重合」，真解是第二条坐标轴、两者互补。**当前站位**：等他消化这两题的判据（迷向 $\iff$ 落在自己正交补里，非迷向时互补），下一步他说走 signature 与惯性律，或先补 Hermite 矩阵分解 $\mathcal M_n=\mathcal H_n\oplus i\mathcal H_n$。教法、题与坑见 `references/sesquilinear-forms-and-adjoints.md`。
已答对：整除链 ↔ Frobenius、素幂 ↔ Jordan；$\mathbb{R}^4$ 上双旋转的不变因子 $(X^2+1,\,X^2+1)$；$\operatorname{diag}(R,1)$ 只有一个不变因子 $(X^2+1)(X-1)$（互素合并）；$\mathbb{C}$ 上 $\lambda$ 两块加 $\mu$ 一块的不变因子 $(X-\lambda)^2(X-\mu)^3$ 与 $(X-\lambda)$（第一答错成三个初等因子，靠整除链与行数两条判据改正）。
**下一步可选**：Frobenius 存在性与唯一性的证明（笔记 09 约 227–254 行）、$\operatorname{Com}(u)=K[u]$（笔记 10 §1）、双换位子定理。有限阿贝尔群按**已掌握**处理，只当接口引用。


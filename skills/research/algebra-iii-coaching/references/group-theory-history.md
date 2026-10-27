# 群论史：已核实的脉络、讲法与出处

**用途**：用户要「好好讲讲数学史」时照它讲（配合 `math-coach` 模式 A；本技能 SKILL.md 的「讲数学史」节是铁律）。
内容已落进 vault 的 `数学/代数/代数III/概念/群论的目的与历史.md`（§2 年表 + §4 术语来历），**先读 vault 再讲，别重复调研**。

## 时间线（均已核实，可直接引用）

| 年代 | 人 | 做了什么 / 卡在哪 |
|---|---|---|
| 1545 | Cardano, Ferrari | 三次、四次有公式 ⇒ 五次看似只差一点 |
| 1770–71 | Lagrange | **预解式**把 2/3/4 次解法统一成一个原理；五次失败（辅助方程次数更高）。贡献是「把能否解变成根间关系的结构问题」；预解式取值计数 = 后来轨道/稳定子的史前史 |
| 1799 | Ruffini | 宣称五次不可能，论证有漏洞 |
| 1824 | Abel | 第一个正确证明（仍无「群」概念，只有「置换的集合与复合」） |
| 1830–32 | Galois | 引入 *groupe*；可解性 ⇔ 一串分解、每层左右陪集重合（*propre*）；1832-05-29 决斗前夜通宵写成致 Chevalier 的信（**那封信里就写着 propre 的条件**），5·30 中弹、5·31 去世，20 岁 |
| 1842/43→1846 | Liouville | 1842–43 开始读遗稿、1843 承认其价值，1846 才发表。史评：他看清了与 Cauchy 置换论的联系，**却没抓住「群」这个概念才是要害** |
| 1844–46 | Cauchy | 置换群的系统工作（循环分解、阶）；已证「$p\mid|G|$ ⇒ 有 $p$ 阶元」（Sylow 第一定理的雏形）。讽刺：当年退稿的人里就有他 |
| 1851 | Betti | 第一个证明 Galois 配的那个东西确实是现代意义的置换群 |
| 1854 | Cayley | 第一个抽象群定义（*θⁿ=1* 那篇）—— 当时几乎无人响应 |
| 1862 / 1872 | Sylow | 三条定理 1862 代课时想通、**压了十年**，1872 才发表（*Math. Ann.* 5, 584–594，十页）；同年 Jordan 访 Christiania，Lie 拉两人散步，Jordan **从 Sylow 本人口中第一次听到**，先惊讶怀疑、后热情传播。中学教师四十年 |
| 1869 / 1870 | Jordan | 《Commentaires sur Galois》(*Math. Ann.* 1869)、《Traitié des substitutions…》(1870)：第一本系统教科书 |
| 1872 | Klein | Erlanger Programm：几何 = 变换群下的不变量 |
| 1882 | von Dyck | 现代意义的抽象群定义（生成元与关系） |
| 1880s–90s | Dedekind, Weber, Hölder | 商群、合成列（Hölder 1889 定成今天的形式，即 Jordan–Hölder）、*Normalteiler*（**首用者未查实**）；德文教科书定型术语 |
| 1897 | Burnside, Frobenius | 《Theory of Groups of Finite Order》；有限群论与特征标 |
| 1896–1904 | Frobenius, Burnside, Schur | **表示论**诞生：Frobenius 自 1896 起造特征标（en-wiki《Character theory》措辞：他「initially developed representation theory of finite groups」）；Burnside 1904 得 $p^aq^b$ 可解 |
| 1928 | Philip Hall | Sylow 定理的系统推广（有限可解群） |
| 1955–2004 | 多人 | **有限单群分类**：Feit–Thompson 1963（奇数阶群可解）→ 1972 Gorenstein 十六步纲领 → 1973 预测 Monster、1982 Griess 造出（196883）→ 1983 宣布完成**过早**（quasithin 误报）→ 2004 Aschbacher–Smith 补 1221 页收口 ⇒ 循环群 / 交错群 / Lie 型 18 个无限族 / 26 个零星群 |
| 2012 | Gonthier 等 | 用 Coq 形式化 Feit–Thompson 定理 |

## 三支来源 + 一次合流（他混过一次，重点讲）

- **三支**（1870 年前后彼此撞车，才逼出「统一语言」的需求）：① **方程/置换**（Lagrange → Galois → Cauchy → Jordan）；
  ② **几何/变换群**（Klein 1872 Erlanger Programm、Lie 的连续群）；③ **数论**（Euler 的模运算 → Gauss 的二次型合成与分圆 → Dedekind/Kronecker）。
- **置换群不是与解方程并列的独立来源** —— 它就是从解方程问题里长出来的（Lagrange 起）。
- 真正与方程无关的是**数论**那一支：Euler 的模运算 → Gauss 的二次型合成与分圆（那里没有置换，也在产生群）。
- 三支到抽象群（Cayley 1854 写下 / von Dyck 1882 定型）才合流。
- 问「研究置换群是顺着 Lagrange 的方向吗」⇒ **分目标与方法答**：目标（解方程）到 Cauchy 就不再是；
  方法（对预解式取值作计数）Lagrange 创立、Ruffini/Abel 沿用、**Galois 换轨**（改看群自身能否分解）、Cauchy 之后换成循环分解/子群/共轭/阶。
- 问「联系是后人读了 Galois 才发现吗」⇒ 不是：联系是 **Galois 自己写下的**（可解 ⇔ 群可分解），Lagrange 的预解式计数已是雏形；后人做的是**读懂并接受**。
- 问「有人把置换的**复合当作乘法**吗？『运算』怎么被推广的」（2026-10-04 追问，已答，全文在 vault §2 的「补问」框里）：
  - 复合从 Lagrange 起就在用；Ruffini 造出「阶 / 共轭 / 轮换分解」；Cauchy 的**两行记号**让复合可算；
    Galois 用**并列**写乘积集合（$HS$）、用 $+$ 写并集；**Cayley 1854 才完整地用「乘积 / 相乘」**（原文 *the product of any two …*、*the group is multiplied by …*）。
    **为什么叫乘法**：保住了结合律、丢掉交换律 —— Cayley 原话 *not in general convertible, but are associative*；「乘」这个字就是「结合但不必交换」的暗号。
  - **「运算」四级推广**：置换（Galois/Cauchy）→ **任意符号**（Cayley 1854：可作用于一个量或一组量，置换只是特例，也可以是普通函数符号）
    → 变换 / 连续变换（Klein 1872 / Lie）→ 「**随便怎样定义的运算**」（von Dyck 1882，只留关系法则 $F_\nu(A)=1$）。
    现代再进一步：运算 = 集合上的映射 $G\times G\to G$（法语 *loi de composition interne*）；再抽象就是范畴里的「群对象」。
  - `[未查实]`「谁第一个写下 *produit de deux substitutions*」没找到坐实材料 —— 讲时明说没查到，别替他猜。

## 术语来历（配合 vault §4 讲）

- 陪集：Galois 只有记号、**没给名字**；英语 `co-set` 首见于 **G. A. Miller, 1910**（*Quart. J. Pure Appl. Math.* 41, p. 382）；
  此前叫 *Nebengruppe*（Weber）、*conjugate group*（Burnside）。
- 法语 normal / distingué / invariant 三者同义；**英语 distinguished subgroup ≠ 正规子群**（那是严格特征子群）。
- `[未查实]` 德语 *Normalteiler* 首用者：常归于 Dedekind–Weber 一代；查证线索 = Wussing《The Genesis of the Abstract Group Concept》p. 115/305、J. J. Nicholson 博士论文《Otto Hölder and the Development of Group Theory and Galois Theory》(Oxford, 1993)。

## `[未查实]` 清单（讲前先看，别重复调研）

- 德语 *Normalteiler* 首用者（线索见上「术语来历」）。
- 「谁第一个写下 *produit de deux substitutions*」。
- **表示论的第一批动机**：常见说法是 Dedekind 1896 前后就「群行列式」写信给 Frobenius、由此引出特征标 ——
  **本次查了 en-wiki 的 Frobenius 传、《Representation theory》《Character theory》《Group determinant》
  以及 Wikipedia 搜索 API，均未见此信**。别当史实讲；非讲不可就标「未坐实」。
  可继续查的方向：Wussing《The Genesis of the Abstract Group Concept》原文、Frobenius 1896 年的论文本身。

## 出处（重核时直接用，已实测可直连）

- MacTutor：`https://mathshistory.st-andrews.ac.uk/HistTopics/Development_group_theory/`；`…/Biographies/{Dedekind,Holder,Sylow}/`
- en.wikipedia：`Normal_subgroup`、`Coset`、`History_of_group_theory`、`Évariste_Galois`、`Joseph-Louis_Lagrange`、`Arthur_Cayley`、`Peter_Ludwig_Mejdell_Sylow`
- fr.wikipedia：`Sous-groupe_distingué`（引 Galois 1832 信原文 + Wussing 页码）、`Théorie_de_Galois`（引 Jordan 1869/1870）
- de.wikipedia：`Normalteiler`

## 最早的定义长什么样（他问过「群最开始的定义是怎么样的」）

- **Galois（1830s）没有给定义** —— 他只是第一次把 *groupe* 当技术词用（史家措辞是「近似于」今天的用法）。讲史时别把公理硬塞回他嘴里。
- **Cayley 1854** 是「第一个抽象**（有限）群**的定义」——一篇 8 页文章，关键点：不再预设元素是变换；标题还带着出身
  （*as depending on the symbolic equation θⁿ = 1*，从「幂与周期」那条路出来）。**当时几乎无人采用：不是被反驳，是被无视。**
- **von Dyck 1882** 才是「第一个给**抽象群**公理化定义」的人（en-wiki *Group (mathematics)* 与 fr-wiki 均如此措辞），
  并首次系统使用**生成元与关系**（《Gruppentheoretische Studien》, *Math. Ann.* 20, 1–44）。公理化的意义点给它：
  **「元素是什么」不再是群的一部分** ⇒ 群成为自足的形式对象，才能同时装下置换、变换、数论里的东西。
- 定型靠教科书一代（Weber《Lehrbuch der Algebra》1895/96、Burnside 1897）。
- 两个常被忽略的精确点（他喜欢这种）：现代三条公理（结合、单位、逆；封闭并入「二元运算」）里，
  **单位与逆的唯一性是推论而非公理**；整套公理可弱化为「左单位 + 左逆」而不损失任何东西。
- **讲法**：这一幕的主线是「**需求先到、定义后到**」——先有 Cayley 1854 的定义无人用，再有 1870 前后三支撞车把抽象需求顶出来，
  von Dyck 1882 才被接受（滞后 28 年，全程最长）。

## 两份原始定义（他追问过「Cayley 和 von Dyck 具体是怎么定义的」，直接引这两段）

**Cayley 1854**（*Philosophical Magazine* vii, 40–47；原文获取：archive.org `collectedmathema02cayluoft`
＝《Collected Mathematical Papers》卷 II 第 125 篇，下 `*_djvu.txt` 后 grep 论文标题定位）：
- 框架：符号是**运算**；正文写道这些符号 "is not in general **convertible**, but are **associative**"（不交换、但结合），
  并要求 $\theta^n=1$ 与指数律（= 标题所说的 symbolic equation）。
- 定义原句：*"A set of symbols $1,\alpha,\beta,\ldots$, all of them different, and such that **the product of any two of them
  (no matter in what order), or the product of any one of them into itself, belongs to the set, is said to be a group**."*
- 要点：**只要封闭**（含单位符号 $1$，"no matter in what order" 指两个顺序都行、不是说交换）；
  **无逆公理** —— 逆是从「有限 + 封闭」推出来的，依据是紧接着的 "…the effect is simply to **reproduce the group**"
  （左乘是集合上的双射）。所以他的群天生**有限**；而且符号虽不要求是置换，仍被理解为**运算**（抽象得不彻底）。

**von Dyck 1882**（《Gruppentheoretische Studien》, *Math. Ann.* 20, 1–44；archive.org `sim_mathematische-annalen_1882_20`）：
- 篇首把 Cayley 的话当**题记**：*"A group is defined by means of the laws of combination of its symbols."*
- 纲领：定义「离散运算的群」，但**抽掉各运算的具体表示形式**，只按「构成群所需要的本质性质」给出。
- 做法：从**生成运算** $A_1,A_2,\ldots$ 出发（对其特殊性质不作任何假设），把生成元之间的关系写成 $F_\nu(A)=1$
  ⇒ 「生成元 + 关系」；并点明这是**遵守结合律、不遵守交换律**的乘法运算。
- 关键句（大意）：「所有同构的群被并成一个群；群的本质不再由运算的具体表示形式表达，而只在于它们彼此的关系」
  —— 这就是抽象群的公理化定义方式。
- **一句话对比**（讲时用）：Cayley = 「一个封闭的符号集合」（核心=封闭，已抽象但还挂在「运算」直觉上）；
  von Dyck = 「由生成元与关系给出的形式对象」（核心=关系法则，「元素是什么」被赶出定义）。课本那个形状从后者开始。

## 剩余技术债（下次接）

- 第 3 幕（抽象化）已在对话里讲完（Cayley 1854 / von Dyck 1882 / Klein 1872 / Dedekind–Weber–Hölder / Burnside 1897），要点即上文。
- **第 4 幕（20 世纪）已在对话里讲完**，内容即上表末四行。主线一句话：**群论先被搬进线性代数（表示论），
  再被搬到「生成元与关系」上（组合群论：Dehn 1911 词问题 / Nielsen–Schreier / Coxeter），最后走向「把所有有限单群列完」。**
  另点群论走出代数：Poincaré 1895 基本群、晶体学空间群、Weyl 量子力学。落点正好接他课程后半
  （$GL_n/SL_n/PSL_n$、Jordan/Frobenius 标准型）。
- 讲这一幕时他反问「线性空间本来就自带 $GL(V)$，那还研究什么」⇒ 答法见本技能 SKILL.md 混淆点第 11 条（先拆对象与主语）。

## 史线收尾：他最后两个「表述层」问题（第 0–4 幕已讲完）

讲完第 4 幕后他不再追史，转而连问两个**表述/语言层**问题 —— 都属于「当时没有 X，怎么做 Y」这一型：

1. **「向量空间还没有明确定义的时候是怎么有线性代数的」**
   - 一句话：**先有一堆具体计算，抽象空间是最后才配上的容器**。史书原话（en-wiki《Linear algebra》，可直接引）：
     「the leading mathematicians of the nineteenth and early twentieth centuries developed and used most of the basic
     results and techniques of linear algebra **for perhaps a hundred years, without even defining an abstract vector space:
     nor is there anything to suggest they suffered thereby.**」
   - 四段家谱（每段的对象都不是「空间」）：① 解方程组与行列式 —— 《九章算术》第八章「方程」已有消元（18 题、2–5 元）、
     Leibniz 1693 系统的行列式解法、Cramer 1750 显式解、Gauss 在测地学里给出消元；② 坐标化 + 二次型 —— Descartes/Fermat 1636、
     Gauss 1801 已在「用可逆线性变换化简」；③ 矩阵与标准型 —— **Cayley 1856** 定义矩阵乘法与逆（并把矩阵当成一个对象、用一个字母写，
     en-wiki 说这一步使**一般线性群**成为可能）、Jordan 标准型 1870；④ 抽象化 —— **Peano 1888** 给出第一个现代而精确的向量空间定义、
     1900 才有「有限维向量空间的线性变换理论」、20 世纪上半叶现代化。超前支线：**Grassmann 1844《扩张论》**已写出「抽象对象 + 运算 +
     线性无关 + 维数」，当时无人响应。
   - 三句「为什么没有定义也能做」：定理只要「数表/变换」这个具体对象就能陈述与证明；换基/化简/等价本来就有操作意义（换变量、换坐标）；
     抽象定义不是许可，是把已在做的事**收进同一个容器** —— 公理化之后反而更强（无限维、函数空间、线性映射不必来自矩阵）。
2. **「Jordan 标准型这么依赖线性映射，当年的证明是纯矩阵语言写的吗」**
   - 答：**两种都不是**。1870 年代主要用**「线性替换」substitution linéaire** 的语言（Jordan 书名 *Traité des* ***substitutions***；
     对象是「用新变量替换旧变量」，账本是行列式与初等因子），另有**型/双线性型**那一路（Weierstrass 1868、Kronecker）；
     矩阵记号 1856 才有（Cayley）、1870s 远非主流。
   - 今天课本那套（线性算子、不变子空间、$\ker(A-\lambda I)^j$、循环子空间、$V$ 视作 $K[X]$-模 + PID 上有限生成模结构定理）
     是 **20 世纪的重述**，好处是能推到更一般的系数环、证明更短（en-wiki *Jordan normal form* 措辞：
     「named after Camille Jordan, **who first stated the Jordan decomposition theorem in 1870**」；现代表述用 *cyclic subspaces* / module 语言）。
     当年的证明同样严格，只是读起来像代数计算而不像几何。
   - **要点（易被他追问）**：「依赖线性映射」是我们语言的错觉 —— 真正依赖的是**线性结构**，同一件事用「替换 / 型 / 矩阵 / 模」四种语言都能说。

**落盘**：两问的答案都进了 vault 的 `数学/代数/代数III/概念/群论的目的与历史.md`（「概念出场顺序」节，含史书原话与标准型语言史）。
**讲法**：先给一句结论 + 史书/原文引语，再摆语言谱，最后点破「语言错觉」—— 别写成教科书式的历史介绍。
- 收尾时留给他、他**未答**的问题：Galois 那种「只有用法、没有定义」的状态，是历史的遗憾，
  还是概念得以活下来的必要条件 —— 放到表示论/单群那一幕回收。
- **调研坑（检索词 vs 条目页）**：查具体史实要**直奔条目页 / 具体人名 / 具体论文名**。用 Wikipedia 搜索 API 拿
  「Dedekind letter Frobenius 1896 group determinant」这类泛检索词，返回的全是无关条目 ——
  那只说明检索词选得不好，**不能据此下「查不到」的结论**；换成具体条目名（人名、论文名、`Group determinant`）再试。
- **调研坑**：MacTutor 改版后旧 URL 会 404（`HistTopics/Abstract_group_concept/` 实测 Page Not Found）；
  需要的一手叙述多在 `HistTopics/Development_group_theory/` 与各 `Biographies/*` 页，
  en-wiki《Group (mathematics)》《History of group theory》可替代。旧 URL 404 只说明页面搬了，不代表内容不存在。

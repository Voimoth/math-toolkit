# 表示论史：Schur–Weyl / Hecke / 量子群 / 范畴化

讲义对应 Rosso 报告 `Interplays between symmetric groups and general linear groups: from classical to
quantum, with a view towards categorification`（vault `代数III/笔记/讲座/`）。讲者要的是「讲座为什么长这样」，
所以史线按**标题的三个词**（classical / quantum / categorification）排成六幕。以下事实均已核（来源标在各条），
标了 **[未查实]** 的不要当史实讲。

## 六幕骨架

### 一｜1890：不变量论「算不出来」
- 不变量论的纲领是**给出显式生成元**（Gordan 是硬算派，被称为 the king of invariant theory）；
  Hilbert 1890 用非构造的存在性论证（基定理）终结了这个纲领。
- Gordan 的名言「Das ist nicht Mathematik, das ist Theologie」**归属不可靠**：最早的书面出处晚于事件约 25 年、
  且在 Gordan 去世之后；是否真说过、是批评还是惊叹都没有定论（en-wiki *Paul Gordan* 条目据 McLarty 的考证如此标注）。
  他后来又说「I have convinced myself that even theology has its merits」，并在 1899 年给了简化证明
  （Gordan, *Neuer Beweis des Hilbertschen Satzes über homogene Funktionen*, Göttingen Nachrichten 1899, 240–242）。
  **讲这一幕时必须把这条引文的不可靠性说出来**——它是最常被引也最不可靠的数学名言之一，正好示范「史实先核」。
- 对本讲座的意义：显式计算那条路没人走了；后来救它的不是算得更狠，是把对称性做成代数。

### 二｜1896–1901：Frobenius 造特征标
- 起点是**群行列式** $
  \det(\sum a_g g)$ 该分解成什么（Dedekind 1885 的论文与 1896 年给 Frobenius 的信）。
- 时间线（MacTutor *Frobenius* 传记）：1896 年 7 月 16 日向柏林科学院提交群特征标论文（引言原话：
  「I shall develop the concept [of character for arbitrary finite groups] here in the belief that through its
  introduction, group theory will be substantially enriched.」）；致 Dedekind 的第一封信 1896 年 4 月 12 日；
  1897–1899 连发（诱导特征标、特征标的张量积；1898 引入诱导表示与 Frobenius 互反）；
  **1900 完全定出 $\mathfrak{S}_n$ 的特征标，1901 做 $A_n$**。
- 人物反差可用：Frobenius 是柏林老派，厌恶 Göttingen 的新风格（1896 年 2 月 3 日致 Hurwitz 的信里在骂），
  结果他发明的特征标成了 20 世纪最「新」的工具。
- 为什么 $\mathfrak{S}_n$ 是硬骨头：$n!$ 个元素，共轭类对应分拆 ⇒ 答案只能用分拆/Young 图写。
  **这解释了「不可约表示由分拆标号」为什么在讲座里出现得那么自然——它 1900 年就是答案，不是后补的。**

### 三｜1901：Schur 从另一头撞上同一批函数
- Schur 是 **Frobenius 1901 年的博士生**（导师还有 Fuchs，summa cum laude）。论文
  *Über eine Klasse von Matrizen, die sich einer gegebenen Matrix zuordnen lassen*（Dissertation, Berlin 1901）。
- **问法变了**：不问「群 $G$ 的表示」，而问「与一个给定矩阵（一个线性变换）交换的矩阵代数是什么」——中心化子。
  得到：$\mathrm{GL}_n$ 的多项式表示完全可约；不可约的由分拆标号；特征标在对角矩阵上就是后来的 Schur 函数。
- 1927 年他又写 *Über die rationalen Darstellungen der allgemeinen linearen Gruppe*
  （Sitzungsber. Akad. Berlin 1927, 58–75）重新证明 1901 的主要结果 ⇒ 1901 那篇当时不好读。
  Green 的评语（en-wiki *Issai Schur* 引）："very original ideas, developed with superb algebraic skill"。
- 于是 1901 年出现「两头得同一批函数」的局面：Frobenius 从群、Schur 从中心化子。
  **Schur–Weyl 这个名字与物理地位是 Weyl 后来的事**（en-wiki *Schur–Weyl duality* 明说：Schur discovered,
  Weyl popularized it in his books on quantum mechanics and invariant theory）。
- **关键卡点**：为什么 Schur 不能照 Frobenius 直接对 $\mathrm{GL}_n$ 做特征标？
  给的唯一事实：$\mathrm{GL}_n$ 无限，Frobenius 那套正交关系是给有限群造的；中心化子是有限维代数，可用双中心化子。

### 四｜1920s–30s：Weyl 把它变成物理语言
- Weyl, *Gruppentheorie und Quantenmechanik* (1928)，英译 *The Theory of Groups and Quantum Mechanics* (1931)；
  1939 *The Classical Groups. Their Invariants and Representations* 重新处理不变量论，覆盖 $\mathfrak{S}_n$、
  $\mathrm{GL}_n$、正交群、辛群的不变量与表示。1928 年 Bologna ICM 全会报告讲连续群及其线性表示。
- 作用：让这门学问在 20 世纪没死（多电子原子的置换对称、谱的群论组织）。讲座本身不再讲物理，一句带过即可。

### 五｜1954–65：搬到 $\mathbb{F}_q$，$\mathfrak{S}_n$ 的群代数长出 $q$
- **Bruhat 分解**由 Bruhat 对经典群给出、Chevalley 给一般情形（en-wiki *Bruhat decomposition*）；
  双陪集 $BwB$ 正好是旗簇的 Schubert 胞腔。作用：把连续群的问题化归成 Weyl 群的组合（$\mathrm{GL}_n$ 时就是 $\mathfrak{S}_n$）。
- Hecke 代数：Coxeter 群群代数的**形变 / q-模拟**，二次关系 $(T_s-q_s)(T_s+1)=0$ 与辫关系；
  Hecke 代数是 Artin 辫群的群环的商（en-wiki *Iwahori–Hecke algebra*）。
  出处：Iwahori & Matsumoto, *On some Bruhat decomposition and the structure of the Hecke rings of p-adic
  Chevalley groups*, Publ. Math. IHÉS **25** (1965) 5–48, doi:10.1007/BF02684396。
- **Tits 定理**：$q$ 取单位根之外的值时，Hecke 代数半单且同构于 $\mathbb{C}[W]$（即 $q\mapsto1$ 那一支）。
  ⇒ 「$q=1$ 退回群代数」不是类比，是定理。
- Hecke 本人（1887–1947，Hilbert 的学生）是模形式/Hecke 算子那条线，不是群论这条线；两条线在名字上合流。

### 六｜1985–86：量子群与「同一个 q」
- 来源不是代数而是可积系统/统计力学（Yang–Baxter 方程、量子逆散射）。
- Drinfeld 1985 (*Hopf algebras and the quantum Yang–Baxter equation*, Sov. Math. Dokl. 32) 与
  Jimbo 1985 (*A q-difference analogue of $U(\mathfrak g)$ and the Yang–Baxter equation*, Lett. Math. Phys.
  **10**, 63–69) 独立给出包络代数的 $q$-形变（仍是 Hopf 代数 ⇒ 张量积仍有意义）。
- 1986 年 Jimbo 的下一篇标题直接就是答案：*A q-analogue of $U(\mathfrak{gl}(N+1))$, Hecke algebra, and the
  Yang–Baxter equation*（Lett. Math. Phys. **11**, 247–252）⇒ Hecke 代数与量子群在同一张量幂上互为中心化子
  = **量子 Schur–Weyl 对偶**。
- 为什么「意外」（en-wiki *Quantum group* 原话可用）：紧群与半单李代数是**刚性**的、不能形变；
  能形变的是更大的结构——群代数/包络代数。
- **Rosso 本人就在这条线上**（zbMATH 作者档 39 条）：1988 *Finite dimensional representations of the quantum
  analog of the enveloping algebra of a complex simple Lie algebra*（Comm. Math. Phys., doi:10.1007/BF01218386，
  量子群的完全可约性 + 最高权定理）、1989 PBW 与 universal $R$-matrix、1988 与 Jones 顶点模型/扭结、
  1990s quantum shuffles 与单位根处的量子群。⇒ **讲座 §3 的 highest weight 与 §7 的量子化是他本行**，不是科普转述。

### 七｜1994–2000：范畴化
- 造词：Crane, *Clock and category: is quantum gravity algebraic?*, J. Math. Phys. **36** (1995) 6180–6193,
  arXiv:gr-qc/9504038。纲领：Baez & Dolan, *Categorification*, Contemp. Math. **230** (1998) 1–36,
  arXiv:math.QA/9802029（集合 → 范畴、函数 → 函子、等式 → 自然同构）。
- 最著名的实例：Khovanov, *A categorification of the Jones polynomial*, arXiv:math.QA/9908171；
  Duke Math. J. **101** (2000) 359–426。判据：分次 Euler 特征退回原来的多项式；
  信息更多（Kronheimer–Mrowka 2010 证明 Khovanov 同调检测平凡结，Jones 多项式至今不知道能不能）。
- **Rosso 说的「第一个范畴化的例子」= 对称函数环由 $\mathfrak{S}_n$ 的表示范畴范畴化**：
  en-wiki *Categorification* 原话「the ring of symmetric functions is categorified by the category of
  representations of the symmetric group」，decategorification 把 Specht 模送到对应的分拆。
  所以标题的 "with a view towards categorification" 意思是：这条 1896 年的线，一百年后被认出是范畴化的第一个样本；
  而讲座最后那步（量子化）在当代研究里又被进一步范畴化。

## 讲这一幕要守的

1. 每幕只讲「谁卡在哪、解决了什么、留给下一幕什么」，不铺技术细节（他要的是动机与位置）。
2. 引文逐条给出处；归属不可靠的（Gordan）当场标出来，这本身就是他要的「诚实」。
3. 讲完三幕踢一次球（Schur 为什么绕道中心化子），不要一口气六幕讲完——他会顺着史提「位置/对象」类上位问题。
4. 年份只在核过的位置给到具体日期（1896-07-16 这种）；其余给世纪或「1980 年代中期」。

## 核史实的本机做法（省时）

- 百科条目用 `web-fetching` 的 `scripts/fetch_keyword_context.py <URL> 'kw1,kw2'` 直连取关键词窗口
  （几百 KB HTML 只打印命中行）。**别拿整页灌上下文，也别用 web_extract 抓百科**。
- 作者的生平/研究领域：zbMATH 开放接口无需 key，一次拿全清单：
  `curl -sSL "https://api.zbmath.org/v1/document/_search?search_string=au%3ARosso%2C%20Marc&results_per_page=100" | python3 -c "import json,sys;[print(r.get('year'),'|',r.get('title',{}).get('title')) for r in json.load(sys.stdin)['result']]"`
  用来判断「讲者讲的是不是自己的本行」，比二手介绍可靠。
- 年表已有落盘：`概念/群论的目的与历史.md` 是**群论**那条线（Lagrange/Sylow/Galois）；**`概念/表示论简史.md` 是本文件这条线的 vault 版**
  （同样的年表，逐条带出处，外加三处不可靠标注：Gordan 引文归属、双中心化子的措辞、$S_\infty$ 属现代框架）；
  本文件是技能内讲稿。三者不重叠，讲之前各读一遍，别重复调研。

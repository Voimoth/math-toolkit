---
name: math-library-search
description: Use when 用户问「哪本书/哪本讲义里讲过XX」「帮我查我书库里关于XX的内容」「这个概念我以前在哪看到过」时的本地书库全文检索。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [math, pdf, rag, search, sqlite, fts5, library]
    related_skills: [pdf-problem-search, user-math-library, math-coaching]
---

# 数学书库本地检索（math-rag）

**用途**：把 `/mnt/e/书籍` 里「课程用」的那批 PDF 建成可全文检索的本地索引，
让「XX 在哪本书里讲过」这类问题能**一次查询、带页码出处**地回答。

**和 `pdf-problem-search` 的分工**：
- `pdf-problem-search` = **已经知道是哪本书**，要定位「第几页」（单本、人工定位）
- 本技能 = **不知道在哪本书**，要跨全部书找（全库、索引检索）
两者可叠加：本技能给出「哪本书哪一页」，再用前者确认。

## 组成

```
~/.local/share/math-rag/
  venv/          # 装了 jieba（中文分词），不污染系统 Python
  index.py       # 增量建索引 / 同步
  query.py       # 检索
  index.db       # SQLite + FTS5（页码级）
```

**索引范围**：`代数`、`分析`、`物理`、`数学学习方法` 四个目录（208 个 PDF）。
**参考书库 `数学专业书籍`（8090 个 PDF / 106 GB）故意不索引** —— 按需再加。

## 用法

```bash
R=~/.local/share/math-rag
# 1) 先同步（秒级；有变化才索引）
$R/venv/bin/python $R/index.py
# 2) 检索
$R/venv/bin/python $R/query.py "正规子群"
$R/venv/bin/python $R/query.py "variational principle" --limit 5
$R/venv/bin/python $R/query.py "群作用" --json       # 给 agent 用
$R/venv/bin/python $R/query.py "Frobenius" --files-only
```

**回答用户时先跑 sync** —— 秒级，保证新加的书也在。

## 已验证的关键事实（别重新踩）

- **SQLite FTS5 的 `unicode61` 对中文完全无效**：中文没有空格，整段会被当成一个 token，
  `变分法` / `分` / `变分` 实测**全部 0 命中**。**必须分词**。
- **`trigram` tokenizer 对中文也不行**（实测 `MATCH '变分法'` 无结果）。
- **jieba 会把拉丁文切碎**（`Théorie` → `Th é orie`、`algèbres` → `alg è bres`），
  所以分词必须**按语言分开**：CJK 段走 `jieba.cut_for_search`，非 CJK 段走空白切分保持整词。
- **切分中英段不能用 `re.split` 的捕获组** —— 本机 Python 3.14 实测：
  `re.split(r'([\u4e00-\u9fff]+)', '正规子群')` 返回 `['', '']`，**中文整段被当分隔符吃掉**
  （同一个 pattern 的 `fullmatch` 却正常）—— 症状是「索引建完了但中文一条也搜不到」。
  正确写法：用**交替 pattern + `finditer`**：
  ```python
  SEG = re.compile(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff]+')
  for m in SEG.finditer(text):
      seg = m.group()
      out.extend(jieba.cut_for_search(seg) if CJK.fullmatch(seg) else seg.split())
  ```
- **法文重音**：`unicode61` 自带重音折叠，`Théorie` 和 `Theorie` 都能命中 ✓
- **法文/英文前缀**：`group` 匹配不到 `groupes`，查询词要写成 `group*`（脚本里对 ≥3 字符的拉丁词自动加 `*`）。
- **约 19% 的 PDF 是扫描件、没有文本层**（本机第一层 208 个里 **40 个**）——它们**检索不到**。
  实测包括：**伯克利《电磁学》585 页**、**谢启鸿《高等代数学》492 页**、**朗道《力学》179 页**、
  **阿诺尔德《经典力学的数学方法》435 页**。要搜这些得先 OCR（见 `user-math-library` 的
  `references/scanned-pdf-ocr.md`）。`index.py` 会把它们记为 `pages = -N`（负数=扫描件）并跳过。
- **绝对不要「逐页调 pdftotext」** —— 每页起一个子进程，1559 页的书实测要**几十秒到几分钟**，
  看起来像卡死。正确做法：**整本一次抽取**（`pdftotext <pdf> -`），再用页分隔符 `\f` 切页：
  ```python
  raw = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True).stdout
  chunks = raw.split('\f')      # chunks[i] 就是第 i+1 页
  ```
  实测同一本书：**逐页版「几分钟」 → 整本版 5.3 秒**（pdftotext 5.24s + 中文分词 0.06s），快约 50 倍。
  扫描件判定也变成一次的事：整本抽完文本 < 400 字符就跳过。
- **jieba 分词不是瓶颈**：稳态实测 **0.6 ms / 700 字符（≈110 万字符/秒）**，首次调用才有
  350 ms 的词典构建开销。别为了「分词慢」去改算法。
- **公式抽取会乱**：`pdftotext` 对数学排版会丢上下标、错位。
  ⇒ **索引擅长「定理陈述、定义、例题讲解」这些散文部分，公式只能回原文看。**
  **不要转述公式**，给出页码让用户自己核对。

## 输出与引用纪律

- 结果必须**带文件相对路径 + 页码**（`query.py` 已给），让用户能翻原文核对。
- 片段是从**PDF 真原文**回读的（`pdftotext -f N -l N`），不是从索引里的分词文本拼的，
  所以不会出现「索引里的词和书里长得不一样」。
- 引用时按用户 wiki 的惯例：**出处 + 原文要点**，不要把检索结果直接倒给用户当答案。

## 结果契约与置信度（2026-10-07 补）

借外部工具包（pika 2.1.5 的检索评测契约）补上「什么算一个合格结果」：

一次合格的检索报告必须给全：**库内相对路径 + 1-based 页码 + 精确原文摘录 + 匹配原因 + 提取状态 + 覆盖警告**。

- **硬概念不许放宽**（`Borel 可测` vs `Lebesgue 可测`、`右连续` vs `连续`、`单调函数` vs 只提单调收敛的页）：
  命中更弱的命题 ⇒ 报「旁证 / 近似命中」，不报精确命中。
- **降权**：章节总览页、只列「习题 21–29」的页、提示页/解答页 —— 它们不是「出处页」。
- **空结果只能说**「在已检查、当前已索引的正文里没找到」，并带上检查范围与查询变体；
  **不能**说「你的书库没有这个」。`pages = -N`（扫描件无文本层）、提取失败、索引缺口都是**覆盖状态**，
  不是「不相关」。
- 他纠正过一次检索后：**当轮**把它记成回归用例（查询 / 期望出处 / 失败层），别攒着。
- 失败分层定位：① 语料覆盖 ② 查询归一化 ③ 页面角色 / 局部陈述 ④ 排序打分；
  优先可复用修复（加特征、加降权规则），不为单个用例打特例补丁。
- 评测用例应覆盖这几类：精确出处查找 / 全库内容检索 / 模糊回忆与改写 / 多个独立有效来源 /
  作用域内应有「未找到」/ 扫描件 no_text / 索引缺口 / 同名文件 / 公式转词。

## 第一层的实测结果（2026-10-02 建成）

```
文件 208 个（可检索 168，扫描件跳过 40）
页数 7449 页, 文本 10.3 MB
建索引耗时 49 秒     索引库 27.4 MB
增量同步（无变化时） < 1 秒
```

**已验证可用的真实查询**（中法文都能搜、都带页码）：

| 查询 | 命中 |
|---|---|
| `正规子群` | 代数/代数I/代数I.pdf p.74,75（中文讲义）|
| `拉格朗日` | 代数I.pdf p.72（拉格朗日定理、指标）|
| `groupes` | 代数I材料/Mathématiques MP.pdf p.6,11（法文）|
| `变分法` | 物理/理论力学/力学与理论力学(秦敢,向守平) p.11,28 |

**已知偏差**：书库里「理论力学」是**秦敢/向守平**那本，不是用户讲义用的**袁业飞** ——
查到力学内容时注意别把参考书当成讲义引用。

## 维护

- 加新书 → 跑一次 `index.py`（增量，只处理新增/变更/删除，幂等）。
- 想让某个目录进来/出去 → 改 `index.py` 顶部的 `ROOTS`，然后 `index.py --rebuild`。
- 索引库位置和大小：`index.db`（跑完 index.py 会打印）。

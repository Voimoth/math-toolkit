# bookdex — 参考书目录索引

在几千本 PDF 参考书里回答「**哪本书讲过 X**」：只索引书名、作者、PDF 书签目录，以及无书签时
前 20 页的目录页文本（有文本层就抽文本，扫描件走 tesseract OCR）。不抽正文，所以几千本书
几分钟到几小时就能建完库，库文件只有几十 MB。

## 依赖

```bash
python3 -m venv venv && ./venv/bin/pip install pymupdf
# 可选：扫描件要 OCR 才装
sudo pacman -S tesseract tesseract-data-chi_sim tesseract-data-eng tesseract-data-fra   # Arch
# Debian/Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-fra
```

## 用法

```bash
# 1. 建库（默认增量：跳过没变的文件；缺目录页文本的重试一次）
./venv/bin/python index.py
./venv/bin/python index.py --rebuild        # 全量重建
./venv/bin/python index.py --limit 200      # 只处理前 200 个待办（先试水）
./venv/bin/python index.py --workers 4      # OCR 并发数
./venv/bin/python index.py --no-ocr         # 只做文本层，不上 OCR

# 2. 查询
./venv/bin/python query.py "正规子群"
./venv/bin/python query.py "variational principle" --limit 15
./venv/bin/python query.py "Riemann-Roch" --books   # 只列书，不列章节
./venv/bin/python query.py "Sylow" --json
```

## 书库怎么放：ROOTS 与层级（tier）

`index.py` 顶部的 `ROOTS` 决定索引哪些目录、每棵树的基础权重。默认布局（可用
`BOOKDEX_ROOT` 环境变量把根指到别处）：

```
<BOOKDEX_ROOT>/
├── 代数/             tier 3（课程在用）
├── 分析/             tier 3
├── 物理/             tier 3
├── 数学学习方法/      tier 3
└── 数学专业书籍/      tier 1（普通参考书；路径含 MPSI 的自动提到 tier 2）
```

查询排序按 `tier` 乘 `1 + 0.6×(tier−1)`：查一个课程书里根本没有的词，它仍然不会冒出来。
目录名可以自己改，改 `ROOTS` 即可；层级提示词在 `TIER_HINTS`。

## 输出怎么读

- `p.123` 是 **PDF 物理页号**（1-based），拿它跳转即可，不是书上的页码。
- `（无书签；前 20 页 OCR 目录页里出现该词，自己去翻）` 表示这本书没有可用书签，
  命中来自目录页兜底文本，**给不出章节页码**——这是刻意不冒充精确。
- 书签里 page ≤ 5 的条目权重压到 0.2：封面/版权页常把书名重复一遍，零信息。

## 已知限制

- 有书签的 PDF 大约只占四成，其余靠目录页兜底；两者的可信度不同，输出里分开标注。
- OCR 文本只作**召回**：中文能认出章节行但会带错字，法文要走 `fra+eng` 才不会丢重音。
- 文件名含 CJK → `chi_sim+eng`；带法语特征（重音字符或 mathématiques/exercices/oraux/MPSI 等词）
  → `fra+eng`；其余 `eng`。语言包没装会静默退化成纯文本层。
- 扫描仪自动生成的书签（`01`、`202512280213` 这类纯数字）会被判为垃圾书签，按无书签处理。
- 建库速度取决于书库所在磁盘：机械盘/USB 上几千本扫描件 OCR 是小时级，先 `--limit 200` 试。

## 配 tesseract 语言包

若语言包不在系统默认路径，设 `TESSDATA_PREFIX` 指到 `tessdata` 目录；脚本会在
`/mnt/h/tesseract/tessdata`、`/usr/share/tesseract-ocr/5/tessdata` 等位置自动找一个。

#!/usr/bin/env node
// 逐条公式校验 md 里的 LaTeX：KaTeX（最严格）+ MathJax（Obsidian 实际引擎）。
// 用法： NODE_PATH=~/.local/share/formula-check/node_modules node check_formulas.js <file.md> [...]
// 依赖：npm i katex mathjax-full --prefix ~/.local/share/formula-check
// 退出码：0 = 全部通过，1 = 有失败；失败项逐条打印「行号 + 引擎 + 报错 + 原式」。
const fs = require('fs');
const katex = require('katex');
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { SVG } = require('mathjax-full/js/output/svg.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
// 坑：手写 packages 列表（如 ['base','ams']）会让 pmatrix/cases/\operatorname/\xrightarrow
// 全报 Unknown environment / Undefined control sequence —— 假阳性。必须用 AllPackages 或默认。
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'none' });
const doc = mathjax.document('', { InputJax: tex, OutputJax: svg });

// 抽取公式：先把代码块抹成等长空白（保持行号），再取 $$..$$（可跨行），最后取行内 $..$。
function extract(src) {
  const clean = src.replace(/```[\s\S]*?```/g, (m) => m.replace(/[^\n]/g, ' '));
  const lineOf = (idx) => clean.slice(0, idx).split('\n').length;
  const items = [];
  const holes = [];
  const reBlock = /\$\$([\s\S]+?)\$\$/g;
  let m;
  while ((m = reBlock.exec(clean)) !== null) {
    items.push({ line: lineOf(m.index), disp: true, text: m[1].trim() });
    holes.push([m.index, m.index + m[0].length]);
  }
  const punched = clean.replace(/\$\$[\s\S]+?\$\$/g, (m) => m.replace(/[^\n]/g, ' '));
  const reInl = /(^|[^$\\])\$([^$\n]+?)\$(?!\$)/g;
  while ((m = reInl.exec(punched)) !== null) {
    const start = m.index + m[1].length;
    items.push({ line: lineOf(start), disp: false, text: m[2] });
  }
  return items;
}

let bad = 0, total = 0;
// 引擎能过、但 Obsidian(MathJax 默认包集) 与 pandoc→xelatex 都不认的环境/命令，单独报。
const PORTABILITY = [
  [/\\begin\{CD\}/, 'CD 环境（amscd）：pandoc 默认模板无此宏包 → Environment CD undefined；Obsidian 默认也不加载 amscd'],
  [/\\begin\{tikzcd\}/, 'tikzcd 环境：Obsidian 不支持'],
  [/\\require\{/, '\\require{...}：Obsidian 行为不可靠'],
];
for (const file of process.argv.slice(2)) {
  const src = fs.readFileSync(file, 'utf8');
  const items = extract(src);
  total += items.length;
  src.split('\n').forEach((ln, i) => {
    for (const [re, why] of PORTABILITY) {
      if (re.test(ln)) { bad++; console.log(`${file}:${i + 1}  可移植性: ${why}`); }
    }
  });
  for (const it of items) {
    let kerr = null, mjerr = null;
    try {
      katex.renderToString(it.text, { displayMode: it.disp, throwOnError: true, strict: false });
    } catch (e) { kerr = e.message.split('\n')[0]; }
    const h = adaptor.outerHTML(doc.convert(it.text, { display: it.disp }));
    const hit = h.match(/data-mjx-error="([^"]*)"/);
    if (hit || h.includes('mjx-merror')) mjerr = hit ? hit[1] : 'merror';
    if (kerr || mjerr) {
      bad++;
      console.log(`${file}:${it.line}  ${it.disp ? '[块]' : '[行内]'}`);
      if (kerr) console.log(`   KaTeX : ${kerr}`);
      if (mjerr) console.log(`   MathJax: ${mjerr}`);
      console.log(`   原式: ${it.text.slice(0, 160)}`);
    }
  }
  console.log(`${file}: ${items.length} 条公式`);
}
console.log(`合计 ${total} 条，失败 ${bad} 条`);
process.exit(bad === 0 ? 0 : 1);

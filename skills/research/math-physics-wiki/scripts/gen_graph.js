#!/usr/bin/env node
// 生成 wiki 知识图谱 graph.html(D3 力导向图)
// 用法: node gen_graph.js [wiki_root]  (默认 /mnt/e/notes)
// 输出: <wiki_root>/graph.html — 浏览器打开即见概念互链网络
// 原理: 扫描所有 .md 的 [[wikilinks]],节点=页面,连线=互链;按 frontmatter type 着色
const fs = require('fs');
const path = require('path');

const WIKI = process.argv[2] || '/mnt/e/notes';
const SKIP_DIRS = ['raw', 'scripts', '_archive', '.obsidian', 'node_modules', '.git'];

function walk(dir, acc = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (SKIP_DIRS.includes(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, acc);
    else if (e.isFile() && e.name.endsWith('.md')) acc.push(full);
  }
  return acc;
}

const pages = walk(WIKI);
const pageMap = new Map();
for (const p of pages) {
  const name = path.basename(p, '.md');
  const content = fs.readFileSync(p, 'utf8');
  const titleMatch = content.match(/^title:\s*(.+)$/m);
  const typeMatch = content.match(/^type:\s*(.+)$/m);
  pageMap.set(name.toLowerCase(), {
    name,
    title: titleMatch ? titleMatch[1].trim() : name,
    type: typeMatch ? typeMatch[1].trim() : 'page',
  });
}

const links = [];
for (const p of pages) {
  const name = path.basename(p, '.md').toLowerCase();
  const content = fs.readFileSync(p, 'utf8');
  const linkRe = /\[\[([^\]|#]+)(?:#[^\]]*)?\]\]/g;
  let m;
  while ((m = linkRe.exec(content)) !== null) {
    const target = m[1].trim().toLowerCase();
    if (target === 'wikilinks') continue; // vault 里说明性文字中的示例链接
    if (pageMap.has(target)) links.push({ source: name, target });
  }
}

const nodes = [...pageMap.keys()].map(n => ({ id: n, name: pageMap.get(n).title, type: pageMap.get(n).type }));
const edges = links.map(l => ({ source: l.source, target: l.target }));
const typeColors = {
  concept: '#4f9cf9', entity: '#f9a14f', comparison: '#9b6cf9',
  query: '#6cf9a1', summary: '#f96c6c', page: '#a0a0a0',
};

// HTML 模板(D3 v7 力导向图,暗色主题,可拖动/缩放/悬停提示)
const html = `<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><title>数学 Wiki 知识图谱</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>body{margin:0;background:#1e1e2e;overflow:hidden;font-family:'Segoe UI',sans-serif}
#info{position:fixed;top:10px;left:10px;color:#cdd6f4;background:rgba(30,30,46,0.85);padding:8px 14px;border-radius:8px;font-size:13px;z-index:10}
.legend{position:fixed;bottom:10px;left:10px;color:#cdd6f4;font-size:12px;z-index:10}
.legend span{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}
.link{stroke:#999;stroke-opacity:0.35}
.node circle{stroke:#fff;stroke-width:1px;cursor:pointer}
.node text{fill:#cdd6f4;font-size:11px;pointer-events:none;text-shadow:0 0 3px #000}
.tooltip{position:absolute;display:none;background:#313244;color:#cdd6f4;padding:6px 10px;border-radius:6px;font-size:12px;pointer-events:none;z-index:20}</style></head>
<body>
<div id="info">📚 数学 Wiki 知识图谱 — ${nodes.length} 节点 / ${edges.length} 连接(可拖动、滚轮缩放)</div>
<div class="legend"><span style="background:#4f9cf9"></span>概念 <span style="background:#f9a14f"></span>实体 <span style="background:#9b6cf9"></span>对比 <span style="background:#6cf9a1"></span>查询 <span style="background:#a0a0a0"></span>其他</div>
<div class="tooltip"></div>
<script>
const nodes=${JSON.stringify(nodes)};const edges=${JSON.stringify(edges)};const typeColors=${JSON.stringify(typeColors)};
const w=window.innerWidth,h=window.innerHeight;
const svg=d3.select('body').append('svg').attr('width',w).attr('height',h);
const g=svg.append('g');
svg.call(d3.zoom().scaleExtent([0.1,4]).on('zoom',e=>g.attr('transform',e.transform)));
const sim=d3.forceSimulation(nodes)
  .force('link',d3.forceLink(edges).id(d=>d.id).distance(90))
  .force('charge',d3.forceManyBody().strength(-280))
  .force('center',d3.forceCenter(w/2,h/2))
  .force('collide',d3.forceCollide(22));
g.append('g').selectAll('line').data(edges).join('line').attr('class','link').attr('stroke-width',0.8);
const node=g.append('g').selectAll('g').data(nodes).join('g')
  .call(d3.drag().on('start',(e,d)=>{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;})
    .on('drag',(e,d)=>{d.fx=e.x;d.fy=e.y;})
    .on('end',(e,d)=>{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}));
node.append('circle').attr('r',d=>d.type==='concept'?9:7).attr('fill',d=>typeColors[d.type]||'#a0a0a0');
node.append('text').text(d=>d.name).attr('dx',14).attr('dy',4);
const tip=d3.select('.tooltip');
node.on('mouseover',(e,d)=>tip.style('display','block').html('<b>'+d.name+'</b><br>'+d.type))
  .on('mousemove',e=>tip.style('left',(e.pageX+12)+'px').style('top',(e.pageY+12)+'px'))
  .on('mouseout',()=>tip.style('display','none'));
sim.on('tick',()=>{g.selectAll('.link').attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);node.attr('transform',d=>'translate('+d.x+','+d.y+')');});
</script></body></html>`;

fs.writeFileSync(path.join(WIKI, 'graph.html'), html, 'utf8');
console.log(`图谱已生成: ${path.join(WIKI, 'graph.html')} (${nodes.length} 节点, ${edges.length} 连线)`);

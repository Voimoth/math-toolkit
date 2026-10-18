// 查重脚本(只读):按 ①同名文件 ②同大小+MD5 找出 /mnt/e/书籍 中的重复文件
// 用法: node find_duplicates.js [根目录]
// 输出: /mnt/e/书籍/_duplicates_report.txt(每组一个 NAME:/HASH: 头 + 缩进路径列表)
// 注意: 只读,不删除任何文件。删除清单由 gen_delete_list.js 生成,实际删除须用户确认。
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = process.argv[2] || '/mnt/e/书籍';
const SKIP_DIRS = ['node_modules', '.git', '_find_dups.js', '_duplicates_report.txt'];

function walk(dir, acc = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (SKIP_DIRS.includes(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, acc);
    else if (e.isFile()) acc.push(full);
  }
  return acc;
}

const files = walk(ROOT);
console.log(`总文件数: ${files.length}`);

// ① 同名文件组
const byName = new Map();
for (const f of files) {
  const name = path.basename(f).toLowerCase();
  if (!byName.has(name)) byName.set(name, []);
  byName.get(name).push(f);
}
const nameDups = [...byName.entries()].filter(([, v]) => v.length > 1);
console.log(`=== 同名文件组: ${nameDups.length} ===`);
let report = [];
for (const [name, paths] of nameDups) {
  report.push(`NAME: ${name}`);
  for (const p of paths) report.push(`  ${p}`);
  report.push('');
}

// ② 同大小(非同名)文件算 MD5
const stats = files.map(f => ({ f, size: fs.statSync(f).size }));
const bySize = new Map();
for (const s of stats) {
  if (!bySize.has(s.size)) bySize.set(s.size, []);
  bySize.get(s.size).push(s.f);
}
const md5Cache = new Map();
function md5(file) {
  if (md5Cache.has(file)) return md5Cache.get(file);
  const h = crypto.createHash('md5');
  try { h.update(fs.readFileSync(file)); } catch { return 'ERR'; }
  const d = h.digest('hex');
  md5Cache.set(file, d);
  return d;
}
const contentDups = [];
let count = 0;
for (const [size, paths] of bySize) {
  if (paths.length < 2) continue;
  const byHash = new Map();
  for (const p of paths) {
    const h = md5(p);
    if (!byHash.has(h)) byHash.set(h, []);
    byHash.get(h).push(p);
  }
  for (const [h, ps] of byHash) {
    if (ps.length > 1) contentDups.push(ps);
  }
  count++;
  if (count % 500 === 0) console.log(`MD5 进度: ${count}/${bySize.size}`);
}
console.log(`=== 同内容(非同名的)组: ${contentDups.length} ===`);
for (const ps of contentDups) {
  report.push(`HASH: ${md5(ps[0])}`);
  for (const p of ps) report.push(`  ${p}`);
  report.push('');
}

const outPath = path.join(ROOT, '_duplicates_report.txt');
fs.writeFileSync(outPath, report.join('\n'), 'utf8');
console.log(`报告已写入 ${outPath} (${report.length} 行)`);

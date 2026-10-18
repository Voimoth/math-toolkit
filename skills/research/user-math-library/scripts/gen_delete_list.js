// 从 _duplicates_report.txt 生成"保留/删除"清单(只读,不删除任何文件)
// 用法: node gen_delete_list.js [根目录]
// 读取: <根目录>/_duplicates_report.txt(find_duplicates.js 的输出)
// 输出: <根目录>/_delete_list.txt(每组: 保留: <路径> + 删除: <路径>...)
// 保留策略: 每组按路径字典序排序,保留第一个(通常是主分类目录),其余列为删除候选。
// 实际删除必须由 agent 展示清单并取得用户确认后执行。
const fs = require('fs');
const path = require('path');

const ROOT = process.argv[2] || '/mnt/e/书籍';
const reportPath = path.join(ROOT, '_duplicates_report.txt');
const report = fs.readFileSync(reportPath, 'utf8').split('\n');

const groups = [];
let cur = null;
for (const line of report) {
  if (line.startsWith('NAME:') || line.startsWith('HASH:')) {
    cur = [];
    groups.push(cur);
  } else if (line.startsWith('  ') && cur) {
    cur.push(line.trim());
  }
}

let delCount = 0;
let keepCount = 0;
const out = [];
for (const g of groups) {
  if (!g || g.length < 2) continue;
  const sorted = g.slice().sort();
  const k = sorted[0];
  out.push(`保留: ${k}`);
  for (let i = 1; i < sorted.length; i++) {
    out.push(`删除: ${sorted[i]}`);
    delCount++;
  }
  keepCount++;
  out.push('');
}

const outPath = path.join(ROOT, '_delete_list.txt');
fs.writeFileSync(outPath, out.join('\n'), 'utf8');
console.log(`重复组数: ${groups.length}`);
console.log(`将保留: ${keepCount} 个, 将删除: ${delCount} 个`);
console.log(`清单: ${outPath} (${out.length} 行)`);

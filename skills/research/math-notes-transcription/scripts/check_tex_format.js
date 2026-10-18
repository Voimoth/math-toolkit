// 验证笔记的公式分隔符配对(Obsidian 渲染前检查):
// 每行 $ 数为偶数、无单独 $ 行、$$ 成对
// 用法: node check_tex_format.js <file.md> [file2.md ...]
const fs = require('fs');
let issues = 0;
for (const file of process.argv.slice(2)) {
  const c = fs.readFileSync(file, 'utf8');
  const lines = c.split('\n');
  let fileIssues = 0;
  for (let i = 0; i < lines.length; i++) {
    const count = (lines[i].match(/\$/g) || []).length;
    if (count % 2 !== 0) {
      fileIssues++;
      console.log(`${file}:${i+1} 奇数个 $ (${count}): ${lines[i].substring(0, 80)}`);
    }
  }
  const soloDollar = lines.filter(l => l.trim() === '$').length;
  if (soloDollar > 0) { fileIssues++; console.log(`${file}: 单独 $ 行 ${soloDollar} 处`); }
  if (fileIssues === 0) console.log(`${file}: FORMAT_OK`);
  else { issues += fileIssues; console.log(`${file}: ${fileIssues} 处问题`); }
}
process.exit(issues === 0 ? 0 : 1);

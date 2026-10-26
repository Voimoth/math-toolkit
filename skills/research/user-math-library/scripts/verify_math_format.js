// 验证 Obsidian markdown 数学公式格式:提交前必跑
// 用法: node verify_math_format.js <file.md> [more.md ...]
// 检查:①奇数 $ 行 ②$$ 成对 ③单独 $ 行(跨行公式残留) ④``` 代码块残留
const fs = require('fs');

let allOk = true;
for (const file of process.argv.slice(2)) {
  const c = fs.readFileSync(file, 'utf8');
  const lines = c.split('\n');
  let issues = 0;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const count = (line.match(/\$/g) || []).length;
    if (count % 2 !== 0) {
      issues++;
      console.log(`[奇数$] ${file}:${i + 1} (${count}个$): ${line.substring(0, 80)}`);
    }
  }
  const displayOpen = (c.match(/\$\$/g) || []).length;
  if (displayOpen % 2 !== 0) { issues++; console.log(`[$$不成对] ${file}: 共${displayOpen}个$$`); }
  const soloDollar = lines.filter(l => l.trim() === '$').length;
  if (soloDollar > 0) { issues++; console.log(`[单独$行] ${file}: ${soloDollar} 行(应转 $$)`); }
  const codeFence = (c.match(/```/g) || []).length;
  if (codeFence % 2 !== 0) { issues++; console.log("[代码块残留] " + file + ": " + codeFence + " 个 ```(应为偶数)"); }
  console.log(`$file: ${issues === 0 ? 'FORMAT_OK' : issues + ' 处问题'}($$=${displayOpen}, 行内$行正常)`);
  if (issues > 0) allOk = false;
}
process.exit(allOk ? 0 : 1);

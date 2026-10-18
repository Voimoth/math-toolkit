// 修复 OCR/视觉模型转写笔记的 Obsidian 渲染问题:
// 1. 去除 ```markdown 代码块包裹(整段不渲染的元凶)
// 2. 单独占一行的 $ -> $$ (Obsidian 行内 $ 要求起止同行,跨行必须 $$)
// 3. 清理视觉模型开场白噪音("Here is the transcription...")
// 用法: node fix_obsidian_notes.js <file.md>
const fs = require('fs');
const file = process.argv[2];
if (!file) { console.error('用法: node fix_obsidian_notes.js <file.md>'); process.exit(1); }
let c = fs.readFileSync(file, 'utf8');

// 1. 去代码块标记
c = c.replace(/```markdown\s*\n/g, '\n');
c = c.replace(/\n```\s*$/g, '\n');
c = c.replace(/```/g, ''); // 兜底清残留

// 2. 单独一行 $ -> $$
const lines = c.split('\n');
for (let i = 0; i < lines.length; i++) {
  if (lines[i].trim() === '$') lines[i] = '$$';
}
c = lines.join('\n');

// 3. 清噪音行
c = c.replace(/^Here is the transcription of .*notes:\s*\n/gm, '');
c = c.replace(/^I'm unable to transcribe.*$/gm, '【此页为空或无法识别】');

fs.writeFileSync(file, c, 'utf8');
console.log('修复完成。验证:');
const after = fs.readFileSync(file, 'utf8');
console.log('  单独 $ 行:', (after.split('\n').filter(l => l.trim() === '$')).length);
console.log('  $$ 对数:', (after.match(/\$\$/g) || []).length / 2);
console.log('  代码块标记:', (after.match(/```/g) || []).length);

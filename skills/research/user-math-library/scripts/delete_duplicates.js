// 执行删除: 读取 "保留:/删除:" 清单, 删除所有 "删除:" 行指向的文件
// 用法: node delete_duplicates.js <清单路径> [<根目录>]
// 安全特性: ①PROTECT 列表保护临时/脚本文件不被误删 ②不存在的文件跳过 ③每项记入日志
// 只读清单来源: scripts/gen_delete_list.js 生成的 "保留:/删除:" 文本
const fs = require('fs');
const path = require('path');

const listFile = process.argv[2] || '/mnt/e/书籍//_delete_list.txt';
const lines = fs.readFileSync(listFile, 'utf8').split('\n');

// 保护名单: 查重脚本自身 + 报告文件, 即使出现在清单里也不删
const PROTECT = [
  'find_duplicates.js', 'gen_delete_list.js', 'delete_duplicates.js',
  '_delete_list.txt', '_duplicates_report.txt', '_final_delete_list.txt',
  '_find_dups.js', '_gen_delete_list.js', '_final_check.js', '_do_delete.js',
  '_deletion_log.txt', 'start-local-llm.bat'
];

let deleted = 0, failed = 0, skipped = 0;
const log = [];

for (const line of lines) {
  if (!line.startsWith('删除: ')) continue;
  const file = line.substring(4).trim();
  const base = path.basename(file);
  if (PROTECT.includes(base)) { skipped++; continue; }
  try {
    if (fs.existsSync(file)) {
      fs.unlinkSync(file);
      deleted++;
      log.push(`已删除: ${file}`);
    } else {
      skipped++;
    }
  } catch (e) {
    failed++;
    log.push(`失败: ${file} — ${e.message}`);
  }
}

const logFile = path.join(path.dirname(listFile), '_deletion_log.txt');
fs.writeFileSync(logFile, log.join('\n'), 'utf8');
console.log(`删除完成: 成功 ${deleted}, 跳过 ${skipped}, 失败 ${failed}`);
console.log(`日志: ${logFile}`);

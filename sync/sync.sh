#!/usr/bin/env bash
# 把本机 agent 技能目录与 nvim 配置同步进本仓库。
# 用法：bash sync/sync.sh [--dry]
#
# 可选的本机配置（不随仓库发布，放 sync/local/，已被 .gitignore 忽略）：
#   sync/local/exclude.txt   每行一个相对 skills/ 的路径，同步后删除
#   sync/local/sanitize.sed  sed 脚本，对文本文件逐条替换（去本地路径等）
set -euo pipefail

SRC="${AGENT_SKILLS:-$HOME/.hermes/skills}"
NVIM="${NVIM_CONFIG:-$HOME/.config/nvim}"
DST="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL="$DST/sync/local"
DRY=0
[[ "${1:-}" == "--dry" ]] && DRY=1

SKILLS=(
  research/math-coach
  research/math-physics-wiki
  research/math-notes-transcription
  bookdex
  research/pdf-problem-search
  research/group-theory-coaching
  research/mechanics-coaching
  research/coaching-index
  research/user-math-library
  research/arxiv
  research/grounded-citations
  research/study-tool-adoption
  note-taking/wiki-writing-conventions
)

RS=(-a --delete --exclude '__pycache__' --exclude '*.pyc' --exclude '.git')
[[ $DRY == 1 ]] && RS+=(-n -v)

for s in "${SKILLS[@]}"; do
  if [[ ! -d "$SRC/$s" ]]; then echo "跳过（本机没有）：$s" >&2; continue; fi
  rsync "${RS[@]}" "$SRC/$s/" "$DST/skills/$s/"
done

if [[ -f "$LOCAL/exclude.txt" ]]; then
  while IFS= read -r p; do
    [[ -z "$p" || "$p" == \#* ]] && continue
    [[ $DRY == 1 ]] && { echo "排除 $p"; continue; }
    rm -rf "$DST/skills/$p"
  done < "$LOCAL/exclude.txt"
fi

rsync "${RS[@]}" --exclude '.git' "$NVIM/" "$DST/nvim/"

# 工具：bookdex（只发布代码与说明，索引库与 venv 不进仓库）
BOOKDEX_SRC="${BOOKDEX_SRC:-$HOME/.local/share/bookdex}"
if [[ -d "$BOOKDEX_SRC" ]]; then
  mkdir -p "$DST/tools/bookdex"
  rsync "${RS[@]}" --exclude 'index.db' --exclude 'venv' "$BOOKDEX_SRC/" "$DST/tools/bookdex/"
fi

if [[ $DRY == 1 ]]; then echo "dry-run 结束"; exit 0; fi

if [[ -f "$LOCAL/sanitize.sed" ]]; then
  while IFS= read -r -d '' f; do
    sed -i -f "$LOCAL/sanitize.sed" "$f"
  done < <(find "$DST/skills" "$DST/nvim" "$DST/tools" -type f \( -name '*.md' -o -name '*.py' -o -name '*.sh' -o -name '*.json' -o -name '*.lua' \) -print0 2>/dev/null)
fi

cd "$DST"
git add -A
if git diff --cached --quiet; then echo "无变化"; exit 0; fi
git commit -q -m "sync: $(date +%Y-%m-%d\ %H:%M)"
git push -q origin main
echo "已推送：$(git log --oneline -1)"

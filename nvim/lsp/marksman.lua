-- marksman：Markdown 语言服务器（[[wiki 链接]] 补全/跳转、标题大纲、反向链接）
-- 你的笔记库 /mnt/e/notes 是 git 仓库，所以 .git 就能当项目根
return {
  cmd = { "marksman", "server" },
  filetypes = { "markdown" },
  root_markers = { ".marksman.toml", ".git" },
}

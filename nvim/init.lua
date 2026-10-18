-- tree-sitter CLI 由系统提供（/usr/bin/tree-sitter），Linux 下无需额外 PATH

-- 初始化 mini.deps（插件管理器）
local path_package = vim.fn.stdpath("data") .. "/site/"
local mini_path = path_package .. "pack/deps/start/mini.deps"
if not vim.loop.fs_stat(mini_path) then
  vim.cmd('echo "Installing `mini.deps`" | redraw')
  local clone_cmd = {
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/echasnovski/mini.deps",
    mini_path,
  }
  vim.fn.system(clone_cmd)
  vim.cmd("packadd mini.deps | helptags ALL")
  vim.cmd('echo "Installed `mini.deps`" | redraw')
end
require("mini.deps").setup({ path = { package = path_package } })

-- 加载各个功能模块（顺序：选项 → 键盘映射 → 自动命令 → 插件）
require("options")
require("keymaps")
require("autocmds")
require("plugins")

-- 固定 socket：zathura 反向搜索（Ctrl+左键）要连回 nvim（路径写死在 ~/.config/zathura/zathurarc）
-- 已有实例占用时会静默失败，这是预期的（远程调用会落到那个实例上）
pcall(vim.fn.serverstart, "/run/user/1000/nvim.pipe")

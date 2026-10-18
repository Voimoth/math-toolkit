-- 所有 Neovim 基本选项
local o = vim.opt

o.number = true
o.fillchars = { eob = " " }
o.mouse = "a"
o.showmode = false
o.breakindent = true
o.cursorline = true
o.expandtab = true
o.tabstop = 2
o.shiftwidth = 2
o.wrap = true
o.linebreak = true -- 在词边界断行（配合 breakindent 对齐），中文按字符断
o.updatetime = 300
o.shortmess = vim.tbl_deep_extend("force", vim.opt.shortmess:get(), { s = true, I = true, c = true, C = true })
o.writebackup = false
o.completeopt = "menu,menuone,noselect"
o.termguicolors = true

o.list = true
o.listchars = { tab = "| ", trail = "·", nbsp = "␣" }

o.ignorecase = true
o.smartcase = true

o.laststatus = 3
o.statusline = " "
o.statuscolumn = [[%!v:lua.require'snacks.statuscolumn'.get()]]

-- 拼写检查语言（默认不开拼写；想只检查法语就写成 { "fr" }）
-- 法语词典已放进 ~/.local/share/nvim/site/spell/，不会再弹「下载词典？」的提示
o.spelllang = { "en", "fr" }
o.spell = false

-- 设置 <leader> 键（必须在 options 中设置，因为插件会用到）
vim.g.mapleader = " "
vim.g.maplocalleader = " "

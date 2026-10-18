local map = vim.keymap.set

-- 普通模式下 <esc> 关闭搜索高亮
map("n", "<esc>", "<cmd>noh<cr>")

-- 复制/粘贴到系统剪贴板
map("v", "<C-c>", '"+y')
map({ "n", "v" }, "<C-v>", '"+p')
map("i", "<C-v>", '<esc>"+p')

-- 窗口导航
map("n", "<C-h>", "<C-w><C-h>", { desc = "Move focus to the left window" })
map("n", "<C-l>", "<C-w><C-l>", { desc = "Move focus to the right window" })
map("n", "<C-j>", "<C-w><C-j>", { desc = "Move focus to the lower window" })
map("n", "<C-k>", "<C-w><C-k>", { desc = "Move focus to the upper window" })

-- 用分号代替冒号
map("n", ";", ":", { desc = "CMD enter command mode" })

-- 保存文件
map({ "i", "x", "n", "s" }, "<C-s>", "<cmd>w<cr><esc>", { desc = "Save File" })

-- 退出
map("n", "<leader>qq", "<cmd>qa<cr>", { desc = "Quit All" })

-- LSP 相关
map("n", "gd", vim.lsp.buf.definition, { desc = "Goto Definition" })
map("n", "gD", vim.lsp.buf.declaration, { desc = "Goto Declaration" })

-- 切换拼写检查（F4）
map("n", "<F4>", ":set spell!<CR>", { desc = "切换拼写检查" })

-- 切换 Markdown 渲染(toggle:自动渲染开启后,可手动关/开)
vim.keymap.set("n", "<leader>md", "<cmd>RenderMarkdown toggle<CR>", { desc = "切换 Markdown 渲染" })

-- PDF 预览（pandoc → zathura）：保存即重编，源文件完全不渲染
vim.keymap.set("n", "<leader>mp", function()
  require("mdpreview").toggle()
end, { desc = "PDF 预览开关（pandoc→zathura）" })

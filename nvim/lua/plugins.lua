-- 此文件在 mini.deps 初始化后被 require，所以可以直接使用 add, now, later
local add, now, later = MiniDeps.add, MiniDeps.now, MiniDeps.later

-- ========================================
-- 立即加载的插件（now）
-- ========================================

-- 颜色主题
now(function()
	add({ source = "rebelot/kanagawa.nvim" })
	require("kanagawa").setup({
		transparent = true,
		theme = "dragon",
	})
	vim.cmd("colorscheme kanagawa")
end)

-- 图标库
now(function()
	add({ source = "echasnovski/mini.icons" })
	require("mini.icons").setup()
end)

-- 状态栏
now(function()
	add({ source = "echasnovski/mini.statusline" })
	require("mini.statusline").setup({
		content = {
			active = function()
				local vimtex_status = ""
				if vim.bo.filetype == "tex" and vim.g.loaded_vimtex then
					local status = vim.g.vimtex_compiler_status or ""
					if status == "success" then
						vimtex_status = "✓ "
					elseif status == "failed" then
						vimtex_status = "✗ "
					elseif status ~= "" then
						vimtex_status = "⟳ " .. status .. " "
					end
				end
				local mode = MiniStatusline.section_mode({ trunc_width = 120 })
				local git = MiniStatusline.section_git({ trunc_width = 75 })
				local fileinfo = MiniStatusline.section_fileinfo({ trunc_width = 120 })
				return vimtex_status .. mode .. git .. fileinfo
			end,
		},
	})
end)

-- snacks.nvim
now(function()
	add({ source = "folke/snacks.nvim" })
	require("snacks").setup({
		explorer = { replace_netrw = true },
		input = { enabled = true },
		notifier = { enabled = true },
		picker = { enabled = true },
		indent = {
			enabled = true,
			char = "┊",
			only_scope = true,
			hl = "Comment",
		},
		scope = { enabled = true },
		-- 图片 / 数学公式渲染：用 kitty 图形协议把 md 里的图片与 $...$ 直接画进缓冲
		-- 依赖（本机都已具备）：pdflatex + magick 编译公式、latex 的 treesitter 解析器、kitty 终端
		-- 公式走真编译（standalone 文档 → PNG），不是 latex2text 那种 unicode 近似
		image = {
			enabled = true,
			doc = {
				enabled = true,
				inline = true, -- 内联渲染（需终端支持 unicode placeholders，kitty 支持）
				max_width = 70,
				max_height = 20,
			},
			math = {
				-- 关掉 snacks 的公式渲染：改由 render-latex.nvim 负责（见下面的说明与配置）
				enabled = false,
				-- 公式的物理尺寸贴近正文：默认 font_size=Large + density 192 会明显比正文字大（行距被撑开）
				latex = { font_size = "normalsize" },
			},
			-- math 的 PNG 由 magick 从 PDF 转来；-density 直接决定像素尺寸 → 决定占几个终端格
			convert = {
				magick = {
					default = { "{src}[0]", "-scale", "1920x1080>" },
					vector = { "-density", 192, "{src}[{page}]" },
					math = { "-density", "160", "{src}[{page}]", "-trim" },
					pdf = { "-density", 192, "{src}[{page}]", "-background", "white", "-alpha", "remove", "-trim" },
				},
			},
		},
	})
	local map = vim.keymap.set
	map("n", "<leader>e", function()
		Snacks.explorer()
	end, { desc = "File Explorer" })
	map("n", "<leader>n", function()
		Snacks.picker.notifications()
	end, { desc = "Picker: Notification History" })
	map("n", "<leader><space>", function()
		Snacks.picker.smart()
	end, { desc = "Picker: Smart Find Files" })
	map("n", "<leader>/", function()
		Snacks.picker.grep()
	end, { desc = "Picker: Grep Workspace" })
end)

-- ========================================
-- render-latex.nvim：块级公式渲染成真图，行内公式保持文字
-- 为什么换掉 snacks 的 math：snacks 把行内公式统一压成「正好 1 格」，压缩比=30px÷墨迹高度，
--   于是单个字母被放大 2.3x、长式子接近 1:1 —— 尺寸漂移是上游行为，没有配置项可调（已核对上游 main）。
--   这个插件只渲染块级公式；行内公式走 conceal（大小天然与正文一致），且声明兼容 obsidian.nvim / render-markdown。
-- worker 是预编译 Rust 二进制，GitHub release 在本机被劫持，已用镜像下载并核对 SHA256SUMS 后手工放到托管路径：
--   ~/.local/share/nvim/render-latex.nvim/bin/v0.1.0-rc4/linux-x64/render-latex-worker
-- 回退：删掉本段，并把上面 snacks 的 image.math.enabled 改回 true。
-- ========================================
later(function()
	add({ source = "techwizrd/render-latex.nvim" })
	require("render_latex").setup({
		render = {
			preset = "match_text", -- 渲染尺寸对齐正文字号（另有 compact / presentation）
			-- 行内公式：保持原样（inline=false）。实测它的 "conceal" 模式会把 \to 这类命令
			-- 替换成看不见的东西（信息丢失，"1 \to N" 变成 "1 N"），而 \xrightarrow{} 又原样留着，
			-- 两头不讨好；要藏 $ 可以换 "highlight"，但同样会做符号替换，得把 inline_symbols 关掉。
			inline = false,
			inline_symbols = false,
		},
		-- nvim 0.12 的 vim.ui.img 在本机不存在（实测 false），auto 会退到 kitty；这里显式钉住
		image = { backend = "kitty" },
		install = { auto = false, version = "v0.1.0-rc4" }, -- worker 已手工装好，别让它去 GitHub 下
	})
	-- 行内公式的 conceal 需要这两个（官方 README 推荐值）
	vim.api.nvim_create_autocmd("FileType", {
		pattern = "markdown",
		callback = function()
			vim.opt_local.conceallevel = 2
			vim.opt_local.concealcursor = "nc"
		end,
		desc = "render-latex: 行内公式 conceal 所需",
	})
end)

-- VimTeX
now(function()
	add({ source = "lervag/vimtex" })
	-- 查看器：zathura。vimtex 会自动给 zathura 传 -x 接管「反向搜索」（PDF→nvim），无需额外配置
	-- 用 _simple 变体：主变体靠 xdotool 查找已有窗口，而 Hyprland(Wayland) 下 xdotool 看不到 Wayland 窗口
	vim.g.vimtex_view_method = "zathura_simple"
	vim.g.vimtex_view_zathura_use_synctex = 1
	vim.g.vimtex_compiler_method = "latexmk"
	vim.g.vimtex_compiler_latexmk = {
		options = {
			"-pdf",
			"-shell-escape",
			"-verbose",
			"-file-line-error",
			"-outdir=build",
			-- 下面三项必须显式写：本配置覆盖了 vimtex 的默认参数，写漏了会同步失效 / 出错时卡住等输入
			"-synctex=1", -- 同步搜索必需
			"-interaction=nonstopmode", -- 出错不要停下来等键盘输入
			"-halt-on-error", -- 出错立刻停（配合上面一项，vimtex 才能拿到错误）
		},
		-- 引擎表：中文文档（ctex/fontspec）用 xelatex，可通过 %!TEX program 或 :VimtexCompilerLatexmkEngine 切换
		engines = { _ = "-pdf", xelatex = "-pdfxe", lualatex = "-pdflua" },
	}
	vim.g.vimtex_complete_enabled = 1
	vim.g.vimtex_complete_common = 1
	-- 编译错误直接进 quickfix（用 <leader>le 打开），不在每次编译后强弹窗口
	vim.g.vimtex_quickfix_mode = 0

	local map = vim.keymap.set
	map("n", "<leader>ll", "<plug>(vimtex-compile)", { desc = "编译 LaTeX（连续模式，保存即重编译）" })
	map("n", "<leader>lL", "<plug>(vimtex-compile-ss)", { desc = "编译 LaTeX（单次）" })

	-- 正向搜索：交给 ~/.local/bin/pdf-preview.sh
	-- 脚本负责：开 zathura、nvim 全屏时先退出全屏（否则新窗口被挡住）、开完把焦点还给 nvim
	-- 为什么不用 vimtex 自带查看器：本机 Hyprland 下它起不来（详见技能 nvim-config 的 LaTeX 节）
	local function view_pdf()
		local tex = vim.fn.expand("%:p")
		local pdf = vim.fn.expand("%:p:h") .. "/build/" .. vim.fn.expand("%:t:r") .. ".pdf"
		if vim.fn.filereadable(pdf) == 0 then
			vim.notify("还没有 PDF：" .. pdf .. "（先按 <leader>ll 编译）", vim.log.levels.WARN)
			return
		end
		vim.fn.jobstart({
			vim.fn.expand("~/.local/bin/pdf-preview.sh"),
			pdf,
			tex,
			tostring(vim.fn.line(".")),
		}, { detach = true })
	end

	map({ "n", "v" }, "<leader>lv", view_pdf, { desc = "查看 PDF / 正向搜索（跳到当前行）" })
	map("n", "<leader>lk", "<plug>(vimtex-stop)", { desc = "停止编译" })
	map("n", "<leader>le", "<plug>(vimtex-errors)", { desc = "错误列表" })
	map("n", "<leader>lc", "<plug>(vimtex-clean)", { desc = "清理编译产物" })
	map("n", "<leader>ls", "<plug>(vimtex-toggle-main)", { desc = "切换主文件" })
	map("n", "<leader>li", "<plug>(vimtex-info)", { desc = "VimTeX 诊断信息" })
end)

-- ========================================
-- 延迟加载的插件（later）
-- ========================================
later(function()
	add({ source = "ThePrimeagen/vim-be-good" })
end)

later(function()
	add({ source = "L3MON4D3/LuaSnip" })
end)

-- render-markdown:立即加载,保证打开 md 文件时渲染已就绪(延迟加载会导致自动渲染不生效)
now(function()
	add({ source = "lukas-reineke/render-markdown.nvim" })
	require("render-markdown").setup({
		enabled = true, -- 打开 md 文件自动渲染
		latex = { enabled = false },
		-- callout / 引用的左侧彩条(▋)要跟着**视觉换行**一起重复：默认只在每个缓冲行的第一屏行画一次，
		-- 长行折行后的续行就没有彩条。repeat_linebreak = true 让它在每个折行行首重画
		-- (需要 neovim >= 0.10，本机 0.12)。
		-- 代价：重画的彩条会占掉续行开头 1 格，不加 showbreak 会盖住正文首字。
		-- 所以配 win_options.showbreak = 2 空格：折行行缩进 2 格，彩条画在第 1 格、
		-- 正文从第 3 格开始，正好与首行「彩条+空格+正文」对齐。breakindent 本来就是 true。
		-- win_options 只在渲染生效时设置，切走/关渲染会还原，不影响别的 buffer。
		quote = { repeat_linebreak = true },
		win_options = {
			showbreak = { default = "", rendered = "  " },
		},
	})
	-- 兜底:进入 markdown 缓冲时确保渲染开启(处理新打开/切换缓冲的场景)
	vim.api.nvim_create_autocmd("FileType", {
		pattern = "markdown",
		callback = function()
			pcall(vim.cmd, "RenderMarkdown enable")
		end,
		desc = "Markdown 自动渲染兜底",
	})
end)

later(function()
	add({ source = "rafamadriz/friendly-snippets" })
	require("luasnip.loaders.from_vscode").lazy_load()
end)

later(function()
	add({ source = "echasnovski/mini.pairs" })
	require("mini.pairs").setup()
end)

later(function()
	add({ source = "echasnovski/mini.surround" })
	require("mini.surround").setup()
end)

-- mini.pick：obsidian.nvim 的 picker 用（它的原版不支持 snacks）
later(function()
	add({ source = "echasnovski/mini.pick" })
	require("mini.pick").setup({
		-- 用 j/k 移动选择（默认是 <C-n>/<C-p>；上下方向键另有硬编码映射，依然可用）
		-- 代价：mini.pick 是「边输入边过滤」，j/k 被占用后就没法在查询串里打 j/k 了
		mappings = {
			move_down = "j",
			move_up = "k",
		},
	})
end)

later(function()
	add({ source = "folke/which-key.nvim" })
	require("which-key").setup({ preset = "helix" })
	vim.keymap.set("n", "<leader>?", function()
		require("which-key").show({ global = false })
	end, { desc = "Buffer Local Keymaps (which-key)" })
end)

later(function()
	local lsp_dir = vim.fn.stdpath("config") .. "/lsp/"
	local lsp_configs = vim.fn.globpath(lsp_dir, "*.lua", false, true)
	for _, lsp_config in ipairs(lsp_configs) do
		local lsp_name = vim.fn.fnamemodify(lsp_config, ":t:r")
		vim.lsp.enable(lsp_name)
	end
end)

later(function()
	add({ source = "stevearc/conform.nvim" })
	require("conform").setup({
		notify_on_error = false,
		format_on_save = {
			timeout_ms = 500,
		},
		formatters_by_ft = {
			lua = { "stylua" },
			tex = { "latexindent" },
		},
		formatters = {
			latexindent = {
				command = "latexindent",
				args = { "-g", "build/indent.log", "-y='defaultIndent: \"  \"'" },
			},
		},
	})
	vim.keymap.set("n", "<leader>cf", function()
		require("conform").format({ async = true, lsp_format = "fallback" })
	end, { desc = "Format buffer" })
end)

later(function()
	add({
		source = "nvim-treesitter/nvim-treesitter",
		checkout = "master",
		monitor = "main",
		hooks = {
			post_checkout = function()
				vim.cmd("TSUpdate")
			end,
		},
	})
	require("nvim-treesitter.configs").setup({
		ensure_installed = {
			-- 不要加 "latex"/"bib"：本机 tree-sitter-cli 与 nvim-treesitter master 的 latex parser
			-- 不兼容（生成时树报 unexpected argument '--no-bindings'），LaTeX 高亮由 vimtex 提供，够用
			"bash",
			"c",
			"diff",
			"html",
			"lua",
			"luadoc",
			"markdown",
			"markdown_inline",
			"query",
			"vim",
			"vimdoc",
		},
		-- latex 的 treesitter 高亮必须关掉：本机手工装了 latex.so（site/parser/latex.so），
		-- nvim-treesitter 会对"有 parser 的 buffer"一律启动 treesitter 高亮，把 &syntax 清空，
		-- VimTeX 随即报 "Syntax highlighting is controlled by Treesitter!"
		-- （判据在 vimtex/autoload/vimtex/nvim.vim：syntax 为空 + highlighter.active 非空）。
		-- LaTeX 高亮本来就走 vimtex 的 syntax，这里只保留其它语言。
		highlight = { enable = true, disable = { "latex" } },
		indent = { enable = true },
	})
end)

later(function()
	add({
		source = "saghen/blink.cmp",
		checkout = "v1.3.1",
		depends = { "rafamadriz/friendly-snippets" },
	})
	require("blink.cmp").setup({
		keymap = {
			preset = "super-tab",
		},
		appearance = { nerd_font_variant = "normal" },
		signature = { enabled = true },
		sources = {
			default = { "lsp", "path", "snippets", "buffer" },
			providers = {
				buffer = {
					min_keyword_length = 12,
				},
			},
		},
		completion = {
			documentation = {
				auto_show = true,
				auto_show_delay_ms = 300,
			},
			menu = {
				draw = {
					columns = {
						{ "kind_icon", "label" },
						{ "kind" },
					},
				},
			},
		},
	})
end)

later(function()
	add({ source = "j-hui/fidget.nvim" })
	require("fidget").setup()
end)

later(function()
	add({ source = "lewis6991/gitsigns.nvim" })
	require("gitsigns").setup({ trouble = true })
end)

-- ========================================
-- Obsidian 风格 Wiki(数学学习知识库)
-- ========================================
later(function()
	add({
		source = "epwalsh/obsidian.nvim",
		depends = { "nvim-lua/plenary.nvim" },
	})
	local obsidian = require("obsidian")
	obsidian.setup({
		dir = "/mnt/e/notes",
		-- picker：本机装的是 epwalsh 原版，它的 pickers/init.lua 只认 obsidian.config.Picker 里
		-- 那三个**原样字符串**：telescope.nvim / fzf-lua / mini.pick
		-- （写 "snacks" 或省事的 "mini" 都会直接 error("not implemented for ...")；
		--  症状：:ObsidianBacklinks / Search / QuickSwitch 一按就报错）。
		-- 这里用 mini.pick（同为 mini.* 系、单文件无依赖，见下方 later() 块）。
		-- 若哪天换成维护中的 fork（obsidian-nvim/obsidian.nvim，2.2k★ 且活跃），可改回 "snacks"。
		picker = {
			name = "mini.pick",
		},
		-- 自动补全 [[wikilinks]] 与标签(配合 blink.cmp 的 buffer 源)
		completion = {
			nvim_cmp = false, -- 我们不用 nvim-cmp,用 blink.cmp
			min_chars = 2,
		},
		-- 笔记模板(注意:键名是 folder,不是 subdir)
		templates = {
			folder = "templates",
			date_format = "%Y-%m-%d",
			time_format = "%H:%M",
		},
		-- 默认不启用 daily_notes,按需用 :ObsidianToday
		daily_notes = {
			folder = "queries",
			date_format = "%Y-%m-%d",
		},
		-- 笔记命名:标题空格转连字符,保留中文;无标题时生成随机 ID
		note_id_func = function(title)
			local suffix = ""
			if title ~= nil then
				-- 空格/空白转连字符,保留中文与其他字符(仅去掉明显的非法字符)
				suffix = title:gsub("%s+", "-")
				suffix = suffix:gsub('[\\/:*?"<>|]', "")
			else
				for _ = 1, 4 do
					suffix = suffix .. string.char(math.random(65, 90))
				end
			end
			return suffix
		end,
		-- wikilink 到 YAML frontmatter 的映射
		wiki_img_func = function(identifier)
			return "![" .. identifier .. "](" .. identifier .. ")"
		end,
	})

	local map = vim.keymap.set
	-- 在 [[wikilink]] 上跟随跳转(用插件官方命令,内部正确处理 follow_link_async)
	map("n", "gf", function()
		if obsidian.util.cursor_on_markdown_link() then
			vim.cmd("ObsidianFollowLink")
		else
			vim.lsp.buf.definition()
		end
	end, { desc = "Follow wikilink / definition", buffer = true })
	-- 跳转后返回:Vim 跳转历史(<C-o> 回退,<C-i> 前进);这里给个直观的 <leader>go
	map("n", "<C-o>", "<C-o>", { desc = "Jump back" })
	map("n", "<leader>go", "<C-o>", { desc = "Jump Back (返回上一个位置)" })
	map("n", "<leader>on", "<cmd>ObsidianNew<CR>", { desc = "Obsidian: New Note" })
	map("n", "<leader>os", "<cmd>ObsidianSearch<CR>", { desc = "Obsidian: Search Notes" })
	map("n", "<leader>ob", "<cmd>ObsidianBacklinks<CR>", { desc = "Obsidian: Backlinks" })
	map("n", "<leader>og", "<cmd>ObsidianQuickSwitch<CR>", { desc = "Obsidian: Quick Switch" })
	map("n", "<leader>ot", "<cmd>ObsidianToday<CR>", { desc = "Obsidian: Today Note" })
end)

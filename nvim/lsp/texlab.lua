-- texlab：LaTeX 语言服务器（补全 / 跳转 / 诊断 / 格式化）
-- 编译不交给它（onSave = false），编译由 vimtex + latexmk 负责，避免两边同时跑
return {
  cmd = { "texlab" },
  filetypes = { "tex", "plaintex", "bib" },
  root_markers = { ".latexmkrc", "latexmkrc", "texlab.toml", ".git" },
  settings = {
    texlab = {
      build = {
        executable = "latexmk",
        args = {
          "-pdf",
          "-interaction=nonstopmode",
          "-synctex=1",
          "-outdir=build",
          "%f",
        },
        onSave = false,
        forwardSearchAfter = false,
      },
      -- 从 texlab 侧发起的正向搜索（vimtex 的 <leader>lv 是另一条路，两条都可用）
      forwardSearch = {
        executable = "zathura",
        args = { "--synctex-forward", "%l:1:%f", "%p" },
      },
      chktex = { onOpenAndSave = false, onEdit = false },
      latexFormatter = "latexindent",
      bibtexFormatter = "texlab",
      latexindent = { modifyLineBreaks = false },
      formatter = { lineLength = 100 },
    },
  },
}

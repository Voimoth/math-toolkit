-- mdpreview: 把当前笔记编成 PDF 并用 zathura 分窗口预览（源文件完全不做渲染）
--   <leader>mp 开关。编译走 pandoc 参数集 `-d mathwiki`
--   （模板 ~/.local/share/pandoc/templates/mathwiki.tex，callout filter 在 filters/）
-- 行为：开启时编译一次并启动 zathura；之后每次 :w 自动重编，zathura 自己会重新读文件。
--       编译失败只在通知里报错，不覆盖上一版 PDF（pandoc 失败时不写输出文件）。

local M = {}

local outdir = vim.fn.stdpath("cache") .. "/mdpreview"
local st = {} -- bufnr -> { pdf = <path>, aug = <augroup>, timer = <uv_timer>, opened = <bool> }

local function log(msg, lvl)
  vim.notify("[预览] " .. msg, lvl or vim.log.levels.INFO)
end

-- 每个笔记一个固定的输出路径（名字 + 绝对路径哈希），避免多个笔记互相覆盖，
-- 也让「重新打开同一个文件」复用同一个 zathura 窗口。
local function pdf_for(src)
  return string.format("%s/%s-%s.pdf", outdir, vim.fn.fnamemodify(src, ":t:r"), vim.fn.sha256(src):sub(1, 8))
end

function M.build(bufnr)
  local s = st[bufnr]
  if not s or not vim.api.nvim_buf_is_valid(bufnr) then
    return
  end
  local src = vim.api.nvim_buf_get_name(bufnr)
  if src == "" or vim.fn.filereadable(src) == 0 then
    return
  end

  vim.system({ "pandoc", "-d", "mathwiki", src, "-o", s.pdf }, {
    cwd = vim.fn.fnamemodify(src, ":h"),
    text = true,
  }, function(res)
    vim.schedule(function()
      if res.code ~= 0 then
        log("编译失败，预览保持上一版：\n" .. vim.trim(res.stderr or ""), vim.log.levels.ERROR)
        return
      end
      if not s.opened then
        s.opened = true
        -- 用 ~/.local/bin/pdf-preview.sh 启动：它会先退出全屏、再让**合成器**去起 zathura，
        -- 这样 Hyprland 才会把预览窗口平铺在 nvim 旁边（子进程直接 launch 会铺满整个工作区）。
        -- 该脚本原本是给 LaTeX 正向搜索用的，第 2、3 个参数（tex 路径、行号）可省略。
        vim.fn.jobstart({ vim.fn.expand("~/.local/bin/pdf-preview.sh"), s.pdf }, { detach = true })
        log("已在右侧打开 zathura：" .. vim.fn.fnamemodify(s.pdf, ":t"))
      else
        log("已更新预览")
      end
    end)
  end)
end

-- 保存后 400ms 再编，避免连按 :w 时并发跑多个 pandoc
local function schedule(bufnr)
  local s = st[bufnr]
  if not s then
    return
  end
  s.timer = s.timer or vim.uv.new_timer()
  s.timer:stop()
  s.timer:start(400, 0, vim.schedule_wrap(function()
    if vim.api.nvim_buf_is_valid(bufnr) and st[bufnr] then
      M.build(bufnr)
    end
  end))
end

-- 扫 /proc 找出「正在显示这份 PDF」的 zathura 进程（返回 pid 列表）。
-- 不用 `pkill -f <路径>`：那是正则匹配，会连带匹配到命令行里含同样字符串的其他进程
-- （踩过：`pkill -f mdprev-test` 把执行命令的那个 shell 自己也 SIGTERM 了，后半段清理没跑）。
local function viewer_pids(pdf)
  local pids = {}
  local handle = vim.uv.fs_scandir("/proc")
  if not handle then
    return pids
  end
  while true do
    local name = vim.uv.fs_scandir_next(handle)
    if not name then
      break
    end
    if name:match("^%d+$") then
      local f = io.open("/proc/" .. name .. "/cmdline", "rb")
      if f then
        local content = (f:read("*a") or ""):gsub("%z", " ")
        f:close()
        if content:find("zathura", 1, true) and content:find(pdf, 1, true) then
          pids[#pids + 1] = tonumber(name)
        end
      end
    end
  end
  return pids
end

local function close_viewer(pdf)
  for _, pid in ipairs(viewer_pids(pdf)) do
    pcall(vim.uv.kill, pid, 15)
  end
end

function M.stop(bufnr, close_window)
  bufnr = bufnr or vim.api.nvim_get_current_buf()
  local s = st[bufnr]
  if not s then
    return false
  end
  if s.aug then
    pcall(vim.api.nvim_del_augroup_by_id, s.aug)
  end
  if s.timer then
    s.timer:stop()
    s.timer:close()
  end
  st[bufnr] = nil
  if close_window and s.pdf then
    close_viewer(s.pdf)
  end
  return true
end

-- 半自动清理：每次开启预览时顺手删掉太老的缓存（默认 60 天）。
-- 一个笔记一个 PDF（见下 clear），所以真正会积的只有改名/移动留下的孤儿；
-- 只按 mtime 判，不猜「源文件是否还在」（文件名里的哈希不可逆）。
local AUTO_PRUNE_DAYS = 60

function M.start(bufnr)
  bufnr = bufnr or vim.api.nvim_get_current_buf()
  local src = vim.api.nvim_buf_get_name(bufnr)
  if src == "" then
    log("这个缓冲区还没有文件名，先保存成 .md", vim.log.levels.WARN)
    return
  end
  if not src:match("%.md$") then
    log("只对 .md 笔记生效", vim.log.levels.WARN)
    return
  end

  vim.fn.mkdir(outdir, "p")
  local s = { pdf = pdf_for(src), opened = false }
  st[bufnr] = s

  -- 半自动清理：开预览时顺手清掉太老的缓存（安静模式，只有真删掉东西才提示）
  local ok_prune, perr = pcall(M.autoprune, AUTO_PRUNE_DAYS)
  if not ok_prune then
    log("自动清理预览缓存失败：" .. tostring(perr), vim.log.levels.WARN)
  end

  s.aug = vim.api.nvim_create_augroup("MdPreview" .. bufnr, { clear = true })
  vim.api.nvim_create_autocmd("BufWritePost", {
    group = s.aug,
    buffer = bufnr,
    callback = function()
      schedule(bufnr)
    end,
  })
  -- 退出 nvim 时把这份笔记的预览窗口一并关掉（用户要求）
  vim.api.nvim_create_autocmd("VimLeavePre", {
    group = s.aug,
    callback = function()
      M.stop(bufnr, true)
    end,
    desc = "退出 nvim 时关闭 PDF 预览窗口",
  })

  -- 缓冲区有未保存的改动就先落盘，否则编出来的是旧内容
  local modified = vim.bo[bufnr].modified
  if modified then
    vim.api.nvim_buf_call(bufnr, function()
      vim.cmd("silent update")
    end)
    schedule(bufnr) -- 上面的 :update 也会触发 BufWritePost，这里只是兜底
  else
    M.build(bufnr)
  end
  return s.pdf
end

-- 缓存目录按 PID… 不，按「源文件路径」命名 → 一个笔记一个 PDF，重复保存只是覆盖同一个文件。
-- 只有笔记被改名/移动后，旧 PDF 会变成孤儿留在目录里，所以给个手动清理入口。
---@param older_than_days? integer 只删这个天数之前的（nil = 全删）
function M.clear(older_than_days)
  local cutoff = older_than_days and (os.time() - older_than_days * 86400) or nil
  local handle = vim.uv.fs_scandir(outdir)
  if not handle then
    log("预览缓存目录还不存在")
    return
  end
  local removed, freed = 0, 0
  while true do
    local name = vim.uv.fs_scandir_next(handle)
    if not name then
      break
    end
    local path = outdir .. "/" .. name
    local st = vim.uv.fs_stat(path)
    if st and st.type == "file" and (not cutoff or (st.mtime.sec or 0) < cutoff) then
      if os.remove(path) then
        removed = removed + 1
        freed = freed + (st.size or 0)
      end
    end
  end
  log(string.format("清掉 %d 个预览缓存（释放 %.1f MB）%s", removed, freed / 1048576,
    older_than_days and string.format("（只删 %d 天前的）", older_than_days) or "（全部）"))
  return removed
end

-- 自动清理只报数（安静模式）：M.clear 里那句 log 在自动调用时会刷屏，这里用它自己的返回值和静默计数
---@param older_than_days integer
function M.autoprune(older_than_days)
  local before = 0
  local handle = vim.uv.fs_scandir(outdir)
  if handle then
    while true do
      local name = vim.uv.fs_scandir_next(handle)
      if not name then
        break
      end
      before = before + 1
    end
  end
  local removed = M.clear(older_than_days)
  if removed and removed > 0 then
    log(string.format("顺手清掉 %d 个过期预览缓存（剩 %d 个）", removed, math.max(before - removed, 0)))
  end
  return removed
end

function M.toggle()
  local bufnr = vim.api.nvim_get_current_buf()
  if st[bufnr] then
    M.stop(bufnr, true)
    log("已关闭自动重编，并关掉预览窗口")
  else
    M.start(bufnr)
  end
end

vim.api.nvim_create_user_command("MdPreview", function()
  M.toggle()
end, { desc = "PDF 预览开关（pandoc → zathura）" })

-- :MdPreviewClear          清空预览缓存
-- :MdPreviewClear 30       只清 30 天前的（正在看的窗口不受影响；下次按 <leader>mp 会自动重编）
vim.api.nvim_create_user_command("MdPreviewClear", function(opts)
  M.clear(tonumber(opts.args))
end, { nargs = "?", desc = "清理 PDF 预览缓存（可带天数）" })

return M

#!/usr/bin/env python3
"""批量视觉转录（Linux 版）—— 对应原来的 vision_transcribe_batch.ps1。

把目录里的图片（png/jpg/jpeg/webp）按页码区间逐一发给任意 OpenAI 兼容的
chat/completions 端点（需要支持 image_url），把返回文本写成同名的 .txt。

只用标准库（urllib），不需要 pip 装任何东西。
API key 从 .env 读取（$HERMES_HOME/.env → ~/.hermes/.env），可用 --env-path 显式指定。

用法示例:
  python3 vision_transcribe_batch.py --dir /mnt/e/书籍/某书/pages --start 45 --end 52 \
      --model deepseek-flash --prompt "转写这一页的全部文字，公式用 LaTeX"

参数与旧 PowerShell 版一致：--dir --start --end --base-url --model --key-var
--prompt --prompt-file --env-path --max-tokens --scale --redo
  （--scale 需要 Pillow；本机没装，缩放请改用 pdftoppm 的 -r 参数控制分辨率）
"""

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def find_env_file(explicit: str | None) -> pathlib.Path | None:
    cands = []
    if explicit:
        cands.append(pathlib.Path(explicit).expanduser())
    home = os.environ.get("HERMES_HOME")
    if home:
        cands.append(pathlib.Path(home) / ".env")
    cands.append(pathlib.Path.home() / ".hermes" / ".env")
    for c in cands:
        if c and c.is_file():
            return c
    return None


def read_key(env_file: pathlib.Path, key_var: str) -> tuple[str | None, str | None]:
    text = env_file.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        m = re.match(rf"^\s*{re.escape(key_var)}\s*=\s*(.+)$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'"), key_var
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Z0-9_]*API_KEY[A-Z0-9_]*)\s*=\s*(.+)$", line)
        if m:
            print(f"WARNING: {key_var} not found, using {m.group(1)}")
            return m.group(2).strip().strip('"').strip("'"), m.group(1)
    return None, None


def collect(dir_path: pathlib.Path, start: int, end: int) -> list[pathlib.Path]:
    imgs = sorted(
        (p for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXT),
        key=lambda p: p.name,
    )
    sel = []
    for p in imgs:
        m = re.search(r"(\d+)\s*$", p.stem)
        n = int(m.group(1)) if m else start  # 无编号的图当作在区间内
        if start <= n <= end:
            sel.append(p)
    return sel


def post_page(uri: str, key: str, model: str, prompt: str, img: pathlib.Path,
              max_tokens: int, scale: float, attempts: int = 3) -> tuple[str, int, object]:
    data = img.read_bytes()
    if scale and scale < 1.0:
        try:
            from PIL import Image  # 可选
            import io
            im = Image.open(io.BytesIO(data))
            im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
            buf = io.BytesIO()
            im.convert("RGB").save(buf, format="PNG")
            data = buf.getvalue()
        except ImportError:
            print("  (--scale 需要 Pillow，本机没有，已按原图发送)")
    b64 = base64.b64encode(data).decode("ascii")
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
            ],
        }],
    }
    body = json.dumps(payload).encode("utf-8")
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(
                uri,
                data=body,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=600) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            j = json.loads(raw)
            content = j["choices"][0]["message"]["content"]
            return content, len(data), j.get("usage")
        except Exception as e:  # noqa: BLE001 - 网络/接口错误都重试
            last_err = e
            if i < attempts - 1:
                time.sleep(2 + 3 * i)
    raise RuntimeError(f"request failed after {attempts} attempts: {last_err}")


def main() -> int:
    ap = argparse.ArgumentParser(description="批量视觉转录（OpenAI 兼容端点）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=9999)
    ap.add_argument("--base-url", default="https://api.deepseek.com")
    ap.add_argument("--model", default="deepseek-flash")
    ap.add_argument("--key-var", default="DEEPSEEK_API_KEY")
    ap.add_argument("--prompt", default="")
    ap.add_argument("--prompt-file", default="")
    ap.add_argument("--env-path", default="")
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()

    prompt = a.prompt
    if a.prompt_file:
        prompt = pathlib.Path(a.prompt_file).expanduser().read_text(encoding="utf-8")
    if not prompt:
        prompt = "把这张图片里的全部文字逐字转写出来（数学公式用 LaTeX 表示，不要翻译、不要总结、不要补全看不清的内容）。"

    env_file = find_env_file(a.env_path)
    if not env_file:
        print("no .env found (pass --env-path)", file=sys.stderr)
        return 1
    key, var = read_key(env_file, a.key_var)
    if not key:
        print(f"NO_KEY_FOUND in {env_file}", file=sys.stderr)
        return 1
    if "..." in key:
        print(f"KEY_LOOKS_LIKE_PLACEHOLDER var={var}", file=sys.stderr)
        return 1
    uri = a.base_url.rstrip("/") + "/chat/completions"
    print(f"ENV_FILE={env_file}")
    print(f"KEY_VAR={var}  KEY_LEN={len(key)}")
    print(f"TARGET={uri}  model={a.model}")

    d = pathlib.Path(a.dir).expanduser()
    if not d.is_dir():
        print(f"dir not found: {d}", file=sys.stderr)
        return 1
    sel = collect(d, a.start, a.end)
    if not sel:
        print("NO_IMAGES_IN_RANGE")
        return 1
    print(f"PAGES={len(sel)}  ({', '.join(p.name for p in sel)})\n")

    ok = skip = 0
    fails: list[str] = []
    for p in sel:
        out = d / (p.stem + ".txt")
        if out.exists() and not a.redo:
            print(f"SKIP  {p.name} -> {out.name} (exists)")
            skip += 1
            continue
        try:
            content, nbytes, usage = post_page(uri, key, a.model, prompt, p, a.max_tokens, a.scale)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL  {p.name} -> {e}")
            fails.append(p.name)
            continue
        if not content or len(content.strip()) < 20:
            print(f"EMPTY {p.name} -> response too short, NOT written")
            fails.append(p.name)
            continue
        out.write_text(content, encoding="utf-8")
        tok = usage.get("total_tokens", "?") if isinstance(usage, dict) else "?"
        print(f"OK    {p.name} -> {out.name}  img={nbytes}B  out={len(content)}ch  tokens={tok}")
        ok += 1

    print(f"\nDONE ok={ok} skip={skip} fail={len(fails)}")
    if fails:
        print("failed: " + ", ".join(fails))
    return 0 if not fails else 2


if __name__ == "__main__":
    sys.exit(main())

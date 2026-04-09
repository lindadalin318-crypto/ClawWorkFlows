"""
x_cookie_manager.py
X (Twitter) Cookie 自动管理模块

功能：
1. 检测当前 Cookie 是否有效
2. 有效时自动续期（访问 x.com 刷新 Cookie，延长有效期）
3. 失效时打印明确提示，告知用户重新导出

使用方式：
    from x_cookie_manager import load_valid_cookies
    cookies = await load_valid_cookies(context)  # 直接拿到可用的 Cookie
"""

import json
import os
import asyncio
from datetime import datetime, timezone
from pathlib import Path

COOKIE_FILE = Path(__file__).parent / "x_cookies.json"
COOKIE_BACKUP_FILE = Path(__file__).parent / "x_cookies_backup.json"

# ─── Cookie 有效性检测 ─────────────────────────────────────────

async def check_cookie_valid(page) -> bool:
    """访问 x.com 首页，检测是否处于登录状态"""
    try:
        await page.goto("https://x.com/home", timeout=20000)
        await page.wait_for_timeout(3000)
        url = page.url
        title = await page.title()

        # 如果跳转到登录页，说明 Cookie 失效
        if "login" in url or "signin" in url:
            return False
        # 如果标题包含 X / Twitter 且不是登录页
        if "Log in" in title and "home" not in url:
            return False
        # 检查是否有 home timeline 元素
        timeline = await page.query_selector('[data-testid="primaryColumn"]')
        return timeline is not None
    except Exception as e:
        print(f"  ⚠️ Cookie 检测异常: {e}")
        return False


# ─── Cookie 续期（刷新有效期）──────────────────────────────────

async def refresh_cookies(context, page) -> dict:
    """
    访问几个 x.com 页面来刷新 Cookie 有效期，
    然后从 context 中导出最新 Cookie 并保存
    """
    try:
        print("  🔄 正在刷新 Cookie 有效期...")
        # 访问几个页面触发 Cookie 刷新
        for url in ["https://x.com/home", "https://x.com/explore"]:
            await page.goto(url, timeout=15000)
            await page.wait_for_timeout(1500)

        # 从 context 导出最新 Cookie
        fresh_cookies = await context.cookies(["https://x.com"])
        if fresh_cookies:
            # 备份旧 Cookie
            if COOKIE_FILE.exists():
                import shutil
                shutil.copy2(COOKIE_FILE, COOKIE_BACKUP_FILE)

            # 保存新 Cookie
            with open(COOKIE_FILE, "w") as f:
                json.dump(fresh_cookies, f, ensure_ascii=False, indent=2)

            print(f"  ✅ Cookie 已刷新并保存（{len(fresh_cookies)} 条）")
            return {"success": True, "count": len(fresh_cookies)}
        else:
            print("  ⚠️ 未能获取到新 Cookie")
            return {"success": False}
    except Exception as e:
        print(f"  ❌ Cookie 刷新失败: {e}")
        return {"success": False, "error": str(e)}


# ─── Cookie 过期提示 ──────────────────────────────────────────

def print_cookie_expired_hint():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  X (Twitter) Cookie 已过期，需要重新导出                    ║
╠══════════════════════════════════════════════════════════════╣
║  操作步骤：                                                    ║
║  1. 打开 Chrome，访问 https://x.com 并确认已登录               ║
║  2. 安装扩展 "Cookie-Editor"（Chrome 应用商店免费）             ║
║  3. 在 x.com 页面点击扩展图标 → Export → Copy                  ║
║  4. 将复制的内容粘贴到：                                        ║
║     /Users/dada/vibe-coding-digest/xjson.md                  ║
║  5. 运行：python3 import_cookies.py                           ║
╚══════════════════════════════════════════════════════════════╝
""")


# ─── 从 xjson.md 导入 Cookie（一键转换）──────────────────────

def import_from_xjson(xjson_path: str = None) -> bool:
    """
    从 xjson.md 读取 Cookie-Editor 格式的 JSON，
    转换为 Playwright 格式并保存到 x_cookies.json
    """
    if xjson_path is None:
        xjson_path = Path(__file__).parent / "xjson.md"

    if not Path(xjson_path).exists():
        print(f"❌ 文件不存在: {xjson_path}")
        return False

    with open(xjson_path) as f:
        content = f.read()

    # 找到 JSON 数组
    lines = content.strip().split("\n")
    json_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("["):
            json_start = i
            break

    try:
        json_content = "\n".join(lines[json_start:])
        cookies_raw = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return False

    # 转换为 Playwright 格式
    playwright_cookies = []
    for c in cookies_raw:
        same_site = c.get("sameSite", "None")
        if same_site in [None, "no_restriction", "unspecified"]:
            same_site = "None"
        elif same_site == "lax":
            same_site = "Lax"
        elif same_site == "strict":
            same_site = "Strict"

        pw_cookie = {
            "name": c["name"],
            "value": c["value"],
            "domain": c["domain"],
            "path": c.get("path", "/"),
            "expires": c.get("expirationDate", -1),
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", False),
            "sameSite": same_site,
        }
        playwright_cookies.append(pw_cookie)

    # 备份旧文件
    if COOKIE_FILE.exists():
        import shutil
        shutil.copy2(COOKIE_FILE, COOKIE_BACKUP_FILE)

    with open(COOKIE_FILE, "w") as f:
        json.dump(playwright_cookies, f, ensure_ascii=False, indent=2)

    # 检查关键 Cookie
    names = {c["name"] for c in playwright_cookies}
    print(f"✅ 已导入 {len(playwright_cookies)} 条 Cookie")
    for key in ["auth_token", "ct0", "twid"]:
        status = "✅" if key in names else "❌"
        print(f"  {status} {key}")

    return all(k in names for k in ["auth_token", "ct0"])


# ─── 主入口：加载并验证 Cookie ────────────────────────────────

async def load_valid_cookies(context, page) -> bool:
    """
    加载 Cookie 到 context，并验证是否有效。
    有效时自动续期；无效时打印提示。
    返回 True/False 表示是否可用。
    """
    if not COOKIE_FILE.exists():
        print("❌ Cookie 文件不存在，请先导出 Cookie")
        print_cookie_expired_hint()
        return False

    with open(COOKIE_FILE) as f:
        cookies = json.load(f)

    await context.add_cookies(cookies)
    print(f"  📂 已加载 {len(cookies)} 条 Cookie，验证中...")

    valid = await check_cookie_valid(page)
    if valid:
        print("  ✅ Cookie 有效，自动续期中...")
        await refresh_cookies(context, page)
        return True
    else:
        print("  ❌ Cookie 已失效")
        print_cookie_expired_hint()
        return False


# ─── 命令行直接运行：导入 Cookie ─────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        success = import_from_xjson(path)
        sys.exit(0 if success else 1)
    else:
        print("用法：")
        print("  python3 x_cookie_manager.py import [xjson.md路径]  # 从 xjson.md 导入 Cookie")

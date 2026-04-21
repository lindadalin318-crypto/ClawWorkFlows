#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xhs_inject_cookies.py — 将小红书 Cookie 注入到持久化 Profile
=====================================================================
使用方法：
  1. 在浏览器（Chrome/Edge）打开小红书并登录
  2. 打开 DevTools (F12) → Application → Cookies → www.xiaohongshu.com
  3. 找到以下关键 Cookie（至少需要 a1 + web_session + webId）：
       - a1           (必须)
       - web_session  (必须)
       - webId        (必须)
       - gid          (推荐)
       - xsecappid    (推荐)
  4. 将值填入下方 XHS_COOKIES 列表，然后运行本脚本：
       python3 scripts/xhs_inject_cookies.py
  5. 显示 "✅ 登录成功" 后，fetch_xiaohongshu() 即可正常使用

注意：Cookie 有效期约 30-90 天，过期后需重新获取
"""

import asyncio
import json
from pathlib import Path

PROFILE_DIR = Path(__file__).parent.parent / "data" / "xhs_profile"
COOKIE_FILE = Path(__file__).parent.parent / "data" / "xhs_cookies.json"

# ── 填入你的小红书 Cookie ──────────────────────────────────────────
# 从浏览器 DevTools → Application → Cookies → www.xiaohongshu.com 复制
XHS_COOKIES = [
    {
        "name": "a1",
        "value": "19d70f4c532r37bx3a3djt6286rfx8vcdhyxq6dmt30000145148",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "web_session",
        "value": "04006979627a3dd5fa179100e23b4bb98c8d99",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": True,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "webId",
        "value": "d4ef61fffcdde3d0a72992b122b29880",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "gid",
        "value": "yjfW8i4fqff4yjfW8i4S2xKfqJFqWDCq0qfVv699KJYKFCq8iCYhSA888y42y4Y8KYq8yYdy",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "xsecappid",
        "value": "xhs-pc-web",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "abRequestId",
        "value": "569747a4-f5bf-5ecc-8475-259c35097545",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "websectiga",
        "value": "9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
    {
        "name": "acw_tc",
        "value": "0a00d96a17757165822391502eaf352e208360750e439964f9885d1e020da1",
        "domain": ".xiaohongshu.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    },
]
# ─────────────────────────────────────────────────────────────────────


async def inject_and_verify():
    from playwright.async_api import async_playwright

    # 过滤空值
    cookies = [c for c in XHS_COOKIES if c["value"].strip()]
    if not cookies:
        print("❌ 请先填入 Cookie 值（见脚本顶部注释）")
        return False

    required = {"a1", "web_session", "webId"}
    provided = {c["name"] for c in cookies}
    missing = required - provided
    if missing:
        print(f"❌ 缺少必要 Cookie: {missing}")
        return False

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Profile 目录: {PROFILE_DIR}")
    print(f"🍪 注入 {len(cookies)} 个 Cookie ...")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
            ],
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="zh-CN",
        )
        page = context.pages[0] if context.pages else await context.new_page()

        # 先访问主页，确保域名已建立
        await page.goto("https://www.xiaohongshu.com/", timeout=20000)
        await page.wait_for_timeout(2000)

        # 注入 Cookie
        await context.add_cookies(cookies)

        # 保存 Cookie 文件（方便后续直接读取，不依赖 Profile）
        COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        # 验证登录状态
        print("🔍 验证登录状态...")
        await page.goto("https://www.xiaohongshu.com/explore", timeout=20000)
        await page.wait_for_load_state("networkidle", timeout=15000)

        content = await page.content()
        url = page.url

        # 检查是否仍在登录页
        if "login" in url:
            print("❌ Cookie 无效或已过期，请重新从浏览器获取")
            await context.close()
            return False

        # 检查页面是否有内容（不只是登录弹窗）
        if len(content) > 100000:
            print("✅ 登录成功！小红书已就绪")
            print(f"   Cookie 已保存至: {COOKIE_FILE}")
            await context.close()
            return True
        else:
            print("⚠️ 页面内容过少，可能登录失败，请检查 Cookie")
            await context.close()
            return False


def main():
    print("=" * 55)
    print("  小红书 Cookie 注入工具")
    print("=" * 55)
    success = asyncio.run(inject_and_verify())
    if success:
        print("\n现在可以运行以下命令测试：")
        print("  python3 scripts/fetcher.py --source xhs --type search --keyword 独立游戏")
    else:
        print("\n请参考脚本顶部注释，填入正确的 Cookie 后重试")


if __name__ == "__main__":
    main()

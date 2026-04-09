"""
inject_cookies.py — 直接将 Cookie 注入到持久化 Profile，无需手动登录
"""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

PROFILE_DIR = Path(__file__).parent / "x_browser_profile"
COOKIE_FILE = Path(__file__).parent / "x_cookies.json"

COOKIES = [
    {
        "name": "auth_token",
        "value": "aca6ff0c177c74f28e2209ee058bc3dc4212485e",
        "domain": ".x.com",
        "path": "/",
        "httpOnly": True,
        "secure": True,
        "sameSite": "None"
    },
    {
        "name": "ct0",
        "value": "d240721bbd5949f5d1c6a540e2785007e5e79d6cb4ecc0f34fabe578793597c9a48a71595c7780a941361f7c950cbbef5cef36c1508f053f53d91c83478afbd6cd0e11673b81503e849462d451502c17",
        "domain": ".x.com",
        "path": "/",
        "httpOnly": False,
        "secure": True,
        "sameSite": "Lax"
    }
]

async def main():
    print("🍪 正在将 Cookie 注入到持久化 Profile...")
    PROFILE_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            args=["--no-sandbox"],
            viewport={"width": 1280, "height": 800},
        )
        page = context.pages[0] if context.pages else await context.new_page()

        # 先访问 x.com 才能设置 Cookie
        await page.goto("https://x.com", timeout=30000)
        await page.wait_for_timeout(2000)

        # 注入 Cookie
        await context.add_cookies(COOKIES)
        print("✅ Cookie 注入完成")

        # 验证登录
        await page.goto("https://x.com/home", timeout=30000)
        await page.wait_for_timeout(4000)

        url = page.url
        if "login" in url or "signin" in url:
            print("❌ Cookie 无效或已过期，请重新获取")
        else:
            timeline = await page.query_selector('[data-testid="primaryColumn"]')
            if timeline:
                print("🎉 登录验证成功！可以运行 x_fetch_scored.py 了")
            else:
                print("⚠️  页面加载异常，但 Cookie 已写入，可尝试运行 x_fetch_scored.py")

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())

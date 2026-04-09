"""
x_login.py — 一次性登录脚本

运行此脚本，会弹出真实浏览器窗口让你手动登录 X (Twitter)。
登录成功后，浏览器状态（Cookie、Session）会永久保存在本地。
之后运行 x_fetch_scored.py 时无需任何操作，自动复用登录状态。

用法：
    python3 x_login.py
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

PROFILE_DIR = Path(__file__).parent / "x_browser_profile"

async def main():
    print("=" * 60)
    print("  X (Twitter) 一次性登录")
    print("=" * 60)
    print(f"\n📁 浏览器状态将保存到：{PROFILE_DIR}\n")

    async with async_playwright() as p:
        # 使用持久化 context，登录状态永久保存在 PROFILE_DIR
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,  # 显示浏览器窗口
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
            ignore_default_args=["--enable-automation"],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )

        page = context.pages[0] if context.pages else await context.new_page()

        # 注入反检测脚本
        await Stealth().apply_stealth_async(page)

        # 先检查是否已经登录
        print("🔍 检查登录状态...")
        await page.goto("https://x.com/home", timeout=30000)
        await page.wait_for_timeout(3000)

        url = page.url
        if "login" not in url and "signin" not in url:
            # 检查是否有 timeline
            timeline = await page.query_selector('[data-testid="primaryColumn"]')
            if timeline:
                print("\n✅ 已经是登录状态！无需重新登录。")
                print("   你可以直接运行 x_fetch_scored.py 了。")
                await context.close()
                return

        # 需要登录
        print("\n🌐 请在弹出的浏览器窗口中登录 X (Twitter)")
        print("   登录完成后，程序会自动检测并保存状态...")
        print("   （如果已经在登录页，直接操作即可）\n")

        await page.goto("https://x.com/login", timeout=30000)

        # 等待用户登录完成（最多等 5 分钟）
        print("⏳ 等待你完成登录（最多 5 分钟）...")
        for i in range(60):  # 每 5 秒检查一次，最多 5 分钟
            await page.wait_for_timeout(5000)
            current_url = page.url
            if "home" in current_url or (
                "login" not in current_url and "signin" not in current_url
            ):
                timeline = await page.query_selector('[data-testid="primaryColumn"]')
                if timeline:
                    break
            if i % 6 == 0 and i > 0:
                print(f"   仍在等待... ({i * 5 // 60} 分 {i * 5 % 60} 秒)")
        else:
            print("\n⚠️  等待超时，请重新运行脚本")
            await context.close()
            return

        print("\n✅ 登录成功！浏览器状态已保存。")
        print("   之后运行 x_fetch_scored.py 将自动复用此登录状态。")
        print("   无需再手动操作！\n")

        # 多访问几个页面，让 Cookie 充分初始化
        for url in ["https://x.com/explore", "https://x.com/home"]:
            await page.goto(url, timeout=15000)
            await page.wait_for_timeout(1500)

        await context.close()
        print("🎉 完成！浏览器已关闭。")


if __name__ == "__main__":
    asyncio.run(main())
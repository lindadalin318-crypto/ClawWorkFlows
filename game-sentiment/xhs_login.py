#!/usr/bin/env python3
"""
小红书一次性登录脚本
运行后会打开浏览器，手动完成登录，之后自动保存 Profile
"""

import os
import sys

XHS_PROFILE = "/Users/dada/game-sentiment/xhs_profile"

def login():
    os.makedirs(XHS_PROFILE, exist_ok=True)
    print("🚀 启动小红书登录浏览器...")
    print("请在浏览器中完成登录（扫码或账号密码）")
    print("登录成功后，按 Enter 键保存并退出\n")

    try:
        from playwright.sync_api import sync_playwright
        try:
            from playwright_stealth import stealth_sync
        except ImportError:
            from playwright_stealth import Stealth
            stealth_sync = lambda page: Stealth().apply_stealth_sync(page)

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                XHS_PROFILE,
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--window-size=1280,900",
                ],
                viewport={"width": 1280, "height": 900},
            )
            page = browser.new_page()
            stealth_sync(page)

            page.goto("https://www.xiaohongshu.com/login", timeout=30000)
            print("✅ 浏览器已打开，请手动登录...")

            input("\n按 Enter 键保存登录状态并退出...")
            browser.close()

        print(f"✅ 登录状态已保存至：{XHS_PROFILE}")
        print("现在可以运行 run_sentiment.py 进行抓取了")

    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    login()

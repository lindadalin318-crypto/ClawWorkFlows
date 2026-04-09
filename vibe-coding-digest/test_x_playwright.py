#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) Playwright 测试脚本
- 使用有头浏览器，让用户手动登录后保存 Cookie
- 后续可无头模式复用 Cookie
"""

import json
import os
import time
from playwright.sync_api import sync_playwright

COOKIE_FILE = "x_cookies.json"

def save_cookies(context):
    cookies = context.cookies()
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"✅ Cookie 已保存到 {COOKIE_FILE}（共 {len(cookies)} 条）")

def load_cookies(context):
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE) as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"✅ 已加载 {len(cookies)} 条 Cookie")
        return True
    return False

def login_and_save():
    """有头模式：让用户手动登录，然后保存 Cookie"""
    print("🌐 打开浏览器，请手动登录 X...")
    print("登录完成后，按 Enter 保存 Cookie 并继续")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto("https://x.com/login")
        
        input("\n👆 请在浏览器中完成登录，然后按 Enter 继续...")
        
        # 检查是否登录成功
        current_url = page.url
        print(f"当前 URL: {current_url}")
        
        if "login" not in current_url:
            save_cookies(context)
            print("✅ 登录成功，Cookie 已保存！")
        else:
            print("❌ 似乎还未登录，请重试")
        
        browser.close()

def test_search(keyword="vibe coding game", headless=True):
    """测试搜索功能"""
    print(f"\n🔍 测试搜索关键词: {keyword}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 加载 Cookie
        if not load_cookies(context):
            print("❌ 未找到 Cookie 文件，请先运行登录流程")
            browser.close()
            return []
        
        page = context.new_page()
        
        # 搜索最新推文（Latest tab）
        search_url = f"https://x.com/search?q={keyword.replace(' ', '%20')}&f=live&src=typed_query"
        print(f"📡 访问: {search_url}")
        
        page.goto(search_url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # 检查是否需要重新登录
        if "login" in page.url:
            print("❌ Cookie 已过期，需要重新登录")
            browser.close()
            return []
        
        print(f"当前 URL: {page.url}")
        
        # 等待推文加载
        try:
            page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
            print("✅ 推文已加载")
        except:
            print("⚠️ 等待推文超时，尝试截图查看页面状态...")
            page.screenshot(path="x_debug.png")
            print("截图已保存到 x_debug.png")
        
        # 抓取推文
        tweets = []
        tweet_elements = page.query_selector_all('[data-testid="tweet"]')
        print(f"找到 {len(tweet_elements)} 条推文")
        
        for elem in tweet_elements[:10]:
            try:
                # 获取文本
                text_elem = elem.query_selector('[data-testid="tweetText"]')
                text = text_elem.inner_text() if text_elem else ""
                
                # 获取时间
                time_elem = elem.query_selector('time')
                pub_time = time_elem.get_attribute('datetime') if time_elem else ""
                
                # 获取链接
                link_elem = elem.query_selector('a[href*="/status/"]')
                link = "https://x.com" + link_elem.get_attribute('href') if link_elem else ""
                
                # 获取作者
                author_elem = elem.query_selector('[data-testid="User-Name"]')
                author = author_elem.inner_text().split('\n')[0] if author_elem else ""
                
                if text:
                    tweets.append({
                        "title": text[:100],
                        "url": link,
                        "author": author,
                        "published": pub_time,
                        "source": "X/Twitter",
                        "keyword": keyword,
                    })
                    print(f"  📝 [{pub_time[:10] if pub_time else '?'}] @{author}: {text[:80]}...")
            except Exception as e:
                print(f"  ⚠️ 解析推文出错: {e}")
        
        browser.close()
        return tweets

if __name__ == "__main__":
    import sys
    
    if not os.path.exists(COOKIE_FILE):
        print("=" * 50)
        print("首次运行：需要先登录 X")
        print("=" * 50)
        login_and_save()
    
    # 测试搜索
    print("\n" + "=" * 50)
    print("开始测试搜索...")
    print("=" * 50)
    
    results = test_search("vibe coding game", headless=True)
    print(f"\n✅ 共获取 {len(results)} 条推文")
    
    if results:
        print("\n前 3 条：")
        for r in results[:3]:
            print(f"  - {r['title'][:60]}")
            print(f"    {r['url']}")

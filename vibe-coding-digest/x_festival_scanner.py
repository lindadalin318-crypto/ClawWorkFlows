#!/usr/bin/env python3
"""
X/Twitter Game Festival 扫描器
功能：扫描指定账号过去1个月的帖子，找出 game festival / event signup 相关内容
用法：python3 x_festival_scanner.py [--accounts @acc1 @acc2 ...]
      python3 x_festival_scanner.py --notify   # 运行完后发 notify
"""

import asyncio
import json
import re
import sys
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from playwright.async_api import async_playwright

# ─── 配置 ─────────────────────────────────────────────────────────────────────

PROFILE_DIR = str(Path(__file__).parent / "x_browser_profile")
COOKIE_FILE  = str(Path(__file__).parent / "x_cookies.json")
OUTPUT_FILE  = str(Path(__file__).parent / "festival_results.json")

# 扫描时间范围：过去 N 天
SCAN_DAYS = 30

# 要扫描的账号列表（可被命令行参数覆盖）
DEFAULT_ACCOUNTS = [
    # ── 从「扫描用x.csv」提取的 X/Twitter 账号 ──
    "turnbasedlovers",       # (无发行商名)
    "gelius__",              # GIG showcase
    "iii_initiative",        # The Triple-i Initiative
    "MarmaladeGames",        # Marmalade Game Studio
    "GoblinzPub",            # Goblinz Publishing
    "11bitstudios",          # 11 bit studios
    "CrunchingKoalas",       # Crunching Koalas
    "acramdigital",          # Acram Digital
    "ansharpublish",         # ansharpublish
    "RetrovibeGames",        # Retrovibe
    "curvegames",            # Curve
    "sugoishowcase",         # sugoi
    "geight_tw",             # G Eight
    "tinyteamsfest",         # Tiny Teams
    "HumanQube",             # HumanQube
    "GCORESPUBLISH",         # GCores
    "IndieArk_Games",        # 独立方舟indieark
    "ThermiteGamesHQ",       # Thermite Games热脉游戏
    "GamirrorGames",         # Gamera Games
    "spiralupgames",         # Spiral Up Games
    "NeverLand_Entmt",       # Neverland Entertainment
    "playismen",             # PLAYISM
    "lightngames",           # Lightining Games
    "indienovacn",           # Indienova
    "PatheaGames",           # Pathea Games（重庆帕斯亚科技）
    "cubegamecn",            # 方块游戏Cube Games
    "2Pcom",                 # 2p games
    "neondoctrine",          # neon doctrine
    "OKJOY_Studio",          # okjoy
    "Kepler_Interact",       # kepler interactive
    "GamerskyIndie",         # 游民星空gamersky
    "Skystone_Games",        # skystone
    "gse_official_",         # GAME SOURCE ENTERTAINMENT
    "eastasiasoft",          # east asia soft
    "dreamhaven",            # Dreamhaven
    "yogscastgames",         # Yogscast Games
    "rogueducknet",          # Rogue Duck Interactive
    "IOInteractive",         # IOI Gamer
    "indiecngames",          # INDIECN
    "SapstarGames",          # SapStaR
    "bilibiligaming",        # bilibili
    "whispergamescn",        # 轻语游戏WhisperGames
    "parasgames",            # paras games
    "CEAsiaHK",              # CE-Asia中电博亚
    "AstrolabeGameJP",       # astrolabe games
    "ediggerstudio",         # edigger
    "WAVEGameStudios",       # wave games
    "i3agency",              # INSTINCT3
    "the4winds_ent",         # The 4 Winds Entertainment
]

# ─── Festival 关键词（命中任意一个即视为相关）────────────────────────────────

FESTIVAL_KEYWORDS = [
    # 通用 festival / event
    "festival", "fest", "showcase", "expo", "convention",
    "game jam", "gamejam", "game show",
    # 报名 / 参展
    "submission", "submit", "apply", "application", "signup", "sign up",
    "sign-up", "register", "registration", "call for",
    "open for", "accepting", "deadline", "last call",
    # 具体知名活动
    "steam next fest", "steam nextfest", "steam festival",
    "steam game festival", "ema week", "emaweek",
    "eastern martial artist", "anime festival", "anime expo",
    "anime game", "anime game fest",
    "bitsummit", "bit summit",
    "gamescom", "game developers conference", "gdc",
    "tokyo game show", "tgs", "pax", "pax east", "pax west",
    "indiecade", "indie game", "indie showcase",
    "wholesome direct", "wholesome games",
    "day of the devs", "day of devs",
    "guerrilla collective",
    "future games show",
    "new game plus expo",
    "digital dragons",
    "devcom",
    "nordic game",
    "game access",
    "replayed",
    "indie live expo",
    "bic festival",
    "latin america games summit",
    "lags",
    "pocket gamer",
    "pocket gamer connects",
    "gameconnect",
    "casual connect",
    "devgamm",
    "game on",
    "featured on steam",
    "steam homepage",
    "steam curator",
    # 主题 / 类型活动
    "ninja", "samurai", "martial arts", "cultivation",
    "cozy game", "cozy fest",
    "horror game", "horror fest",
    "pixel game", "pixel art game",
    "rpg fest", "jrpg",
    "visual novel", "vn fest",
    "demo fest", "demo event",
    # 中文关键词
    "游戏节", "展会", "报名", "征集", "参展", "截止",
    "动漫节", "独立游戏", "游戏展",
]

# ─── 工具函数 ──────────────────────────────────────────────────────────────────

def is_festival_related(text: str) -> tuple[bool, list[str]]:
    """检查文本是否包含 festival 相关关键词，返回 (是否相关, 命中的关键词列表)"""
    text_lower = text.lower()
    matched = []
    for kw in FESTIVAL_KEYWORDS:
        if kw.lower() in text_lower:
            matched.append(kw)
    return len(matched) > 0, matched

def parse_tweet_date(date_str: str) -> datetime | None:
    """解析 X 的时间字符串，返回 UTC datetime"""
    if not date_str:
        return None
    # 格式示例: "11:14 AM · Apr 24, 2025"
    try:
        # 去掉前面的时间部分，只取日期
        parts = date_str.split("·")
        if len(parts) >= 2:
            date_part = parts[1].strip()
            return datetime.strptime(date_part, "%b %d, %Y").replace(tzinfo=timezone.utc)
    except:
        pass
    return None

def is_within_days(dt: datetime | None, days: int) -> bool:
    """检查日期是否在最近 N 天内"""
    if dt is None:
        return True  # 无法解析日期时，默认保留
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return dt >= cutoff

# ─── 核心抓取逻辑 ──────────────────────────────────────────────────────────────

async def fetch_user_posts(page, username: str, max_scrolls: int = 20) -> list[dict]:
    """
    访问用户主页，滚动抓取过去 SCAN_DAYS 天内的所有帖子
    返回帖子列表
    """
    url = f"https://x.com/{username}"
    print(f"\n  → 访问 @{username} 主页: {url}")
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
    except Exception as e:
        print(f"  ✗ 访问失败: {e}")
        return []

    posts = []
    seen_ids = set()
    oldest_date_seen = datetime.now(timezone.utc)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=SCAN_DAYS)
    stop_scrolling = False

    for scroll_num in range(max_scrolls):
        if stop_scrolling:
            break

        # 抓取当前页面的所有帖子
        try:
            articles = await page.query_selector_all('article[data-testid="tweet"]')
        except:
            articles = []

        for article in articles:
            try:
                # 获取帖子文本
                text_el = await article.query_selector('[data-testid="tweetText"]')
                text = await text_el.inner_text() if text_el else ""

                # 获取帖子链接（用于唯一 ID）
                time_link = await article.query_selector("time")
                post_url = ""
                post_id = ""
                post_date = None
                
                if time_link:
                    date_text = await time_link.get_attribute("datetime") or ""
                    # datetime 属性格式: "2025-04-24T11:14:00.000Z"
                    if date_text:
                        try:
                            post_date = datetime.fromisoformat(date_text.replace("Z", "+00:00"))
                        except:
                            pass
                    
                    # 找父链接获取帖子 URL
                    parent_link = await time_link.evaluate_handle(
                        "el => el.closest('a')"
                    )
                    if parent_link:
                        href = await parent_link.get_attribute("href")
                        if href and "/status/" in href:
                            post_url = f"https://x.com{href}" if href.startswith("/") else href
                            post_id = href.split("/status/")[-1].split("/")[0]

                if not post_id:
                    # 备用：用文本内容做 ID
                    post_id = text[:50] if text else f"scroll_{scroll_num}"

                if post_id in seen_ids:
                    continue
                seen_ids.add(post_id)

                # 检查日期是否超出范围
                if post_date:
                    if post_date < oldest_date_seen:
                        oldest_date_seen = post_date
                    if post_date < cutoff_date:
                        stop_scrolling = True
                        continue

                if not text:
                    continue

                # 获取互动数据
                likes = 0
                retweets = 0
                replies = 0
                
                try:
                    like_btn = await article.query_selector('[data-testid="like"]')
                    if like_btn:
                        like_text = await like_btn.inner_text()
                        likes = int(re.sub(r'[^\d]', '', like_text) or '0')
                except:
                    pass
                
                try:
                    rt_btn = await article.query_selector('[data-testid="retweet"]')
                    if rt_btn:
                        rt_text = await rt_btn.inner_text()
                        retweets = int(re.sub(r'[^\d]', '', rt_text) or '0')
                except:
                    pass

                try:
                    reply_btn = await article.query_selector('[data-testid="reply"]')
                    if reply_btn:
                        reply_text = await reply_btn.inner_text()
                        replies = int(re.sub(r'[^\d]', '', reply_text) or '0')
                except:
                    pass

                posts.append({
                    "id": post_id,
                    "username": username,
                    "text": text,
                    "url": post_url or f"https://x.com/{username}/status/{post_id}",
                    "date": post_date.isoformat() if post_date else None,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                })

            except Exception as e:
                continue

        # 检查是否已超出时间范围
        if stop_scrolling:
            print(f"  ✓ 已到达 {SCAN_DAYS} 天前，停止滚动（最早帖子: {oldest_date_seen.strftime('%Y-%m-%d')}）")
            break

        # 向下滚动
        await page.keyboard.press("End")
        await page.wait_for_timeout(2000)

        # 检查是否到达页面底部
        new_articles = await page.query_selector_all('article[data-testid="tweet"]')
        if len(new_articles) == len(articles) and scroll_num > 2:
            print(f"  ✓ 页面无新内容，停止滚动（第 {scroll_num+1} 次）")
            break

        print(f"  ... 第 {scroll_num+1}/{max_scrolls} 次滚动，已抓取 {len(posts)} 条")

    print(f"  ✓ @{username} 共抓取 {len(posts)} 条帖子（{SCAN_DAYS}天内）")
    return posts


async def scan_accounts(accounts: list[str]) -> list[dict]:
    """扫描所有账号，返回 festival 相关帖子"""
    
    results = []
    
    async with async_playwright() as p:
        # 使用持久化 Profile（保留登录状态）
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
            locale="en-US",
        )
        
        # 尝试注入 Cookie（如果 Profile 不够用）
        try:
            if Path(COOKIE_FILE).exists():
                with open(COOKIE_FILE) as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
        except:
            pass

        page = await context.new_page()
        
        # 检查是否已登录
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        current_url = page.url
        
        if "login" in current_url or "flow" in current_url:
            print("⚠️  未检测到登录状态，请先运行 x_login.py 完成登录")
            print("   命令: cd /Users/dada/vibe-coding-digest && source venv/bin/activate && python3 x_login.py")
            await context.close()
            return []
        
        print(f"✅ 已登录 X，开始扫描 {len(accounts)} 个账号...\n")

        for i, username in enumerate(accounts, 1):
            username = username.lstrip("@")
            print(f"[{i}/{len(accounts)}] 扫描 @{username}")
            
            posts = await fetch_user_posts(page, username)
            
            # 筛选 festival 相关帖子
            festival_posts = []
            for post in posts:
                is_related, matched_kws = is_festival_related(post["text"])
                if is_related:
                    post["matched_keywords"] = matched_kws
                    festival_posts.append(post)
            
            print(f"  🎯 命中 {len(festival_posts)} 条 festival 相关帖子")
            results.extend(festival_posts)
            
            # 账号间间隔，避免被限速
            if i < len(accounts):
                await page.wait_for_timeout(2000)

        await context.close()
    
    return results


# ─── 输出格式化 ────────────────────────────────────────────────────────────────

def format_results(results: list[dict]) -> str:
    """格式化输出结果"""
    if not results:
        return "🔍 未找到任何 festival 相关帖子。"
    
    # 按账号分组
    by_account = {}
    for post in results:
        acc = post["username"]
        if acc not in by_account:
            by_account[acc] = []
        by_account[acc].append(post)
    
    lines = [
        f"# 🎮 Game Festival 扫描报告",
        f"扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"扫描范围：过去 {SCAN_DAYS} 天",
        f"共发现 **{len(results)}** 条相关帖子，涉及 **{len(by_account)}** 个账号",
        "",
    ]
    
    for username, posts in sorted(by_account.items()):
        lines.append(f"## @{username}（{len(posts)} 条）")
        lines.append("")
        
        # 按日期倒序
        posts.sort(key=lambda x: x.get("date") or "", reverse=True)
        
        for post in posts:
            date_str = ""
            if post.get("date"):
                try:
                    dt = datetime.fromisoformat(post["date"])
                    date_str = dt.strftime("%Y-%m-%d")
                except:
                    date_str = post["date"][:10]
            
            lines.append(f"### [{date_str}] {post['url']}")
            lines.append("")
            lines.append(f"> {post['text'][:300]}{'...' if len(post['text']) > 300 else ''}")
            lines.append("")
            lines.append(f"💬 {post['replies']} 回复  🔁 {post['retweets']} 转推  ❤️ {post['likes']} 点赞")
            lines.append(f"🏷️ 命中关键词：`{'`, `'.join(post['matched_keywords'][:5])}`")
            lines.append("")
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)


def format_notify_message(results: list[dict]) -> str:
    """格式化企业微信通知消息（简短版）"""
    if not results:
        return "🔍 Game Festival 扫描完成，未发现相关帖子。"
    
    by_account = {}
    for post in results:
        acc = post["username"]
        if acc not in by_account:
            by_account[acc] = []
        by_account[acc].append(post)
    
    lines = [
        f"🎮 **Game Festival 扫描报告**",
        f"共发现 {len(results)} 条相关帖子 | {len(by_account)} 个账号有新内容",
        "",
    ]
    
    for username, posts in sorted(by_account.items()):
        lines.append(f"**@{username}**（{len(posts)} 条）")
        # 只显示最新的 2 条
        posts.sort(key=lambda x: x.get("date") or "", reverse=True)
        for post in posts[:2]:
            date_str = (post.get("date") or "")[:10]
            preview = post["text"][:100].replace("\n", " ")
            lines.append(f"• [{date_str}] {preview}...")
            lines.append(f"  🔗 {post['url']}")
        if len(posts) > 2:
            lines.append(f"  ...还有 {len(posts)-2} 条")
        lines.append("")
    
    return "\n".join(lines)


# ─── 主入口 ────────────────────────────────────────────────────────────────────

async def main():
    global SCAN_DAYS
    parser = argparse.ArgumentParser(description="X Game Festival 扫描器")
    parser.add_argument("--accounts", nargs="+", help="要扫描的账号列表（不含@）")
    parser.add_argument("--days", type=int, default=SCAN_DAYS, help=f"扫描天数（默认 {SCAN_DAYS}）")
    parser.add_argument("--notify", action="store_true", help="扫描完成后发送企业微信通知")
    parser.add_argument("--output", default=OUTPUT_FILE, help="结果输出 JSON 路径")
    args = parser.parse_args()

    SCAN_DAYS = args.days
    accounts = args.accounts or DEFAULT_ACCOUNTS

    print(f"🎮 Game Festival Scanner")
    print(f"   账号数量: {len(accounts)}")
    print(f"   扫描范围: 过去 {SCAN_DAYS} 天")
    print(f"   关键词数: {len(FESTIVAL_KEYWORDS)}")
    print("=" * 50)

    results = await scan_accounts(accounts)

    # 保存 JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump({
            "scan_time": datetime.now().isoformat(),
            "scan_days": SCAN_DAYS,
            "accounts": accounts,
            "total": len(results),
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {args.output}")

    # 打印格式化报告
    report = format_results(results)
    print("\n" + "=" * 50)
    print(report)

    # 保存 Markdown 报告
    md_path = args.output.replace(".json", ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📄 Markdown 报告: {md_path}")

    return results


if __name__ == "__main__":
    asyncio.run(main())

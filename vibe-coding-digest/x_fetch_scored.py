#!/usr/bin/env python3
"""
X/Twitter 抓取 + 影响力评分脚本
评分维度：
  1. 博主影响力 (Author Score)    - 粉丝数、认证状态
  2. 互动热度 (Engagement Score)  - likes、retweets、replies、views
  3. 内容相关性 (Relevance Score) - 关键词匹配深度
  4. 时效性 (Freshness Score)     - 发布时间距今
"""
import asyncio, json, re, math, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from playwright.async_api import async_playwright
import urllib.parse

COOKIE_FILE = "x_cookies.json"

# ─── 广告/垃圾账号黑名单 ────────────────────────────────────
# handle（不含@）全小写
SPAM_ACCOUNTS = {
    "interactivebrokers", "ibkr", "coinbase", "binance", "okx",
    "kucoin", "bybit", "bitget", "cryptocom", "gemini",
    "superform", "aave", "uniswap", "compound",
    # 可持续追加
}

# ─── 垃圾内容特征 ────────────────────────────────────────────
SPAM_PATTERNS = [
    "Here's a high-quality", "Here's a high quality",
    "under 270 characters", "quote comment for", "reply comment for",
    "Deposit USDC", "earn yield", "SuperVault",
    "crypto trading", "sign up now", "limited offer",
    "100x", "airdrop", "nft mint",
]

def is_spam(text: str, handle: str = "") -> bool:
    # 账号黑名单
    if handle.lower().lstrip("@") in SPAM_ACCOUNTS:
        return True
    # 内容特征
    for p in SPAM_PATTERNS:
        if p.lower() in text.lower():
            return True
    return False

# ─── 工具函数 ───────────────────────────────────────────────

def parse_count(s: str) -> int:
    """解析 '1.2K', '34', '5M' 等为整数"""
    if not s:
        return 0
    s = str(s).strip().replace(',', '')
    try:
        if s.endswith('K') or s.endswith('k'):
            return int(float(s[:-1]) * 1000)
        if s.endswith('M') or s.endswith('m'):
            return int(float(s[:-1]) * 1_000_000)
        return int(float(s))
    except:
        return 0

# ─── 粉丝数缓存（避免重复抓同一用户主页）─────────────────────
_followers_cache: dict = {}

async def fetch_followers(page, handle: str) -> int:
    """访问用户主页抓取粉丝数，带缓存"""
    clean_handle = handle.lstrip("@").strip()
    if not clean_handle:
        return 0
    if clean_handle in _followers_cache:
        return _followers_cache[clean_handle]
    try:
        await page.goto(f"https://x.com/{clean_handle}", timeout=20000)
        await page.wait_for_timeout(3000)
        # 粉丝数选择器
        follower_el = await page.query_selector('a[href$="/followers"] span span')
        if not follower_el:
            follower_el = await page.query_selector('[data-testid="UserProfileHeader_Items"] a[href*="followers"] span')
        if follower_el:
            text = await follower_el.inner_text()
            count = parse_count(text)
            _followers_cache[clean_handle] = count
            return count
    except Exception as e:
        pass
    _followers_cache[clean_handle] = 0
    return 0

# 关键词分类
M1_KWS = [
    "vibe coding game", "ai game dev", "cursor unity",
    "claude game", "llm game development", "AI NPC",
]
M2_KWS = [
    "vibe coding", "cursor ide", "claude code",
    "AI coding agent", "windsurf ide",
]

# ─── 评分函数 ───────────────────────────────────────────────

def author_score(followers: int, verified: bool) -> float:
    """
    博主影响力得分 (0-40分)
    - 粉丝数对数映射：log10(followers+1) * 8，上限 35 分
    - 认证加 5 分
    """
    follower_score = min(math.log10(followers + 1) * 8, 35)
    verify_bonus = 5 if verified else 0
    return round(follower_score + verify_bonus, 1)

def engagement_score(likes: int, retweets: int, replies: int, views: int) -> float:
    """
    互动热度得分 (0-40分)
    权重：likes*1 + retweets*3 + replies*2，再用 views 做归一化修正
    对数映射后映射到 0-40
    """
    raw = likes * 1 + retweets * 3 + replies * 2
    # views 修正：互动率 = raw / views（避免水军高赞）
    if views > 0:
        engagement_rate = raw / views
        view_factor = min(engagement_rate * 1000, 1.5)  # 互动率加成，上限 1.5x
    else:
        view_factor = 1.0
    adjusted = raw * view_factor
    score = min(math.log10(adjusted + 1) * 10, 40)
    return round(score, 1)

def relevance_score(text: str, kw: str) -> float:
    """
    内容相关性得分 (0-10分)
    - 关键词出现次数
    - 是否包含核心词（ai/game/code/cursor/vibe）
    """
    text_lower = text.lower()
    kw_lower = kw.lower()
    
    # 关键词命中次数
    kw_hits = text_lower.count(kw_lower.split()[0]) if kw_lower else 0
    kw_score = min(kw_hits * 2, 5)
    
    # 核心词加分
    core_words = ['ai', 'game', 'vibe cod', 'cursor', 'claude', 'llm', 'agent', 'unity', 'unreal']
    core_hits = sum(1 for w in core_words if w in text_lower)
    core_score = min(core_hits * 1.5, 5)
    
    return round(kw_score + core_score, 1)

def freshness_score(pub_time_str: str) -> float:
    """
    时效性得分 (0-10分)
    - 0-6h: 10分
    - 6-12h: 8分
    - 12-24h: 6分
    - 24-48h: 3分
    - >48h: 0分
    """
    if not pub_time_str:
        return 5.0  # 未知时间给中间分
    try:
        pub_time = datetime.fromisoformat(pub_time_str.replace('Z', '+00:00'))
        hours_ago = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
        if hours_ago <= 6:
            return 10.0
        elif hours_ago <= 12:
            return 8.0
        elif hours_ago <= 24:
            return 6.0
        elif hours_ago <= 48:
            return 3.0
        else:
            return 0.0
    except:
        return 5.0

def total_score(author_s, engagement_s, relevance_s, freshness_s) -> float:
    """综合得分 (0-100)"""
    return round(author_s + engagement_s + relevance_s + freshness_s, 1)

def score_level(score: float) -> str:
    if score >= 70:
        return "🔥 高价值"
    elif score >= 45:
        return "⭐ 中等"
    elif score >= 20:
        return "💬 普通"
    else:
        return "🔇 低价值"

# ─── 抓取函数 ───────────────────────────────────────────────

async def scrape_tweets(page, kw: str, max_tweets: int = 15) -> list:
    url = f"https://x.com/search?q={urllib.parse.quote(kw)}&f=live"
    results = []
    try:
        await page.goto(url, timeout=25000)
        await page.wait_for_timeout(4000)
        await page.wait_for_selector('article[data-testid="tweet"]', timeout=12000)

        # 滚动加载更多
        for _ in range(3):
            await page.evaluate('window.scrollBy(0, 1000)')
            await page.wait_for_timeout(1200)

        tweets = await page.query_selector_all('article[data-testid="tweet"]')
        print(f"  [{kw}] 找到 {len(tweets)} 条原始推文")

        for tweet in tweets[:max_tweets]:
            try:
                # 推文文本
                text_el = await tweet.query_selector('[data-testid="tweetText"]')
                text = await text_el.inner_text() if text_el else ""
                if not text:
                    continue

                # 链接
                link_el = await tweet.query_selector('a[href*="/status/"]')
                href = await link_el.get_attribute("href") if link_el else ""
                tweet_url = f"https://x.com{href}" if href and href.startswith("/") else href
                if not tweet_url:
                    continue

                # 时间
                time_el = await tweet.query_selector('time')
                pub_time = await time_el.get_attribute("datetime") if time_el else ""

                # 作者名 + handle
                user_el = await tweet.query_selector('[data-testid="User-Name"]')
                author_text = await user_el.inner_text() if user_el else ""
                author_lines = author_text.strip().split('\n')
                author_name = author_lines[0] if author_lines else ""
                author_handle = author_lines[1] if len(author_lines) > 1 else ""

                # 垃圾过滤（文本 + 账号）
                if is_spam(text, author_handle):
                    print(f"    ⛔ 过滤垃圾: @{author_handle} - {text[:40]}")
                    continue

                # 认证标志
                verified_el = await tweet.query_selector('[data-testid="icon-verified"]')
                verified = verified_el is not None

                # 互动数据 - likes
                like_el = await tweet.query_selector('[data-testid="like"] span[data-testid="app-text-transition-container"]')
                likes_str = await like_el.inner_text() if like_el else "0"

                # retweets
                rt_el = await tweet.query_selector('[data-testid="retweet"] span[data-testid="app-text-transition-container"]')
                rt_str = await rt_el.inner_text() if rt_el else "0"

                # replies
                reply_el = await tweet.query_selector('[data-testid="reply"] span[data-testid="app-text-transition-container"]')
                reply_str = await reply_el.inner_text() if reply_el else "0"

                # views
                view_el = await tweet.query_selector('a[href*="/analytics"] span[data-testid="app-text-transition-container"]')
                views_str = await view_el.inner_text() if view_el else "0"

                likes = parse_count(likes_str)
                retweets = parse_count(rt_str)
                replies = parse_count(reply_str)
                views = parse_count(views_str)

                results.append({
                    "kw": kw,
                    "text": text.replace('\n', ' ').strip(),
                    "url": tweet_url,
                    "author_name": author_name,
                    "author_handle": author_handle,
                    "verified": verified,
                    "followers": -1,  # 待后续批量抓取
                    "pub_time": pub_time,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "views": views,
                })
            except Exception as e:
                continue

    except Exception as e:
        print(f"  [{kw}] 失败: {e}")

    return results


PROFILE_DIR = str(Path(__file__).parent / "x_browser_profile")

async def main():
    # ─── 检查是否已登录（持久化 profile 是否存在）──────────
    if not Path(PROFILE_DIR).exists():
        print("❌ 尚未登录！请先运行：python3 x_login.py")
        sys.exit(1)

    all_results = []
    async with async_playwright() as p:
        # 使用持久化 Context，自动复用登录状态，无需 Cookie 文件
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=True,
            args=["--no-sandbox"],
            viewport={"width": 1280, "height": 800},
        )
        page = context.pages[0] if context.pages else await context.new_page()

        # ─── 验证登录状态 ────────────────────────────────────
        print("🔍 验证登录状态...")
        await page.goto("https://x.com/home", timeout=20000)
        await page.wait_for_timeout(3000)
        cur_url = page.url
        if "login" in cur_url or "signin" in cur_url:
            print("❌ 登录状态已失效，请重新运行：python3 x_login.py")
            await context.close()
            sys.exit(1)
        print("✅ 登录状态有效，开始抓取...\n")

        print("=== 抓取 M1 关键词 ===")
        for kw in M1_KWS:
            tweets = await scrape_tweets(page, kw)
            for t in tweets:
                t["module"] = "M1"
            all_results.extend(tweets)
            await page.wait_for_timeout(1500)

        print("=== 抓取 M2 关键词 ===")
        for kw in M2_KWS:
            tweets = await scrape_tweets(page, kw)
            for t in tweets:
                t["module"] = "M2"
            all_results.extend(tweets)
            await page.wait_for_timeout(1500)

        # ─── 去重 ───────────────────────────────────────────
        seen = set()
        unique = []
        for r in all_results:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique.append(r)
        print(f"\n去重后共 {len(unique)} 条，开始抓取博主粉丝数...")

        # ─── 批量抓取粉丝数（只对高互动推文的博主才抓，节省时间）──
        # 筛选条件：likes+retweets > 5 或者有认证
        priority_handles = {
            r["author_handle"].lstrip("@").strip()
            for r in unique
            if (r["likes"] + r["retweets"] > 5 or r["verified"])
            and r["author_handle"]
        }
        handles_to_fetch = list(priority_handles - set(_followers_cache.keys()))
        print(f"共 {len(handles_to_fetch)} 个高互动博主需要抓取粉丝数（低互动博主跳过）")

        for i, handle in enumerate(handles_to_fetch):
            followers = await fetch_followers(page, handle)
            print(f"  [{i+1}/{len(handles_to_fetch)}] @{handle} → {followers:,} 粉丝")
            await page.wait_for_timeout(800)

        # 回填粉丝数 + 计算评分
        for r in unique:
            handle = r["author_handle"].lstrip("@").strip()
            followers = _followers_cache.get(handle, 0)
            r["followers"] = followers

            a_score = author_score(followers, r["verified"])
            e_score = engagement_score(r["likes"], r["retweets"], r["replies"], r["views"])
            r_score = relevance_score(r["text"], r["kw"])
            f_score = freshness_score(r["pub_time"])
            t_score = total_score(a_score, e_score, r_score, f_score)

            r["score_author"] = a_score
            r["score_engagement"] = e_score
            r["score_relevance"] = r_score
            r["score_freshness"] = f_score
            r["score_total"] = t_score
            r["score_level"] = score_level(t_score)

        await context.close()

    # 按总分排序
    unique.sort(key=lambda x: x["score_total"], reverse=True)

    # 保存 JSON
    with open("/tmp/x_scored.json", "w") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 共 {len(unique)} 条（去重），已保存到 /tmp/x_scored.json")

    # 生成 MD
    generate_md(unique)


def generate_md(results: list):
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone(timedelta(hours=8)))

    m1 = [r for r in results if r["module"] == "M1"]
    m2 = [r for r in results if r["module"] == "M2"]

    lines = []
    lines.append("# 🐦 X/Twitter 抓取结果（含影响力评分）")
    lines.append(f"> 生成时间：{now.strftime('%Y-%m-%d %H:%M')} CST | 共 {len(results)} 条")
    lines.append("")
    lines.append("## 📊 评分体系说明")
    lines.append("")
    lines.append("| 维度 | 满分 | 说明 |")
    lines.append("|------|------|------|")
    lines.append("| 🧑 博主影响力 | 40 | 粉丝数（对数映射）+ 认证状态 |")
    lines.append("| 🔥 互动热度 | 40 | likes×1 + retweets×3 + replies×2，views 修正 |")
    lines.append("| 🎯 内容相关性 | 10 | 关键词命中深度 + 核心词覆盖 |")
    lines.append("| ⏱️ 时效性 | 10 | 0-6h满分，>48h零分 |")
    lines.append("| **综合** | **100** | 四维加权总分 |")
    lines.append("")
    lines.append("**评级：** 🔥 高价值(≥70) | ⭐ 中等(45-70) | 💬 普通(20-45) | 🔇 低价值(<20)")
    lines.append("")

    def render_section(title, items):
        lines.append(f"## {title}（{len(items)} 条，按评分排序）")
        lines.append("")
        for i, r in enumerate(items, 1):
            pub = r["pub_time"][:16].replace("T", " ") if r.get("pub_time") else "未知"
            verified_badge = " ✅" if r.get("verified") else ""
            lines.append(f"### {i}. {r['score_level']} **{r['score_total']}分** | @{r['author_name']}{verified_badge}")
            lines.append(f"> 🔍 `{r['kw']}` | 🕐 {pub} UTC | ❤️ {r['likes']} | 🔁 {r['retweets']} | 💬 {r['replies']} | 👁️ {r['views']}")
            lines.append(f"> 📊 博主:{r['score_author']} + 互动:{r['score_engagement']} + 相关:{r['score_relevance']} + 时效:{r['score_freshness']}")
            lines.append("")
            lines.append(r["text"][:300])
            lines.append("")
            lines.append(f"🔗 {r['url']}")
            lines.append("")
            lines.append("---")
            lines.append("")

    render_section("🎮 M1：AI + 游戏", m1)
    render_section("🤖 M2：AI 通用", m2)

    md_content = "\n".join(lines)
    out_path = "/Users/dada/vibe-coding-digest/x_preview.md"
    with open(out_path, "w") as f:
        f.write(md_content)
    print(f"✅ MD 已生成：{out_path} ({len(md_content)} 字符)")


if __name__ == "__main__":
    asyncio.run(main())
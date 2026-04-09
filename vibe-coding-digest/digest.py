#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 AI Game Dev & Vibe Coding Daily Digest v3.0
工作流版本：v0.5

模块一：【AI + 游戏】
  严格平台顺序：KM → 微信公众号 → X → Reddit ✅ → HN → Dev.to → RSS → ProductHunt → GitHub Trending
  前三个平台穷尽 24h 内容

模块二：【AI 通用】
  多渠道综合抓取

关键词策略：
  国内平台（KM/微信）：中文为主 + 英文补充
  X：英文为主 + 中文补充
  国外平台（Reddit/HN/Dev.to/GitHub等）：纯英文
"""

import requests
import feedparser
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════════════════════════
#  关键词配置 — 按平台语言差异化
# ═══════════════════════════════════════════════════════════════

# ── 模块一：KM（中文为主 + 英文补充）──────────────────────────
KW_KM_M1_ZH = [
    "游戏开发 AI", "AI 游戏开发", "游戏 AI 编程", "AI 游戏编程",
    "Unity AI", "Unity 人工智能", "Unity 智能编程",
    "Unreal AI", "UE5 AI", "虚幻引擎 AI",
    "Godot AI",
    "vibe coding", "AI 编程", "AI 辅助开发", "AI 辅助游戏开发",
    "智能编程", "AI 代码生成",
    "Cursor 游戏", "Cursor Unity", "Cursor Unreal",
    "Claude 游戏开发", "Copilot 游戏",
    "游戏开发经验", "独立游戏 AI", "游戏开发 tips",
    "AI NPC", "程序化生成 AI",
]
KW_KM_M1_EN = [
    "vibe coding game", "ai game development",
    "unity cursor", "unreal cursor", "godot cursor",
    "unity copilot", "unreal copilot",
    "llm game", "ai gamedev",
]
KW_KM_M1 = KW_KM_M1_ZH + KW_KM_M1_EN

# ── 模块一：X/Twitter（英文为主 + 中文补充）────────────────────
KW_X_M1_EN = [
    "vibe coding game", "vibe coding unity", "vibe coding unreal", "vibe coding godot",
    "ai game dev", "ai game development", "ai gamedev",
    "cursor unity", "cursor unreal", "cursor godot",
    "claude unity", "claude unreal", "claude godot",
    "copilot unity", "copilot unreal", "copilot godot",
    "llm game dev", "llm unity", "llm unreal", "llm godot",
    "ai game workflow", "ai indie game", "ai npc",
    "game dev ai tips", "ai assisted game dev",
    "procedural generation ai",
]
KW_X_M1_ZH = [
    "游戏开发 AI", "vibe coding 游戏", "Unity AI 开发",
    "Unreal AI", "Godot AI", "AI 游戏编程", "Cursor 游戏开发",
]
KW_X_M1 = KW_X_M1_EN + KW_X_M1_ZH

# ── 模块一：国外平台（HN / Dev.to / Reddit / GitHub）纯英文 ───
KW_EN_M1 = [
    "vibe coding game", "ai game development", "ai gamedev",
    "unity ai", "unreal ai", "godot ai",
    "cursor game", "claude game", "llm game",
    "ai indie game", "ai npc", "game ai tools",
    "vibe coding unity", "vibe coding unreal", "vibe coding godot",
    "ai game workflow", "ai game programming",
    "procedural generation ai", "unity llm", "unreal llm", "godot llm",
    "unity cursor", "unreal cursor", "godot cursor",
    "unity copilot", "unreal copilot", "godot copilot",
]

# ── 模块二：国内平台（KM/微信）中文为主 ───────────────────────
KW_M2_ZH = [
    "vibe coding", "AI 编程", "AI 辅助编程", "AI 代码助手",
    "智能编程", "AI IDE", "AI 开发工具",
    "Cursor", "Cursor AI", "Cursor 教程", "Cursor 使用技巧",
    "Claude Code", "Windsurf", "Copilot",
    "bolt.new", "v0.dev",
    "大模型", "LLM", "GPT", "Claude", "Gemini",
    "AI Agent", "AI 工作流", "Agentic Coding",
    "OpenAI", "Anthropic",
    "AI 提效", "AI 开发效率", "程序员 AI",
]

# ── 模块二：国外平台 纯英文 ────────────────────────────────────
KW_M2_EN = [
    "vibe coding", "vibe-coding",
    "cursor ide", "cursor ai",
    "windsurf ide", "windsurf ai",
    "claude code",
    "ai agent ide", "agentic coding",
    "copilot agent", "github copilot agent",
    "bolt.new", "v0.dev",
    "devin ai", "codeium",
    "ai coding assistant", "llm coding",
    "ai pair programming", "coding agent",
    "ai ide", "ai coding",
    "openai", "anthropic", "ai developer tools",
]

# ── 模块二：X（英文为主 + 中文补充）──────────────────────────
KW_X_M2_EN = KW_M2_EN
KW_X_M2_ZH = [
    "vibe coding", "AI 编程", "Cursor 使用", "Claude Code",
    "AI 开发工具", "大模型编程",
]
KW_X_M2 = KW_X_M2_EN + KW_X_M2_ZH

# ── 合并（用于通用匹配）──────────────────────────────────────
ALL_KEYWORDS_M1 = list(set(KW_KM_M1 + KW_X_M1 + KW_EN_M1))
ALL_KEYWORDS_M2 = list(set(KW_M2_ZH + KW_M2_EN))
ALL_KEYWORDS = list(set(ALL_KEYWORDS_M1 + ALL_KEYWORDS_M2))

# ═══════════════════════════════════════════════════════════════
#  全局配置
# ═══════════════════════════════════════════════════════════════

HOURS_BACK = 24
MAX_ITEMS_PER_SOURCE = 15

# RSS 订阅源（按语言区分）
RSS_FEEDS_ZH = [
    ("少数派",      "https://sspai.com/feed"),
    ("36kr",        "https://36kr.com/feed"),
    ("机器之心",    "https://www.jiqizhixin.com/rss"),
]
RSS_FEEDS_EN = [
    ("Game Developer",         "https://www.gamedeveloper.com/rss.xml"),
    ("Unity Blog",             "https://blog.unity.com/feed"),
    ("Simon Willison's Blog",  "https://simonwillison.net/atom/everything/"),
    ("DEV.to AI",              "https://dev.to/feed/tag/ai"),
    ("DEV.to GameDev",         "https://dev.to/feed/tag/gamedev"),
]

# ═══════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════

def is_within_hours(dt, hours=24):
    if dt is None:
        return True
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=hours)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt >= cutoff

def classify_module(text):
    """
    判断内容属于哪个模块，以及在模块一中的优先级
    返回：(module, priority_label)
    module: "M1" / "M2" / None
    """
    text_lower = (text or "").lower()
    # 先判断是否属于模块一（游戏×AI）
    if any(kw.lower() in text_lower for kw in ALL_KEYWORDS_M1):
        return "M1", "🎮 AI+游戏"
    # 再判断是否属于模块二（AI通用）
    if any(kw.lower() in text_lower for kw in ALL_KEYWORDS_M2):
        return "M2", "🤖 AI通用"
    return None, "其他"

def matches_keywords(text, keywords):
    """检查文本是否包含关键词列表中的任意一个"""
    text_lower = (text or "").lower()
    return any(kw.lower() in text_lower for kw in keywords)

def truncate(text, max_len=200):
    if not text:
        return ""
    text = text.strip().replace("\n", " ")
    return text[:max_len] + "…" if len(text) > max_len else text

def safe_get(url, params=None, headers=None, timeout=15):
    try:
        h = {"User-Agent": "AIGameDevDigest/3.0 (daily digest bot)"}
        if headers:
            h.update(headers)
        resp = requests.get(url, params=params, headers=h, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  ⚠️  请求失败 {url}: {e}", file=sys.stderr)
        return None

def make_item(title, url, source, platform_order, meta="", summary="", full_summary="", score=0, module="M2", priority_label="🤖 AI通用"):
    return {
        "title": title,
        "url": url,
        "title_zh": "",              # 中文翻译标题（英文平台由 Claude 填充）
        "source": source,
        "platform_order": platform_order,  # 平台顺序（模块一用）
        "meta": meta,
        "summary": summary,          # 简短摘要（150字以内，用于模块二 & 通知）
        "full_summary": full_summary, # 完整总结（原文20%字数，用于模块一）
        "score": score,
        "module": module,
        "priority_label": priority_label,
    }

# 英文平台集合（这些平台的内容需要翻译成中文）
ENGLISH_PLATFORMS = {"X/Twitter", "Reddit", "HackerNews", "Dev.to", "ProductHunt", "GitHub"}

def is_english_platform(source):
    """判断是否为英文平台（需要翻译）"""
    for p in ENGLISH_PLATFORMS:
        if p.lower() in source.lower():
            return True
    # RSS 英文源
    if source.startswith("RSS·") and any(
        en in source for en in ["Game Developer", "Unity Blog", "Simon Willison", "DEV.to"]
    ):
        return True
    return False

# ═══════════════════════════════════════════════════════════════
#  平台 1：KM（腾讯内部）— 中文为主 + 英文补充
#  平台顺序：1（模块一最高优先级）
# ═══════════════════════════════════════════════════════════════

def fetch_km():
    """
    抓取 KM（腾讯内部知识管理平台）
    语言策略：中文为主 + 英文补充
    覆盖要求：穷尽 24h 内容
    平台顺序：1

    数据来源：读取 fetch_km_mcp.py 生成的 km_results.json
    """
    print("📡 [1/9] 抓取 KM（腾讯内部）...")

    km_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "km_results.json")

    if not os.path.exists(km_json_path):
        print("  ⚠️  km_results.json 不存在，跳过 KM 模块")
        print("  💡 提示：请先运行 fetch_km_mcp.py 生成 KM 数据")
        return []

    try:
        with open(km_json_path, "r", encoding="utf-8") as f:
            km_data = json.load(f)
    except Exception as e:
        print(f"  ❌ 读取 km_results.json 失败: {e}", file=sys.stderr)
        return []

    # 检查数据时效性（超过 2 小时则警告）
    generated_at_str = km_data.get("generated_at", "")
    if generated_at_str:
        try:
            generated_at = datetime.fromisoformat(generated_at_str)
            age_minutes = (datetime.now() - generated_at).total_seconds() / 60
            if age_minutes > 120:
                print(f"  ⚠️  KM 数据已有 {int(age_minutes)} 分钟，建议重新抓取")
            else:
                print(f"  ✅ KM 数据时效：{int(age_minutes)} 分钟前生成")
        except Exception:
            pass

    articles = km_data.get("articles", [])
    results = []

    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        if not title or not url:
            continue

        module = article.get("module", "M2")
        priority_label = "🎮 AI+游戏" if module == "M1" else "🤖 AI通用"

        # 构建 meta 信息
        meta_parts = ["📚 KM"]
        if article.get("author"):
            meta_parts.append(f"作者: {article['author']}")
        if article.get("km_recommended"):
            meta_parts.append("⭐KM推荐")
        if article.get("km_headline"):
            meta_parts.append("🔥头条")
        if article.get("kbar"):
            # 提取 K 吧名称（去掉链接部分）
            kbar = article["kbar"]
            kbar_name = kbar.split("https://")[0].strip().rstrip()
            # 去掉 "#12345 " 前缀
            import re
            kbar_name = re.sub(r"#\d+\s+", "", kbar_name).strip()
            if kbar_name:
                meta_parts.append(f"📂{kbar_name}")

        meta = " | ".join(meta_parts)

        # 分数：优先用热度，其次用阅读数
        score = article.get("hot_value", 0) or article.get("read_count", 0)

        # full_summary：优先用 AI 摘要（ai_summary），其次用正文摘要（summary）
        ai_summary = article.get("ai_summary", "")
        article_summary = article.get("summary", "")
        full_summary = ai_summary or article_summary  # 完整20%总结用
        short_summary = truncate(article_summary or ai_summary, 150)  # 短摘要用于通知

        if not short_summary and article.get("tags"):
            short_summary = f"标签：{article['tags']}"

        results.append(make_item(
            title=title,
            url=url,
            source="KM",
            platform_order=1,
            meta=meta,
            summary=short_summary,
            full_summary=full_summary,
            score=score,
            module=module,
            priority_label=priority_label,
        ))

    m1_count = sum(1 for r in results if r["module"] == "M1")
    m2_count = sum(1 for r in results if r["module"] == "M2")
    print(f"  ✅ KM 加载 {len(results)} 条（M1:{m1_count} M2:{m2_count}）")
    return results


def inject_km_results(km_raw_items):
    """
    将 KM MCP 工具返回的结果转换为标准格式
    km_raw_items: list of dict，每项包含 title, url, summary 等字段
    """
    results = []
    for item in km_raw_items:
        title = item.get("title", "")
        url = item.get("url", "")
        summary = item.get("summary", item.get("abstract", ""))
        combined = title + " " + summary

        module, priority_label = classify_module(combined)
        if module is None:
            continue

        results.append(make_item(
            title=title,
            url=url,
            source="KM",
            platform_order=1,
            meta=f"📚 KM | {item.get('author', '')}",
            summary=truncate(summary, 150),
            score=item.get("read_count", 0),
            module=module,
            priority_label=priority_label,
        ))

    print(f"  ✅ KM 注入 {len(results)} 条")
    return results

# ═══════════════════════════════════════════════════════════════
#  平台 2：微信公众号（搜狗微信搜索）
#  平台顺序：2
# ═══════════════════════════════════════════════════════════════

def fetch_wechat():
    """
    微信公众号抓取 — 通过搜狗微信搜索（weixin.sogou.com）
    语言策略：中文为主 + 英文补充
    覆盖要求：穷尽 24h 内容（多关键词覆盖，按相关度排序）
    平台顺序：2

    说明：
    - 使用 HTTP（非HTTPS）访问搜狗微信，规避 SSL 问题
    - tsn 时间过滤（1天/1周）会导致结果为空，改为不过滤时间，
      依赖多关键词覆盖 + 搜狗默认相关度排序
    - 链接为搜狗跳转链接（http://weixin.sogou.com/link?url=...）
    """
    import warnings
    warnings.filterwarnings('ignore')

    print("📡 [2/9] 抓取微信公众号（搜狗微信搜索）...")

    SOGOU_BASE = "http://weixin.sogou.com/weixin"
    SOGOU_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "http://weixin.sogou.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    # ── 关键词列表（中文为主 + 英文补充，模块一优先）──────────────
    # 模块一（AI + 游戏）关键词
    WECHAT_KW_M1 = [
        "AI游戏开发", "游戏AI", "Unity AI开发", "Unreal AI",
        "Godot AI", "AI游戏编程", "vibe coding游戏",
        "Cursor游戏开发", "Claude游戏", "AI NPC",
        "AI独立游戏", "游戏开发AI工具",
        "vibe coding game", "ai gamedev",
        "Cocos AI", "AI游戏策划", "AI游戏美术", "AI关卡设计", "AI生成游戏",
    ]
    # 模块二（AI 通用）关键词
    WECHAT_KW_M2 = [
        "vibe coding", "AI编程", "Cursor AI", "Claude Code",
        "Windsurf IDE", "AI代码助手", "AI辅助编程",
        "大模型编程", "AI开发工具", "AI IDE",
        "cursor使用技巧", "claude使用",
    ]
    all_wechat_kw = WECHAT_KW_M1 + WECHAT_KW_M2

    results = []
    seen_urls = set()

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("  ⚠️  缺少 beautifulsoup4，跳过微信公众号抓取")
        print("  💡 安装：pip install beautifulsoup4")
        return []

    import re as _re

    # 48h 时间窗口（覆盖今日 + 昨日）
    _now_ts = time.time()
    _cutoff_ts = _now_ts - 48 * 3600

    def _parse_sogou_ts(art_el):
        """从搜狗文章元素中提取 Unix 时间戳，失败返回 None"""
        s2_el = art_el.select_one(".s2")
        if not s2_el:
            return None
        script_text = s2_el.get_text()
        m = _re.search(r"timeConvert\('(\d+)'\)", script_text)
        if not m:
            # 也尝试从 script 标签原始 HTML 中找
            raw = str(s2_el)
            m = _re.search(r"timeConvert\('(\d+)'\)", raw)
        if m:
            return int(m.group(1))
        return None

    def _search_sogou(query, max_pages=1):
        """搜索单个关键词，返回文章列表（仅保留 48h 内）"""
        items = []
        for page in range(1, max_pages + 1):
            try:
                resp = requests.get(
                    SOGOU_BASE,
                    params={"type": "2", "query": query, "ie": "utf8", "page": page},
                    headers=SOGOU_HEADERS,
                    timeout=12,
                    verify=False,
                )
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, "html.parser")
                articles = soup.select("ul.news-list li")
                if not articles:
                    break

                page_has_recent = False  # 本页是否有 48h 内的文章
                for art in articles:
                    title_el = art.select_one("h3 a")
                    summary_el = art.select_one(".txt-info")
                    account_el = art.select_one(".all-time-y2")
                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    href = title_el.get("href", "")
                    # 构造完整搜狗跳转链接
                    if href.startswith("/"):
                        url = f"http://weixin.sogou.com{href}"
                    elif href.startswith("http"):
                        url = href
                    else:
                        continue

                    # ── 时间过滤：仅保留 48h 内文章 ──────────────
                    pub_ts = _parse_sogou_ts(art)
                    if pub_ts is not None:
                        if pub_ts < _cutoff_ts:
                            continue  # 超过 48h，跳过
                        page_has_recent = True
                        pub_dt = datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d %H:%M")
                    else:
                        # 时间戳解析失败时保留文章（不因解析问题漏掉内容）
                        page_has_recent = True
                        pub_dt = ""

                    summary = summary_el.get_text(strip=True) if summary_el else ""
                    account = account_el.get_text(strip=True) if account_el else "微信公众号"

                    items.append({
                        "title": title,
                        "url": url,
                        "summary": summary,
                        "account": account,
                        "pub_dt": pub_dt,
                        "pub_ts": pub_ts or 0,
                    })

                # 若本页全部文章都超过 48h，不再翻页
                if not page_has_recent and page > 1:
                    break

                time.sleep(1.2)  # 礼貌性延迟，避免触发反爬
            except Exception as e:
                print(f"  ⚠️  搜狗搜索失败 [{query}]: {e}", file=sys.stderr)
                break
        return items

    # ── 逐关键词搜索 ──────────────────────────────────────────────
    for kw in all_wechat_kw:
        # 判断该关键词属于哪个模块（用于分类）
        is_m1_kw = kw in WECHAT_KW_M1

        raw = _search_sogou(kw, max_pages=1)
        for item in raw:
            url = item["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)

            # 模块分类：先尝试内容匹配，再回退到关键词归属
            combined = item["title"] + " " + item["summary"]
            if matches_keywords(combined, KW_KM_M1):
                module, priority_label = "M1", "🎮 AI+游戏"
            elif matches_keywords(combined, KW_M2_ZH + KW_M2_EN):
                module, priority_label = "M2", "🤖 AI通用"
            elif is_m1_kw:
                module, priority_label = "M1", "🎮 AI+游戏"
            else:
                module, priority_label = "M2", "🤖 AI通用"

            pub_dt = item.get("pub_dt", "")
            meta_time = f" | 🕐 {pub_dt}" if pub_dt else ""
            results.append(make_item(
                title=item["title"],
                url=url,
                source="微信公众号",
                platform_order=2,
                meta=f"💬 微信公众号 | 📢 {item['account']}{meta_time}",
                summary=truncate(item["summary"], 150),
                score=item.get("pub_ts", 0),  # 用时间戳作 score，越新越前
                module=module,
                priority_label=priority_label,
            ))

    # 模块一优先，同模块内按发布时间倒序（最新在前）
    results.sort(key=lambda x: (0 if x["module"] == "M1" else 1, -x.get("score", 0)))

    m1_count = sum(1 for r in results if r["module"] == "M1")
    m2_count = sum(1 for r in results if r["module"] == "M2")
    print(f"  ✅ 微信公众号 获取 {len(results)} 条（M1:{m1_count} M2:{m2_count}）")
    return results

# ═══════════════════════════════════════════════════════════════
#  平台 3：X / Twitter ⏸️（待完成）
#  平台顺序：3
# ═══════════════════════════════════════════════════════════════

def fetch_x_twitter():
    """
    X (Twitter) 抓取 — Playwright 无头浏览器 + Cookie 登录
    语言策略：英文为主 + 中文补充
    覆盖要求：穷尽 24h 内容
    平台顺序：3

    前置条件：x_cookies.json 存在（通过 extract_x_cookies.py 生成）
    """
    print("📡 [3/9] 抓取 X/Twitter（Playwright）...")

    import asyncio

    COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "x_cookies.json")
    if not os.path.exists(COOKIE_FILE):
        print("  ⚠️  x_cookies.json 不存在，跳过 X 模块")
        print("  💡 提示：请先运行 extract_x_cookies.py 生成 Cookie")
        return []

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("  ⚠️  playwright 未安装，跳过 X 模块")
        return []

    with open(COOKIE_FILE) as f:
        cookies = json.load(f)

    # 48h 时间窗口
    _now = datetime.now(timezone.utc)
    _cutoff = _now - timedelta(hours=48)

    def _parse_x_time(time_str):
        """解析 X 的时间字符串，返回 datetime 或 None"""
        if not time_str:
            return None
        try:
            return datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        except Exception:
            return None

    async def _search_x(keywords_m1, keywords_m2):
        results = []
        seen_ids = set()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )
            await context.add_cookies(cookies)
            page = await context.new_page()

            # 按优先级搜索：模块一关键词先搜
            all_kw = [(kw, "M1") for kw in keywords_m1] + [(kw, "M2") for kw in keywords_m2]

            for kw, kw_module in all_kw:
                try:
                    import urllib.parse
                    encoded = urllib.parse.quote(kw)
                    url = f"https://x.com/search?q={encoded}&f=live&src=typed_query"
                    await page.goto(url, timeout=25000)
                    await page.wait_for_timeout(4000)

                    # 等待推文出现
                    try:
                        await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
                    except Exception:
                        print(f"    ⚠️  [{kw}] 未找到推文")
                        continue

                    # 滚动加载更多
                    for _ in range(2):
                        await page.evaluate("window.scrollBy(0, 800)")
                        await page.wait_for_timeout(1500)

                    tweets = await page.query_selector_all('article[data-testid="tweet"]')

                    for tweet in tweets:
                        try:
                            # 推文文本
                            text_el = await tweet.query_selector('[data-testid="tweetText"]')
                            tweet_text = await text_el.inner_text() if text_el else ""

                            # 时间
                            time_el = await tweet.query_selector("time")
                            time_str = await time_el.get_attribute("datetime") if time_el else ""
                            pub_dt = _parse_x_time(time_str)

                            # 时间过滤
                            if pub_dt and pub_dt < _cutoff:
                                continue

                            # 推文链接
                            link_el = await tweet.query_selector('a[href*="/status/"]')
                            tweet_url = ""
                            if link_el:
                                href = await link_el.get_attribute("href")
                                if href:
                                    tweet_url = f"https://x.com{href}" if href.startswith("/") else href

                            if not tweet_url:
                                continue

                            # 去重（按 URL）
                            if tweet_url in seen_ids:
                                continue
                            seen_ids.add(tweet_url)

                            # 作者
                            user_el = await tweet.query_selector('[data-testid="User-Name"]')
                            author = await user_el.inner_text() if user_el else "Unknown"
                            author = author.split("\n")[0]  # 只取第一行（显示名）

                            # 互动数（likes）
                            like_el = await tweet.query_selector('[data-testid="like"] span')
                            likes = 0
                            if like_el:
                                like_text = await like_el.inner_text()
                                try:
                                    like_text = like_text.replace("K", "000").replace("M", "000000")
                                    likes = int(like_text) if like_text.strip().isdigit() else 0
                                except Exception:
                                    likes = 0

                            # 模块分类
                            combined = tweet_text
                            if matches_keywords(combined, KW_X_M1):
                                module, priority_label = "M1", "🎮 AI+游戏"
                            elif matches_keywords(combined, KW_X_M2):
                                module, priority_label = "M2", "🤖 AI通用"
                            elif kw_module == "M1":
                                module, priority_label = "M1", "🎮 AI+游戏"
                            else:
                                module, priority_label = "M2", "🤖 AI通用"

                            pub_str = pub_dt.strftime("%Y-%m-%d %H:%M") if pub_dt else ""
                            meta_time = f" | 🕐 {pub_str}" if pub_str else ""

                            results.append(make_item(
                                title=truncate(tweet_text, 120),
                                url=tweet_url,
                                source="X/Twitter",
                                platform_order=3,
                                meta=f"🐦 X | @{author}{meta_time} | ❤️ {likes}",
                                summary=truncate(tweet_text, 200),
                                score=likes,
                                module=module,
                                priority_label=priority_label,
                            ))

                        except Exception:
                            continue

                    print(f"    ✅ [{kw}] 获取 {len(tweets)} 条推文")
                    await page.wait_for_timeout(2000)  # 礼貌延迟

                except Exception as e:
                    print(f"    ⚠️  [{kw}] 搜索失败: {e}", file=sys.stderr)
                    continue

            await browser.close()
        return results

    # 模块一关键词（英文为主）
    x_kw_m1 = [
        "vibe coding game", "vibe coding unity", "vibe coding unreal",
        "ai game dev", "ai gamedev", "cursor unity",
        "cursor unreal", "cursor godot", "llm game dev",
        "ai indie game", "ai npc game",
    ]
    # 模块二关键词（英文为主）
    x_kw_m2 = [
        "vibe coding", "cursor ide", "claude code",
        "windsurf ide", "agentic coding", "ai coding assistant",
    ]

    try:
        results = asyncio.run(_search_x(x_kw_m1, x_kw_m2))
    except Exception as e:
        print(f"  ❌ X 抓取失败: {e}", file=sys.stderr)
        return []

    # 去重 + 排序
    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: (0 if x["module"] == "M1" else 1, -x.get("score", 0))):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    m1_count = sum(1 for r in unique if r["module"] == "M1")
    m2_count = sum(1 for r in unique if r["module"] == "M2")
    print(f"  ✅ X/Twitter 获取 {len(unique)} 条（M1:{m1_count} M2:{m2_count}）")
    return unique[:MAX_ITEMS_PER_SOURCE * 2]

# ═══════════════════════════════════════════════════════════════
#  平台 4：Reddit ✅（RSS Feed 方案，已跑通）
#  平台顺序：4
# ═══════════════════════════════════════════════════════════════

def fetch_reddit():
    """
    Reddit 抓取 — RSS Feed 方案（无需 API 认证）
    语言策略：纯英文
    目标 subreddits：r/gamedev, r/Unity3D, r/unrealengine, r/godot,
                     r/LocalLLaMA, r/MachineLearning, r/learnmachinelearning
    平台顺序：4
    """
    from email.utils import parsedate_to_datetime
    import re as _re

    print("📡 [4/9] 抓取 Reddit (RSS)...")
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RSS Reader)"}

    # (subreddit, sort, time_period)
    # M1 优先的游戏相关 subreddit
    subreddits_m1 = [
        ("gamedev",       "top", "day"),
        ("Unity3D",       "top", "day"),
        ("unrealengine",  "top", "day"),
        ("godot",         "top", "day"),
    ]
    # M2 AI/编程相关 subreddit
    subreddits_m2 = [
        ("LocalLLaMA",          "hot",  None),
        ("MachineLearning",     "top",  "day"),
        ("learnmachinelearning","top",  "day"),
        ("programming",         "top",  "day"),
    ]

    cutoff_ts = time.time() - HOURS_BACK * 3600

    for sub, sort, period in subreddits_m1 + subreddits_m2:
        url = f"https://www.reddit.com/r/{sub}/{sort}.rss"
        if period:
            url += f"?t={period}"
        try:
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code != 200:
                print(f"  ⚠️ r/{sub} 返回 {r.status_code}，跳过")
                continue
            feed = feedparser.parse(r.content)
        except Exception as e:
            print(f"  ⚠️ r/{sub} 请求失败: {e}")
            continue

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link  = entry.get("link", "")
            published = entry.get("published", "")

            # 时间过滤
            try:
                pub_ts = parsedate_to_datetime(published).timestamp()
                if pub_ts < cutoff_ts:
                    continue
            except Exception:
                pass  # 解析失败则不过滤

            # 从 summary HTML 提取纯文本摘要
            summary_html = entry.get("summary", "")
            summary_text = _re.sub(r"<[^>]+>", " ", summary_html)
            summary_text = " ".join(summary_text.split())[:200]

            combined = f"{title} {summary_text}"

            # subreddits_m1（gamedev/Unity3D/unrealengine/godot）直接归入 M1
            # subreddits_m2 才走关键词分类过滤
            m1_subs = {s for s, _, _ in subreddits_m1}
            if sub in m1_subs:
                module, priority_label = "M1", "🎮 AI+游戏"
            else:
                module, priority_label = classify_module(combined)
                if module is None:
                    continue

            results.append(make_item(
                title=title,
                url=link,
                source=f"Reddit r/{sub}",
                platform_order=4,
                meta=f"🤖 Reddit r/{sub}",
                summary=summary_text[:120] if summary_text else "",
                score=0,   # RSS 不含 upvote 数
                module=module,
                priority_label=priority_label,
            ))

    # 去重
    seen = set()
    unique = []
    for item in sorted(results, key=lambda x: (0 if x["module"] == "M1" else 1, x["title"])):
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    m1 = sum(1 for r in unique if r["module"] == "M1")
    m2 = sum(1 for r in unique if r["module"] == "M2")
    print(f"  ✅ Reddit 获取 {len(unique)} 条（M1:{m1} M2:{m2}）")
    return unique[:MAX_ITEMS_PER_SOURCE]

# ═══════════════════════════════════════════════════════════════
#  平台 5：HackerNews — 纯英文
#  平台顺序：5
# ═══════════════════════════════════════════════════════════════

def fetch_hackernews():
    """
    抓取 HackerNews - Algolia API
    语言策略：纯英文
    平台顺序：5
    """
    print("📡 [5/9] 抓取 HackerNews...")
    results = []

    # 模块一（游戏×AI）关键词优先
    search_terms_m1 = [
        "vibe coding game", "ai game development",
        "unity ai", "unreal ai", "godot ai",
        "cursor unity", "cursor game",
        "vibe coding unity", "vibe coding unreal", "vibe coding godot",
        "llm game dev", "ai gamedev",
    ]
    # 模块二（AI通用）关键词
    search_terms_m2 = [
        "vibe coding", "cursor ide", "claude code",
        "windsurf", "ai agent ide", "agentic coding",
    ]

    cutoff_ts = int(time.time()) - HOURS_BACK * 3600

    for kw in search_terms_m1 + search_terms_m2:
        data = safe_get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": kw,
                "tags": "story",
                "numericFilters": f"created_at_i>{cutoff_ts}",
                "hitsPerPage": 8,
            }
        )
        if not data:
            continue

        for hit in data.get("hits", []):
            title = hit.get("title", "")
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            points = hit.get("points", 0)
            comments = hit.get("num_comments", 0)
            combined = title

            module, priority_label = classify_module(combined)
            if module is None:
                continue

            results.append(make_item(
                title=title,
                url=url,
                source="HackerNews",
                platform_order=5,
                meta=f"⬆️ {points} | 💬 {comments}",
                score=points,
                module=module,
                priority_label=priority_label,
            ))

    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: (0 if x["module"] == "M1" else 1, -x["score"])):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    print(f"  ✅ HackerNews 获取 {len(unique)} 条（M1:{sum(1 for r in unique if r['module']=='M1')} M2:{sum(1 for r in unique if r['module']=='M2')}）")
    return unique[:MAX_ITEMS_PER_SOURCE]

# ═══════════════════════════════════════════════════════════════
#  平台 6：Dev.to — 纯英文
#  平台顺序：6
# ═══════════════════════════════════════════════════════════════

def fetch_devto():
    """
    抓取 Dev.to 文章
    语言策略：纯英文
    平台顺序：6
    """
    print("📡 [6/9] 抓取 Dev.to...")
    results = []

    # 模块一优先的 tag
    tags_m1 = ["gamedev", "unity", "unrealengine", "godot"]
    # 模块二 tag
    tags_m2 = ["ai", "llm", "tooling", "productivity", "webdev"]

    for tag in tags_m1 + tags_m2:
        data = safe_get(
            "https://dev.to/api/articles",
            params={"tag": tag, "per_page": 20, "top": 1}
        )
        if not data:
            continue

        for article in data:
            title = article.get("title", "")
            description = article.get("description", "")
            combined = title + " " + description

            # 模块一先检查
            if matches_keywords(combined, KW_EN_M1):
                module, priority_label = "M1", "🎮 AI+游戏"
            elif matches_keywords(combined, KW_M2_EN):
                module, priority_label = "M2", "🤖 AI通用"
            else:
                continue

            published = article.get("published_at", "")
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if not is_within_hours(dt, HOURS_BACK):
                    continue
            except Exception:
                pass

            results.append(make_item(
                title=title,
                url=article.get("url", ""),
                source="Dev.to",
                platform_order=6,
                meta=f"❤️ {article.get('positive_reactions_count', 0)} | 💬 {article.get('comments_count', 0)}",
                summary=truncate(description, 150),
                score=article.get("positive_reactions_count", 0),
                module=module,
                priority_label=priority_label,
            ))

    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: (0 if x["module"] == "M1" else 1, -x["score"])):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    print(f"  ✅ Dev.to 获取 {len(unique)} 条（M1:{sum(1 for r in unique if r['module']=='M1')} M2:{sum(1 for r in unique if r['module']=='M2')}）")
    return unique[:MAX_ITEMS_PER_SOURCE]

# ═══════════════════════════════════════════════════════════════
#  平台 7：RSS 聚合 — 按来源区分语言
#  平台顺序：7
# ═══════════════════════════════════════════════════════════════

def fetch_rss():
    """
    抓取 RSS 订阅源
    语言策略：中文 Feed 用中文关键词，英文 Feed 用英文关键词
    平台顺序：7
    """
    print("📡 [7/9] 抓取 RSS 订阅源...")
    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)

    # 中文 RSS — 用中文+英文关键词
    zh_keywords = KW_KM_M1_ZH + KW_M2_ZH
    # 英文 RSS — 用英文关键词
    en_keywords = KW_EN_M1 + KW_M2_EN

    feed_groups = [
        (RSS_FEEDS_ZH, zh_keywords, "zh"),
        (RSS_FEEDS_EN, en_keywords, "en"),
    ]

    for feed_list, keywords, lang in feed_groups:
        for feed_name, feed_url in feed_list:
            try:
                feed = feedparser.parse(feed_url)
                count = 0
                for entry in feed.entries[:50]:
                    title = entry.get("title", "")
                    summary = entry.get("summary", entry.get("description", ""))
                    combined = title + " " + summary

                    if not matches_keywords(combined, keywords):
                        continue

                    published = None
                    for tf in ["published_parsed", "updated_parsed"]:
                        tp = entry.get(tf)
                        if tp:
                            try:
                                published = datetime(*tp[:6], tzinfo=timezone.utc)
                                break
                            except Exception:
                                pass

                    if published and published < cutoff:
                        continue

                    # 模块分类
                    if matches_keywords(combined, KW_EN_M1 if lang == "en" else KW_KM_M1):
                        module, priority_label = "M1", "🎮 AI+游戏"
                    else:
                        module, priority_label = "M2", "🤖 AI通用"

                    results.append(make_item(
                        title=title,
                        url=entry.get("link", ""),
                        source=f"RSS·{feed_name}",
                        platform_order=7,
                        meta=f"📰 {feed_name}",
                        summary=truncate(summary, 150),
                        score=0,
                        module=module,
                        priority_label=priority_label,
                    ))
                    count += 1

                if count:
                    print(f"    • {feed_name}（{lang}）: {count} 条")
            except Exception as e:
                print(f"  ⚠️  RSS 解析失败 {feed_name}: {e}", file=sys.stderr)

    print(f"  ✅ RSS 共获取 {len(results)} 条")
    return results[:MAX_ITEMS_PER_SOURCE * 2]

# ═══════════════════════════════════════════════════════════════
#  平台 8：ProductHunt — 纯英文
#  平台顺序：8
# ═══════════════════════════════════════════════════════════════

def fetch_producthunt():
    """
    抓取 ProductHunt RSS
    语言策略：纯英文
    平台顺序：8
    """
    print("📡 [8/9] 抓取 ProductHunt...")
    results = []

    feed = feedparser.parse("https://www.producthunt.com/feed")
    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)

    for entry in feed.entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        combined = title + " " + summary

        if not matches_keywords(combined, KW_EN_M1 + KW_M2_EN):
            continue

        try:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published < cutoff:
                continue
        except Exception:
            pass

        if matches_keywords(combined, KW_EN_M1):
            module, priority_label = "M1", "🎮 AI+游戏"
        else:
            module, priority_label = "M2", "🤖 AI通用"

        results.append(make_item(
            title=title,
            url=entry.get("link", ""),
            source="ProductHunt",
            platform_order=8,
            meta="🚀 ProductHunt 新发布",
            summary=truncate(summary, 150),
            score=0,
            module=module,
            priority_label=priority_label,
        ))

    print(f"  ✅ ProductHunt 获取 {len(results)} 条")
    return results[:MAX_ITEMS_PER_SOURCE]

# ═══════════════════════════════════════════════════════════════
#  平台 9：GitHub Trending — 纯英文（放最后）
#  平台顺序：9
# ═══════════════════════════════════════════════════════════════

def fetch_github():
    """
    抓取 GitHub 仓库搜索
    语言策略：纯英文
    平台顺序：9（放最后）
    """
    print("📡 [9/9] 抓取 GitHub Trending...")
    results = []
    since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # 模块一查询（游戏×AI）
    queries_m1 = [
        "unity ai coding assistant",
        "unreal engine ai coding",
        "godot ai assistant",
        "vibe coding game",
        "ai game development llm",
        "game dev ai tools",
        "unity llm", "unreal llm", "godot llm",
    ]
    # 模块二查询（AI通用）
    queries_m2 = [
        "vibe coding",
        "ai agent ide",
        "claude code cli",
        "cursor ai extension",
        "agentic coding",
    ]

    headers = {"Accept": "application/vnd.github.v3+json"}
    github_token = os.environ.get("GITHUB_TOKEN", "")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    for query in queries_m1 + queries_m2:
        data = safe_get(
            "https://api.github.com/search/repositories",
            params={
                "q": f"{query} pushed:>{since_date}",
                "sort": "stars",
                "order": "desc",
                "per_page": 5,
            },
            headers=headers
        )
        if not data:
            continue
        time.sleep(0.5)

        for repo in data.get("items", []):
            desc = repo.get("description") or "无描述"
            full_text = f"{repo.get('full_name', '')} {desc}"

            if matches_keywords(full_text, KW_EN_M1):
                module, priority_label = "M1", "🎮 AI+游戏"
            elif matches_keywords(full_text, KW_M2_EN):
                module, priority_label = "M2", "🤖 AI通用"
            else:
                continue

            results.append(make_item(
                title=f"{repo.get('full_name')} — {desc[:80]}",
                url=repo.get("html_url", ""),
                source="GitHub",
                platform_order=9,
                meta=f"⭐ {repo.get('stargazers_count', 0)} | {repo.get('language', 'N/A')}",
                score=repo.get("stargazers_count", 0),
                module=module,
                priority_label=priority_label,
            ))

    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: (0 if x["module"] == "M1" else 1, -x["score"])):
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    print(f"  ✅ GitHub 获取 {len(unique)} 条（M1:{sum(1 for r in unique if r['module']=='M1')} M2:{sum(1 for r in unique if r['module']=='M2')}）")
    return unique[:MAX_ITEMS_PER_SOURCE]

# ═══════════════════════════════════════════════════════════════
#  KM MCP 集成（通过 km MCP 工具抓取）
# ═══════════════════════════════════════════════════════════════

def fetch_km_via_mcp():
    """
    通过 KM MCP 工具抓取腾讯内部 KM 文章
    使用中文+英文双语关键词搜索
    此函数在 main() 中被调用，结果注入 inject_km_results()
    """
    print("📡 [1/9] 通过 KM MCP 抓取腾讯内部 KM...")
    km_items = []

    # 使用 km MCP 的 list-articles 工具
    # 中文关键词搜索（分批，每批搜索一个关键词）
    zh_search_keywords = [
        ["游戏开发", "AI"],
        ["Unity", "AI"],
        ["Unreal", "AI"],
        ["Godot", "AI"],
        ["vibe coding"],
        ["AI编程", "游戏"],
        ["Cursor", "游戏"],
    ]
    en_search_keywords = [
        ["vibe coding game"],
        ["ai game development"],
        ["unity cursor"],
        ["unreal cursor"],
        ["godot cursor"],
    ]

    # 注：实际 MCP 调用在 main() 中通过外部注入完成
    # 这里返回空列表，由 main() 中的 KM MCP 调用结果填充
    print("  ℹ️  KM MCP 调用由主流程处理")
    return km_items

# ═══════════════════════════════════════════════════════════════
#  摘要 & 翻译说明
# ═══════════════════════════════════════════════════════════════
#
#  翻译和摘要生成由「对话中的 Claude」完成，无需配置 ANTHROPIC_API_KEY：
#  1. digest.py 运行后，自动保存 digest_{date}_raw.json（含 m1/m2 原始数据）
#  2. 在 Knot 对话中，Claude 读取 raw.json，直接翻译英文标题、生成中文摘要
#  3. 将翻译结果写回 digest_{date}.md 报告文件
#
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
#  报告生成
# ═══════════════════════════════════════════════════════════════

# 平台顺序名称映射（用于模块一分组展示）
PLATFORM_ORDER_NAMES = {
    1: ("🏢 KM（腾讯内部）", "穷尽 24h"),
    2: ("💬 微信公众号", "搜狗微信搜索，穷尽 24h"),
    3: ("🐦 X / Twitter", "Playwright + Cookie，穷尽 24h"),
    4: ("🤖 Reddit", "RSS Feed，r/gamedev 等"),
    5: ("📰 HackerNews", ""),
    6: ("📝 Dev.to", ""),
    7: ("📡 RSS 聚合", ""),
    8: ("🚀 ProductHunt", ""),
    9: ("⭐ GitHub Trending", "放最后"),
}

def generate_report(m1_items, m2_items, summary_m2=None):
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")

    lines = []
    lines.append(f"# 🎮 AI 游戏开发 & Vibe Coding 每日资讯")
    lines.append(f"**{date_str} {time_str}** | 过去 24 小时精选")
    lines.append("")
    lines.append("| 模块 | 条数 |")
    lines.append("|------|------|")
    lines.append(f"| 🎮 模块一：AI + 游戏 | {len(m1_items)} 条 |")
    lines.append(f"| 🤖 模块二：AI 通用 | {len(m2_items)} 条 |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 模块一 ──────────────────────────────────────────────────
    lines.append("## 🎮 模块一：AI + 游戏")
    lines.append("> Unity / Unreal / Godot × AI/Vibe Coding 最新资讯")
    lines.append("> 平台顺序：KM → 微信公众号 → X → Reddit → HN → Dev.to → RSS → ProductHunt → GitHub Trending")
    lines.append("> 📌 格式：标题 + 原文链接 + 原文约 20% 字数总结")
    lines.append("")

    if m1_items:
        # 按平台顺序分组
        from collections import defaultdict
        m1_by_platform = defaultdict(list)
        for item in m1_items:
            m1_by_platform[item["platform_order"]].append(item)

        for order in sorted(m1_by_platform.keys()):
            platform_name, note = PLATFORM_ORDER_NAMES.get(order, (f"平台 {order}", ""))
            note_str = f"（{note}）" if note else ""
            lines.append(f"### {platform_name}{note_str}")
            lines.append("")
            for item in m1_by_platform[order]:
                # 标题：英文平台优先展示中文译名，保留原文
                raw_title = item['title']
                title_zh = item.get("title_zh", "")
                if title_zh:
                    display_title = f"{title_zh} / {raw_title}"
                else:
                    display_title = raw_title

                # 格式：标题(链接) + 来源meta + 20%总结
                lines.append(f"#### [{display_title}]({item['url']})")
                lines.append(f"> {item['priority_label']} | {item['meta']}")
                lines.append("")
                # 20% 总结：优先用 full_summary，其次 summary，最后用 AI 摘要占位
                full_summary = item.get("full_summary") or item.get("summary", "")
                if full_summary:
                    lines.append(full_summary)
                else:
                    lines.append("*（正在生成摘要…）*")
                lines.append("")
                lines.append("---")
                lines.append("")
    else:
        lines.append("> 今日暂无 AI + 游戏相关资讯 👀")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── 模块二 ──────────────────────────────────────────────────
    lines.append("## 🤖 模块二：AI 通用")
    lines.append("> Cursor / Claude Code / Windsurf / Vibe Coding 使用技巧与行业动态")
    lines.append("")

    if summary_m2:
        lines.append("### 🤖 Claude AI 综合摘要（模块二）")
        lines.append("")
        lines.append(summary_m2)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("### 📋 原始资讯")
        lines.append("")

    if m2_items:
        for item in sorted(m2_items, key=lambda x: (x["platform_order"], -x.get("score", 0))):
            # 标题：英文平台优先展示中文译名
            raw_title = item['title']
            title_zh = item.get("title_zh", "")
            if title_zh:
                display_title = f"{title_zh} / {raw_title}"
            else:
                display_title = raw_title

            lines.append(f"#### [{display_title}]({item['url']})")
            lines.append(f"> {item['priority_label']} | {item['meta']}")
            if item.get("summary"):
                lines.append(f"> {item['summary']}")
            lines.append("")
    else:
        lines.append("> 今日暂无 AI 通用资讯")
        lines.append("")

    lines.append("---")
    lines.append("")
    total = len(m1_items) + len(m2_items)
    sources = list(set(i["source"].split("·")[0].strip() for i in m1_items + m2_items))
    lines.append(f"*共收录 {total} 条 | 覆盖平台：{', '.join(sources)}*")
    lines.append(f"*抓取时间：{time_str} | 过去 {HOURS_BACK} 小时*")

    return "\n".join(lines)


def generate_notify_summary(m1_items, m2_items):
    """生成企业微信通知用的简短摘要"""
    now = datetime.now()
    date_str = now.strftime("%m/%d")
    total = len(m1_items) + len(m2_items)

    if not total:
        return f"📭 [{date_str}] AI游戏开发日报：今日暂无新资讯"

    lines = [f"🎮 AI游戏开发 & Vibe Coding 日报 [{date_str}]"]
    lines.append(f"共 {total} 条 | 🎮模块一:{len(m1_items)}条 🤖模块二:{len(m2_items)}条\n")

    if m1_items:
        lines.append("── 🎮 AI+游戏 精选 ──")
        for item in m1_items[:3]:
            title = item['title'][:55] + ('…' if len(item['title']) > 55 else '')
            lines.append(f"• {title}")
            lines.append(f"  {item['source']} | {item['url']}")
        lines.append("")

    if m2_items:
        lines.append("── 🤖 AI通用 精选 ──")
        for item in m2_items[:2]:
            title = item['title'][:55] + ('…' if len(item['title']) > 55 else '')
            lines.append(f"• {title}")
            lines.append(f"  {item['source']}")
        lines.append("")

    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
#  主函数
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("🎮 AI Game Dev & Vibe Coding Digest v3.0")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 抓取过去 {HOURS_BACK} 小时 | 双模块架构")
    print("📋 模块一：AI+游戏（严格平台顺序）| 模块二：AI通用")
    print("=" * 65)

    all_items = []

    # 平台抓取顺序（严格按 workflow-v0.5 定义）
    # 平台 1：KM（通过 MCP，main 外部注入）
    # 平台 2-4：⏸️ 待完成
    fetchers = [
        fetch_km,           # 1 - KM（读取 km_results.json）
        fetch_wechat,       # 2 - 微信公众号（搜狗微信搜索）
        fetch_x_twitter,    # 3 - X/Twitter（Playwright + Cookie）
        fetch_reddit,       # 4 - Reddit（RSS Feed）
        fetch_hackernews,   # 5 - HackerNews
        fetch_devto,        # 6 - Dev.to
        fetch_rss,          # 7 - RSS 聚合
        fetch_producthunt,  # 8 - ProductHunt
        fetch_github,       # 9 - GitHub Trending（放最后）
    ]

    for fetcher in fetchers:
        try:
            items = fetcher()
            all_items.extend(items)
        except Exception as e:
            print(f"  ❌ 抓取失败 {fetcher.__name__}: {e}", file=sys.stderr)
        time.sleep(1)

    # 全局去重（按 URL）
    seen = set()
    unique_items = []
    for item in all_items:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            unique_items.append(item)

    # 按模块分组
    m1_items = [i for i in unique_items if i["module"] == "M1"]
    m2_items = [i for i in unique_items if i["module"] == "M2"]

    # 模块一按平台顺序排序，同平台内按 score 降序
    m1_items.sort(key=lambda x: (x["platform_order"], -x.get("score", 0)))
    # 模块二按平台顺序 + score
    m2_items.sort(key=lambda x: (x["platform_order"], -x.get("score", 0)))

    print(f"\n📊 抓取完成（去重后共 {len(unique_items)} 条）")
    print(f"   🎮 模块一 AI+游戏: {len(m1_items)} 条")
    print(f"   🤖 模块二 AI通用:  {len(m2_items)} 条")

    # 平台分布统计
    from collections import Counter
    platform_dist = Counter(i["source"].split("·")[0].strip() for i in unique_items)
    print("\n   平台分布：")
    for platform, count in sorted(platform_dist.items(), key=lambda x: -x[1]):
        print(f"   • {platform}: {count} 条")

    # 翻译：由 Knot 对话 Claude 在 cron 任务中自动完成（读取 raw.json → 翻译 → 重新生成报告）
    summary_m2 = None

    # 生成报告
    report = generate_report(m1_items, m2_items, summary_m2)
    summary = generate_notify_summary(m1_items, m2_items)

    # 保存文件
    output_dir = os.path.dirname(os.path.abspath(__file__))
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(output_dir, f"digest_{today}.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📄 报告已保存：{report_path}")

    # 保存原始数据 JSON（含翻译后的 title_zh / full_summary）
    raw_data_path = os.path.join(output_dir, f"digest_{today}_raw.json")
    with open(raw_data_path, "w", encoding="utf-8") as f:
        json.dump({"m1": m1_items, "m2": m2_items, "date": today}, f, ensure_ascii=False, indent=2)
    print(f"💾 原始数据已保存：{raw_data_path}")

    summary_path = os.path.join(output_dir, "latest_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n" + "=" * 65)
    print("✅ 完成！通知摘要预览：")
    print("=" * 65)
    print(summary)

    return summary, report_path


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
work-assistant / fetcher.py
============================
统一数据抓取器，支持以下平台：
  - X (Twitter)       ← cookie 复用 vibe-coding-digest
  - Reddit             ← RSS
  - Hacker News        ← 官方 JSON API
  - Steam              ← Steam 官方 API
  - SteamDB            ← SteamCharts + Steam 官方 API（在线人数/打折/新游/单游详情）
  - itch.io            ← JSON API
  - YouTube (频道)     ← RSS
  - Bilibili           ← 公开 API
  - KM                 ← mcporter-internal (运行时调用)

用法示例：
  python3 fetcher.py --source x --query "vibe coding" --limit 10
  python3 fetcher.py --source reddit --subreddit gamedev --limit 20
  python3 fetcher.py --source hn --query "game development" --limit 15
  python3 fetcher.py --source steam --type trending
  python3 fetcher.py --source steamdb --type top           # 实时在线人数排行
  python3 fetcher.py --source steamdb --type deals         # 当前打折游戏
  python3 fetcher.py --source steamdb --type new           # 新发售游戏
  python3 fetcher.py --source steamdb --type app --keyword "1091500"  # 单游详情(appid)
  python3 fetcher.py --source bilibili --type hot --keyword "独立游戏"
"""

import argparse
import json
import os
import sys
import time
import sqlite3
from datetime import datetime, timedelta

import requests
import feedparser

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config", "platforms.json")
CACHE_DIR   = os.path.join(SCRIPT_DIR, "cache")
DIGEST_DIR  = os.path.join(SCRIPT_DIR, "..", "vibe-coding-digest")

os.makedirs(CACHE_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
#  工具函数
# ─────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cache_path(key):
    return os.path.join(CACHE_DIR, f"{key}.json")


def save_cache(key, data):
    with open(cache_path(key), "w", encoding="utf-8") as f:
        json.dump({"ts": datetime.now().isoformat(), "data": data}, f, ensure_ascii=False, indent=2)


def load_cache(key, max_age_minutes=30):
    p = cache_path(key)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        c = json.load(f)
    ts = datetime.fromisoformat(c["ts"])
    if datetime.now() - ts > timedelta(minutes=max_age_minutes):
        return None
    return c["data"]


def req(url, params=None, headers=None, timeout=15):
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    }
    if headers:
        default_headers.update(headers)
    resp = requests.get(url, params=params, headers=default_headers, timeout=timeout)
    resp.raise_for_status()
    return resp


# ─────────────────────────────────────────────────────────────
#  X (Twitter)
# ─────────────────────────────────────────────────────────────

def get_x_cookies():
    """从 accounts.db 加载 X cookie"""
    db_path = os.path.join(DIGEST_DIR, "accounts.db")
    if not os.path.exists(db_path):
        # fallback: x_cookies.json
        cj_path = os.path.join(DIGEST_DIR, "x_cookies.json")
        if os.path.exists(cj_path):
            with open(cj_path) as f:
                return json.load(f)
        return None
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT cookies FROM accounts WHERE active=1 LIMIT 1").fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None


def fetch_x(query, limit=20):
    """通过 X 搜索 API (v2-like GraphQL) 抓取推文"""
    cache_key = f"x_{query.replace(' ','_')}_{limit}"
    cached = load_cache(cache_key, max_age_minutes=60)
    if cached:
        print(f"  📦 使用缓存 ({cache_key})")
        return cached

    cookies_data = get_x_cookies()
    if not cookies_data:
        print("  ⚠️  未找到 X cookie，请先确保 vibe-coding-digest/accounts.db 中有有效账号")
        return []

    # 构造 cookie jar
    cookies = {}
    if isinstance(cookies_data, list):
        for c in cookies_data:
            cookies[c.get("name", "")] = c.get("value", "")
    elif isinstance(cookies_data, dict):
        cookies = cookies_data

    # 使用 X 的 SearchTimeline API
    BEARER = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    headers = {
        "Authorization": f"Bearer {BEARER}",
        "x-csrf-token": cookies.get("ct0", ""),
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "zh-cn",
        "x-twitter-active-user": "yes",
        "Content-Type": "application/json",
    }

    variables = {
        "rawQuery": query,
        "count": limit,
        "product": "Latest",
        "querySource": "typed_query"
    }
    features = {
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    }

    url = "https://api.x.com/graphql/UN1i3zUiCWa-6r-Uaho4fw/SearchTimeline"
    try:
        resp = requests.get(
            url,
            params={
                "variables": json.dumps(variables),
                "features": json.dumps(features),
            },
            headers=headers,
            cookies=cookies,
            timeout=20
        )
        resp.raise_for_status()
        data = resp.json()

        # 解析推文
        results = []
        instructions = (
            data.get("data", {})
                .get("search_by_raw_query", {})
                .get("search_timeline", {})
                .get("timeline", {})
                .get("instructions", [])
        )
        for inst in instructions:
            for entry in inst.get("entries", []):
                try:
                    tweet = (entry["content"]["itemContent"]["tweet_results"]["result"])
                    core = tweet.get("core", {}).get("user_results", {}).get("result", {})
                    legacy = tweet.get("legacy", {})
                    user_legacy = core.get("legacy", {})
                    results.append({
                        "id": legacy.get("id_str"),
                        "text": legacy.get("full_text", ""),
                        "user": user_legacy.get("screen_name", ""),
                        "name": user_legacy.get("name", ""),
                        "likes": legacy.get("favorite_count", 0),
                        "retweets": legacy.get("retweet_count", 0),
                        "created_at": legacy.get("created_at", ""),
                        "url": f"https://x.com/{user_legacy.get('screen_name')}/status/{legacy.get('id_str')}"
                    })
                except Exception:
                    continue

        save_cache(cache_key, results)
        return results

    except Exception as e:
        print(f"  ❌ X 抓取失败: {e}")
        return []


# ─────────────────────────────────────────────────────────────
#  Reddit (RSS)
# ─────────────────────────────────────────────────────────────

def fetch_reddit(subreddit="gamedev", limit=20, sort="hot"):
    cache_key = f"reddit_{subreddit}_{sort}_{limit}"
    cached = load_cache(cache_key, 30)
    if cached:
        return cached

    url = f"https://www.reddit.com/r/{subreddit}/{sort}.rss?limit={limit}"
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:limit]:
            results.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "author": entry.get("author", ""),
                "summary": entry.get("summary", "")[:300],
                "published": entry.get("published", ""),
            })
        save_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"  ❌ Reddit 抓取失败: {e}")
        return []


# ─────────────────────────────────────────────────────────────
#  Hacker News
# ─────────────────────────────────────────────────────────────

def fetch_hn(query=None, limit=20, story_type="top"):
    """抓取 HN 热门/最新，或搜索关键词"""
    if query:
        cache_key = f"hn_search_{query.replace(' ','_')}_{limit}"
        cached = load_cache(cache_key, 60)
        if cached:
            return cached
        url = f"https://hn.algolia.com/api/v1/search"
        resp = req(url, params={"query": query, "hitsPerPage": limit, "tags": "story"})
        data = resp.json()
        results = []
        for hit in data.get("hits", []):
            results.append({
                "title": hit.get("title", ""),
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                "author": hit.get("author", ""),
                "points": hit.get("points", 0),
                "comments": hit.get("num_comments", 0),
                "created_at": hit.get("created_at", ""),
            })
        save_cache(cache_key, results)
        return results
    else:
        cache_key = f"hn_{story_type}_{limit}"
        cached = load_cache(cache_key, 30)
        if cached:
            return cached
        base = "https://hacker-news.firebaseio.com/v0"
        ids = req(f"{base}/{story_type}stories.json").json()[:limit]
        results = []
        for sid in ids:
            try:
                item = req(f"{base}/item/{sid}.json").json()
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    "author": item.get("by", ""),
                    "points": item.get("score", 0),
                    "comments": item.get("descendants", 0),
                })
            except Exception:
                continue
        save_cache(cache_key, results)
        return results


# ─────────────────────────────────────────────────────────────
#  Steam
# ─────────────────────────────────────────────────────────────

def fetch_steam(query_type="trending", keyword=None, limit=20):
    """
    query_type:
      trending   - SteamSpy 最近热门
      search     - 按游戏名搜索
      new        - 新发布的游戏
    """
    cache_key = f"steam_{query_type}_{keyword}_{limit}"
    cached = load_cache(cache_key, 120)
    if cached:
        return cached

    results = []
    try:
        if query_type == "trending":
            # 使用 Steam 官方 featured categories API
            resp = req("https://store.steampowered.com/api/featuredcategories/",
                       params={"cc": "cn", "l": "schinese"})
            data = resp.json()
            items = []
            for cat in ["top_sellers", "specials", "coming_soon"]:
                items += data.get(cat, {}).get("items", [])
            seen_ids = set()
            for item in items:
                appid = str(item.get("id", ""))
                if appid in seen_ids:
                    continue
                seen_ids.add(appid)
                # name 可能在 item 直接，也可能在 large_capsule_image 等字段旁
                name = item.get("name") or item.get("title") or ""
                # 若 name 为空，尝试从 header_image URL 中提取 appid 确认
                results.append({
                    "appid": appid,
                    "name": name,
                    "discount": item.get("discount_percent", 0),
                    "price": item.get("final_price", 0),
                    "url": f"https://store.steampowered.com/app/{appid}",
                })
                if len(results) >= limit:
                    break
        elif query_type == "search" and keyword:
            resp = req("https://store.steampowered.com/api/storesearch/",
                       params={"term": keyword, "l": "schinese", "cc": "cn"})
            data = resp.json()
            for item in data.get("items", [])[:limit]:
                results.append({
                    "appid": item.get("id"),
                    "name": item.get("name", ""),
                    "price": item.get("price", {}).get("final_formatted", ""),
                    "url": f"https://store.steampowered.com/app/{item.get('id')}",
                })
        elif query_type == "new":
            resp = req("https://store.steampowered.com/api/featuredcategories/",
                       params={"cc": "cn", "l": "schinese"})
            data = resp.json()
            items = data.get("new_releases", {}).get("items", [])[:limit]
            for item in items:
                results.append({
                    "appid": item.get("id"),
                    "name": item.get("name", ""),
                    "discount": item.get("discount_percent", 0),
                    "price": item.get("final_price", 0),
                    "url": f"https://store.steampowered.com/app/{item.get('id')}",
                })
    except Exception as e:
        print(f"  ❌ Steam 抓取失败: {e}")

    save_cache(cache_key, results)
    return results


# ─────────────────────────────────────────────────────────────
#  SteamDB  (via SteamCharts + Steam Official API)
#  注：steamdb.info 被 Cloudflare 保护，直链均已在下方标注
# ─────────────────────────────────────────────────────────────

def _steamdb_link(appid):
    return f"https://steamdb.info/app/{appid}/"

def _steam_appdetails(appid, fields="name,genres,short_description,release_date,price_overview,developers,publishers"):
    """调用 Steam appdetails API 获取单游元数据"""
    try:
        resp = req(
            "https://store.steampowered.com/api/appdetails",
            params={"appids": appid, "fields": fields, "cc": "cn", "l": "schinese"},
            timeout=10
        )
        data = resp.json().get(str(appid), {})
        if data.get("success"):
            return data.get("data", {})
    except Exception:
        pass
    return {}


def fetch_steamdb(query_type="top", keyword=None, limit=20):
    """
    SteamDB 风格数据（通过 SteamCharts + Steam 官方 API 组合实现）

    query_type:
      top     - 实时在线人数 Top N（SteamCharts）
      peak    - 历史在线峰值 Top N（Steam ISteamChartsService API）
      deals   - 当前打折促销游戏（Steam Store API）
      new     - 新发售游戏（Steam Store API）
      app     - 单个游戏详情（keyword = appid）
      search  - 按名称搜索游戏（keyword = 游戏名）
    """
    cache_key = f"steamdb_{query_type}_{keyword}_{limit}"
    # top / deals 缓存短一些，保证数据新鲜
    cache_ttl = 20 if query_type in ("top", "deals") else 60
    cached = load_cache(cache_key, cache_ttl)
    if cached:
        print(f"  📦 使用缓存 ({cache_key})")
        return cached

    results = []
    try:
        from bs4 import BeautifulSoup

        if query_type == "top":
            # ── SteamCharts 实时在线人数排行 ──
            resp = req("https://steamcharts.com/top",
                       headers={"Referer": "https://steamcharts.com/"})
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("table.common-table tbody tr")[:limit]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 5:
                    continue
                rank      = cols[0].get_text(strip=True).rstrip(".")
                name_el   = cols[1].find("a")
                name      = name_el.get_text(strip=True) if name_el else cols[1].get_text(strip=True)
                href      = name_el["href"] if name_el else ""
                # href 形如 /app/730
                appid     = href.split("/")[-1] if href else ""
                current   = cols[2].get_text(strip=True)
                avg_30d   = cols[3].get_text(strip=True)
                peak      = cols[4].get_text(strip=True)
                results.append({
                    "rank":     rank,
                    "name":     name,
                    "appid":    appid,
                    "current_players": current,
                    "avg_30d":  avg_30d,
                    "peak":     peak,
                    "url":      f"https://store.steampowered.com/app/{appid}" if appid else "",
                    "steamdb":  _steamdb_link(appid) if appid else "",
                    "steamcharts": f"https://steamcharts.com/app/{appid}" if appid else "",
                })

        elif query_type == "peak":
            # ── Steam 官方 ISteamChartsService API（近期峰值在线）──
            resp = req("https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/",
                       timeout=10)
            ranks = resp.json().get("response", {}).get("ranks", [])[:limit]
            # 批量获取游戏名（避免太多请求，只查前 limit 个）
            for entry in ranks:
                appid = entry.get("appid")
                detail = _steam_appdetails(appid, fields="name")
                name = detail.get("name", f"App {appid}")
                results.append({
                    "rank":        entry.get("rank"),
                    "name":        name,
                    "appid":       appid,
                    "peak_2weeks": entry.get("peak_in_game", 0),
                    "last_week_rank": entry.get("last_week_rank"),
                    "url":     f"https://store.steampowered.com/app/{appid}",
                    "steamdb": _steamdb_link(appid),
                })

        elif query_type == "deals":
            # ── Steam 当前促销特惠（折扣 ≥ 50%）──
            resp = req("https://store.steampowered.com/api/featuredcategories/",
                       params={"cc": "cn", "l": "schinese"})
            data = resp.json()
            specials = data.get("specials", {}).get("items", [])
            for item in specials:
                disc = item.get("discount_percent", 0)
                if disc <= 0:
                    continue
                appid = str(item.get("id", ""))
                orig  = item.get("original_price", 0)
                final = item.get("final_price", 0)
                results.append({
                    "name":      item.get("name", ""),
                    "appid":     appid,
                    "discount":  disc,
                    "orig_price":  f"¥{orig/100:.0f}" if orig else "Free",
                    "final_price": f"¥{final/100:.0f}" if final else "Free",
                    "url":     f"https://store.steampowered.com/app/{appid}",
                    "steamdb": _steamdb_link(appid),
                })
                if len(results) >= limit:
                    break

        elif query_type == "new":
            # ── 新发售游戏 ──
            resp = req("https://store.steampowered.com/api/featuredcategories/",
                       params={"cc": "cn", "l": "schinese"})
            data = resp.json()
            items = data.get("new_releases", {}).get("items", [])[:limit]
            for item in items:
                appid = str(item.get("id", ""))
                results.append({
                    "name":    item.get("name", ""),
                    "appid":   appid,
                    "discount": item.get("discount_percent", 0),
                    "price":   f"¥{item.get('final_price',0)/100:.0f}",
                    "url":     f"https://store.steampowered.com/app/{appid}",
                    "steamdb": _steamdb_link(appid),
                })

        elif query_type == "app":
            # ── 单游戏详情 ──
            appid = keyword or "1091500"
            detail = _steam_appdetails(appid)
            if not detail:
                print(f"  ❌ 未找到 appid={appid} 的游戏")
                return []

            # 获取 SteamCharts 历史在线人数（网页解析）
            chart_data = []
            try:
                cr = req(f"https://steamcharts.com/app/{appid}",
                         headers={"Referer": "https://steamcharts.com/"})
                cs = BeautifulSoup(cr.text, "html.parser")
                rows = cs.select("table.common-table tbody tr")[:6]
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        chart_data.append({
                            "month":   cols[0].get_text(strip=True),
                            "avg":     cols[1].get_text(strip=True),
                            "peak":    cols[2].get_text(strip=True),
                            "gain":    cols[3].get_text(strip=True),
                        })
            except Exception:
                pass

            price_info = detail.get("price_overview", {})
            results.append({
                "name":        detail.get("name", ""),
                "appid":       appid,
                "developers":  ", ".join(detail.get("developers", [])),
                "publishers":  ", ".join(detail.get("publishers", [])),
                "genres":      ", ".join(g.get("description","") for g in detail.get("genres",[])),
                "description": detail.get("short_description", "")[:200],
                "release_date": detail.get("release_date", {}).get("date", ""),
                "price":       price_info.get("final_formatted", ""),
                "discount":    price_info.get("discount_percent", 0),
                "steam_url":   f"https://store.steampowered.com/app/{appid}",
                "steamdb_url": _steamdb_link(appid),
                "steamcharts_url": f"https://steamcharts.com/app/{appid}",
                "player_history": chart_data,
            })

        elif query_type == "search":
            # ── 按名称搜索 ──
            kw = keyword or "indie"
            resp = req("https://store.steampowered.com/api/storesearch/",
                       params={"term": kw, "l": "schinese", "cc": "cn"})
            data = resp.json()
            for item in data.get("items", [])[:limit]:
                appid = str(item.get("id", ""))
                results.append({
                    "name":    item.get("name", ""),
                    "appid":   appid,
                    "price":   item.get("price", {}).get("final_formatted", ""),
                    "url":     f"https://store.steampowered.com/app/{appid}",
                    "steamdb": _steamdb_link(appid),
                })

    except Exception as e:
        import traceback
        print(f"  ❌ SteamDB 数据抓取失败: {e}")
        traceback.print_exc()

    save_cache(cache_key, results)
    return results


# ─────────────────────────────────────────────────────────────
#  itch.io (RSS)
# ─────────────────────────────────────────────────────────────

def fetch_itch(feed_type="top-rated", limit=20):
    """
    feed_type:
      top-rated  - 高评分
      new        - 最新游戏
      hot        - 热门
    """
    cache_key = f"itch_{feed_type}_{limit}"
    cached = load_cache(cache_key, 60)
    if cached:
        return cached

    sort_map = {"top-rated": "top-rated", "new": "date", "hot": "popular"}
    sort = sort_map.get(feed_type, "top-rated")

    try:
        from html.parser import HTMLParser

        class ItchParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.games = []
                self._in_title = False
                self._current = {}

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "div" and "game_cell" in attrs.get("class", ""):
                    self._current = {"appid": attrs.get("data-game_id", "")}
                if tag == "a" and "game_link" in attrs.get("class", ""):
                    self._current["url"] = attrs.get("href", "")
                if tag == "div" and "game_title" in attrs.get("class", ""):
                    self._in_title = True

            def handle_data(self, data):
                if self._in_title:
                    self._current["title"] = data.strip()
                    self._in_title = False
                    if self._current.get("url"):
                        self.games.append(dict(self._current))

        resp = req("https://itch.io/games", params={"sort": sort, "format": "json"},
                   headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
        import json as _json
        html = _json.loads(resp.text).get("content", "")

        parser = ItchParser()
        parser.feed(html)
        results = [{"title": g.get("title",""), "url": g.get("url",""),
                    "author": "", "summary": "", "published": ""}
                   for g in parser.games[:limit] if g.get("title")]

        save_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"  ❌ itch.io 抓取失败: {e}")
        return []


# ─────────────────────────────────────────────────────────────
#  YouTube (RSS by channel/topic)
# ─────────────────────────────────────────────────────────────

# 预置常用 YouTube 频道
YOUTUBE_CHANNELS = {
    "GDC": "UCVisk1OiqZteyUsFO1WnB2A",
    "GameMaker's Toolkit": "UCqJ-Xo29CKyLTjn6z2XwYAw",
    "Brackeys": "UCYbK_tjZ2OrIZFBvU6CCMiA",
    "Extra Credits": "UCCODtTcd5M1JavPCOr_Uydg",
    "AI Explained": "UCNJ1Ymd5yFuUPtn21xtRbbw",
}

def fetch_youtube(channel_id=None, channel_name=None, limit=10):
    if channel_name and channel_name in YOUTUBE_CHANNELS:
        channel_id = YOUTUBE_CHANNELS[channel_name]
    if not channel_id:
        print("  ⚠️  请指定 channel_id 或已知的 channel_name")
        return []

    cache_key = f"youtube_{channel_id}_{limit}"
    cached = load_cache(cache_key, 120)
    if cached:
        return cached

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:limit]:
            results.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "author": entry.get("author", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:200],
            })
        save_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"  ❌ YouTube 抓取失败: {e}")
        return []


# ─────────────────────────────────────────────────────────────
#  Bilibili
# ─────────────────────────────────────────────────────────────

# 分区 tid 映射
BILI_PARTITIONS = {
    "独立游戏": 321,
    "单机游戏": 4,
    "网络游戏": 5,
    "手机游戏": 8,
    "游戏资讯": 17,
    "科技": 188,
    "AI": 311,
}

def fetch_bilibili(btype="hot", keyword=None, partition=None, limit=20):
    """
    btype:
      hot      - 分区热门视频
      search   - 关键词搜索
      trending - 全站热搜榜
    """
    cache_key = f"bili_{btype}_{keyword}_{partition}_{limit}"
    cached = load_cache(cache_key, 30)
    if cached:
        return cached

    results = []
    try:
        headers = {
            "Referer": "https://www.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        if btype == "trending":
            resp = req("https://s.search.bilibili.com/main/hotword", headers=headers)
            data = resp.json()
            for item in data.get("list", [])[:limit]:
                results.append({
                    "keyword": item.get("keyword", ""),
                    "hot_id": item.get("hot_id", ""),
                    "show_name": item.get("show_name", ""),
                    "heat_score": item.get("heat_score", 0),
                })

        elif btype == "search" and keyword:
            # Bilibili 搜索需要完整 headers，否则空响应
            search_headers = {
                **headers,
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.bilibili.com",
            }
            resp = requests.get(
                "https://api.bilibili.com/x/web-interface/search/type",
                params={"search_type": "video", "keyword": keyword,
                        "page": 1, "page_size": limit},
                headers=search_headers,
                timeout=15
            )
            if resp.status_code == 200 and resp.text:
                data = resp.json()
                for item in data.get("data", {}).get("result", [])[:limit]:
                    results.append({
                        "title": item.get("title", "").replace('<em class="keyword">', '').replace('</em>', ''),
                        "url": f"https://www.bilibili.com/video/{item.get('bvid')}",
                        "author": item.get("author", ""),
                        "play": item.get("play", 0),
                        "pubdate": datetime.fromtimestamp(item.get("pubdate", 0)).strftime("%Y-%m-%d"),
                    })

        elif btype == "hot":
            # ranking v2 API 需要登录，改用公开 RSS
            tid_map = {"独立游戏": 321, "单机游戏": 4, "网络游戏": 5, "手机游戏": 8, "游戏资讯": 17}
            tid = tid_map.get(partition, 321) if partition else 321
            rss_url = f"https://www.bilibili.com/rss/region/{tid}/ranking/0/day.xml"
            try:
                feed = feedparser.parse(rss_url)
                for entry in feed.entries[:limit]:
                    results.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "author": entry.get("author", ""),
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", "")[:150],
                    })
            except Exception as rss_err:
                print(f"  ⚠️  Bilibili RSS 失败，尝试热搜替代: {rss_err}")
                resp2 = req("https://s.search.bilibili.com/main/hotword", headers=headers)
                data2 = resp2.json()
                for item in data2.get("list", [])[:limit]:
                    results.append({
                        "keyword": item.get("keyword", ""),
                        "show_name": item.get("show_name", ""),
                        "heat_score": item.get("heat_score", 0),
                    })

    except Exception as e:
        print(f"  ❌ Bilibili 抓取失败: {e}")

    save_cache(cache_key, results)
    return results


# ─────────────────────────────────────────────────────────────
#  小红书 (Playwright + Cookie 鉴权)
# ─────────────────────────────────────────────────────────────

XHS_PROFILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "data", "xhs_profile")
XHS_COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "data", "xhs_cookies.json")


def _xhs_logged_in():
    """检查小红书 Cookie 文件是否存在且有内容"""
    if not os.path.exists(XHS_COOKIE_FILE):
        return False
    try:
        with open(XHS_COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        return any(c.get("value") for c in cookies if c.get("name") == "web_session")
    except Exception:
        return False


def fetch_xiaohongshu(query_type="search", keyword="独立游戏", limit=20):
    """
    抓取小红书笔记（需要先运行 xhs_inject_cookies.py 完成登录）

    query_type:
      search  - 搜索关键词（默认）
      hot     - 发现页热门（首页推荐）

    使用前请先注入 Cookie：
      python3 scripts/xhs_inject_cookies.py
    """
    if not _xhs_logged_in():
        print("  ⚠️  小红书未登录，请先运行：")
        print("      python3 scripts/xhs_inject_cookies.py")
        return []

    cache_key = f"xhs_{query_type}_{(keyword or '').replace(' ','_')}_{limit}"
    cached = load_cache(cache_key, 30)
    if cached:
        print(f"  📦 使用缓存 ({cache_key})")
        return cached

    results = []
    try:
        from playwright.sync_api import sync_playwright
        from playwright_stealth import Stealth
        from bs4 import BeautifulSoup
        import urllib.parse

        # 读取 Cookie
        with open(XHS_COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = [c for c in json.load(f) if c.get("value")]

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                XHS_PROFILE_DIR,
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
            page = context.pages[0] if context.pages else context.new_page()
            Stealth().apply_stealth_sync(page)

            # 确保 Cookie 生效
            page.goto("https://www.xiaohongshu.com/", timeout=20000)
            page.wait_for_timeout(1500)
            context.add_cookies(cookies)

            if query_type == "hot":
                # ── 发现页热门 ──
                page.goto("https://www.xiaohongshu.com/explore", timeout=20000)
                page.wait_for_load_state("networkidle", timeout=15000)

            else:
                # ── 搜索关键词 ──
                kw_enc = urllib.parse.quote(keyword or "独立游戏")
                url = (f"https://www.xiaohongshu.com/search_result"
                       f"?keyword={kw_enc}&source=web_search_result_notes&type=51")
                page.goto(url, timeout=20000)
                page.wait_for_load_state("networkidle", timeout=15000)

            # 等待笔记卡片
            try:
                page.wait_for_selector(
                    "section.note-item, .note-item, [class*='NoteItem'], "
                    "a[href*='/explore/']",
                    timeout=8000
                )
            except Exception:
                pass

            page.wait_for_timeout(2000)
            soup = BeautifulSoup(page.content(), "html.parser")

            # 检查登录状态
            text = soup.get_text()
            if "登录后查看" in text or "登录" in page.url:
                print("  ❌ Cookie 已失效，请重新运行 xhs_inject_cookies.py")
                context.close()
                return []

            # 解析笔记卡片
            note_items = soup.select(
                "section.note-item, .note-item, "
                "[class*='NoteCard'], [class*='note-card']"
            )

            for note in note_items[:limit]:
                # 标题
                title_el = note.select_one(
                    ".title, a.title, span.title, "
                    "[class*='title'], footer span"
                )
                title = title_el.get_text(strip=True) if title_el else ""

                # 作者
                author_el = note.select_one(
                    ".author-wrapper .name, .user-info .name, "
                    "[class*='author'] [class*='name'], "
                    "a[class*='author']"
                )
                author = author_el.get_text(strip=True) if author_el else ""

                # 点赞数
                likes_el = note.select_one(
                    ".like-wrapper .count, .interact-info .count, "
                    "[class*='like'] [class*='count'], "
                    "span[class*='like-count']"
                )
                likes = likes_el.get_text(strip=True) if likes_el else ""

                # 链接
                link_el = (note.select_one("a[href*='/explore/']")
                           or note.select_one("a[href*='/search_result']"))
                url = ""
                if link_el and link_el.get("href"):
                    href = link_el["href"]
                    url = href if href.startswith("http") else f"https://www.xiaohongshu.com{href}"

                if title:
                    results.append({
                        "title":  title,
                        "author": author,
                        "likes":  likes,
                        "url":    url,
                        "source": "小红书",
                    })

            context.close()

    except Exception as e:
        import traceback
        print(f"  ❌ 小红书抓取失败: {e}")
        traceback.print_exc()

    save_cache(cache_key, results)
    return results


# ─────────────────────────────────────────────────────────────
#  CLI 入口
# ─────────────────────────────────────────────────────────────

def print_results(results, label=""):
    if label:
        print(f"\n{'='*55}\n  {label}\n{'='*55}")
    if not results:
        print("  （无结果）")
        return
    for i, r in enumerate(results, 1):
        title = (r.get("title") or r.get("name") or r.get("text", "")[:80]
                 or r.get("keyword", "") or r.get("show_name", ""))
        url   = r.get("url", "") or r.get("steam_url", "")
        steamdb_url = r.get("steamdb") or r.get("steamdb_url", "")
        extra = ""
        if r.get("rank"):             extra += f"  #{r['rank']}"
        if r.get("current_players"):  extra += f"  👥在线:{r['current_players']}"
        if r.get("peak_2weeks"):      extra += f"  📈峰值:{r['peak_2weeks']}"
        if r.get("avg_30d"):          extra += f"  30天均:{r['avg_30d']}"
        if r.get("points"):           extra += f"  ⬆ {r['points']}"
        if r.get("likes"):            extra += f"  ❤ {r['likes']}"
        if r.get("play"):             extra += f"  ▶ {r['play']}"
        if r.get("ccu"):              extra += f"  CCU:{r['ccu']}"
        if r.get("discount") and r["discount"] > 0:
            extra += f"  -{r['discount']}%"
            if r.get("final_price"):  extra += f" ({r['final_price']})"
        if r.get("heat_score"):       extra += f"  🔥{r['heat_score']}"

        # 单游详情特殊展示
        if r.get("player_history"):
            print(f"  {'─'*50}")
            print(f"  🎮 {title}")
            if r.get("developers"):  print(f"     开发商: {r['developers']}")
            if r.get("genres"):      print(f"     类型: {r['genres']}")
            if r.get("release_date"):print(f"     发售: {r['release_date']}")
            if r.get("price"):       print(f"     现价: {r['price']}{' (折扣'+str(r['discount'])+'%)' if r.get('discount') else ''}")
            if r.get("description"): print(f"     简介: {r['description'][:100]}...")
            if url:          print(f"     Steam:    {url}")
            if steamdb_url:  print(f"     SteamDB:  {steamdb_url}")
            if r.get("steamcharts_url"): print(f"     Charts:   {r['steamcharts_url']}")
            if r.get("player_history"):
                print(f"     历史在线:")
                for h in r["player_history"][:4]:
                    print(f"       {h['month']:12s} 均:{h['avg']:>8s}  峰:{h['peak']:>8s}  {h['gain']}")
            continue

        print(f"  {i:>2}. {title[:65]}")
        if url: print(f"      Steam:   {url}")
        if steamdb_url and steamdb_url != url: print(f"      SteamDB: {steamdb_url}")
        if extra: print(f"     {extra}")


def main():
    parser = argparse.ArgumentParser(description="Work Assistant Fetcher")
    parser.add_argument("--source", required=True,
                        choices=["x", "reddit", "hn", "steam", "steamdb", "itch",
                                 "youtube", "bilibili", "xhs", "all-game", "all-ai"])
    parser.add_argument("--query",     default=None)
    parser.add_argument("--subreddit", default="gamedev")
    parser.add_argument("--type",      default=None, help="子类型: trending/search/new/hot/top/latest")
    parser.add_argument("--keyword",   default=None)
    parser.add_argument("--channel",   default="GDC")
    parser.add_argument("--partition", default="独立游戏")
    parser.add_argument("--limit",     type=int, default=10)
    parser.add_argument("--json",      action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    source = args.source
    limit  = args.limit

    if source == "x":
        q = args.query or "game development indie"
        data = fetch_x(q, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"X (Twitter) 搜索: {q}")

    elif source == "reddit":
        sort = args.type or "hot"
        data = fetch_reddit(args.subreddit, limit, sort)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"Reddit r/{args.subreddit} ({sort})")

    elif source == "hn":
        q = args.query
        data = fetch_hn(q, limit, args.type or "top")
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"Hacker News {'搜索: '+q if q else '热门'}")

    elif source == "steam":
        t = args.type or "trending"
        data = fetch_steam(t, args.keyword, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"Steam {t}")

    elif source == "steamdb":
        t = args.type or "top"
        kw = args.keyword or args.query
        data = fetch_steamdb(t, kw, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            label_map = {
                "top": "SteamDB - 实时在线人数排行 (via SteamCharts)",
                "peak": "SteamDB - 近2周峰值在线排行",
                "deals": "SteamDB - 当前打折促销",
                "new": "SteamDB - 新发售游戏",
                "app": f"SteamDB - 游戏详情 (appid={kw})",
                "search": f"SteamDB - 搜索: {kw}",
            }
            print_results(data, label_map.get(t, f"SteamDB {t}"))

    elif source == "itch":
        t = args.type or "new"
        data = fetch_itch(t, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"itch.io ({t})")

    elif source == "youtube":
        data = fetch_youtube(channel_name=args.channel, limit=limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"YouTube: {args.channel}")

    elif source == "bilibili":
        t = args.type or "hot"
        data = fetch_bilibili(t, args.keyword, args.partition, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else: print_results(data, f"Bilibili {t} - {args.keyword or args.partition}")

    elif source == "xhs":
        t = args.type or "search"
        kw = args.keyword or args.query or "独立游戏"
        data = fetch_xiaohongshu(t, kw, limit)
        if args.json: print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            label = f"小红书 {'热门' if t == 'hot' else '搜索: ' + kw}"
            print_results(data, label)

    elif source == "all-game":
        print("\n🎮 游戏新趋势全平台抓取\n")
        print_results(fetch_steamdb("top", limit=limit),       "SteamDB 实时在线排行 (SteamCharts)")
        print_results(fetch_steam("trending", limit=limit),    "Steam 特惠/新游榜")
        print_results(fetch_itch("top-rated", limit=limit),    "itch.io 高评分独立游戏")
        print_results(fetch_reddit("gamedev", limit, "hot"),   "Reddit r/gamedev 热门")
        print_results(fetch_reddit("indiegaming", limit, "hot"),"Reddit r/indiegaming 热门")
        print_results(fetch_bilibili("hot", None, "独立游戏", limit), "Bilibili 独立游戏热门")
        print_results(fetch_hn("game development", limit),     "HN 游戏开发话题")
        print_results(fetch_xiaohongshu("search", "独立游戏", limit), "小红书 独立游戏")

    elif source == "all-ai":
        print("\n🤖 AI 编程动态全平台抓取\n")
        print_results(fetch_hn("AI coding agent", limit),      "HN AI编程动态")
        print_results(fetch_reddit("LocalLLaMA", limit, "hot"),"Reddit r/LocalLLaMA 热门")
        print_results(fetch_reddit("cursor_ai", limit, "hot"), "Reddit r/cursor_ai 热门")
        print_results(fetch_bilibili("search", "AI编程", None, limit), "Bilibili AI编程")
        print_results(fetch_x("vibe coding cursor claude", limit), "X: vibe coding动态")


if __name__ == "__main__":
    main()

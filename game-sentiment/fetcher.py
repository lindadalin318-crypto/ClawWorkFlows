#!/usr/bin/env python3
"""
游戏舆情监控 - 数据抓取模块
支持平台：TapTap / B站 / NGA / 小红书
"""

import requests
import json
import re
import time
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from config import GAME_CONFIG, FETCH_CONFIG

logger = logging.getLogger(__name__)

# ============================================================
# 工具函数
# ============================================================

def get_cutoff_time():
    """返回抓取截止时间（N小时前）"""
    return datetime.now() - timedelta(hours=FETCH_CONFIG["hours_lookback"])

def clean_html(text):
    """清理HTML标签"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def make_session(referer=None):
    """创建带基础 headers 的 Session"""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
    })
    if referer:
        s.headers["Referer"] = referer
    return s


# ============================================================
# TapTap 抓取
# ============================================================

def fetch_taptap_reviews():
    """抓取 TapTap 评论（最新评价）"""
    app_id = GAME_CONFIG["taptap_app_id"]
    items = []
    cutoff = get_cutoff_time()

    # 每次用全新 Session，避免 WAF 识别
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    })
    # 必须先访问主页 + 评论页，获取 WAF cookie (acw_tc)，再调用 API
    try:
        s.get("https://www.taptap.cn/", timeout=10)
        time.sleep(1)
        s.get(f"https://www.taptap.cn/app/{app_id}/review", timeout=10)
        time.sleep(0.5)
    except Exception:
        pass

    # TapTap 评论 API（通过浏览器抓包确认的真实端点，limit 最大为 10）
    url = "https://www.taptap.cn/webapiv2/review/v2/list-by-app"
    base_params = {
        "app_id": app_id,
        "X-UA": "V=1&PN=WebApp&LANG=zh_CN&VN_CODE=102&LOC=CN&PLT=PC&DS=PC&UID=&OS=MacOS&OSV=10.15.7&DT=PC",
        "sort": "new",
        "limit": FETCH_CONFIG["taptap_max_reviews"],  # 最大 10
        "label": "",
        "mapping": "",
        "source_type": "",
        "stage_type": "",
        "test_plan_id": "",
    }

    try:
        cursor = ""
        pages = FETCH_CONFIG.get("taptap_pages", 3)
        for page in range(pages):
            params = dict(base_params)
            if cursor:
                params["from"] = cursor
            r = s.get(url, params=params, headers={"Referer": f"https://www.taptap.cn/app/{app_id}/review", "Accept": "application/json"}, timeout=15)
            if r.status_code != 200:
                logger.warning(f"TapTap reviews page {page+1} failed: {r.status_code}")
                break
            data = r.json()
            moment_list = data.get("data", {}).get("list", [])
            if not moment_list:
                break
            cursor = data.get("data", {}).get("next_cursor", "")
            for item in moment_list:
                moment = item.get("moment", {})
                review = moment.get("review", {})
                if not review:
                    continue
                ts = moment.get("publish_time", 0) or moment.get("created_time", 0)
                dt = datetime.fromtimestamp(ts) if ts else None
                if dt and dt < cutoff:
                    continue
                contents = review.get("contents", {})
                text = clean_html(contents.get("text", "") or contents.get("raw_text", "") or contents.get("summary", ""))
                author_info = moment.get("author", {}).get("user", {})
                stat = moment.get("stat", {})
                review_id = review.get("id", "")
                items.append({
                    "source": "TapTap",
                    "type": "review",
                    "title": "",
                    "content": text[:500],
                    "score": review.get("score", 0),
                    "author": author_info.get("name", ""),
                    "likes": stat.get("ups", 0),
                    "comments": stat.get("comments_count", 0),
                    "url": f"https://www.taptap.cn/review/{review_id}" if review_id else f"https://www.taptap.cn/app/{app_id}/review",
                    "published_at": dt.isoformat() if dt else "",
                    "raw": {},
                })
            if not cursor:
                break
            time.sleep(0.5)
        logger.info(f"TapTap reviews: {len(items)} items")
    except Exception as e:
        logger.error(f"TapTap fetch error: {e}")

    return items


def fetch_taptap_forum():
    """抓取 TapTap 论坛帖子"""
    app_id = GAME_CONFIG["taptap_app_id"]
    items = []
    cutoff = get_cutoff_time()

    # 每次用全新 Session，先访问论坛页获取 WAF cookie
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    })
    try:
        s.get("https://www.taptap.cn/", timeout=10)
        time.sleep(1)
        s.get(f"https://www.taptap.cn/app/{app_id}/topic", timeout=10)
        time.sleep(0.5)
    except Exception:
        pass

    # TapTap 论坛帖子 API（通过浏览器抓包确认）
    url = "https://www.taptap.cn/webapiv2/topic/v3/by-app"
    params = {
        "app_id": app_id,
        "X-UA": "V=1&PN=WebApp&LANG=zh_CN&VN_CODE=102&LOC=CN&PLT=PC&DS=PC&UID=&OS=MacOS&OSV=10.15.7&DT=PC",
        "type": "new",
        "limit": FETCH_CONFIG["taptap_max_reviews"],
    }

    try:
        r = s.get(url, params=params, headers={"Referer": "https://www.taptap.cn/app/188212/topic", "Accept": "application/json"}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            topics = data.get("data", {}).get("list", [])
            for t in topics:
                moment = t.get("moment", t)  # 兼容两种数据格式
                ts = moment.get("publish_time", 0) or moment.get("created_time", 0)
                dt = datetime.fromtimestamp(ts) if ts else None
                if dt and dt < cutoff:
                    continue
                contents = moment.get("contents", {})
                title = clean_html(contents.get("title", "") or moment.get("title", ""))
                summary = clean_html(contents.get("text", "") or moment.get("summary", ""))
                author_info = moment.get("author", {}).get("user", moment.get("user", {}))
                stat = moment.get("stat", {})
                moment_id = moment.get("id_str", moment.get("id", ""))
                items.append({
                    "source": "TapTap论坛",
                    "type": "post",
                    "title": title,
                    "content": summary[:300],
                    "author": author_info.get("name", ""),
                    "likes": stat.get("ups", stat.get("liked_count", 0)),
                    "comments": stat.get("comments_count", 0),
                    "url": f"https://www.taptap.cn/moment/{moment_id}" if moment_id else f"https://www.taptap.cn/app/{app_id}/topic",
                    "published_at": dt.isoformat() if dt else "",
                    "raw": t,
                })
        logger.info(f"TapTap forum: {len(items)} items")
    except Exception as e:
        logger.error(f"TapTap forum error: {e}")

    return items


# ============================================================
# B站抓取
# ============================================================

def fetch_bilibili_videos():
    """抓取 B站最新视频"""
    items = []
    cutoff = get_cutoff_time()
    keywords = GAME_CONFIG["bilibili_keywords"]

    s = make_session("https://www.bilibili.com")
    # 获取 buvid3 cookie
    try:
        s.get("https://www.bilibili.com", timeout=10)
    except Exception:
        pass

    for kw in keywords:
        try:
            r = s.get(
                "https://api.bilibili.com/x/web-interface/search/type",
                params={
                    "search_type": "video",
                    "keyword": kw,
                    "order": "pubdate",
                    "page": 1,
                    "page_size": FETCH_CONFIG["bilibili_max_videos"],
                },
                headers={"Referer": "https://www.bilibili.com"},
                timeout=15,
            )
            if r.status_code != 200:
                continue
            data = r.json()
            results = data.get("data", {}).get("result", [])
            for v in results:
                pub_ts = v.get("pubdate", 0)
                dt = datetime.fromtimestamp(pub_ts) if pub_ts else None
                if dt and dt < cutoff:
                    continue
                title = clean_html(v.get("title", ""))
                desc = clean_html(v.get("description", ""))
                items.append({
                    "source": "B站",
                    "type": "video",
                    "title": title,
                    "content": desc[:200],
                    "author": v.get("author", ""),
                    "views": v.get("play", 0),
                    "likes": v.get("like", 0),
                    "danmaku": v.get("video_review", 0),
                    "url": f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                    "bvid": v.get("bvid", ""),
                    "published_at": dt.isoformat() if dt else "",
                    "raw": {k: v[k] for k in ["bvid", "title", "author", "play", "like", "pubdate"] if k in v},
                })
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Bilibili fetch error ({kw}): {e}")

    # 去重（按 bvid）
    seen = set()
    unique = []
    for item in items:
        key = item.get("bvid", item["title"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    logger.info(f"Bilibili videos: {len(unique)} items")
    return unique


def fetch_bilibili_comments(bvid, max_comments=20):
    """抓取单个 B站视频的热门评论"""
    items = []
    s = make_session("https://www.bilibili.com")
    try:
        s.get("https://www.bilibili.com", timeout=10)
        # 获取视频 oid（cid）
        r = s.get(
            f"https://api.bilibili.com/x/web-interface/view",
            params={"bvid": bvid},
            timeout=10,
        )
        if r.status_code == 200:
            oid = r.json().get("data", {}).get("aid", "")
            if oid:
                r2 = s.get(
                    "https://api.bilibili.com/x/v2/reply",
                    params={"type": 1, "oid": oid, "sort": 2, "ps": max_comments},
                    timeout=10,
                )
                if r2.status_code == 200:
                    replies = r2.json().get("data", {}).get("replies", []) or []
                    for rep in replies:
                        items.append({
                            "source": "B站评论",
                            "type": "comment",
                            "content": rep.get("content", {}).get("message", ""),
                            "author": rep.get("member", {}).get("uname", ""),
                            "likes": rep.get("like", 0),
                            "url": f"https://www.bilibili.com/video/{bvid}",
                        })
    except Exception as e:
        logger.error(f"Bilibili comments error ({bvid}): {e}")
    return items


# ============================================================
# NGA 抓取（Playwright）
# ============================================================

def fetch_nga_posts():
    """
    抓取 NGA 帖子
    NGA 需要登录 Cookie，使用 Playwright 持久化 Profile
    若无登录状态，降级为关键词搜索页面解析
    """
    items = []
    cutoff = get_cutoff_time()

    # 方案一：直接 HTTP（搜索页面）
    items_http = _fetch_nga_via_http()
    if items_http:
        items.extend(items_http)

    # 方案二：Playwright（需要登录）
    if len(items) < 5:
        items_pw = _fetch_nga_via_playwright()
        items.extend(items_pw)

    logger.info(f"NGA posts: {len(items)} items")
    return items


def _fetch_nga_via_http():
    """通过 HTTP 抓取 NGA（不需要登录的部分）"""
    items = []
    keywords = GAME_CONFIG["nga_keywords"]
    cutoff = get_cutoff_time()

    s = make_session()
    s.headers["Accept-Charset"] = "GBK,utf-8;q=0.7,*;q=0.3"

    for kw in keywords:
        try:
            # NGA 帖子列表（按关键词+时间过滤）
            r = s.get(
                "https://bbs.nga.cn/thread.php",
                params={"forumkey": kw, "orderby": "postdateline", "page": 1},
                timeout=15,
            )
            if r.status_code != 200:
                continue

            content = r.content.decode("gbk", errors="ignore")
            soup = BeautifulSoup(content, "lxml")

            # 解析帖子列表
            rows = soup.select("tr.topicrow, div.topic_row, .forumbox tbody tr")
            for row in rows[:FETCH_CONFIG["nga_max_posts"]]:
                link = row.select_one("a[href*='read.php']")
                if not link:
                    continue
                title = link.get_text(strip=True)
                href = link.get("href", "")
                tid = re.search(r"tid=(\d+)", href)
                url = f"https://bbs.nga.cn{href}" if href.startswith("/") else href

                # 时间
                time_el = row.select_one(".postdate, .time, td:last-child")
                pub_str = time_el.get_text(strip=True) if time_el else ""

                items.append({
                    "source": "NGA",
                    "type": "post",
                    "title": title,
                    "content": "",
                    "author": "",
                    "url": url,
                    "tid": tid.group(1) if tid else "",
                    "published_at": pub_str,
                    "raw": {},
                })

        except Exception as e:
            logger.error(f"NGA HTTP error ({kw}): {e}")

    return items


def _fetch_nga_via_playwright():
    """通过 Playwright 抓取 NGA（需要登录 profile）"""
    items = []
    try:
        from playwright.sync_api import sync_playwright
        try:
            from playwright_stealth import stealth_sync
        except ImportError:
            from playwright_stealth import Stealth
            stealth_sync = lambda page: Stealth().apply_stealth_sync(page)
        from config import XHS_PROFILE  # 复用 profile 目录概念
        import os

        nga_profile = "/Users/dada/game-sentiment/nga_profile"
        os.makedirs(nga_profile, exist_ok=True)

        keywords = GAME_CONFIG["nga_keywords"]
        cutoff = get_cutoff_time()

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                nga_profile,
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            page = browser.new_page()
            stealth_sync(page)

            for kw in keywords[:1]:  # 只搜第一个关键词避免太慢
                try:
                    url = f"https://bbs.nga.cn/thread.php?forumkey={requests.utils.quote(kw)}&orderby=postdateline"
                    page.goto(url, timeout=20000)
                    page.wait_for_load_state("domcontentloaded")

                    # 检查是否需要登录
                    content = page.content()
                    if "访客不能" in content or "请登录" in content:
                        logger.warning("NGA requires login, skipping Playwright fetch")
                        break

                    soup = BeautifulSoup(content, "lxml")
                    rows = soup.select("a[href*='read.php?tid']")
                    for link in rows[:FETCH_CONFIG["nga_max_posts"]]:
                        title = link.get_text(strip=True)
                        href = link.get("href", "")
                        if not title or len(title) < 3:
                            continue
                        url_post = f"https://bbs.nga.cn{href}" if href.startswith("/") else href
                        items.append({
                            "source": "NGA",
                            "type": "post",
                            "title": title,
                            "content": "",
                            "author": "",
                            "url": url_post,
                            "published_at": "",
                        })

                except Exception as e:
                    logger.error(f"NGA Playwright page error: {e}")

            browser.close()

    except Exception as e:
        logger.error(f"NGA Playwright error: {e}")

    return items


# ============================================================
# 小红书抓取（Playwright，需要登录）
# ============================================================

def fetch_xiaohongshu_notes():
    """
    抓取小红书笔记（需要 Playwright + 登录）
    首次运行需手动登录，之后持久化 profile
    """
    items = []
    try:
        from playwright.sync_api import sync_playwright
        try:
            from playwright_stealth import stealth_sync
        except ImportError:
            from playwright_stealth import Stealth
            stealth_sync = lambda page: Stealth().apply_stealth_sync(page)
        import os

        xhs_profile = "/Users/dada/game-sentiment/xhs_profile"
        os.makedirs(xhs_profile, exist_ok=True)
        keywords = GAME_CONFIG["xiaohongshu_keywords"]
        cutoff = get_cutoff_time()

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                xhs_profile,
                headless=False,  # 小红书反爬严格，用有头模式
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            page = browser.new_page()
            stealth_sync(page)

            for kw in keywords[:1]:
                try:
                    search_url = f"https://www.xiaohongshu.com/search_result?keyword={requests.utils.quote(kw)}&source=web_search_result_notes&type=51"
                    page.goto(search_url, timeout=30000)
                    page.wait_for_load_state("networkidle", timeout=15000)

                    # 检查登录状态
                    content = page.content()
                    if "登录" in content and "注册" in content and len(content) < 50000:
                        logger.warning("XHS requires login. Please run xhs_login.py first.")
                        break

                    # 等待笔记卡片加载
                    page.wait_for_selector("section.note-item, .feeds-container .note-item", timeout=10000)

                    soup = BeautifulSoup(page.content(), "lxml")
                    notes = soup.select("section.note-item, .note-item")

                    for note in notes[:FETCH_CONFIG["xhs_max_notes"]]:
                        title_el = note.select_one(".title, a.title, span.title")
                        title = title_el.get_text(strip=True) if title_el else ""
                        author_el = note.select_one(".author-wrapper .name, .user-info .name")
                        author = author_el.get_text(strip=True) if author_el else ""
                        likes_el = note.select_one(".like-wrapper .count, .interact-info .count")
                        likes = likes_el.get_text(strip=True) if likes_el else "0"
                        link_el = note.select_one("a[href*='/explore/']")
                        url = f"https://www.xiaohongshu.com{link_el['href']}" if link_el else ""

                        if title:
                            items.append({
                                "source": "小红书",
                                "type": "note",
                                "title": title,
                                "content": "",
                                "author": author,
                                "likes": likes,
                                "url": url,
                                "published_at": "",
                            })

                    time.sleep(2)

                except Exception as e:
                    logger.error(f"XHS page error ({kw}): {e}")

            browser.close()

    except Exception as e:
        logger.error(f"XHS fetch error: {e}")

    logger.info(f"XiaoHongShu notes: {len(items)} items")
    return items


# ============================================================
# 主入口
# ============================================================

def fetch_all():
    """抓取所有平台数据，返回合并结果"""
    results = {
        "game": GAME_CONFIG["name"],
        "fetched_at": datetime.now().isoformat(),
        "sources": {},
    }

    print("📱 抓取 TapTap 评论...")
    results["sources"]["taptap_reviews"] = fetch_taptap_reviews()

    print("📱 抓取 TapTap 论坛...")
    results["sources"]["taptap_forum"] = fetch_taptap_forum()

    print("📺 抓取 B站视频...")
    results["sources"]["bilibili"] = fetch_bilibili_videos()

    print("🎮 抓取 NGA 帖子...")
    results["sources"]["nga"] = fetch_nga_posts()

    print("📕 抓取小红书笔记...")
    results["sources"]["xiaohongshu"] = fetch_xiaohongshu_notes()

    # 统计
    total = sum(len(v) for v in results["sources"].values())
    print(f"\n✅ 抓取完成，共 {total} 条数据")
    for src, items in results["sources"].items():
        print(f"   {src}: {len(items)} 条")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    data = fetch_all()
    out = "/Users/dada/game-sentiment/raw_latest.json"
    with open(out, "w", encoding="utf-8") as f:
        # 不保存 raw 字段（太大）
        for src in data["sources"].values():
            for item in src:
                item.pop("raw", None)
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 原始数据已保存：{out}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
work-assistant / assistant.py
==============================
工作辅助主入口，供 Knot (AI助手) 直接调用。
支持：
  - 查游戏新趋势（Steam / itch.io / Reddit / Bilibili）
  - 查 AI 编程动态（HN / Reddit / X）
  - 解答设计问题（联网搜索 + KM 内部资料）
  - 自定义关键词跨平台搜索

直接 import 使用：
  from scripts.assistant import run_task
  result = run_task("游戏趋势", limit=10)
  result = run_task("search", keyword="roguelike", platforms=["steam","reddit","x"])
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from fetcher import (
    fetch_steam, fetch_steamdb, fetch_itch, fetch_reddit, fetch_hn,
    fetch_bilibili, fetch_youtube, fetch_x, fetch_xiaohongshu,
    print_results
)

# ──────────────────────────────────────────────
TASK_MAP = {
    "游戏趋势":  "game_trend",
    "game":      "game_trend",
    "game_trend":"game_trend",
    "ai":        "ai_trend",
    "ai趋势":    "ai_trend",
    "ai_trend":  "ai_trend",
    "search":    "search",
    "搜索":      "search",
    "bilibili":  "bilibili",
    "b站":       "bilibili",
    "steam":     "steam",
    "steamdb":   "steamdb",
    "reddit":    "reddit",
    "x":         "x",
    "twitter":   "x",
    "hn":        "hn",
    "itch":      "itch",
    "youtube":   "youtube",
    "xhs":       "xhs",
    "小红书":    "xhs",
}


def run_task(task: str, keyword: str = None, platforms: list = None,
             limit: int = 10, output_json: bool = False):
    """
    task: 任务名（见 TASK_MAP）
    keyword: 搜索关键词
    platforms: 指定平台列表（用于 search 任务）
    limit: 返回条数
    output_json: 是否返回 JSON（否则打印可读格式）
    """
    import json

    task_key = TASK_MAP.get(task.lower(), task.lower())
    all_results = {}

    if task_key == "game_trend":
        all_results["steamdb_top"]       = fetch_steamdb("top", limit=limit)
        all_results["steam_trending"]    = fetch_steam("trending", limit=limit)
        all_results["itch_top_rated"]    = fetch_itch("top-rated", limit=limit)
        all_results["reddit_gamedev"]    = fetch_reddit("gamedev", limit, "hot")
        all_results["reddit_indiegaming"]= fetch_reddit("indiegaming", limit, "hot")
        all_results["bilibili_indie"]    = fetch_bilibili("hot", None, "独立游戏", limit)
        all_results["xhs_indie"]         = fetch_xiaohongshu("search", "独立游戏", limit)
        all_results["hn_game"]           = fetch_hn("game development indie", limit)

    elif task_key == "xhs":
        t = keyword if keyword in ("search", "hot") else "search"
        kw = keyword if t == "search" else None
        all_results["xhs"] = fetch_xiaohongshu(t, kw or "独立游戏", limit)

    elif task_key == "steamdb":
        t = keyword if keyword in ("top","peak","deals","new","app","search") else "top"
        kw = None if t == keyword else keyword
        all_results["steamdb"] = fetch_steamdb(t, kw, limit)

    elif task_key == "ai_trend":
        all_results["hn_ai"]             = fetch_hn("AI coding agent LLM", limit)
        all_results["reddit_localllama"] = fetch_reddit("LocalLLaMA", limit, "hot")
        all_results["reddit_cursor"]     = fetch_reddit("cursor_ai", limit, "hot")
        all_results["bilibili_ai"]       = fetch_bilibili("search", "AI编程", None, limit)
        all_results["x_vibe"]            = fetch_x("vibe coding cursor claude agent", limit)

    elif task_key == "search":
        kw = keyword or "game design"
        targets = platforms or ["hn", "reddit", "steam", "bilibili", "x"]
        for p in targets:
            if p == "hn":
                all_results["hn"]       = fetch_hn(kw, limit)
            elif p == "reddit":
                all_results["reddit"]   = fetch_reddit("gamedev", limit, "hot")
            elif p == "steam":
                all_results["steam"]    = fetch_steam("search", kw, limit)
            elif p == "bilibili":
                all_results["bilibili"] = fetch_bilibili("search", kw, None, limit)
            elif p == "x":
                all_results["x"]        = fetch_x(kw, limit)
            elif p == "itch":
                all_results["itch"]     = fetch_itch("new", limit)

    elif task_key == "steam":
        t = "search" if keyword else "trending"
        all_results["steam"] = fetch_steam(t, keyword, limit)

    elif task_key == "itch":
        all_results["itch"] = fetch_itch("top-rated", limit)

    elif task_key == "reddit":
        sub = keyword or "gamedev"
        all_results["reddit"] = fetch_reddit(sub, limit)

    elif task_key == "x":
        kw = keyword or "indie game"
        all_results["x"] = fetch_x(kw, limit)

    elif task_key == "hn":
        all_results["hn"] = fetch_hn(keyword, limit)

    elif task_key == "bilibili":
        if keyword:
            all_results["bilibili"] = fetch_bilibili("search", keyword, None, limit)
        else:
            all_results["bilibili"] = fetch_bilibili("hot", None, "独立游戏", limit)

    elif task_key == "youtube":
        ch = keyword or "GDC"
        all_results["youtube"] = fetch_youtube(channel_name=ch, limit=limit)

    else:
        print(f"⚠️  未知任务: {task}，支持: {list(TASK_MAP.keys())}")
        return {}

    # 输出
    if output_json:
        return all_results

    print(f"\n{'='*60}")
    print(f"  任务: {task_key}  关键词: {keyword or '(无)'}  条数/平台: {limit}")
    print(f"{'='*60}")
    for label, results in all_results.items():
        print_results(results, label)

    return all_results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("task",    help="任务名，例如: 游戏趋势 / ai趋势 / search / steam / bilibili")
    p.add_argument("--keyword",   default=None)
    p.add_argument("--platforms", nargs="*", default=None)
    p.add_argument("--limit",     type=int, default=10)
    p.add_argument("--json",      action="store_true")
    args = p.parse_args()
    run_task(args.task, args.keyword, args.platforms, args.limit, args.json)

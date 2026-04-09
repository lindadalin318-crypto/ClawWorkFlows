#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KM MCP 抓取脚本
通过 km MCP 工具抓取腾讯内部 KM 文章，输出为 JSON 文件
供 digest.py 读取

运行方式：由 run_digest.sh 通过 Knot/OpenClaw 调用
输出文件：km_results.json
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timezone, timedelta

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "km_results.json")
HOURS_BACK = 24

# ══════════════════════════════════════════════════════
#  模块一（AI + 游戏）关键词 - 中文为主 + 英文补充
# ══════════════════════════════════════════════════════
M1_KEYWORDS_ZH = [
    "游戏开发", "Unity", "Unreal", "UE5", "Godot",
    "游戏 AI", "AI 游戏", "游戏编程",
    "vibe coding", "VibeCoding",
    "AI NPC", "程序化生成",
    "游戏引擎", "独立游戏",
]
M1_KEYWORDS_EN = [
    "vibe coding game", "unity cursor", "unreal cursor",
    "godot cursor", "unity ai", "unreal ai", "godot ai",
    "game dev ai", "llm game",
]

# ══════════════════════════════════════════════════════
#  模块二（AI 通用）关键词 - 中文为主 + 英文补充
# ══════════════════════════════════════════════════════
M2_KEYWORDS_ZH = [
    "vibe coding", "AI 编程", "AI 辅助编程", "AI 代码",
    "Cursor", "Claude Code", "Windsurf", "Copilot",
    "CodeBuddy", "codebuddy", "OpenClaw",
    "AI Agent", "AI 工作流", "大模型", "LLM",
    "AI IDE", "AI 开发", "AI 效率",
    "MCP", "Agentic", "提示词工程",
    "context engineering",
]
M2_KEYWORDS_EN = [
    "vibe coding", "cursor ide", "claude code",
    "windsurf", "ai coding", "ai agent",
    "codebuddy", "MCP", "agentic coding",
]

ALL_M1_KW = M1_KEYWORDS_ZH + M1_KEYWORDS_EN
ALL_M2_KW = M2_KEYWORDS_ZH + M2_KEYWORDS_EN


def classify_article(title, tags="", summary=""):
    """
    判断文章属于哪个模块
    返回: "M1" / "M2" / None
    """
    text = (title + " " + tags + " " + summary).lower()

    # 游戏专属关键词（直接判定为 M1）
    game_specific = [
        "游戏开发", "unity", "unreal", "ue5", "godot",
        "游戏 ai", "ai 游戏", "游戏引擎", "独立游戏",
        "game dev", "gamedev", "game ai", "ai npc",
        "unity cursor", "unreal cursor", "godot cursor",
        "vibe coding game", "game dev ai",
    ]
    for kw in game_specific:
        if kw.lower() in text:
            return "M1"

    # 通用 AI 编程关键词（M2）
    for kw in ALL_M2_KW:
        if kw.lower() in text:
            return "M2"

    return None


def parse_km_article_line(line):
    """
    解析 KM MCP 返回的单行文章数据
    格式：标题: xxx, 作者: xxx, 创建时间: xxx, ..., 链接: xxx
    """
    item = {}
    try:
        # 提取标题
        if "标题:" in line:
            title_start = line.index("标题:") + 3
            title_end = line.index(", 作者:") if ", 作者:" in line else len(line)
            item["title"] = line[title_start:title_end].strip()

        # 提取作者
        if ", 作者:" in line:
            author_start = line.index(", 作者:") + 5
            author_end = line.index(",", author_start) if "," in line[author_start:] else len(line)
            item["author"] = line[author_start:author_end].strip()

        # 提取导语/摘要
        if "导语:" in line:
            summary_start = line.index("导语:") + 3
            # 导语结束于下一个主字段
            for end_marker in [", 标签:", ", 阅读:", ", 链接:"]:
                if end_marker in line[summary_start:]:
                    summary_end = line.index(end_marker, summary_start)
                    item["summary"] = line[summary_start:summary_end].strip()
                    break
            else:
                item["summary"] = line[summary_start:summary_start+200].strip()

        # 提取标签
        if "标签:" in line:
            tags_start = line.index("标签:") + 3
            tags_end = line.index(", 阅读:") if ", 阅读:" in line else len(line)
            item["tags"] = line[tags_start:tags_end].strip()

        # 提取阅读数
        if "阅读:" in line:
            read_start = line.index("阅读:") + 3
            read_end = line.index(",", read_start) if "," in line[read_start:] else len(line)
            try:
                item["read_count"] = int(line[read_start:read_end].strip())
            except ValueError:
                item["read_count"] = 0

        # 提取热度
        if "热度:" in line:
            hot_start = line.index("热度:") + 3
            hot_end = line.index(",", hot_start) if "," in line[hot_start:] else len(line)
            try:
                item["hot_value"] = int(line[hot_start:hot_end].strip())
            except ValueError:
                item["hot_value"] = 0

        # 提取链接
        if "链接:" in line:
            link_start = line.index("链接:") + 3
            item["url"] = line[link_start:].strip()

        # 提取创建时间
        if "创建时间:" in line:
            ct_start = line.index("创建时间:") + 5
            ct_end = line.index(",", ct_start) if "," in line[ct_start:] else len(line)
            item["created_time"] = line[ct_start:ct_end].strip()

        # 提取 KM 推荐 / 头条
        item["km_recommended"] = "KM推荐: 是" in line
        item["km_headline"] = "KM头条: 是" in line

        # 提取 K 吧
        if "K吧:" in line:
            kbar_start = line.index("K吧:") + 3
            kbar_end = line.index(",", kbar_start) if "," in line[kbar_start:] else len(line)
            item["kbar"] = line[kbar_start:kbar_end].strip()

    except Exception as e:
        print(f"  ⚠️  解析行失败: {e}", file=sys.stderr)

    return item if "title" in item and "url" in item else None


def fetch_km_articles():
    """
    通过 KM MCP API（HTTP）抓取文章
    使用 list-articles 工具，按关键词 + 时间范围过滤
    """
    print("📡 KM MCP 抓取开始...")

    # 计算 24 小时前的时间
    cutoff = datetime.now(timezone(timedelta(hours=8))) - timedelta(hours=HOURS_BACK)
    created_after = cutoff.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    results = []
    seen_urls = set()

    # ── 搜索策略 ──────────────────────────────────────────
    # 1. 先用游戏相关关键词搜索（模块一）
    # 2. 再用 AI 编程关键词搜索（模块二）
    # 3. 最后抓热榜兜底

    search_batches = [
        # (关键词列表, 描述)
        (["游戏开发", "Unity", "Unreal", "Godot", "UE5", "游戏 AI", "AI 游戏"], "游戏×AI（中文）"),
        (["vibe coding", "VibeCoding", "AI NPC", "游戏引擎 AI"], "游戏×VibeCoding"),
        (["CodeBuddy", "codebuddy", "Cursor", "Claude Code", "AI 编程"], "AI编程工具（中文）"),
        (["AI Agent", "MCP", "AI 工作流", "大模型", "vibe coding"], "AI通用（中文）"),
        (["unity cursor", "unreal cursor", "godot cursor", "game dev ai"], "游戏×AI（英文）"),
    ]

    for keywords, desc in search_batches:
        print(f"  🔍 搜索：{desc} ({len(keywords)} 个关键词)...")

        # 调用 KM MCP API
        # 注意：这里通过 subprocess 调用 mcp 命令行工具
        # 实际在 Knot/OpenClaw 环境中，直接通过 MCP 协议调用
        try:
            result = call_km_mcp_list_articles(
                keywords=keywords,
                created_after=created_after,
                limit=50,
                sort="updated"
            )

            if not result:
                continue

            # 解析结果
            lines = result.strip().split("\n")
            batch_count = 0
            for line in lines:
                line = line.strip()
                if not line.startswith("- 标题:"):
                    continue

                article = parse_km_article_line(line[2:])  # 去掉 "- " 前缀
                if not article or not article.get("url"):
                    continue

                url = article["url"]
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # 模块分类
                module = classify_article(
                    article.get("title", ""),
                    article.get("tags", ""),
                    article.get("summary", "")
                )
                if module is None:
                    continue

                article["module"] = module
                results.append(article)
                batch_count += 1

            print(f"    ✅ 获取 {batch_count} 条")

        except Exception as e:
            print(f"    ⚠️  搜索失败 {desc}: {e}", file=sys.stderr)

        time.sleep(0.5)

    # ── 热榜兜底（抓取今日热门，补充可能遗漏的内容）──────
    print("  🔥 抓取热榜兜底...")
    try:
        hot_result = call_km_mcp_hot_articles(period=2, limit=20)
        if hot_result:
            lines = hot_result.strip().split("\n")
            hot_count = 0
            for line in lines:
                line = line.strip()
                if not line.startswith("标题:"):
                    continue

                article = parse_km_article_line(line)
                if not article or not article.get("url"):
                    continue

                url = article["url"]
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                module = classify_article(
                    article.get("title", ""),
                    article.get("tags", ""),
                    article.get("summary", "")
                )
                if module is None:
                    continue

                article["module"] = module
                results.append(article)
                hot_count += 1

            print(f"    ✅ 热榜补充 {hot_count} 条")

    except Exception as e:
        print(f"    ⚠️  热榜抓取失败: {e}", file=sys.stderr)

    # ── 按模块分组统计 ─────────────────────────────────────
    m1 = [r for r in results if r.get("module") == "M1"]
    m2 = [r for r in results if r.get("module") == "M2"]

    print(f"\n  📊 KM 抓取完成：共 {len(results)} 条")
    print(f"     🎮 模块一（AI+游戏）: {len(m1)} 条")
    print(f"     🤖 模块二（AI通用）:  {len(m2)} 条")

    return results


def call_km_mcp_list_articles(keywords, created_after, limit=50, sort="updated"):
    """
    调用 KM MCP list-articles 工具
    通过 Python subprocess 调用 mcp 命令
    """
    # 构建 MCP 请求参数
    params = {
        "keywords": keywords,
        "created_after": created_after,
        "limit": limit,
        "sort": sort,
    }

    return _call_mcp_tool("km", "list-articles", params)


def call_km_mcp_hot_articles(period=2, limit=20):
    """
    调用 KM MCP hot-articles 工具
    """
    params = {
        "period": period,
        "limit": limit,
    }
    return _call_mcp_tool("km", "hot-articles", params)


def _call_mcp_tool(server, tool, params):
    """
    通过 mcp 命令行工具调用 MCP 服务
    """
    try:
        cmd = [
            "python3", "-c",
            f"""
import sys
sys.path.insert(0, '/Users/dada')
# 通过 mcp 客户端调用
import json
params = {json.dumps(params)}
print(json.dumps(params))
"""
        ]
        # 实际上这里需要通过 Knot 的 MCP bridge 来调用
        # 在 run_digest.sh 中，我们通过 Knot CLI 来执行
        # 这里作为占位，实际调用由 inject_km_from_file() 完成
        return None
    except Exception as e:
        print(f"  ⚠️  MCP 调用失败: {e}", file=sys.stderr)
        return None


def inject_km_from_raw(raw_text):
    """
    直接解析 KM MCP 返回的原始文本（由外部注入）
    raw_text: KM MCP list-articles 返回的完整文本
    """
    results = []
    seen_urls = set()

    lines = raw_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line.startswith("- 标题:"):
            continue

        article = parse_km_article_line(line[2:])
        if not article or not article.get("url"):
            continue

        url = article["url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)

        module = classify_article(
            article.get("title", ""),
            article.get("tags", ""),
            article.get("summary", "")
        )
        if module is None:
            continue

        article["module"] = module
        results.append(article)

    return results


def save_results(results):
    """保存结果到 JSON 文件"""
    output = {
        "generated_at": datetime.now().isoformat(),
        "total": len(results),
        "m1_count": sum(1 for r in results if r.get("module") == "M1"),
        "m2_count": sum(1 for r in results if r.get("module") == "M2"),
        "articles": results,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  💾 已保存到 {OUTPUT_PATH}")
    return OUTPUT_PATH


def main():
    print("=" * 55)
    print("📡 KM MCP 抓取脚本")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔍 抓取过去 {HOURS_BACK} 小时的 KM 文章")
    print("=" * 55)

    # 如果有命令行参数（raw text 文件路径），直接解析
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        print(f"📂 读取外部数据文件: {sys.argv[1]}")
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw_text = f.read()
        results = inject_km_from_raw(raw_text)
    else:
        results = fetch_km_articles()

    if results:
        save_results(results)
        print(f"\n✅ KM 数据已就绪，共 {len(results)} 条")
    else:
        print("\n⚠️  未获取到 KM 数据，创建空文件")
        save_results([])

    return OUTPUT_PATH


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
游戏舆情监控 - 报告生成模块
输入：analysis_latest.json
输出：sentiment_YYYY-MM-DD.md + latest_summary.txt
"""

import json
import os
from datetime import datetime
from config import GAME_CONFIG, OUTPUT_DIR


def generate_report(analysis, raw_data=None):
    """生成 Markdown 舆情报告"""
    game_name = analysis.get("game", GAME_CONFIG["name"])
    analyzed_at = analysis.get("analyzed_at", "")
    date_str = analyzed_at[:10] if analyzed_at else datetime.now().strftime("%Y-%m-%d")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    overview = analysis.get("sentiment_overview", {})
    platform_stats = analysis.get("platform_stats", {})
    hot_topics = analysis.get("hot_topics", [])
    complaints = analysis.get("complaints", [])
    memes = analysis.get("memes", [])
    top_positive = analysis.get("top_positive", [])
    top_negative = analysis.get("top_negative", [])
    top_keywords = analysis.get("top_keywords", [])

    lines = []

    # ---- 标题 ----
    lines.append(f"# 🎮 {game_name} 舆情日报")
    lines.append(f"> 生成时间：{now_str}　|　数据来源：TapTap · B站 · NGA · 小红书")
    lines.append("")

    # ---- 今日概览 ----
    lines.append("## 📊 今日舆情概览")
    lines.append("")
    overall = overview.get("overall", "")
    pos_pct = overview.get("positive_pct", 0)
    neg_pct = overview.get("negative_pct", 0)
    total = overview.get("total", 0)

    lines.append(f"**整体情绪：{overall}**")
    lines.append("")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 监控数据总量 | {total} 条 |")
    lines.append(f"| 正面情绪占比 | {pos_pct}% |")
    lines.append(f"| 负面情绪占比 | {neg_pct}% |")
    lines.append(f"| 中性内容占比 | {round(100 - pos_pct - neg_pct, 1)}% |")
    lines.append("")

    # ---- 各平台数据 ----
    lines.append("## 📱 各平台数据")
    lines.append("")

    platform_display = {
        "taptap_reviews": "TapTap 评论",
        "taptap_forum": "TapTap 论坛",
        "bilibili": "B站视频",
        "nga": "NGA 论坛",
        "xiaohongshu": "小红书笔记",
    }

    lines.append("| 平台 | 数据量 | 正面% | 负面% |")
    lines.append("|------|--------|-------|-------|")
    for src, stats in platform_stats.items():
        name = platform_display.get(src, src)
        pos = stats.get("sentiment_ratio", {}).get("positive_pct", 0)
        neg = stats.get("sentiment_ratio", {}).get("negative_pct", 0)
        lines.append(f"| {name} | {stats['total']} 条 | {pos}% | {neg}% |")
    lines.append("")

    # ---- 热点话题 ----
    lines.append("## 🔥 热点话题 Top 10")
    lines.append("")
    for i, topic in enumerate(hot_topics[:10], 1):
        sentiment_icons = {"positive": "😊", "negative": "😤", "neutral": "😐"}
        # 统计话题内情感分布
        sentiments = [item.get("sentiment", "neutral") for item in topic.get("items", [])]
        main_sentiment = max(set(sentiments), key=sentiments.count) if sentiments else "neutral"
        icon = sentiment_icons.get(main_sentiment, "💬")
        lines.append(f"### {i}. {icon} {topic['topic']}（{topic['count']} 条讨论）")
        # 列出典型帖子
        for item in topic.get("items", [])[:3]:
            title = item.get("title", "")
            source = item.get("source", "")
            url = item.get("url", "")
            if title:
                if url:
                    lines.append(f"- [{title[:40]}]({url}) `{source}`")
                else:
                    lines.append(f"- {title[:40]} `{source}`")
        lines.append("")

    # ---- 吐槽榜 ----
    lines.append("## 😤 吐槽榜 Top 10")
    lines.append("")
    if complaints:
        seen_complaints = set()
        count = 0
        for c in complaints:
            text = c.get("text", "").strip()
            if text in seen_complaints or len(text) < 4:
                continue
            seen_complaints.add(text)
            count += 1
            if count > 10:
                break
            source = c.get("source", "")
            url = c.get("url", "")
            original = c.get("original", "")[:60]
            lines.append(f"{count}. **{text}**")
            if original:
                lines.append(f"   > _{original}..._")
            lines.append(f"   来源：`{source}`")
            lines.append("")
    else:
        lines.append("_暂无明显吐槽内容_")
        lines.append("")

    # ---- 玩家梗/流行词 ----
    lines.append("## 😂 玩家梗 & 流行词")
    lines.append("")
    if memes:
        meme_strs = [f"`{m[0]}`（{m[1]}次）" for m in memes[:15]]
        lines.append("　".join(meme_strs))
    else:
        lines.append("_暂未发现明显梗词_")
    lines.append("")

    # ---- 高频关键词 ----
    lines.append("## 🏷️ 高频关键词")
    lines.append("")
    if top_keywords:
        kw_strs = [f"`{kw}`×{cnt}" for kw, cnt in top_keywords[:20]]
        lines.append("　".join(kw_strs))
    lines.append("")

    # ---- 好评摘录 ----
    lines.append("## 💚 好评摘录（Top 5）")
    lines.append("")
    for i, item in enumerate(top_positive[:5], 1):
        title = item.get("title", "")
        content = item.get("content", "")[:100]
        source = item.get("source", "")
        url = item.get("url", "")
        text = title or content
        if not text:
            continue
        lines.append(f"{i}. **{text[:60]}**")
        if content and title:
            lines.append(f"   > {content}...")
        lines.append(f"   来源：`{source}`" + (f" · [查看原文]({url})" if url else ""))
        lines.append("")

    # ---- 差评摘录 ----
    lines.append("## ❤️‍🔥 差评摘录（Top 5）")
    lines.append("")
    for i, item in enumerate(top_negative[:5], 1):
        title = item.get("title", "")
        content = item.get("content", "")[:100]
        source = item.get("source", "")
        url = item.get("url", "")
        text = title or content
        if not text:
            continue
        lines.append(f"{i}. **{text[:60]}**")
        if content and title:
            lines.append(f"   > {content}...")
        lines.append(f"   来源：`{source}`" + (f" · [查看原文]({url})" if url else ""))
        lines.append("")

    # ---- 运营建议 ----
    lines.append("## 💡 运营关注点")
    lines.append("")
    suggestions = []
    if neg_pct > 30:
        suggestions.append("⚠️ 负面情绪占比较高，建议排查主要吐槽点并快速响应")
    if any("服务器" in c.get("text", "") for c in complaints[:5]):
        suggestions.append("🔧 服务器/登录问题多次出现，建议优先处理技术稳定性")
    if any("氪金" in c.get("text", "") or "充钱" in c.get("text", "") for c in complaints[:10]):
        suggestions.append("💰 付费相关吐槽较多，建议评估当前付费设计")
    if pos_pct > 60:
        suggestions.append("✨ 正面情绪良好，可考虑在 TapTap/B站 加大官方互动")

    # 基于热点话题的建议
    for topic in hot_topics[:3]:
        if "服务器" in topic["topic"] and topic["count"] > 3:
            suggestions.append(f"🚨 「{topic['topic']}」讨论量 {topic['count']} 条，需紧急关注")

    if not suggestions:
        suggestions.append("✅ 当前舆情整体平稳，保持日常监控即可")

    for s in suggestions:
        lines.append(f"- {s}")
    lines.append("")

    lines.append("---")
    lines.append(f"_本报告由自动化舆情监控系统生成 · {now_str}_")

    return "\n".join(lines)


def generate_summary(analysis):
    """生成企微推送用的简短摘要"""
    game_name = analysis.get("game", "")
    overview = analysis.get("sentiment_overview", {})
    hot_topics = analysis.get("hot_topics", [])
    complaints = analysis.get("complaints", [])
    memes = analysis.get("memes", [])
    platform_stats = analysis.get("platform_stats", {})

    total = overview.get("total", 0)
    pos_pct = overview.get("positive_pct", 0)
    neg_pct = overview.get("negative_pct", 0)
    overall = overview.get("overall", "")

    now_str = datetime.now().strftime("%Y-%m-%d")
    lines = []

    lines.append(f"🎮 **{game_name} 舆情日报 · {now_str}**")
    lines.append("")
    lines.append(f"📊 **今日概览**：{overall}")
    lines.append(f"监控数据 **{total}** 条 | 正面 **{pos_pct}%** | 负面 **{neg_pct}%**")
    lines.append("")

    # 各平台数据量
    platform_display = {
        "taptap_reviews": "TapTap评论",
        "taptap_forum": "TapTap论坛",
        "bilibili": "B站",
        "nga": "NGA",
        "xiaohongshu": "小红书",
    }
    platform_parts = []
    for src, stats in platform_stats.items():
        if stats.get("total", 0) > 0:
            name = platform_display.get(src, src)
            platform_parts.append(f"{name} {stats['total']}条")
    if platform_parts:
        lines.append("📱 " + " · ".join(platform_parts))
        lines.append("")

    # 热点话题 Top 3
    if hot_topics:
        lines.append("🔥 **热点话题**")
        for t in hot_topics[:3]:
            lines.append(f"  · {t['topic']}（{t['count']}条）")
        lines.append("")

    # 主要吐槽
    if complaints:
        seen = set()
        unique_complaints = []
        for c in complaints[:10]:
            text = c.get("text", "").strip()
            if text not in seen and len(text) >= 4:
                seen.add(text)
                unique_complaints.append(text)
        if unique_complaints[:3]:
            lines.append("😤 **主要吐槽**")
            for c in unique_complaints[:3]:
                lines.append(f"  · {c[:30]}")
            lines.append("")

    # 玩家梗
    if memes:
        meme_words = [m[0] for m in memes[:5]]
        lines.append(f"😂 **玩家流行词**：{'　'.join(meme_words)}")
        lines.append("")

    lines.append("📎 完整报告见附件下载链接")

    return "\n".join(lines)


def save_reports(analysis, raw_data=None):
    """保存报告文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 生成 Markdown 报告
    md_content = generate_report(analysis, raw_data)
    md_path = os.path.join(OUTPUT_DIR, f"sentiment_{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"📄 报告已保存：{md_path}")

    # 生成摘要
    summary = generate_summary(analysis)
    summary_path = os.path.join(OUTPUT_DIR, "latest_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"📝 摘要已保存：{summary_path}")

    return md_path, summary_path


if __name__ == "__main__":
    import json
    with open("/Users/dada/game-sentiment/analysis_latest.json", encoding="utf-8") as f:
        analysis = json.load(f)
    save_reports(analysis)

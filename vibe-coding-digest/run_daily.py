#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vibe-coding-digest 每日自动运行入口
由 Knot cron 定时任务调用

流程：
  1. 通过 mcporter-internal 调用 KM MCP 抓取最新 KM 文章
  2. 解析写入 km_results.json
  3. 运行 digest.py 生成报告
  4. 输出摘要供 Knot notify 推送
"""

import json
import os
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KM_JSON = os.path.join(SCRIPT_DIR, "km_results.json")
TODAY = datetime.now().strftime("%Y-%m-%d")
REPORT_PATH = os.path.join(SCRIPT_DIR, f"digest_{TODAY}.md")


# ══════════════════════════════════════════════════════
#  Step 1: 通过 mcporter-internal 抓取 KM 文章
# ══════════════════════════════════════════════════════

def fetch_km_via_mcporter():
    """调用 mcporter-internal 抓取 KM 文章，返回原始文本"""
    yesterday = datetime.now().strftime("%Y-%m-%d") 
    # 抓取过去 24h
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

    print("📡 Step 1: 通过 KM MCP 抓取最新文章...")

    all_lines = []
    seen_urls = set()

    # 抓取 headline 文章（今日头条/推荐）
    try:
        result = subprocess.run(
            ["mcporter-internal", "call", "km.list-articles(headline:true)", "--output", "json"],
            capture_output=True, text=True, timeout=30
        )
        text = _extract_text_from_mcp_json(result.stdout)
        for line in text.split("\n"):
            if line.startswith("- 标题:") and "链接:" in line:
                url = line.split("链接:")[-1].strip()
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_lines.append(line)
        print(f"  ✅ 头条文章：{len(all_lines)} 条")
    except Exception as e:
        print(f"  ⚠️  头条抓取失败: {e}")

    # 抓取最新文章（按时间）
    try:
        result = subprocess.run(
            ["mcporter-internal", "call", f"km.list-articles(created_after:'{cutoff}')", "--output", "json"],
            capture_output=True, text=True, timeout=30
        )
        text = _extract_text_from_mcp_json(result.stdout)
        new_count = 0
        for line in text.split("\n"):
            if line.startswith("- 标题:") and "链接:" in line:
                url = line.split("链接:")[-1].strip()
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_lines.append(line)
                    new_count += 1
        print(f"  ✅ 最新文章：新增 {new_count} 条")
    except Exception as e:
        print(f"  ⚠️  最新文章抓取失败: {e}")

    return "\n".join(all_lines)


def _extract_text_from_mcp_json(raw_output):
    """从 mcporter-internal JSON 输出中提取 text 字段"""
    try:
        # mcporter-internal 输出是 JS 风格的 JSON，尝试直接提取 text 内容
        import re
        match = re.search(r"text: '(.*?)'(?:\s*\+\s*'(.*?)')*", raw_output, re.DOTALL)
        if match:
            # 有多行拼接的情况，用正则提取所有 text 片段
            texts = re.findall(r"text: '(.*?)'(?=\s*[,\+\}])", raw_output, re.DOTALL)
            return "\n".join(texts).replace("\\n", "\n").replace("\\'", "'")
        # 备用：直接找 - 标题: 开头的行
        lines = [l for l in raw_output.split("\n") if "标题:" in l]
        return "\n".join(lines)
    except Exception:
        return raw_output


def parse_and_save_km(raw_text):
    """解析 KM 原始文本，写入 km_results.json"""

    GAME_KW = ["游戏", "unity", "unreal", "ue5", "godot", "game", "indie", "npc"]
    AI_KW = ["ai", "vibe", "cursor", "claude", "copilot", "agent", "llm", "大模型",
             "编程", "coding", "skill", "mcp", "agentic", "openclaw", "codebuddy", "harness"]

    def classify(title, tags="", summary=""):
        text = (title + " " + tags + " " + summary).lower()
        for kw in GAME_KW:
            if kw in text:
                return "M1"
        for kw in AI_KW:
            if kw in text:
                return "M2"
        return "M2"

    def extract(line, field_start, end_markers):
        if field_start not in line:
            return ""
        s = line.index(field_start) + len(field_start)
        for em in end_markers:
            if em in line[s:]:
                return line[s: line.index(em, s)].strip()
        return line[s:].strip()

    results = []
    seen = set()

    for line in raw_text.strip().split("\n"):
        line = line.strip()
        if "标题:" not in line or "链接:" not in line:
            continue
        if line.startswith("- "):
            line = line[2:]

        url = extract(line, "链接: ", ["\n"])
        if not url or url in seen:
            continue
        seen.add(url)

        title = extract(line, "标题: ", [", 作者:", ", 创建时间:"])
        if not title:
            continue

        tags = extract(line, "标签: ", [", 阅读:", ", 点赞:", ", 链接:"])
        summary = extract(line, "导语: ", [", 标签:", ", 阅读:", ", 链接:"])

        try:
            rc = extract(line, "阅读: ", [", 点赞:"])
            read_count = int(rc) if rc else 0
        except:
            read_count = 0

        article = {
            "title": title,
            "author": extract(line, "作者: ", [", 共同作者:", ", 创建时间:"]),
            "summary": summary,
            "tags": tags,
            "url": url,
            "read_count": read_count,
            "km_recommended": "KM推荐: 是" in line,
            "km_headline": "KM头条: 是" in line,
            "module": classify(title, tags, summary),
        }
        results.append(article)

    m1 = [r for r in results if r["module"] == "M1"]
    m2 = [r for r in results if r["module"] == "M2"]

    output = {
        "generated_at": datetime.now().isoformat(),
        "total": len(results),
        "m1_count": len(m1),
        "m2_count": len(m2),
        "articles": results,
    }

    with open(KM_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  💾 km_results.json 已保存：共 {len(results)} 条（M1:{len(m1)} M2:{len(m2)}）")
    return len(results)


# ══════════════════════════════════════════════════════
#  Step 2: 运行 digest.py
# ══════════════════════════════════════════════════════

def run_digest():
    print("\n🚀 Step 2: 运行 digest.py 生成报告...")
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "digest.py")],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
    if result.returncode != 0:
        print(f"  ⚠️  digest.py 退出码: {result.returncode}")
        if result.stderr:
            print(result.stderr[-1000:])
    return result.returncode == 0


# ══════════════════════════════════════════════════════
#  Step 3: 读取报告返回摘要
# ══════════════════════════════════════════════════════

def get_summary():
    summary_path = os.path.join(SCRIPT_DIR, "latest_summary.txt")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            return f.read()
    return "日报已生成，请查看报告文件。"


def get_report():
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# ══════════════════════════════════════════════════════
#  主流程
# ══════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"🎮 Vibe Coding Digest 每日自动运行")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: 抓取 KM
    km_raw = fetch_km_via_mcporter()
    if km_raw.strip():
        parse_and_save_km(km_raw)
    else:
        print("  ⚠️  KM 抓取结果为空，使用已有数据（如有）")

    # Step 2: 运行 digest
    success = run_digest()

    # Step 3: 输出摘要
    summary = get_summary()
    report = get_report()

    print("\n" + "=" * 60)
    print("📋 今日摘要（用于企业微信推送）：")
    print("=" * 60)
    print(summary)

    if report:
        print(f"\n📄 完整报告已保存至：{REPORT_PATH}")

    return summary, report


if __name__ == "__main__":
    main()

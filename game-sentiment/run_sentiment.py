#!/usr/bin/env python3
"""
游戏舆情监控 - 主运行脚本
完整流程：抓取 → 分析 → 生成报告 → 保存文件
"""

import json
import logging
import os
import sys
from datetime import datetime
from config import OUTPUT_DIR

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(OUTPUT_DIR, "sentiment.log"), encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def run():
    """完整运行一次舆情监控流程"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*60}")
    print(f"🎮 游戏舆情监控启动 · {date_str}")
    print(f"{'='*60}\n")

    # Step 1: 抓取数据
    print("【Step 1】数据抓取...")
    from fetcher import fetch_all
    raw_data = fetch_all()

    # 保存原始数据
    raw_path = os.path.join(OUTPUT_DIR, f"raw_{date_str}.json")
    raw_latest = os.path.join(OUTPUT_DIR, "raw_latest.json")
    for src in raw_data["sources"].values():
        for item in src:
            item.pop("raw", None)  # 去掉大字段
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    with open(raw_latest, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print(f"   💾 原始数据：{raw_path}")

    # 检查是否有数据
    total_items = sum(len(v) for v in raw_data["sources"].values())
    if total_items == 0:
        logger.warning("没有抓取到任何数据，请检查各平台连接状态")
        print("\n⚠️ 没有抓取到数据，流程终止")
        return None

    # Step 2: AI 分析
    print(f"\n【Step 2】分析 {total_items} 条数据...")
    from analyzer import analyze
    analysis = analyze(raw_data)

    # 保存分析结果
    analysis_path = os.path.join(OUTPUT_DIR, f"analysis_{date_str}.json")
    analysis_latest = os.path.join(OUTPUT_DIR, "analysis_latest.json")
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    with open(analysis_latest, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"   💾 分析结果：{analysis_path}")

    # Step 3: 生成报告
    print(f"\n【Step 3】生成报告...")
    from reporter import save_reports
    md_path, summary_path = save_reports(analysis, raw_data)

    print(f"\n{'='*60}")
    print(f"✅ 舆情监控完成！")
    print(f"   📄 完整报告：{md_path}")
    print(f"   📝 推送摘要：{summary_path}")
    print(f"{'='*60}\n")

    return {
        "md_path": md_path,
        "summary_path": summary_path,
        "analysis": analysis,
    }


if __name__ == "__main__":
    result = run()
    if result:
        # 打印摘要
        with open(result["summary_path"], encoding="utf-8") as f:
            print("\n📋 推送摘要预览：")
            print("-" * 40)
            print(f.read())

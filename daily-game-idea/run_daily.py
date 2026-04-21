#!/usr/bin/env python3
"""
run_daily.py: 每日游戏创意定时任务入口
由 Knot cron 任务每日 11:45 调用
"""

import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

TODAY = datetime.date.today().isoformat()
LATEST_TXT = os.path.join(SCRIPT_DIR, "latest_ideas.txt")
IDEAS_DIR = os.path.join(SCRIPT_DIR, "ideas")


def read_summary() -> str:
    """读取最新摘要内容"""
    if os.path.exists(LATEST_TXT):
        with open(LATEST_TXT, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def build_notify_message(summary: str, idea_count: int) -> str:
    """构建推送通知的正文"""
    date_str = datetime.date.today().strftime("%Y年%m月%d日")
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_cn[datetime.date.today().weekday()]
    
    msg = f"## 🎮 每日游戏创意 · {date_str} {weekday}\n\n"
    msg += f"今日为你准备了 **{idea_count} 个全新游戏创意**，涵盖玩法融合、文化趋势、爆款新方向等多个维度 👇\n\n"
    msg += "---\n\n"
    
    # 从摘要中提取 idea 列表部分（跳过标题行）
    lines = summary.split("\n")
    idea_lines = [l for l in lines if l.strip() and not l.startswith("===") and not l.startswith("详细")]
    msg += "\n".join(idea_lines)
    msg += "\n\n---\n"
    msg += f"📁 完整创意详情已保存至 `ideas/ideas_{TODAY}.md`，查看核心玩法与差异化分析"
    
    return msg


def main():
    print(f"\n[run_daily] 开始执行每日游戏创意推送任务 - {TODAY}")
    
    # Step 1: 调用生成脚本
    print("[run_daily] Step 1: 生成今日游戏创意...")
    import generate_ideas
    try:
        result = generate_ideas.main()
    except SystemExit:
        print("[run_daily] 生成脚本异常退出")
        result = None
    
    # Step 2: 读取摘要
    print("[run_daily] Step 2: 读取摘要内容...")
    summary = read_summary()
    
    if not summary:
        print("[run_daily] 摘要内容为空，使用降级消息")
        summary = f"今日游戏创意生成失败，请手动运行 generate_ideas.py 检查原因"
        idea_count = 0
    else:
        idea_count = result.get("idea_count", 10) if result else 10
    
    # Step 3: 构建并输出推送内容
    print("[run_daily] Step 3: 构建推送内容...")
    notify_msg = build_notify_message(summary, idea_count)
    
    print("\n" + "="*60)
    print("📤 推送内容预览：")
    print("="*60)
    print(notify_msg[:800])
    print("="*60 + "\n")
    
    # 输出供 Knot cron 任务使用的结构化信息
    print("[run_daily] ✅ 任务完成，请使用 notify 工具推送以上内容给用户")
    print(f"[run_daily] NOTIFY_TITLE=🎮 今日游戏创意已送达（{TODAY}）")
    print(f"[run_daily] NOTIFY_BODY_START")
    print(notify_msg)
    print(f"[run_daily] NOTIFY_BODY_END")


if __name__ == "__main__":
    main()

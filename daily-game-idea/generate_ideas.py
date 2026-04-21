#!/usr/bin/env python3
"""
daily-game-idea: 每日游戏创意生成脚本
每日自动生成 10 个全新游戏创意，涵盖玩法融合、文化趋势、爆款新方向等
"""

import os
import json
import subprocess
import datetime
import re
import sys

# ── 路径配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IDEAS_DIR = os.path.join(SCRIPT_DIR, "ideas")
os.makedirs(IDEAS_DIR, exist_ok=True)

TODAY = datetime.date.today().isoformat()          # e.g. 2026-04-13
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
TODAY_WEEKDAY = WEEKDAY_CN[datetime.date.today().weekday()]

OUTPUT_MD = os.path.join(IDEAS_DIR, f"ideas_{TODAY}.md")
LATEST_TXT = os.path.join(SCRIPT_DIR, "latest_ideas.txt")

# ── Prompt ────────────────────────────────────────────────────────────────────
SYSTEM_CONTEXT = """你是一位经验丰富的游戏创意总监，深入了解全球手游市场趋势、玩家心理、爆款机制设计。
你熟悉超休闲、中度游戏、独立游戏各品类的核心玩法，也关注互联网文化、社交热点、影视动漫等领域对游戏创意的启发。
你的创意既有市场可行性，也有足够的新鲜感和差异化。"""

IDEA_PROMPT = f"""今天是 {TODAY}（{TODAY_WEEKDAY}），请为我生成 **10 个全新游戏创意**。

## 创意来源要求（每次生成时随机混合以下多个维度，不要每次都用同一种）：

1. **玩法融合**：把两款或多款经典游戏的核心机制组合成新玩法（如 Flappy Bird × 三消、贪吃蛇 × 塔防）
2. **文化趋势融合**：把当前互联网热点/社会现象/流行文化（如 AI、打工人文化、MBTI、特种兵旅游）与一个合适的游戏机制结合
3. **爆款新方向**：选取一个已有爆款游戏（如羊了个羊、合成大西瓜、弓箭传说），探索它在**未被验证的其他方向**上的变体
4. **反直觉设计**：颠覆玩家对某类游戏的固有认知（如"失败才能胜利的游戏"、"越笨越强的解谜"）
5. **感官 / 情绪驱动**：以特定情绪体验为核心设计目标（解压、治愈、紧张、仪式感），反推机制设计
6. **真实世界映射**：将日常生活场景游戏化（做饭、通勤、职场会议、减肥打卡）

## 输出格式（严格遵守，每个 idea 独立一段）：

### 🎮 Idea N：[创意名称]
**来源维度**：[从上面6个维度中选择]
**一句话描述**：[用最吸引人的方式说清楚这个游戏是什么]
**核心玩法**：[具体描述主要操作方式和循环，2-4句话]
**差异化亮点**：[这个创意和已有游戏的本质区别，或者为什么玩家会上瘾]
**目标平台**：[手游/小游戏/PC独立游戏等]
**参考原型**：[1-2个类似的游戏作为参照系，帮助理解定位]

---

请确保 10 个 idea 来自**不同的来源维度**，风格多样，不要重复类似的概念。
今天的 idea 要有创意，要有惊喜感！"""

# ── 调用 AI 生成 ──────────────────────────────────────────────────────────────

def generate_ideas_via_knot_cli() -> str:
    """通过 knot-cli 调用 AI 生成游戏创意"""
    full_prompt = f"{SYSTEM_CONTEXT}\n\n{IDEA_PROMPT}"
    
    print(f"[{TODAY}] 正在调用 AI 生成游戏创意...")
    
    # 查找 knot-cli 路径
    knot_cmd = "/app/background_agent_cli/bin/knot-cli"
    if not os.path.exists(knot_cmd):
        import shutil
        knot_cmd = shutil.which("knot-cli") or shutil.which("knot") or "knot-cli"
    
    try:
        result = subprocess.run(
            [knot_cmd, "chat", "-p", full_prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=SCRIPT_DIR
        )
        if result.returncode == 0 and result.stdout.strip():
            print(f"[{TODAY}] AI 生成成功，共 {len(result.stdout)} 字符")
            return result.stdout.strip()
        else:
            err = result.stderr or result.stdout or "未知错误"
            print(f"[{TODAY}] knot CLI 调用失败: {err[:300]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"[{TODAY}] AI 调用超时（>120s）")
        return None
    except FileNotFoundError:
        print(f"[{TODAY}] 未找到 knot-cli 命令，请确认已安装并在 PATH 中")
        return None
    except Exception as e:
        print(f"[{TODAY}] 调用异常: {e}")
        return None


def build_markdown(ideas_content: str) -> str:
    """构建完整的 Markdown 文件"""
    header = f"""# 🎮 每日游戏创意 · {TODAY}（{TODAY_WEEKDAY}）

> 自动生成 | 来源维度：玩法融合 · 文化趋势 · 爆款新方向 · 反直觉设计 · 情绪驱动 · 真实世界映射

---

"""
    footer = f"""

---

*生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return header + ideas_content + footer


def extract_summary(ideas_content: str) -> str:
    """提取每个 idea 的名称和一句话描述，用于推送摘要"""
    lines = []
    ideas = re.findall(
        r'###\s*🎮\s*Idea\s*\d+[：:]\s*(.+?)\n.*?\*\*一句话描述\*\*[：:]\s*(.+?)(?:\n|$)',
        ideas_content,
        re.DOTALL
    )
    for i, (name, desc) in enumerate(ideas, 1):
        name = name.strip()
        desc = desc.strip()
        lines.append(f"{i}. **{name}**：{desc}")
    
    if not lines:
        # fallback: 只提取标题行
        titles = re.findall(r'###\s*🎮\s*Idea\s*\d+[：:]\s*(.+)', ideas_content)
        lines = [f"{i}. **{t.strip()}**" for i, t in enumerate(titles, 1)]
    
    return "\n".join(lines)


def save_results(ideas_content: str) -> dict:
    """保存 Markdown 文件和摘要文件"""
    # 保存完整 Markdown
    md_content = build_markdown(ideas_content)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[{TODAY}] 完整创意已保存至: {OUTPUT_MD}")
    
    # 保存摘要（用于推送通知）
    summary = extract_summary(ideas_content)
    with open(LATEST_TXT, "w", encoding="utf-8") as f:
        f.write(f"=== 每日游戏创意 {TODAY} ===\n\n")
        f.write(summary)
        f.write(f"\n\n详细内容见: {OUTPUT_MD}")
    print(f"[{TODAY}] 摘要已保存至: {LATEST_TXT}")
    
    return {
        "date": TODAY,
        "weekday": TODAY_WEEKDAY,
        "output_md": OUTPUT_MD,
        "summary": summary,
        "idea_count": len(re.findall(r'###\s*🎮\s*Idea', ideas_content))
    }


def main():
    print(f"\n{'='*50}")
    print(f"  每日游戏创意生成器 - {TODAY} {TODAY_WEEKDAY}")
    print(f"{'='*50}\n")
    
    # 生成创意
    ideas_content = generate_ideas_via_knot_cli()
    
    if not ideas_content:
        print("[ERROR] AI 生成失败，退出")
        sys.exit(1)
    
    # 保存结果
    result = save_results(ideas_content)
    
    print(f"\n✅ 生成完成！共 {result['idea_count']} 个创意")
    print(f"📄 详细内容: {result['output_md']}")
    print(f"\n--- 摘要预览 ---\n{result['summary'][:500]}")
    
    return result


if __name__ == "__main__":
    main()

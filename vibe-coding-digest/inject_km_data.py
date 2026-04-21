#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 KM MCP 抓取的原始文本整合写入 km_results.json
供 digest.py 读取
"""
import json, os, re
from datetime import datetime

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "km_results.json")

# ── KM 原始数据（由 mcporter-internal 抓取）────────────────────────────
RAW_KM_TEXT = """
- 标题: AI的死穴与应用策略：指标看板实例分享, 作者: frankmiao, 创建时间: 2026-04-09 11:48:22, 更新时间: 2026-04-09 11:49:15, 标签: AI | Python | 模型, 阅读: 2, 点赞: 0, 收藏: 0, 评论: 0, K吧: #52486 S2专业智慧圈 https://km.woa.com/group/52486?jumpfrom=kmmcp, 链接: https://km.woa.com/articles/show/657098?jumpfrom=kmmcp
- 标题: Skill Assistant — 一句话搜遍全网 Agent Skill，你的 skill 一站式管理助手, 作者: lintonliu, 创建时间: 2026-04-09 11:48:11, 更新时间: 2026-04-09 12:40:24, 导语: Skill Assistant 是一个 meta-skill：用来管理 Skill 的 Skill。它帮你从 skills.sh、Knot、GitHub 等 9 个主流渠道搜索和发现 Skill；帮你基于项目和技术栈智能推荐最合适的 Skill；帮你安全扫描后一键安装，统一管理版本和更新；帮你给已有 Skill 做质量体检和效能诊断，从全网优秀 Skill 中汲取精华来改善你的 Skill。, 标签: agent | AI | skill | knot, 阅读: 11, 点赞: 0, 收藏: 0, 评论: 0, K吧: #45812 PCG代码委员会 https://km.woa.com/group/45812?jumpfrom=kmmcp, 链接: https://km.woa.com/articles/show/657097?jumpfrom=kmmcp
- 标题: AI问题分析实践：刷掌识别App覆盖安装后界面样式错乱问题, 作者: wenjiewu, 创建时间: 2026-04-09 11:37:11, 更新时间: 2026-04-09 11:37:11, 导语: 一次疑难杂症的AI分析过程。, 标签: AI | 问题分析, 阅读: 11, 点赞: 0, 收藏: 0, 评论: 0, K吧: #52304 商户产品部 https://km.woa.com/group/52304?jumpfrom=kmmcp, 链接: https://km.woa.com/articles/show/657095?jumpfrom=kmmcp
- 标题: 正是 AI 编码时：AIBrick —— 4个引擎让 AI 真正"看懂" Android 项目, 作者: icezheng, 创建时间: 2026-04-09 11:35:22, 更新时间: 2026-04-09 11:53:36, 导语: AI 编码很强，但存在不确定性，偶尔抽风漂移让人忍俊不禁，而AIBrick做的就是铺好地板砖让AI踏实接地气。, 标签: 代码 | AI, 阅读: 14, 点赞: 0, 收藏: 0, 评论: 0, K吧: #38985 腾讯VATeam-社交增值产品部研发团队 https://km.woa.com/group/38985?jumpfrom=kmmcp, 链接: https://km.woa.com/articles/show/657094?jumpfrom=kmmcp
- 标题: AI 驱动的日系恋爱条漫制作流水线, 作者: lyricszhang, 创建时间: 2026-04-09 11:16:01, 更新时间: 2026-04-09 11:16:01, 标签: AI, 阅读: 4, 点赞: 0, 收藏: 0, 评论: 0, 链接: https://km.woa.com/articles/show/657090?jumpfrom=kmmcp
- 标题: 从需求到发布的AI全自动化交付的探索与实践, 作者: jacksondeng, 共同作者: yuxuanlai/gcchaoguo, 创建时间: 2026-04-09 10:43:31, 更新时间: 2026-04-09 10:43:31, 导语: 在需求到交付的全链路中，除 Coding 之外，需求评审、方案设计、代码评审、部署发布等环节同样需要大量人工介入，频繁的上下文切换与等待严重拖累了研效。为此，我们在持续深耕 Coding 阶段 AI 能力的同时，也逐步向需求、测试、部署等上下游环节延伸，联动效能与测试团队协同探索。经过一系列实践沉淀，我们提炼出一套适配审核业务现阶段的 AI 全自动化交付框架——该框架已支持通过 OpenClaw 或 CodeBuddy 对话驱动，实现从需求到部署的全链路自动化执行。, 标签: AI | 全自动化 | 代码 | 全链路, 阅读: 811, 点赞: 19, 收藏: 48, 评论: 9, KM推荐: 是, KM头条: 是, K吧: #52878 腾讯广告研效 https://km.woa.com/group/52878?jumpfrom=kmmcp, 链接: https://km.woa.com/articles/show/657086?jumpfrom=kmmcp
- 标题: 超越 OpenClaw 13.4%：LightClawACE 的"六层记忆"做对了什么？, 作者: eileennchen, 共同作者: bingjiachen/xunpeihu, 创建时间: 2026-04-09 10:39:07, 更新时间: 2026-04-09 10:39:07, 导语: 当 Agent 开始从"回答一次问题"走向"持续服务一个用户"，Memory 就不再是锦上添花的增强项，而是决定产品体验与能力上限的核心基础设施。在公开 benchmark LongMemEval 上，LightClawACE 以 255/500（51.0%）显著高于 OpenClaw 的 188/500（37.6%）。, 标签: memory | 记忆 | Session | OpenClaw | lightclaw, 阅读: 131, 点赞: 14, 收藏: 10, 评论: 8, KM推荐: 是, KM头条: 是, 链接: https://km.woa.com/articles/show/657081?jumpfrom=kmmcp
- 标题: 养龙虾最佳实践：构建持久运营型 Multi-Agent 团队, 作者: zachyzhang, 创建时间: 2026-04-08 22:59:16, 更新时间: 2026-04-08 22:59:16, 标签: multi-agent | 龙虾 | OpenClaw | AI架构, 阅读: 80, 点赞: 4, 收藏: 4, 评论: 3, KM推荐: 是, KM头条: 是, 热度: 8, 链接: https://km.woa.com/articles/show/657065?jumpfrom=kmmcp
- 标题: 小程序 UI 还原度自动检查实践：从人工救火到 UI Harness, 作者: jazzjia, 创建时间: 2026-04-08 20:49:42, 更新时间: 2026-04-08 20:49:42, 标签: 微信小程序 | Harness | harnessengineering | AI应用实践, 阅读: 246, 点赞: 9, 收藏: 7, 评论: 0, KM推荐: 是, KM头条: 是, 热度: 22, 链接: https://km.woa.com/articles/show/657058?jumpfrom=kmmcp
- 标题: 让 AI 守住代码质量的底线——借助多 Agent 编排提效code review, 作者: hijackzhang, 创建时间: 2026-04-08 20:29:00, 更新时间: 2026-04-08 20:29:00, 导语: 本文旨在分享一种多 Agent 编排协作模式——一种多轨交叉Subagent 评审代码工具。, 标签: AI, 阅读: 70, 点赞: 0, 收藏: 3, 评论: 2, KM推荐: 是, KM头条: 是, 热度: 8, 链接: https://km.woa.com/articles/show/657055?jumpfrom=kmmcp
- 标题: 将团队智慧编译为AI指令：OneID质量团队的AI技能化实践, 作者: gillguo, 共同作者: chaoychen/danicadhe/luffytian/robinjin, 创建时间: 2026-04-08 19:07:35, 更新时间: 2026-04-09 11:15:43, 导语: 本文提出经验→方法论→约束三级转化体系，将OneID测试团队积累的业务规则和架构经验编译为AI可执行的技能（Skill）和规则（Rule），构建生成→验证→反馈闭环。, 标签: 自动化 | AI | skill, 阅读: 59, 点赞: 1, 收藏: 1, 评论: 0, KM推荐: 是, KM头条: 是, 热度: 39, 链接: https://km.woa.com/articles/show/657050?jumpfrom=kmmcp
- 标题: ⁠AI Agent 框架怎么选？DeerFlow / ClaudeCode / OpenClaw / nanobot 源码级深度对比, 作者: luiszhu, 创建时间: 2026-04-08 18:11:13, 更新时间: 2026-04-08 21:32:15, 导语: 2026年上半年，AI Agent 赛道迎来了寒武纪大爆发，字节的 DeerFlow 2.0 冲上 57K Star、Anthropic 的 ClaudeCode 因源码泄露意外开源引发全球关注、OpenClaw 4个月狂揽 27 万 Star 登顶 GitHub 第一、港大 nanobot 用 4000 行代码打造99%瘦身版OpenClaw。, 标签: deerflow | AI Agent | claudecode | OpenClaw | nanobot, 阅读: 177, 点赞: 5, 收藏: 12, 评论: 1, KM推荐: 是, KM头条: 是, 热度: 29, 链接: https://km.woa.com/articles/show/657045?jumpfrom=kmmcp
"""

# 游戏相关关键词（M1 判断）
GAME_KW = ["游戏", "unity", "unreal", "ue5", "godot", "game", "indie", "npc"]
# AI编程/通用关键词（M2 判断）
AI_KW = ["ai", "vibe", "cursor", "claude", "copilot", "agent", "llm", "大模型",
         "编程", "coding", "skill", "mcp", "agentic", "openClaw", "codebuddy", "harness"]


def classify(title, tags="", summary=""):
    text = (title + " " + tags + " " + summary).lower()
    for kw in GAME_KW:
        if kw in text:
            return "M1"
    for kw in AI_KW:
        if kw in text:
            return "M2"
    return None


def parse_line(line):
    item = {}
    def extract(field_start, end_markers):
        if field_start not in line:
            return ""
        s = line.index(field_start) + len(field_start)
        for em in end_markers:
            if em in line[s:]:
                return line[s: line.index(em, s)].strip()
        return line[s:].strip()

    item["title"] = extract("标题: ", [", 作者:", ", 创建时间:"])
    item["author"] = extract("作者: ", [", 共同作者:", ", 创建时间:"])
    item["summary"] = extract("导语: ", [", 标签:", ", 阅读:", ", 链接:"])
    item["tags"] = extract("标签: ", [", 阅读:", ", 点赞:", ", 链接:"])
    item["url"] = extract("链接: ", ["\n"])
    item["km_recommended"] = "KM推荐: 是" in line
    item["km_headline"] = "KM头条: 是" in line

    try:
        rc = extract("阅读: ", [", 点赞:"])
        item["read_count"] = int(rc) if rc else 0
    except:
        item["read_count"] = 0

    try:
        hv = extract("热度: ", [", 链接:", "\n"])
        item["hot_value"] = int(hv) if hv else 0
    except:
        item["hot_value"] = 0

    if not item.get("title") or not item.get("url"):
        return None
    return item


def main():
    results = []
    seen = set()

    for line in RAW_KM_TEXT.strip().split("\n"):
        line = line.strip()
        if not line.startswith("- 标题:"):
            continue
        line = line[2:]  # 去掉 "- "
        article = parse_line(line)
        if not article:
            continue
        url = article["url"]
        if url in seen:
            continue
        seen.add(url)

        module = classify(article.get("title", ""), article.get("tags", ""), article.get("summary", ""))
        if module is None:
            module = "M2"  # 默认归入 M2
        article["module"] = module
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

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ km_results.json 已生成：共 {len(results)} 条（M1: {len(m1)} 条，M2: {len(m2)} 条）")
    print(f"   路径：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()

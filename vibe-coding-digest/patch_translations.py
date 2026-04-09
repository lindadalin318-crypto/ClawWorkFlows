#!/usr/bin/env python3
"""
patch_translations.py - 将翻译结果写入 raw.json 并重新生成报告
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 翻译数据：{url: (title_zh, full_summary)}
TRANSLATIONS = {
    "https://x.com/superformxyz/status/2022076393870569800/analytics": (
        "SuperVaults：赚取收益并获得$UP代币",
        "将USDC存入SuperVaults，在赚取收益的同时获得$UP代币奖励，成为Superform早期参与者。（广告内容）"
    ),
    "https://x.com/IBKR/status/2011622731440337083/analytics": (
        "Interactive Brokers：全球交易，值得信赖",
        "Interactive Brokers广告：全球市场交易，工具卓越，成本低廉。（广告内容）"
    ),
    "https://x.com/IBKR/status/1981829270940082501/analytics": (
        "实时响应市场动态，随时随地交易",
        "Interactive Brokers广告：第一时间响应市场重大新闻，随时随地便捷交易。（广告内容）"
    ),
    "https://x.com/IBKR/status/2011630152003043681/analytics": (
        "升级你的交易体验——更强工具、更低成本、全球市场",
        "Interactive Brokers广告：提供更优质的交易工具、更低的交易成本和全球市场准入。（广告内容）"
    ),
    "https://x.com/BlueDawnCasting/status/2033248806783906249": (
        "Blue Dawn：专注独立游戏的配音与语音指导公司",
        "Blue Dawn是一家专注独立游戏的配音/语音指导公司，全程协助客户完成演员合作与配音流程，坚持使用真人配音而非AI语音。"
    ),
    "https://x.com/zivdotcat/status/2033367458544054634": (
        "1.43亿人以为在抓宝可梦，实际上在构建史上最大AI数据集之一",
        "Niantic披露：Pokémon Go玩家共生成了超过300亿条真实世界数据，成为有史以来最大规模的分布式AI训练数据集之一。"
    ),
    "https://x.com/timbo_jay/status/2032862785256702162": (
        "250个手绘像素敌人/NPC精灵图，仅需$3",
        "正在制作古怪JRPG或地牢爬行游戏？可获取250个独特手绘像素风敌人/NPC精灵图（非AI生成），itch.io上仅售$3，现享75折优惠。"
    ),
    "https://x.com/jettelly/status/2033392817817481289": (
        "Godot 4.6魂系战斗原型：实时网格切割+AI战斗行为",
        "Moong在Godot 4.6中构建了一个魂系战斗原型，通过自定义GDExtension实现实时网格切割，结合AI战斗行为与动画驱动的近战系统，展示了Godot在高级战斗机制上的潜力。"
    ),
    "https://x.com/rahul__gh0sh/status/2033371775783121325": (
        "独立游戏开发者：我构建了一个AI角色绑定与动画智能体",
        "针对独立游戏开发者的痛点，作者开发了一个AI智能体，可自动完成角色骨骼绑定并生成完整动画包，即将上线。"
    ),
    "https://x.com/genxdegenerate/status/2033407132394225706": (
        "Freaks AI PvP游戏市场正在起飞",
        "一款AI PvP游戏"Freaks"的市场正在快速增长，开发者粉丝数不足400但已有大钱包在扫货，链上组织化迹象明显。"
    ),
    "https://x.com/ShyamOza/status/2032825222571655661": (
        "游戏AI根本不智能，它只是一种幻觉",
        "游戏内AI并非真正智能，只是为了让玩家"感觉真实"而设计的模拟系统。NPC路径失效、无法应对新颖情况，都是因为底层逻辑是规则而非真正的推理。"
    ),
    "https://x.com/hamdoesyoutube/status/2033382934510797221": (
        "AI在几秒内生成完整游戏UI资源，这就是未来",
        "作者一直在宣扬AI开发运动，如今AI已能在几秒内生成完整的游戏UI资源，这正是游戏开发的未来方向。"
    ),
    "https://x.com/MarcusSchuler/status/2033404901443703134": (
        "游戏开发者对AI情绪跌至历史低点：52%持负面态度",
        "GDC调查显示，游戏开发者对生成式AI的负面看法已从两年前的18%飙升至52%，创历史新高，仅7%持正面态度。"
    ),
    "https://x.com/PastCoded/status/2033386950854361262": (
        "期待人们戴上手工AI面部识别遮罩上街",
        "作者调侃：未来人们可能会戴上手工制作的AI面部识别遮罩出门，就像独立游戏《We Happy Few》里的场景一样。"
    ),
    "https://x.com/Aaron_Wacker/status/2033358758689050706": (
        "Parks and Peaks：用Three.js构建的美国地理策略卡牌游戏",
        "新独立游戏Parks and Peaks，基于Three.js的3D几何图形，以美国各州地理为基础，融入AI对战的策略卡牌玩法。"
    ),
    "https://x.com/LibertyCipher/status/2033304508453863551": (
        "AI将让圣经游戏独立开发者重新崛起",
        "AI将降低独立游戏开发门槛，就像NES/SNES时代小团队也能做游戏一样，圣经题材等小众游戏的独立开发者将迎来复兴。"
    ),
    "https://x.com/dEXploarer/status/2032697466806542386": (
        "Agent Worlds：每个NPC都是有钱包的AI智能体",
        "概念游戏"Agent Worlds"：每个NPC都是AI智能体，每个智能体都有钱包，可以随时间学习并离开游戏独立存在，是AI与区块链结合的游戏新形态。"
    ),
    "https://x.com/Aoleihal/status/2033377779777966136": (
        "游戏开发正从资产创作转向系统设计",
        "游戏开发范式正在转变：开发者将专注于架构规则和行为系统，AI动态生成内容。类似Diablo的程序化生成但更有意图性，Tripo P1.0让这一愿景更近了一步。"
    ),
    "https://x.com/NatlaGPT/status/2033358251819999365": (
        "我用AI游戏工作室赚了12英镑",
        "作者用AI提示词为游戏打了补丁，靠7个粉丝的"Atlantis AI游戏工作室"赚了12英镑，调侃自己在游戏行业悄然崛起。"
    ),
    "https://x.com/shinoartshop/status/2033410764514664783": (
        "中世纪幻想城堡食物储藏室背景图（AI生成，10张套装）",
        "日文推文：中世纪幻想城堡设施系列——食物储藏室背景图，AI生成，10张套装，在Booth平台出售。"
    ),
    "https://x.com/implicatorai/status/2033404707696259322": (
        "游戏开发者对AI情绪跌至历史低点（52%负面）",
        "GDC调查：52%游戏开发者对生成式AI持负面态度，仅7%持正面，负面比例是两年前的近三倍。"
    ),
    "https://x.com/valthvisuals/status/2032990965867155576": (
        "游戏开发者Mac工具清单大曝光",
        "推文列举了一位游戏开发者Mac上安装的所有工具，包括Finder、日历、Chrome、Photoshop、Epic Games等，展示了现代游戏开发者的完整工具链。"
    ),
    "https://x.com/andrew_bobnyuk/status/2033281544262160564": (
        "GDC 2026：我的第一次大型游戏开发者大会体验",
        "作者分享了首次参加GDC 2026的感受，与风险投资人、游戏开发者深度交流，收获远超预期，是一次难忘的行业盛会。"
    ),
    "https://x.com/gemsnper/status/2033247885869936686": (
        "CoPaw本地运行Ollama对独立开发者AI部署的影响",
        "探讨CoPaw结合Ollama本地运行对独立开发者的意义：无需庞大云资源即可部署AI，可能成为资源有限的独立开发者的游戏规则改变者。"
    ),
    "https://x.com/Stigern87/status/2033241244470485291": (
        "Iron Command：RTS游戏战斗机升空展示",
        "独立RTS游戏Iron Command展示战斗机升空并锁定目标的实机画面，支持Windows平台，融合AI、策略等元素，采用vibe coding开发。"
    ),
    "https://x.com/NanoCommando/status/2033293367631573387": (
        "Web3游戏首创：AI NPC DISPENSO能跨全局记住你",
        "Nano Commando游戏推出AI NPC DISPENSO，能在整个游戏中记住玩家的一切，不是存档加载，而是真正的持久化记忆，是Web3游戏中前所未有的AI NPC实现。"
    ),
    "https://x.com/kisekiseki30626/status/2033240824163561657": (
        "澄清：游戏里一直都有AI，只是不是生成式AI",
        "作者澄清游戏开发常识：游戏从来不存在"没有AI"的情况，任何NPC行为系统都是AI，只是不同于当今的生成式AI，路径失效等问题本质上是规则系统的局限。"
    ),
    "https://x.com/CreateLex/status/2032915188190687241": (
        "我们的用户正在用Unreal Engine进行Vibe Coding游戏开发",
        "Createlex分享：他们的用户已经在用Unreal Engine进行vibe coding游戏开发，AI辅助编程正在渗透进专业游戏引擎工作流。"
    ),
    "https://x.com/flowmi_ai/status/2033389256786485436": (
        "AI自动化：它能看DOM、点击、输入，你只需旁观",
        "Flowmi AI工具演示：AI能直接感知网页DOM结构，自动点击和输入，是网页测试、数据抓取和自动化的革命性工具。"
    ),
    "https://x.com/ai_shion42229/status/2033386110810747314": (
        "一位游戏开发者在Twitch看到Steam上线30小时销售数据后哭了",
        "一位独立游戏开发者在Twitch直播中，看到自己游戏上线30小时后的Steam销售数据后流泪。一个人、一款游戏、数年心血，创作者经济不是理论，而是真实的人在为梦想哭泣。"
    ),
    # Reddit
    "https://www.reddit.com/r/Unity3D/comments/1ruolzq/1_million_231k_poly_statues_rendered_using/": (
        "用Atomize渲染100万个23.1万面雕像（基于Nanite）",
        "作者展示其虚拟几何系统在Unity中渲染100万个高精度雕像的最新视频，基于类似Nanite的Atomize技术，正在探索性能极限。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1ruf6hf/3_minutes_of_skiers_skiing_and_workers_working/": (
        "3分钟滑雪者滑雪与工人工作的游戏演示",
        "Unity3D游戏演示视频，展示滑雪者滑雪和工人工作的场景动画，3分钟的游戏实机展示。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1ruhrtf/3_years_developing_the_last_general/": (
        "《The Last General》开发三周年！",
        "作者分享独立游戏《The Last General》开发三周年纪念，发布了一段回顾视频，记录了三年来游戏从零到现在的完整开发历程。"
    ),
    "https://www.reddit.com/r/godot/comments/1ruan7a/a_friend_of_mine_made_me_these_cool_things/": (
        "朋友给我做了这些超酷的东西！",
        "Godot开发者分享朋友为其制作的周边物品，展示游戏社区的温情互动。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1rux67w/angle_math_is_hard_but_worth_it/": (
        "角度数学很难但很值得",
        "Unity3D开发者分享：终于在物理代码中实现了真实的汽车转向逻辑，不再用"两辆自行车拼在一起"来模拟，角度数学复杂但效果显著提升。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rudmv6/building_reactive_turnbased_rpg_template_for_fab/": (
        "为FAB构建响应式回合制RPG模板——拾取物品 | Devlog #7",
        "Devlog #7：展示在Unreal Engine中为FAB市场构建回合制RPG模板，本期实现了拾取系统，包括药水、金币和可招募角色。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1rugh2e/deadly_threat_spotted_initiating_imminent/": (
        "发现致命威胁：即将触发遭遇战",
        "Unity3D游戏片段展示：敌人AI检测到玩家并触发战斗遭遇，配合pdkmusic的原创音乐，无剧透展示。"
    ),
    "https://www.reddit.com/r/godot/comments/1rulavc/dynamic_healthbar_with_shader/": (
        "用Shader实现动态血条",
        "Godot开发者分享：用Shader实现的动态血条，每100和1000HP有视觉提示，展示了Godot Shader在UI上的应用。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rum0wz/dynamically_scaling_ragdoll_bones/": (
        "动态缩放布娃娃骨骼？",
        "Unreal Engine开发者探讨：在实现角色比例自定义（缩短躯干、放大腿部等）后，如何让布娃娃物理与之匹配，寻求动态缩放Ragdoll骨骼的解决方案。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1ruoufo/early_gameplay_prototype_made_in_unity_combat/": (
        "用Unity制作的早期战斗原型——战斗系统与敌人角色",
        "独立游戏《Pull on Heart》早期战斗原型展示，重点展示战斗系统和不同敌人角色的设计，作者分享开发进展并寻求社区反馈。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1ruy41r/eternal_voyager_livelink_wardrobe_test/": (
        "Eternal Voyager LiveLink服装测试",
        "Unreal Engine LiveLink服装测试视频，展示角色穿戴完整服装后的实时动作捕捉效果。"
    ),
    "https://www.reddit.com/r/godot/comments/1rub9rn/experimenting_with_increasing_the_players_speed/": (
        "实验性增加玩家速度与操控感的变化",
        "Godot开发者分享实验：随游戏进程逐渐提升玩家移动速度和操控响应，探索如何通过速度变化增强游戏体验。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1ruxd0g/fab_marketing_question/": (
        "FAB市场营销问题咨询",
        "Unreal Engine开发者正在制作魔法开放世界游戏，同时开发了多个自动化RPG插件，寻求关于FAB市场营销策略的建议。"
    ),
    "https://www.reddit.com/r/godot/comments/1rup7tb/first_foray_into_3d/": (
        "初次尝试3D游戏开发",
        "Godot开发者分享：在多年2D像素艺术开发后首次涉足3D，已完成角色建模和动画，正在探索3D游戏开发的新世界。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1ruakok/flat_or_smooth_shading_for_my_turret_in_a_lowpoly/": (
        "低多边形世界中的炮塔：平面着色还是平滑着色？",
        "Unity3D VR游戏开发者分享：在低多边形风格游戏中，为炮塔选择平面着色还是平滑着色的纠结，附上两种效果对比图寻求社区意见。"
    ),
}

def main():
    date = "2026-03-16"
    raw_path = os.path.join(BASE_DIR, f"digest_{date}_raw.json")
    
    print(f"📖 读取 {raw_path}")
    with open(raw_path, encoding="utf-8") as f:
        data = json.load(f)
    
    # 更新翻译
    updated = 0
    for key in ("m1", "m2"):
        for item in data[key]:
            url = item["url"]
            if url in TRANSLATIONS:
                title_zh, full_summary = TRANSLATIONS[url]
                item["title_zh"] = title_zh
                item["full_summary"] = full_summary
                updated += 1
    
    print(f"✅ 更新了 {updated} 条翻译")
    
    # 保存
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 已保存 raw.json")
    
    # 重新生成报告
    print("📝 重新生成报告...")
    sys.path.insert(0, BASE_DIR)
    import importlib.util
    spec = importlib.util.spec_from_file_location("digest", os.path.join(BASE_DIR, "digest.py"))
    digest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(digest_module)
    
    m1_items = data["m1"]
    m2_items = data["m2"]
    report = digest_module.generate_report(m1_items, m2_items)
    
    report_path = os.path.join(BASE_DIR, f"digest_{date}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 报告已更新: {report_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译 2026-04-02 X/Twitter 和 Reddit 条目"""
import json

with open('/Users/dada/vibe-coding-digest/digest_2026-04-02_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# X/Twitter 翻译（按 URL 匹配）
x_translations = [
    ("https://x.com/clemmygames/status/2039357220337406261",
     "独立开发者正制作「疾速追杀」风格第三人称游戏：赛博朋克城市中混合近战与枪战，对抗专制AI政权",
     "一位独立开发者正在制作第三人称游戏，基本上就是「疾速追杀」风格——在赛博朋克城市中混合近战与枪战，对抗专制AI政权。"),
    ("https://x.com/wildmindai/status/2039276724735594596",
     "全新AI插图工具See-through：单张动漫图像分解为19个语义RGBA图层，支持Live2D自动绑定",
     "全新AI插图工具See-through：将单张动漫插图分解为19个语义RGBA身体图层，支持inpainting；在RTX 4090上90秒内生成2.5D模型；自动Live2D绑定。"),
    ("https://x.com/5mingame2/status/2039318046264016897",
     "NVIDIA GDC 2026演讲视频公开：用Cursor在Godot中快速实现路径追踪",
     "NVIDIA GDC 2026演讲视频已公开，其中包括用Cursor在Godot中快速实现路径追踪的演讲，推荐观看。"),
    ("https://x.com/rafsby_art/status/2039191516826767373",
     "受Beast卡丁车赛车项目启发，用AI为BEAST角色制作了视频",
     "受Beast卡丁车赛车项目启发，用AI为Rafsby的BEAST角色制作了视频。"),
    ("https://x.com/Mago_Gamedev/status/2039252948183863307",
     "Mago的《Nightly Take Out》Demo更新：修复对话错字并调整部分提示",
     "Mago的《Nightly Take Out》Demo刚刚更新！修复了对话中的错字并调整了部分提示文字。"),
    ("https://x.com/KevSmithDev/status/2039259898027417605",
     "我现在如何在游戏开发中使用AI #gamedev #ai #indiedev",
     "分享了在游戏开发中使用AI的当前方式和心得。#gamedev #ai #indiedev"),
    ("https://x.com/GameDevAlf/status/2039211200706330625",
     "修一个bug冒出三个新bug：维修扣钱逻辑、拍卖出价上限、建筑成本叠加问题",
     "修一个bug，冒出三个新bug。当前问题：维修不正确扣钱、拍卖允许出价超过余额、建筑成本无限叠加。"),
    ("https://x.com/simonw/status/2039302099038335003",
     "精彩帖子揭示LLM驱动开发真实现状：确实是游戏规则改变者，但远未达到炒作水平",
     "一篇精彩的帖子展示了LLM驱动开发的真实现状：确实是游戏规则改变者，但远未达到炒作水平。"),
]

# Reddit 翻译（按标题前缀匹配）
reddit_translations = [
    ("(UE4) All reflective surfaces flickering",
     "(UE4) 特定角度下所有反射表面闪烁，仅在使用低质量设置时出现",
     "UE4中特定角度下所有反射表面出现闪烁问题，仅在使用低质量设置时复现，寻求解决方案。"),
    ("1970 Mercedes Benz Lowpoly Bus",
     "1970年梅赛德斯-奔驰低多边形巴士（Blender 3D制作）",
     "用Blender 3D制作的1970年梅赛德斯-奔驰低多边形巴士模型，可用于Unity3D游戏。"),
    ("3 things about Godot's multiplayer API",
     "关于Godot多人游戏API，我希望早点知道的3件事",
     "分享了在使用Godot多人游戏API时踩过的坑，以及希望早点知道的3个重要知识点。"),
    ("Added ground shadows & lighting based on feedback",
     "根据反馈添加了地面阴影和光照，但感觉还缺点什么，求助",
     "根据社区反馈添加了地面阴影和光照效果，但感觉视觉上还缺点什么，希望获得进一步建议。"),
    ("After Translating my Game into 6 Different Languages",
     "将我的游戏翻译成6种语言之后的感想",
     "分享了将游戏本地化为6种不同语言的经验和心得。"),
    ("After feedback from this sub, I've made a slight change to character sprites",
     "根据本版块反馈，对角色精灵图做了小调整",
     "根据Unity3D社区的反馈，对游戏角色精灵图进行了小幅调整，展示前后对比。"),
    ("Another episode of is it a cake",
     "又一集「这是蛋糕吗？」——Godot游戏场景展示",
     "又一集「这是蛋糕吗？」系列，展示了用Godot制作的逼真游戏场景。"),
    ("Are different art styles between gameplay and steam page",
     "游戏玩法与Steam页面/封面使用不同美术风格，你们觉得可以吗？",
     "讨论游戏玩法内的美术风格与Steam页面、封面美术风格不一致是否可以接受。"),
    ("Artemis II NASA website in Unity3D",
     "用Unity3D复现阿尔忒弥斯II NASA网站交互体验",
     "用Unity3D复现了阿尔忒弥斯II NASA网站的3D交互体验。"),
    ("Backwards compatability",
     "Godot向后兼容性问题讨论",
     "讨论Godot引擎的向后兼容性问题及其对开发者的影响。"),
    ("Best Places To Find Sound Effects",
     "哪里可以找到最好的音效资源？",
     "讨论游戏开发中寻找高质量音效资源的最佳平台和网站。"),
    ("Best way to design immersive ambient sound for a horror game",
     "如何为恐怖游戏（UE5）设计沉浸式环境音效？我的做法对吗？",
     "讨论在UE5中为恐怖游戏设计沉浸式环境音效的最佳实践，分享当前做法并寻求反馈。"),
    ("Building a free, open-source quest system for UE5 called SimpleQuest",
     "为UE5构建免费开源任务系统SimpleQuest，附演示视频",
     "正在为UE5构建免费开源任务系统SimpleQuest，分享了演示视频和开发进展。"),
    ("Camera rendering black image",
     "Unity摄像机渲染黑色图像问题求助",
     "Unity3D中摄像机渲染输出黑色图像，寻求解决方案。"),
    ("Cool Psychedelic Shader Effect I Made",
     "我用Godot制作的炫酷迷幻Shader效果",
     "分享了用Godot制作的炫酷迷幻Shader视觉效果，附效果展示。"),
]

def apply_trans(items):
    count = 0
    for item in items:
        source = item.get('source', '')
        url = item.get('url', '')
        title = item.get('title', '')
        
        if item.get('title_zh'):
            continue
            
        if 'X/Twitter' in source:
            for trans_url, title_zh, full_summary in x_translations:
                if url == trans_url:
                    item['title_zh'] = title_zh
                    item['full_summary'] = full_summary
                    count += 1
                    break
            else:
                # 没有精确匹配，用原标题截断
                item['title_zh'] = title[:80]
                item['full_summary'] = item.get('summary', '')[:200]
                count += 1
        elif 'Reddit' in source:
            matched = False
            for prefix, title_zh, full_summary in reddit_translations:
                if title.startswith(prefix[:25]):
                    item['title_zh'] = title_zh
                    item['full_summary'] = full_summary
                    count += 1
                    matched = True
                    break
            if not matched:
                item['title_zh'] = title[:80]
                item['full_summary'] = item.get('summary', '')[:200]
                count += 1
    return count

c1 = apply_trans(data['m1'])
c2 = apply_trans(data['m2'])
print(f'M1翻译: {c1}条, M2翻译: {c2}条')

with open('/Users/dada/vibe-coding-digest/digest_2026-04-02_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('已保存翻译结果')

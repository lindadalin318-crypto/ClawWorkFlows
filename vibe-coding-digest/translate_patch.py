#!/usr/bin/env python3
import json

with open('/Users/dada/vibe-coding-digest/digest_2026-04-09_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    # M1 X/Twitter
    'https://x.com/maseylia/status/2041859250868060372': (
        '当我开始做独立游戏时，AI让我倍感沮丧',
        '作者分享开始做独立游戏时被AI打击的心路历程：每当自己迈出一小步，生成式AI就似乎迈出了一大步，让人不断怀疑等游戏发布时市场上会不会已有几十款类似的游戏。'
    ),
    'https://x.com/iam678/status/2041896507075653871': (
        'HTC用AI和Vibe Coding复活了被遗弃的VR头显VIVE Flow',
        'HTC于2021年发布VR头显VIVE Flow，因生态系统薄弱几乎无可用应用而被放弃。如今有人用AI和Vibe Coding为其开发了一款游戏，证明即便是被遗弃的硬件，AI辅助开发也能赋予其新生命。'
    ),
    'https://x.com/RatsbaneGame/status/2041561148005195952': (
        '【Ratsbane游戏趣事#4】游戏里的老鼠居然喜欢追光标',
        '独立游戏Ratsbane的开发者分享了一个有趣发现：游戏中的老鼠角色似乎特别喜欢追逐光标，当开发者把光标给它看时，它会疯狂追逐，眼睛形状也会随之改变。#gamedev'
    ),
    'https://x.com/theartofyoutube/status/2041868749142118487': (
        '有效缩略图发现：AI可轻松替换的独立游戏风格动画',
        '分析了一种有效的YouTube缩略图风格：类似独立游戏或桌游的简洁动画风格，极客机器人造型，干净清晰，且易于用AI替换生成。该频道拥有45.4万订阅者。'
    ),
    'https://x.com/asimo3089/status/2041956636626133453': (
        '我愿意让AI玩我的游戏来自动填写发布问卷',
        '开发者表示非常厌烦游戏发布流程中的问卷调查，宁愿让AI自动玩游戏来测试代码并填写问卷，认为问卷流程完全可以被AI自动化取代。'
    ),
    'https://x.com/LuLuviahhh/status/2041683560508109058': (
        '独立游戏工作室被曝使用AI制作概念图却赢得多项独立游戏大奖',
        '某独立游戏工作室被揭露使用AI生成概念图，但仍赢得多项独立游戏奖项引发争议。评论者认为该工作室规模已不算真正的独立工作室，却占用了本应属于小型独立开发者的奖项名额。'
    ),
    'https://x.com/mewlist/status/2041472950348763566': (
        '我在开发对话与事件系统，AI直接帮我实现了GraphView',
        '开发者正在制作对话和事件系统，原本因为GraphView使用起来麻烦而回避，结果AI直接帮忙实现了。感叹只要能正确引导AI，很多原本觉得麻烦的功能都能快速完成。'
    ),
    'https://x.com/CheetahTownGame/status/2041966869767442583': (
        '【Hex Judge】行刑前嫌疑人说出了令人不寒而栗的遗言',
        '独立游戏Hex Judge的开发者分享了游戏中的一幕：一名嫌疑人在行刑前说出了听起来像遗言的话语，游戏中的AI对话系统让每次审讯都有独特体验。#indiedev #gamedev #AI'
    ),
    'https://x.com/CheetahTownGame/status/2041974372160995506': (
        '【Hex Judge】嫌疑人Thomas：看似诚实的牧羊人，审讯中故事却会改变',
        'Hex Judge游戏中的嫌疑人Thomas是个年轻牧羊人，看似诚实但审讯时故事会发生变化。AI对话系统让每次对话都略有不同，增强了游戏的悬疑感。'
    ),
    'https://x.com/buildbox/status/2041952969499857305': (
        '【AI游戏开发技巧】用Buildbox 4的AI场景生成器秒出关卡背景',
        'AI游戏开发小技巧：被背景或关卡视觉效果卡住时，让AI来加速。Buildbox 4的AI场景生成器可以将详细文字描述在几秒内转化为完整游戏环境，描述越清晰效果越好。'
    ),
    'https://x.com/CheetahTownGame/status/2042001349345472652': (
        '我用AI辅助写推文，因为我正在做一款AI驱动的游戏',
        '开发者分享了自己发推时会用AI辅助修改文字，认为这与自己正在开发AI驱动游戏的身份非常契合。'
    ),
    'https://x.com/fronkongames/status/2041957169784877503': (
        'Intel Arc Pro B70在LLM/AI、OpenCL、OpenGL和Vulkan上的跑分测试',
        '分享了Intel Arc Pro B70在Linux平台上针对LLM/AI、OpenCL、OpenGL和Vulkan的基准测试结果，对游戏开发者和AI开发者选择GPU有参考价值。#ai #indiedev #gamedev'
    ),
    'https://x.com/StudioAtelico/status/2041936130325496285': (
        'GDC生物合集第2卷发布！设备端AI驱动的游戏生物',
        'Studio Atelico发布了GDC生物合集第2卷，展示了设备端AI（On-Device AI）驱动的游戏生物效果。#GameDev #AI #IndieDev #OnDeviceAI #Gaming'
    ),
    'https://x.com/gabe_teee/status/2042082054251196901': (
        'Base44正在悄悄改变游戏规则：无需漫长开发周期即可构建应用',
        'Base44正在悄然改变开发格局，让开发者可以构建应用、自动化工作流并比以往更快地发布，无需陷入漫长的开发循环。如果你还在用老方法，已经落后了。'
    ),
    'https://x.com/WarforgeXP/status/2042034254813487170': (
        '不拥抱AI工具和流程的游戏开发者终将被淘汰',
        '明确表态：不采取拥抱AI工具和流程步骤的人终将变得无关紧要。在游戏开发领域，接受AI工具和AI流程是必须面对的未来，没有选择余地。'
    ),
    'https://x.com/UrLocalClown666/status/2042034092607234298': (
        '本周游戏圈大事：虚假谋杀指控毁了一款游戏，性骚扰指控曝光',
        '本周游戏圈发生的大事：1.虚假谋杀指控毁掉了一名开发者的游戏，同时暴露了参与测试的糟糕工作人员问题；2.针对某游戏开发者的真实性骚扰指控曝光。'
    ),
    'https://x.com/PlatoEvolved/status/2041947273987551251': (
        '用Claude AI和一条提示词，45秒内构建扫雷游戏',
        '展示了用Claude AI和一条提示词在45秒内构建扫雷游戏的完整过程，由Morgan Page演示。这是AI辅助游戏开发快速原型验证能力的生动案例。#AIGames #GameDev #AIProjects'
    ),
    'https://x.com/chigamespace/status/2041962101086773745': (
        '本周六来芝加哥Gamespace体验AI驱动NPC侦探游戏',
        '芝加哥Gamespace邀请玩家本周六来体验ReLu Games开发的AI驱动NPC侦探游戏《Uncover the Smoking Gun》，同时可参观游戏历史收藏展。'
    ),
    'https://x.com/shad0va/status/2041684579137024135': (
        'AI生成内容不等于游戏内AI，NPC AI和ChatGPT是完全不同的东西',
        '澄清了一个常见混淆：游戏中使用AI生成的内容（如图像）和游戏内置AI（如NPC行为AI）是完全不同的概念。NPC AI不等于ChatGPT，不能混为一谈。'
    ),
    'https://x.com/laubeq_28/status/2042022749875421518': (
        '独立开发者Antti的游戏刚上线EA阶段，AI系统还在完善中',
        '评论某款刚上线抢先体验（EA）的独立游戏：开发者Antti是一个人在做，游戏AI系统可能比之前还差一点，但这是EA版本还没完成，Antti是个完美主义者后续会持续改进。'
    ),
    'https://x.com/igwefran6/status/2041951308500861253': (
        '后端开发最适合AI来做，尤其是API集成类工作',
        '认为后端开发是最适合AI执行的领域，特别是基于清晰的分阶段架构计划进行API集成工作。真正的数据操作仍有挑战，但大部分后端工作AI可以很好地完成。'
    ),
    'https://x.com/ReactorcoreDev/status/2042063310955421900': (
        'Reactorcore：游戏设计、2D/3D美术、Mod制作与AI提示工程综合资源中心',
        'Reactorcore分享了自己的Linktree页面，涵盖游戏设计、2D/3D美术、Mod制作和AI提示工程等内容，是游戏开发与AI结合领域的综合资源中心。#GameDev #DigitalArt'
    ),
    'https://x.com/AgentRank_ai/status/2041811420363329759': (
        'Unity MCP在AgentRank排名第一（98.07分）：让AI助手直接操控Unity编辑器',
        'CoplayDev开发的unity-mcp在AgentRank平台以98.07分排名第一。Unity MCP作为桥梁，让Claude、Cursor等AI助手可以通过本地MCP服务器直接与Unity编辑器交互，是AI辅助游戏开发的重要工具。'
    ),
    'https://x.com/DamienHOFFSCHIR/status/2041868912090869897': (
        '独立开发者同时构建AI Agent和Claude Agent驱动的独立游戏',
        '独立开发者正在同时构建两个项目：Lain（具有持久记忆和主动任务的AI Agent）和Aekan（由一组Claude Agent驱动的独立游戏），主要使用C#开发。'
    ),
    'https://x.com/andreintg/status/2041799086794326200': (
        '独立游戏圈大V正在给使用AI的开发者判死刑',
        '感叹独立游戏圈中一些有影响力的人正在对使用AI的开发者造成最后一击，告诉开发者使用AI是错误的、不酷的，并暗示会被取消关注，这种舆论压力令人担忧。'
    ),
    'https://x.com/AnishSukhramani/status/2041752846044164449': (
        '"公开构建"对独立开发者的吸引力：AI自动化如何缓解单人创业压力',
        '探讨公开构建（Build in Public）对独立黑客的吸引力，以及AI自动化如何在日常工作流程中帮助缓解单人创始人的压力，特别是在反馈循环方面。'
    ),
    'https://x.com/RandomWordsGuy/status/2041706470887055496': (
        'X的算法会把用户分组并推送特定内容，我的信息流里有AI、动漫和独立游戏',
        '观察到X/Twitter的算法似乎会将用户分类并向特定群体推送特定内容，自己的信息流中包含AI、动漫和独立游戏相关内容，印证了算法的精准分组推送机制。'
    ),
    'https://x.com/IAMDORIANGRAE/status/2041834502792650983': (
        '什么是CPU瓶颈游戏：物理、NPC密度、AI和物品处理都是关键因素',
        '科普游戏性能优化知识：CPU瓶颈游戏指CPU成为硬性限制的情况，包括物理计算、NPC密度、AI逻辑、物品处理等都是CPU密集型操作，CPU的硬性限制无法像GPU那样简单通过硬件升级改变。'
    ),
    'https://x.com/futureiscome/status/2041388611233370338': (
        '懂一点基础编程，Vibe Coding在Unity开发中效果非常好',
        '分享了对Vibe Coding的看法：如果懂一点基础编程知识，在Unity开发中Vibe Coding效果非常好，可以非常具体地告诉AI你想要什么。当然也有人直接不懂编程就Vibe Coding，效果因人而异。'
    ),
    'https://x.com/matterhornso/status/2042082632423653573': (
        '区块链AI不能简单地用Web开发AI微调来实现，需要专门构建',
        '指出区块链开发不只是代码问题，还涉及经济学、共识机制和对抗性博弈论。不能简单地对Web开发AI进行再训练就称其为Web3就绪，需要专门为区块链场景构建的AI模型。'
    ),
    # M1 Reddit
    'https://www.reddit.com/r/unrealengine/comments/1sg87x5/ue5_adimensional/': (
        '【UE5】Adimensional - 附自制音乐',
        'UE5独立游戏项目Adimensional展示，作者还自己制作了游戏配乐。'
    ),
    'https://www.reddit.com/r/Unity3D/comments/1sgb64h/wip_what_do_you_guys_think_of_my_car_controller/': (
        '【WIP】大家觉得我的Unity赛车控制器怎么样？',
        '开发者分享了开发约6个月的Unity赛车控制器，目前仍在制作中但接近完成，征求社区反馈。'
    ),
    'https://www.reddit.com/r/gamedev/comments/1sfrnaj/after_9_years_and_thousands_of_boardgame_pitches/': (
        '9年从发行商视角审阅数千份桌游提案后，我的建议',
        '一位有9年经验的桌游发行商分享了从发行商视角审阅数千份提案后总结的经验教训，指出了反复出现的常见问题和成功要素。'
    ),
    'https://www.reddit.com/r/gamedev/comments/1sgdi2x/almost_at_20k_wishlists_and_im_not_sure_how_to/': (
        '恐怖游戏《Dread Neighbor》即将达到2万愿望单，心情复杂',
        '独立恐怖游戏《Dread Neighbor》开发者分享了游戏即将达到2万Steam愿望单的喜悦与迷茫，不确定该如何看待这个里程碑。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sgcky2/am_i_allowed_to_use_assets_from_my_fab_libary_for/': (
        '我可以将Fab素材库中的资产用于自由职业项目吗？',
        '开发者询问Fab授权许可中关于将个人素材库资产用于客户自由职业项目的条款，因为许可协议中的表述存在一定歧义。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sfvheh/announcing_the_pines_a_psychological_horror_rpg/': (
        '宣布《The Pines》：UE独立开发的心理恐怖RPG',
        '开发者正式宣布其独立开发的心理恐怖RPG《The Pines》，使用Unreal Engine开发，游戏中玩家的选择真正影响故事走向。'
    ),
    'https://www.reddit.com/r/gamedev/comments/1sgcobd/anyone_use_beamable_for_backend_infra/': (
        '有人用Beamable做游戏后端基础设施吗？',
        '开发者正在为UE游戏选择后端基础设施，考虑使用Beamable对比PlayFab等方案，征求社区使用经验分享。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sfqx4w/arc_slash_fx_in_unreal_engine_5_niagara/': (
        '虚幻引擎5 Niagara实现弧形斩击特效',
        '分享了使用UE5 Niagara粒子系统制作的弧形斩击特效教程或展示。'
    ),
    'https://www.reddit.com/r/gamedev/comments/1sg52kw/at_what_point_do_you_start_looking_for_a_team/': (
        '什么时候开始组建团队合适？',
        '开发者探讨独立游戏开发中何时开始寻找团队成员的问题，观察到社区中常有人对求组队帖子表示不满，想了解大家的看法。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sgaxzl/attempting_to_export_combined_skeletal_mesh_of/': (
        '尝试导出UE5.6中MetaHuman的合并骨骼网格，只导出了皮肤碎片和手部',
        '开发者在UE5.6中尝试导出MetaHuman的合并骨骼网格时遇到问题，只导出了部分皮肤碎片和手部，寻求解决方案。'
    ),
    'https://www.reddit.com/r/gamedev/comments/1sfrxsk/beginner_game_developers_should_first_do_a_gamejam/': (
        '新手游戏开发者应该先参加GameJam',
        '建议新手游戏开发者首先参加GameJam，以解决常见问题：如何开始一个游戏项目、如何坚持下去以及如何完成一个长期搁置的项目。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sfpxk2/can_you_help/': (
        '求助：在UE中制作类似战争召唤的游戏时遇到2D切换问题',
        '开发者在用UE制作类似战争召唤的游戏时，遇到切换到2D视角的奇怪问题无法正常移动，寻求帮助。'
    ),
    'https://www.reddit.com/r/unrealengine/comments/1sfsif6/common_material_nodes_detailed_explanation_unreal/': (
        'UE5.7常用材质节点详解',
        '分享了UE5.7中常用材质节点的详细说明教程，填补了作者自己学习UE5时缺少此类教程的遗憾。'
    ),
    'https://www.reddit.com/r/godot/comments/1sfx5dp/connecting_signals_to_grandparent/': (
        '如何将Godot信号连接到祖父节点？',
        '开发者在Godot中制作含有多个程序化生成关卡的Roguelike游戏，遇到如何将信号正确连接到祖父节点的技术问题，寻求解决方案。'
    ),
    'https://www.reddit.com/r/godot/comments/1sg6pcr/demo_out/': (
        'Demo上线了！Godot独立游戏开发3个月成果',
        '开发者分享了历时3个月开发的Godot独立游戏Demo正式上线的喜讯，邀请大家体验。'
    ),
}

count = 0
for item in data['m1'] + data['m2']:
    url = item['url']
    if url in translations and not item.get('title_zh'):
        item['title_zh'] = translations[url][0]
        item['full_summary'] = translations[url][1]
        count += 1

with open('/Users/dada/vibe-coding-digest/digest_2026-04-09_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'翻译完成！共更新 {count} 条条目')

# 统计
m1_x = sum(1 for item in data['m1'] if item['source'].startswith('X/Twitter') and item.get('title_zh'))
m1_r = sum(1 for item in data['m1'] if item['source'].startswith('Reddit') and item.get('title_zh'))
print(f'M1: X/Twitter 翻译 {m1_x} 条，Reddit 翻译 {m1_r} 条')

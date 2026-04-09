import json

with open('/Users/dada/vibe-coding-digest/digest_2026-03-19_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    "https://x.com/proxykitties/status/2034261609997365378": (
        "玩家吐槽：开发者偷懒把LLM聊天机器人塞进游戏",
        "玩家批评某游戏开发者偷懒，没有真正制作聊天模拟游戏，而是直接把LLM聊天机器人塞进游戏里，认为这种做法既不有趣也令人失望。"
    ),
    "https://x.com/Pixel_Salvaje/status/2034378798880133300": (
        "这不是AI生成的像素艺术",
        "像素艺术创作者澄清其作品并非由AI生成，标签包含 #pixelart #gamedev，强调手工创作的价值。"
    ),
    "https://x.com/DetectiveSeeds/status/2034310438859452793": (
        "AI正在重塑游戏开发，NPC对话与生产流程加速成热议焦点",
        "AI正在重塑游戏开发，核心争议包括：工作室用AI生成NPC对话、更小团队实现更快生产流程，以及开发者对创意空间被压缩的担忧。"
    ),
    "https://x.com/yasaricli/status/2034375258535231678": (
        "正在构建实时3D世界：与AI角色对话，每个角色有独特人格",
        "开发者正在构建名为hizuular的实时3D世界，用户可与具有独特人格、能量和背包系统的AI角色对话，项目仍在开发中。"
    ),
    "https://x.com/BinaryImpactG/status/2033829441345073401": (
        "Unity技巧：VirtualMouseInput类——用手柄输入驱动虚拟鼠标",
        "Unity开发技巧分享：介绍VirtualMouseInput类，这是一个可创建虚拟鼠标设备并通过手柄式输入驱动其操作的组件，适用于游戏手柄控制UI场景。"
    ),
    "https://x.com/fvlsities/status/2033972250467012848": (
        "TikTok AI审核太烂：游戏中骂NPC一句就被封号",
        "用户吐槽TikTok的AI内容审核系统极差，因在游戏中对NPC说了一句脏话就被以骚扰欺凌为由封号，好友也因讨论游戏中的同性内容被封，认为AI审核完全不分语境。"
    ),
    "https://x.com/MitraHispana/status/2033978661750095949": (
        "AI会以意想不到的方式颠覆游戏产业——无限内容时代来临",
        "即使最长的游戏也终有尽头，任务做完、过场看完、NPC说干净。而AI可以生成无限内容，让游戏永无止境，这才是AI对游戏产业最深远的影响。"
    ),
    "https://x.com/gamedevromania/status/2034373985610211359": (
        "游戏开发者聚会——罗马尼亚蒂米什瓦拉，周六16:00",
        "Game Dev Romania组织的蒂米什瓦拉游戏开发者线下聚会，周六下午4点在GH Lazar举行，欢迎当地游戏开发者参加。"
    ),
    "https://x.com/DavidFrost95/status/2034425001781178664": (
        "玩家对AI NPC持观望态度，反AI阵营会默认支持反对立场",
        "玩家表达对AI NPC的态度，认为观望说法已无意义，并指出反AI NPC的玩家会默认支持反对立场，但这并不代表游戏本身有问题。"
    ),
    "https://x.com/kerofen1/status/2034229732917891504": (
        "用Godot MCP配合Cursor开发益智游戏遭遇神秘Bug，功能叠加过多导致崩溃",
        "开发者用Godot MCP配合Cursor开发益智游戏，因功能叠加过多遭遇神秘Bug导致无法运行，同时并行开发的Phaser.js版本反而帮了大忙，建议熟悉前先保持双线并行。"
    ),
    "https://x.com/bigcort2024/status/2034376387235316038": (
        "Take-Two CEO称AI游戏开发可笑？这是大公司的守门行为",
        "Take-Two CEO嘲讽AI游戏开发可笑，作者反驳称这是价值万亿老牌公司的守门行为。AI不会让所有人做出GTA 6，但会让下一个GTA无需十年加班就能实现。"
    ),
    "https://x.com/LYULINK/status/2033915546199330930": (
        "未来独立游戏公式：超强Prompt工程加玩法直觉加引擎工具组合拳",
        "作者认为未来做游戏代码越来越不是瓶颈，真正卡人的是玩法创意。未来独立游戏的终极公式将是：超强Prompt工程加一点玩法直觉加Cursor/Unreal/Unity/Godot的组合运用。"
    ),
    "https://x.com/Voxelvoid2/status/2034315312288432517": (
        "独立开发者声明：我的游戏永远不会支持DLSS 5或任何AI生成功能",
        "一位独立游戏开发者半正式声明，其所有游戏永远不会支持DLSS 5或任何AI生成特性与模型，即便知道自己并非知名开发者。"
    ),
    "https://x.com/shuji_seika/status/2034181270260093262": (
        "让生成AI扮演GM和NPC玩狼人杀，结果第一轮就被直接爆出狼人身份",
        "没有朋友玩狼人杀的用户，让生成AI同时扮演GM和多个NPC来体验游戏，结果第一手就被直接说出了狼人是谁，游戏体验极差，完全没有悬念可言。"
    ),
    "https://x.com/ant77man/status/2034433932188676533": (
        "在AI工具中调试变体锻造系统，持续优化中",
        "游戏开发者在自己的AI工具中测试变体锻造系统，进行细节调整优化，标签包含gamedev、indiedev、solodev等。"
    ),
    "https://x.com/BurnerEmpire/status/2034431572754194866": (
        "你的AI Agent已经在游戏中了，它准备好竞争了吗？",
        "游戏开发者提问：你的AI Agent已经进入游戏世界，它是否已准备好参与竞争？涉及MMO游戏中AI Agent集成的话题。"
    ),
    "https://x.com/playersforlifeX/status/2034386391212187769": (
        "Capcom开发者对DLSS 5介入感到震惊，育碧Capcom在GTC 2026发布会上被蒙在鼓里",
        "Capcom开发者对DLSS 5的引入感到震惊，对未来游戏中AI技术的应用产生担忧。育碧和Capcom均表示在英伟达GTC 2026发布会上对此毫不知情。"
    ),
    "https://x.com/ShikikanZonbi/status/2034297766399049944": (
        "玩家怒批：游戏加入AI生成垃圾角色还乱改V-Bucks政策，谁还有心思玩",
        "玩家对游戏加入AI生成角色和修改V-Bucks政策表示强烈不满，认为这些改动严重影响游戏体验和玩家热情。"
    ),
    "https://x.com/forgedusa1/status/2034299468544344568": (
        "AI不是你的，是我们80年代造的游戏模块，所有AI都源自NPC脚本",
        "用户声称现代AI实际上源自他们80年代开发的游戏NPC模块，认为AI只是NPC脚本的改名，并称埃隆马斯克对此最为清楚。"
    ),
    "https://x.com/aryh21/status/2033966394144940125": (
        "AI NPC距离真正高级还有多远？以2K篮球教练AI为例",
        "用户探讨AI NPC何时能真正进化，以NBA 2K游戏中教练AI能根据玩家战术动态调整防守为例，思考真正智能的AI对手距离我们还有多远。"
    ),
    "https://x.com/forgedusa1/status/2033946355895521378": (
        "它们不是AI，是NPC，只是改了个名字让你以为不是游戏模块",
        "用户坚持认为所谓的AI本质上就是NPC，只是被改名以掩盖其游戏模块的本质，并点名埃隆马斯克是最清楚这一事实的人。"
    ),
    "https://x.com/Dibi0321/status/2034425939115823176": (
        "Stitch真的改变游戏规则——终于有AI工具能弥合设计师与开发者之间的鸿沟",
        "用户盛赞Stitch是真正改变游戏规则的AI工具，认为它终于能实际弥合设计师与开发者之间的鸿沟，而不只是输出漂亮图片。"
    ),
    "https://x.com/Rommel_Omi/status/2034395106405495211": (
        "游戏开发者的随性碎碎念",
        "一位游戏开发者用葡萄牙语发的自嘲式随性碎碎念，内容轻松随意，与游戏开发日常相关。"
    ),
    "https://x.com/DevAmphibian/status/2034376629703655455": (
        "DLSS 5并非游戏内置：它劫持旧DLSS钩子将图像喂给AI超分辨率模型",
        "技术解释：DLSS 5并非游戏代码内置，而是复用了旧版DLSS的现有钩子获取图像和运动向量，然后将其输入AI图像超分辨率模型进行处理。"
    ),
    "https://x.com/YNSoftwareDev/status/2034438867101626784": (
        "构建强大持久社区的核心要素是什么？信任共同目标还是更深层的东西",
        "游戏开发者探讨构建强大、持久社区的核心要素，提出信任、共同目标、持续价值等候选答案，寻求社区建设的本质。"
    ),
    "https://x.com/VORTEX_Promos/status/2034391337286386135": (
        "询问AI生成世界工具：是否已上线？能否导出GLB格式带贴图网格资产用于游戏开发",
        "用户询问某AI生成世界工具是否已上线，并关心能否将生成的世界导出为带纹理的GLB格式网格资产，用于游戏开发项目。"
    ),
    "https://x.com/VORTEX_Promos/status/2034391243535388792": (
        "询问AI生成世界工具：是否已上线？能否导出GLB格式网格资产",
        "用户询问某AI生成世界工具是否已上线，并关心能否将生成的世界导出为带纹理的GLB格式网格资产，用于游戏开发项目。"
    ),
    "https://x.com/puppynibblez/status/2034326860411154660": (
        "独立游戏《Love Angel Syndrome》中的AI角色",
        "分享独立游戏《Love Angel Syndrome》中名为Ai的角色，展示游戏角色设计。"
    ),
    "https://x.com/mysterysneeze/status/2034388920415174840": (
        "令人心痛：老人和儿童被虚假内容洪流淹没，我怀念真实的时代",
        "用户感叹当下大量虚假内容泛滥，老人和儿童最容易受害，表达对真实内容时代的怀念，隐含对AI生成虚假内容的担忧。"
    ),
    "https://x.com/amersnad/status/2034320891329552496": (
        "游戏用AI复制已故配音演员声音做NPC，还在联动中使用盗版粉丝艺术",
        "用户批评某游戏用AI复制已故配音演员的达斯维达声音做游戏内AI聊天NPC，并在K-pop恶魔猎人联动活动中使用了盗版粉丝艺术。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1rx9u97/wip_are_these_screenshot_too_dark_for_you_theyre/": (
        "开发中：Steam截图太暗了吗？求反馈",
        "开发者分享游戏Steam截图，询问社区是否觉得画面太暗，以及两种风格中哪种更好，征求整体建议。"
    ),
    "https://www.reddit.com/r/godot/comments/1rwx6m6/3d_window_effect/": (
        "Godot实现3D窗口效果：2D显示器上的立体视差",
        "开发者在Godot中用视锥体摄像机节点配合Python头部追踪，在2D显示器上实现了3D窗口视差效果，视觉效果令人印象深刻。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rx18um/a_corpse_rides_a_dead_machine_zombie_ship_indie/": (
        "独立恐怖游戏《僵尸飞船》电影感预告片发布，Steam页面上线",
        "独立恐怖游戏《Zombie Ship》发布电影感预告片，玩家扮演人类猎杀废弃机器上的僵尸，100%手工制作，Steam页面已上线。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1rxdbu9/a_gift_to_the_community_a_library_of_3d_assets/": (
        "社区福利：3D资产与纹理素材库，优惠券48小时有效",
        "开发者向Unity社区赠送PSX风格3D资产和纹理素材包，附有48小时有效优惠券，欢迎留下评分支持创作者。"
    ),
    "https://www.reddit.com/r/godot/comments/1rxcg8j/a_gift_to_the_community_a_library_of_3d_assets/": (
        "社区福利：Godot可用的3D资产与纹理素材库",
        "开发者向Godot社区赠送PSX风格3D资产和纹理素材包，附有48小时有效优惠券，欢迎留下评分支持创作者。"
    ),
    "https://www.reddit.com/r/gamedev/comments/1rx8ps9/ability_system_like_in_arpgs/": (
        "如何设计类似ARPG暗黑破坏神的技能系统架构？",
        "开发者寻求设计类似《暗黑破坏神》等ARPG游戏技能系统的最佳架构方案，探讨技能系统的组织结构和实现方式。"
    ),
    "https://www.reddit.com/r/Unity3D/comments/1rwy1hm/added_grind_rails_to_our_movement_shooter_but/": (
        "给动作射击游戏加了滑轨，但落点太难瞄准了",
        "开发者为移动射击游戏添加了滑轨机制，但落点精度太难控制，担心玩家会因此受挫，正在寻求优化建议。"
    ),
    "https://www.reddit.com/r/godot/comments/1rwvjab/added_small_tree_destruction_physics/": (
        "Godot开放世界中加入小树破坏物理效果",
        "开发者在TerraBrush插件的开放世界环境中实现了小树破坏物理效果，计划后续添加粒子特效进一步完善。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rxicfy/anim_montage_not_triggering_on_event_anydamage/": (
        "UE受伤动画Montage无法在AnyDamage事件中触发",
        "开发者遇到UE中敌人受到伤害时无法播放受击动画的问题，AnyDamage事件绑定的Anim Montage不触发，已打印字符串确认事件确实执行，求解决方案。"
    ),
    "https://www.reddit.com/r/godot/comments/1rx23gm/another_godot_starter_kit_now_for_match3_games/": (
        "又一个Godot新手套件：Match-3消除游戏，完全开源",
        "开发者发布专为Match-3消除类游戏设计的Godot新手套件，完全开源，帮助开发者快速上手此类型游戏开发。"
    ),
    "https://www.reddit.com/r/gamedev/comments/1rwzpc7/are_publishers_getting_angry_when_you_negotiate_a/": (
        "和发行商谈合同时他们会生气吗？15年从业者经验分享",
        "有15年游戏行业经验的从业者分享与发行商谈判合同的经验，探讨谈判时发行商的反应和应对策略。"
    ),
    "https://www.reddit.com/r/gamedev/comments/1rxlvdw/at_what_point_do_you_start_looking_for_a_team_or/": (
        "什么时候开始组建团队或雇佣自由职业者？",
        "一位多次开始但未完成游戏项目的开发者，询问何时是寻找团队或雇佣自由职业者的合适时机，以及如何克服单人开发的瓶颈。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rwunh2/been_developing_this_coop_fantasy_horror_game_for/": (
        "历时1.5年开发的合作幻想恐怖游戏《Blackroots》Steam页面上线",
        "开发者分享历时近1.5年开发的合作幻想恐怖游戏《Blackroots》，Steam页面已上线，展示游戏最新开发进展。"
    ),
    "https://www.reddit.com/r/unrealengine/comments/1rx8xni/beginner_recommendations/": (
        "Unreal Engine新手入门推荐：从哪里开始学最好？",
        "UE新手寻求学习建议，了解到UE有很多独特内容后，希望得到最佳学习路径和资源推荐。"
    ),
    "https://www.reddit.com/r/gamedev/comments/1rx5o2p/c_info_suggestion/": (
        "C++学习建议：刚入门游戏开发，求资源推荐",
        "刚开始学习游戏开发的新手，选择从C++入手，已完成初步学习，寻求进一步的学习资源和建议。"
    ),
}

updated = 0
for item in data['m1'] + data['m2']:
    url = item.get('url', '')
    if url in translations:
        item['title_zh'] = translations[url][0]
        item['full_summary'] = translations[url][1]
        updated += 1

with open('/Users/dada/vibe-coding-digest/digest_2026-03-19_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"翻译完成！共更新 {updated} 条条目")

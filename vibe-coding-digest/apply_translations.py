#!/usr/bin/env python3
import json

translations = {
    "https://x.com/DITOGAMESch/status/1809885065066733956/analytics": {
        "title_zh": "你有鼠标，就必须玩这款游戏",
        "full_summary": "DITO GAMES 发推力推旗下游戏，称只要有鼠标就必须体验，该帖获得3万点赞，是本轮 X 热度最高的游戏推广内容。"
    },
    "https://x.com/job_medley/status/1618917575408353280/analytics": {
        "title_zh": "医疗护理转职首选 JobMedley，求职数量业界最大，满意度96%",
        "full_summary": "日本医疗护理行业招聘平台 JobMedley 的推广广告，宣称求职数量业界最大、用户满意度96%。（广告内容）"
    },
    "https://x.com/superformxyz/status/2022076393870569800/analytics": {
        "title_zh": "存入USDC到SuperVaults获取收益并获得$UP代币",
        "full_summary": "Superform 平台推广：将 USDC 存入 SuperVaults 可赚取收益，并提前获得 $UP 代币奖励。（Web3广告内容）"
    },
    "https://x.com/DannyLimanseta/status/2033567995122143363": {
        "title_zh": "用 Cursor Vibe Coding 在 Unity 引擎做钓鱼游戏原型的心得",
        "full_summary": "产品设计师 Danny 用 Cursor（Sonnet 4.6）在 Unity 引擎 vibe code 了一个钓鱼游戏原型，全程无需 Unity MCP，完全依赖 Cursor 模型生成，分享了详细经验教训，获968点赞，是本期 X 最高质量的 AI 游戏开发实践帖。"
    },
    "https://x.com/IndieGameJoe/status/2033664243824730220": {
        "title_zh": "我希望游戏看起来像游戏，而不是AI滤镜垃圾",
        "full_summary": "独立游戏博主 Indie Game Joe 针对 Nvidia DLSS 5 AI 增强功能发表批评，认为 AI 滤镜破坏了游戏的美术风格，获791点赞，引发大量讨论。"
    },
    "https://x.com/SilentHill/status/2032030149374591298/analytics": {
        "title_zh": "《寂静岭f》限时5折优惠，系列新手也能轻松入坑",
        "full_summary": "《寂静岭》官方账号宣布《SILENT HILL f》限时5折促销，适合系列新手体验这款全新心理恐怖作品。"
    },
    "https://x.com/TrueMoveH/status/2028346908880867670/analytics": {
        "title_zh": "泰国 True dtac HAPPY 旅游电话卡，无限流量畅游泰国",
        "full_summary": "泰国运营商 True5G 推广旅游 SIM 卡广告，支持无限流量，可在微信、Klook、飞猪、京东、携程购买。（广告内容）"
    },
    "https://x.com/HeroWarsWeb/status/2032428509780389948/analytics": {
        "title_zh": "浏览器内完整RPG游戏，无需下载即点即玩",
        "full_summary": "Hero Wars 网页 RPG 游戏推广：无需下载，直接在浏览器内体验完整 RPG 玩法。（广告内容）"
    },
    "https://x.com/SwooshBagen/status/2033672017518416287": {
        "title_zh": "反驳「未来所有游戏都将由AI开发」的说法",
        "full_summary": "推主对「未来所有游戏都将由AI开发」的说法提出反驳：这只适用于追求销量的AAA大作，独立游戏依然会由人类创作，因为独立游戏的灵魂在于个人表达。"
    },
    "https://x.com/JateLIVE/status/2033684263678169108": {
        "title_zh": "DLSS 5 AI增强最大的问题是改变了开发者的艺术视野",
        "full_summary": "独立游戏爱好者 JateLIVE 指出 DLSS 5 AI 增强的核心问题：光照变得更刺眼、AI 添加皱纹模拟细节，根本上改变了开发者的艺术意图，这比帧生成技术更令人担忧。"
    },
    "https://x.com/robin_esque/status/2033628027733573687": {
        "title_zh": "Nvidia DLSS 5 把游戏NPC变成AI生成的修图脸，令人绝望",
        "full_summary": "robin 批评 Nvidia DLSS 5 将游戏 NPC 脸部变成类似 AI 修图滤镜效果，认为这是 AI 在游戏领域的滥用，方向完全错误。"
    },
    "https://x.com/tibor_tee/status/2033585136110080324": {
        "title_zh": "产品设计师 Danny 记录了他的 Vibe Coding 游戏开发方法",
        "full_summary": "Tibor 转发推荐产品设计师 Danny Limanseta 关于 vibe coding 游戏开发的实践记录，建议关注评论区的详细链接与说明。"
    },
    "https://x.com/the_davey/status/2033734479383302557": {
        "title_zh": "Roblox 游戏开发 + 插件 + AI + Web3",
        "full_summary": "DaveY 的个人简介推文，聚焦 Roblox 游戏开发、插件制作、AI 应用和 Web3 领域。"
    },
    "https://x.com/TheWzrd/status/2033583385076023689": {
        "title_zh": "Unity 小白用 Cursor 达到这个效果还需要多久？",
        "full_summary": "Tim Harris 询问 Unity 完全新手使用 Cursor 能达到 Danny 展示效果还需多久，并表示正在关注 Unity Agent 模式的发展动态。"
    },
    "https://x.com/the_OPX/status/2033664045589442932": {
        "title_zh": "我的独立游戏跑通了 DLSS 5 预览版，但我更爱像素风",
        "full_summary": "OHMplex 分享在即将发布的独立游戏中成功运行 DLSS 5 预览版，画面效果不错，但个人仍偏爱像素风格和高帧率，对 Nvidia 表示抱歉。"
    },
    "https://x.com/AcayDr/status/2033657056377369003": {
        "title_zh": "GTD第二阶段开放，仅288名玩家，挑战赢取奖励",
        "full_summary": "Vibe Coding Arc 频道的 Dr.Acay 宣布 GTD 第二阶段开放，限288人参与，挑战通关游戏可获奖励，附游戏链接。"
    },
    "https://x.com/Spectromachina/status/2033683192494858267": {
        "title_zh": "开发者掌控 DLSS 5 对游戏的处理方式，别当NPC重复反AI陈词",
        "full_summary": "Spectro 为 DLSS 5 辩护：开发者完全可以控制 AI 增强效果的应用方式，批评某 YouTube 游戏博主不做调研、懒惰地重复反 AI 言论。"
    },
    "https://x.com/Mushey_peas/status/2033742983812555051": {
        "title_zh": "一觉醒来看到AI滤镜和独立开发恐惧症，不是我的菜",
        "full_summary": "推主 Mosh 表达对 AI 游戏滤镜争议和独立游戏开发者被排斥现象的不满，认为这种舆论环境令人不适。"
    },
    "https://x.com/itplaysout/status/2033740370539098536": {
        "title_zh": "韩国用户优化AI算力硬件，说明其游戏开发迭代速度更快",
        "full_summary": "PlaysOut 观察到韩国用户已在为 AI 工作负载优化硬件，认为这正是韩国游戏工作室能更快迭代游戏开发循环的原因。"
    },
    "https://x.com/SofiaSyscoin/status/2033726098698301768": {
        "title_zh": "游戏开发周期5年以上，开发中途如何应对新技术涌现？",
        "full_summary": "推主思考：当游戏开发周期长达5年以上，开发团队如何在开发过程中应对 AI 等新技术的快速迭代？以一款期待已久的游戏为例提出疑问。"
    },
    "https://x.com/ElOso2022/status/2033740113063116917": {
        "title_zh": "《存档点》——战前只有沉默，AI日本艺术家的独立游戏概念图",
        "full_summary": "AI 日本艺术家 Hide 分享独立游戏《The Save Point》的角色设计概念图，主题为战前寂静的武士女孩，风格融合传统与现代 AI 绘画。"
    },
    "https://x.com/ezzgama/status/2033711103524671706": {
        "title_zh": "漂亮，Cursor 模型用得很聪明",
        "full_summary": "koushikr0y 对某位开发者聪明使用 Cursor 模型的方式表示赞赏，简短评论。"
    },
    "https://x.com/DannyLimanseta/status/2033728440533410137": {
        "title_zh": "Godot 开发也不需要 MCP，直接用 Cursor 就行",
        "full_summary": "Danny Limanseta 补充说明：在 Godot 引擎开发中同样无需 Unity MCP，直接使用 Cursor 即可完成开发，与 Unity 经验一致。"
    },
    "https://x.com/Niv005/status/2033727351482372271": {
        "title_zh": "未来市场将全面AI化，独立游戏开发者会越来越稀缺",
        "full_summary": "Niv 预测未来游戏市场将全面 AI 驱动，独立游戏开发者会越来越少，尤其随着无需专用硬件的 AI 工具普及，这一趋势将加速。"
    },
    "https://x.com/JateLIVE/status/2033699442973675583": {
        "title_zh": "AI只是工具，但很多人用得太懒，生成式AI目前弊大于利",
        "full_summary": "JateLIVE 认为 AI 本质上只是工具，但大量人以懒惰方式使用。生成式 AI（非全部 AI）目前在游戏领域弊大于利，但仍有希望走向正途。"
    },
    "https://x.com/FerVeloz_Art/status/2033730350476599786": {
        "title_zh": "停止用AI做视觉垃圾，AI应该用来做NPC行为和进化",
        "full_summary": "Fer Veloz 批评开发者用 AI 制造视觉垃圾，呼吁将 AI 真正用于 NPC 行为设计和动态进化，而非表面美化。"
    },
    "https://x.com/________renan/status/2033670045734232205": {
        "title_zh": "不管是不是AI，她的脸从游戏发售起就不对，DLSS 5反而让她好看了",
        "full_summary": "Renan 表示不在乎某角色是否使用了 AI 增强，该角色从游戏发售就长得奇怪，DLSS 5 反而是本作中让她看起来最好的角色之一。"
    },
    "https://x.com/I_DO_JUEGOS/status/2033636088657465847": {
        "title_zh": "现在需要AI工具修复动画和NPC行为，想象一下真实行为的NPC",
        "full_summary": "YERBO-MALO 呼吁开发真正能修复动画和 NPC 行为的 AI 工具，畅想未来游戏中 NPC 拥有真实行为、独立关系和情感的可能性。"
    },
    "https://x.com/NanoCommando/status/2033293367631573387": {
        "title_zh": "Web3游戏首创：AI NPC DISPENSO能跨整个游戏记住你",
        "full_summary": "Nano Commando 游戏介绍新 AI NPC DISPENSO，能跨游戏记忆玩家信息，不是读取存档式记忆，而是真正记得玩家说过的话和做过的事，Web3游戏领域首创。"
    },
    "https://x.com/FitrianRuli/status/2033665244514377835": {
        "title_zh": "为Canopy帖子生成的高质量引用评论（AI流程自动化）",
        "full_summary": "Ruli 发布一条 AI 自动生成的引用评论，内容关于 Octopus RPA 的 AI 流程写作功能，称其为非程序员构建自动化的游戏规则改变者。（疑似AI生成内容）"
    },
    "https://www.reddit.com/r/gamedev/comments/1rvd4et/4_months_after_our_steam_page_launch_demo_release/": {
        "title_zh": "Steam页面上线4个月后：Demo发布、开发进展与营销数据（第三部分）",
        "full_summary": "独立游戏开发者分享 Steam 页面上线4个月的完整历程，包括 Demo 发布、开发步骤、营销努力与具体数据，是系列游戏开发日记第三篇。"
    },
    "https://www.reddit.com/r/gamedev/comments/1rvdanl/404_games_publisher_contact/": {
        "title_zh": "关于404 GAMES发行商的联系情况说明",
        "full_summary": "独立开发者长期收到 404 GAMES 发行商的联系消息，本帖详细介绍该发行商的背景情况，提醒开发者社区注意。"
    },
    "https://www.reddit.com/r/unrealengine/comments/1rv3b01/57_metahuman_to_maya_plugin_i_dont_know_what_im/": {
        "title_zh": "UE5.7 MetaHuman 导出到 Maya 插件问题求助",
        "full_summary": "开发者按照步骤安装并加载了插件，但在选择 MetaHuman 目录时没有任何内容显示，求助 Unreal Engine 社区解决 MetaHuman 到 Maya 的导出问题。"
    },
    "https://www.reddit.com/r/godot/comments/1rv8sa2/adding_new_towers_to_my_typing_tower_defense_game/": {
        "title_zh": "我的打字塔防游戏新增了新塔，效果如何？",
        "full_summary": "Godot 开发者分享打字塔防游戏《type:def》的最新进展，感谢社区反馈，展示新增塔楼的效果图，邀请玩家评价。"
    },
    "https://www.reddit.com/r/gamedev/comments/1rv7o92/advice_on_learning_how_to_make_games/": {
        "title_zh": "26岁女生转行学游戏开发，求建议",
        "full_summary": "一位26岁女性决定转行学习编程和游戏开发，在 r/gamedev 社区寻求入门建议和学习路径推荐。"
    },
    "https://www.reddit.com/r/Unity3D/comments/1rveg3k/after_4_years_my_physical_ai_system_is_finally/": {
        "title_zh": "历时4年，我的物理AI系统终于达到游戏可用状态",
        "full_summary": "Essential_NPC_ 分享耗时4年开发的物理 AI 系统终于达到游戏可用状态，在 r/Unity3D 社区发布成果展示。"
    },
    "https://www.reddit.com/r/unrealengine/comments/1rvmasj/animating_bolt_action_rifles/": {
        "title_zh": "第三人称射击游戏中栓动步枪的动画制作问题",
        "full_summary": "开发者在制作第三人称射击游戏时遇到栓动步枪动画问题，使用 Unreal Engine 动画系统，寻求社区提供解决方案。"
    },
    "https://www.reddit.com/r/unrealengine/comments/1rvbgj8/are_ccby_assets_completely_useless/": {
        "title_zh": "CC-BY 授权资产在 Steam 上是否完全没用？",
        "full_summary": "CC-BY 资产要求在游戏内署名，但 Steam 不允许链接到 FAB 等其他商店页面，开发者探讨这一限制是否导致 CC-BY 资产在 Steam 发行中完全无法使用。"
    },
    "https://www.reddit.com/r/gamedev/comments/1rv6bwm/are_there_any_downsides_to_releasing_steam_store/": {
        "title_zh": "Steam 商店页面早期上线有什么缺点吗？",
        "full_summary": "开发者询问在游戏原型阶段就上线 Steam 即将推出页面是否存在缺点，探讨早期曝光策略的利弊。"
    },
    "https://www.reddit.com/r/unrealengine/comments/1rv0z5k/are_there_any_tutorials_on_how_to_setup/": {
        "title_zh": "Chaos 车辆系统球形射线检测设置教程求推荐",
        "full_summary": "开发者发现 Chaos 车辆使用射线检测判断轮子高度，在非平坦赛道上效果不佳，寻求球形射线检测的设置教程以改善越野效果。"
    },
    "https://www.reddit.com/r/unrealengine/comments/1rv495f/blender_animation_looks_different_when_imported/": {
        "title_zh": "Blender 动画导入 Unreal 后效果不同的问题",
        "full_summary": "开发者制作了仅移动臀部、四肢通过 IK 保持不动的动画，但导入 Unreal 后脚部位置发生漂移，寻求解决 Blender 到 UE 动画导入差异的方法。"
    },
    "https://www.reddit.com/r/godot/comments/1rvayeh/bouncing_floor/": {
        "title_zh": "弹弹地板！Godot 物理效果演示",
        "full_summary": "开发者 Lucky_Ferret4036 应社区要求实现了弹跳地板效果，地板会弹动，在 r/godot 分享这个有趣的物理效果演示。"
    },
    "https://www.reddit.com/r/Unity3D/comments/1rvbduk/built_a_ui_builder_inside_unity_drag_templates/": {
        "title_zh": "Unity 内置UI构建器：拖拽模板、连接按钮、运行时编辑C#无需重新编译",
        "full_summary": "开发者展示 Smart Editor Suite 工具集中的 UI 构建器模块，支持在 Unity 运行模式下拖拽 UI 模板、连接按钮事件、实时编辑 C# 代码且无需重新编译。"
    },
    "https://www.reddit.com/r/Unity3D/comments/1rvd55w/camera_toolbox_for_unity_old_film_effects/": {
        "title_zh": "Unity 相机工具箱新增老电影特效",
        "full_summary": "开发者为 Unity 相机工具箱新增复古电影效果：棕褐色调模式、简单屏幕模糊、胶片颗粒等，分享最新版本更新内容。"
    },
    "https://www.reddit.com/r/gamedev/comments/1rvuz9p/card_game_data_driven_architecuture/": {
        "title_zh": "卡牌游戏数据驱动架构设计求建议",
        "full_summary": "一位有多年非游戏开发经验的程序员决定开始做游戏，在设计卡牌游戏的数据驱动架构时寻求社区建议和最佳实践。"
    },
    "https://news.ycombinator.com/item?id=47405937": {
        "title_zh": "问HN：重新考虑Vibe Coding这个名字还来得及吗？",
        "full_summary": "HN 用户发起讨论，质疑 Vibe Coding 这个名称是否合适，探讨这一新兴编程范式的命名问题。"
    },
    "https://www.businessinsider.com/vibe-coding-becoming-a-real-job-startups-entrepreneurship-2026-3": {
        "title_zh": "Vibe Coding 已成为一份真实的工作",
        "full_summary": "Business Insider 报道：Vibe Coding 正从概念变为真实职位，初创公司开始招聘以 AI 辅助编程为核心技能的开发者，这一编程范式正在重塑软件行业就业市场。"
    },
    "https://lawsofux.com/": {
        "title_zh": "UX 设计法则——在 AI Vibe Coding 时代的意义",
        "full_summary": "HN 讨论 AI Vibe Coding 时代下 UX 设计法则的重要性，探讨当 AI 能快速生成界面时，人类设计原则是否依然适用。"
    },
    "https://github.com/htdt/godogen": {
        "title_zh": "Show HN: Claude Code Skills 自动构建完整 Godot 游戏",
        "full_summary": "Godogen 开源项目：通过 Claude Code Skills 实现从纯文本提示词到完整 Godot 游戏的全自动生成流水线，自动完成架构设计、代码编写和游戏组装，获191票和122条评论，是本期 HN 最热门的 AI 游戏开发项目。"
    },
    "https://futuresearch.ai/blog/mcp-leaks-docker-containers/": {
        "title_zh": "Claude Code 的 MCP 配置可能悄悄产生孤立的 Docker 容器",
        "full_summary": "FutureSearch 博客披露：Claude Code 的 MCP 配置存在问题，可能在用户不知情的情况下产生孤立的 Docker 容器，造成资源泄漏，需要开发者注意清理。"
    },
    "https://signb.ee": {
        "title_zh": "Show HN: Signbee — 让 AI Agent 发送文件签名请求的 API",
        "full_summary": "Signbee 推出专为 AI Agent 设计的电子签名 API，允许 AI 自动发起文件签名流程，简化合同和文档签署的自动化工作流。"
    },
    "https://discoverbsd.com/p/8a7660c31b": {
        "title_zh": "FreeBSD 若忽视 Claude Code 等 AI 工具将面临边缘化风险",
        "full_summary": "DiscoverBSD 文章警告：FreeBSD 若继续忽视 Claude Code 等 AI 编程工具的支持，将面临在开发者社区中逐渐边缘化的风险，建议尽快跟进 AI 工具生态。"
    },
    "https://news.ycombinator.com/item?id=47402125": {
        "title_zh": "Show HN: 用持久化 Markdown 文件解决 Claude Code 的上下文漂移问题",
        "full_summary": "开发者分享用结构化 Markdown 文件作为持久记忆的方案，解决 Claude Code 长对话中上下文漂移导致的遗忘问题，获 HN 社区讨论。"
    },
    "https://github.com/RA1NCS/svelte-lsp": {
        "title_zh": "Show HN: 为 Claude Code 的 .svelte 文件提供完整 LSP 智能支持的插件",
        "full_summary": "开发者发布 Claude Code 插件，为 Svelte 文件提供完整的语言服务器协议（LSP）智能支持，包括代码补全、类型检查等功能。"
    },
    "https://github.com/marciopuga/cog": {
        "title_zh": "Cog — 基于 Markdown 文件的 Claude Code 认知架构",
        "full_summary": "Cog 是一个轻量级认知架构框架，完全基于 Markdown 文件为 Claude Code 提供持久记忆、任务跟踪和上下文管理能力，零依赖。"
    },
    "https://github.com/getpaseo/paseo": {
        "title_zh": "Show HN: Paseo — 从手机、桌面或终端运行 Coding Agent（开源）",
        "full_summary": "Paseo 是开源的跨平台 Coding Agent 运行器，支持从手机、桌面或终端启动和管理 AI 编程 Agent，降低 AI 辅助开发的使用门槛。"
    },
    "https://www.devsecai.io/": {
        "title_zh": "Show HN: Arko — 在 Cursor 和 VS Code 中实时 AI 威胁建模",
        "full_summary": "Arko 是集成在 Cursor 和 VS Code 中的实时 AI 安全威胁建模工具，在编码过程中自动识别安全风险，将安全分析融入日常开发工作流。"
    },
    "https://hyper.ai/cn/notebooks/49873": {
        "title_zh": "Show HN: 在 HyperAI 上运行热门 LLM-Course 教程",
        "full_summary": "HyperAI 平台提供一键运行热门大模型课程教程的功能，降低 LLM 学习门槛，用户无需本地配置即可运行完整的 AI 课程实验环境。"
    },
    "https://github.com/aiwebb/llmonster-rancher": {
        "title_zh": "Show HN: LLMonster Rancher — 多LLM实例管理工具",
        "full_summary": "LLMonster Rancher 是一个管理和调度多个大语言模型实例的工具，帮助开发者像管理牧场一样统一管理多个 LLM 服务。"
    },
    "https://github.com/aklos/scryer": {
        "title_zh": "Show HN: Scryer — AI Agent 的可视化架构建模工具",
        "full_summary": "Scryer 提供可视化界面用于建模 AI Agent 的系统架构，帮助开发者直观设计和理解复杂的多 Agent 系统结构。"
    },
    "https://dev.to/hamed_farag/i-built-a-browser-ui-for-claude-code-heres-why-4959": {
        "title_zh": "我为 Claude Code 构建了一个浏览器 UI，原因如下",
        "full_summary": "开发者使用 Claude Code 数月后，在终端优先模式下发现了一些痛点，决定自建浏览器端 UI 界面，分享了构建动机、设计思路和实现细节，获17个点赞。"
    },
    "https://dev.to/dannwaneri/beyond-the-scrapbook-building-a-developer-knowledge-commons-4d40": {
        "title_zh": "超越剪贴簿：构建开发者知识公共库",
        "full_summary": "DEV.to 上线了 Agent Sessions 测试功能，允许上传 Claude Code 会话记录。作者探讨如何将这些碎片化的 AI 编程经验沉淀为可共享的开发者知识公共库。"
    },
    "https://dev.to/mecanik/i-built-a-desktop-cobol-migration-tool-that-converts-to-6-modern-languages-2337": {
        "title_zh": "我构建了一个桌面 COBOL 迁移工具，支持转换为6种现代语言",
        "full_summary": "COBOL 迁移是当前企业技术热点，开发者受 Anthropic Claude Code 博文启发，构建了一款桌面工具，可将 COBOL 代码自动转换为6种现代编程语言。"
    },
    "https://dev.to/hugo662/claude-code-vs-cursor-what-i-learned-using-both-for-30-days-17en": {
        "title_zh": "Claude Code vs Cursor：连续使用30天后的对比心得",
        "full_summary": "开发者将 Claude Code 和 Cursor 作为主力 AI 编程工具各使用30天，从实际项目角度深度对比两款工具的优劣势，提供选型参考。"
    },
    "https://dev.to/hugo662/how-i-set-up-claude-code-to-run-my-entire-dev-workflow-3jcp": {
        "title_zh": "我如何配置 Claude Code 来驱动整个开发工作流",
        "full_summary": "开发者分享将 Claude Code 作为主力开发工具数月后的完整配置方案，介绍如何让 Claude Code 接管从代码编写到测试部署的全流程开发工作。"
    },
    "https://dev.to/stelixx-insider/claude-code-agentic-coding-tool-for-terminal-89m": {
        "title_zh": "Claude Code：面向终端的 Agentic 编程工具",
        "full_summary": "介绍 Claude Code 作为终端 Agentic 编程工具的核心特性，探讨其在不断演进的 AI 辅助开发领域中的定位与优势。"
    },
    "https://simonwillison.net/2026/Mar/16/mistral-small-4/#atom-everything": {
        "title_zh": "Mistral Small 4 发布",
        "full_summary": "Mistral 发布 Small 4 新模型，Simon Willison 进行解读分析，这是 Mistral 本次发布的重要里程碑。"
    },
    "https://simonwillison.net/2026/Mar/16/codex-subagents/#atom-everything": {
        "title_zh": "Codex 支持子 Agent 和自定义 Agent",
        "full_summary": "OpenAI Codex 宣布支持子 Agent 和自定义 Agent 功能，Simon Willison 记录这一重要更新，扩展了 Codex 的多 Agent 协作能力。"
    },
    "https://simonwillison.net/2026/Mar/16/blackmail/#atom-everything": {
        "title_zh": "引用 Anthropic 对齐科学团队成员的言论",
        "full_summary": "Simon Willison 引用 Anthropic 对齐科学团队成员关于五角大楼与 Anthropic 博弈的相关言论，涉及 AI 安全与军事应用的核心争议。"
    },
    "https://simonwillison.net/2026/Mar/16/coding-agents-for-data-analysis/#atom-everything": {
        "title_zh": "用于数据分析的 Coding Agent",
        "full_summary": "Simon Willison 为 NICAR 2026 会议准备的讲义，介绍如何将 Coding Agent 应用于数据分析场景，提供实用的操作指南。"
    },
    "https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/#atom-everything": {
        "title_zh": "Coding Agent 的工作原理",
        "full_summary": "Simon Willison《Agentic Engineering Patterns》系列文章，深入解析 Coding Agent 的底层工作机制，帮助开发者理解 AI 编程 Agent 的技术原理。"
    },
    "https://github.com/anomalyco/opencode": {
        "title_zh": "anomalyco/opencode — 开源 Coding Agent",
        "full_summary": "opencode 是开源的 Coding Agent 平台，TypeScript 构建，GitHub 标星超12万，是目前最热门的开源 AI 编程 Agent 项目之一。"
    },
    "https://github.com/affaan-m/everything-claude-code": {
        "title_zh": "affaan-m/everything-claude-code — Agent Harness 性能优化系统",
        "full_summary": "集成 Skills、直觉、记忆、会话管理的 Claude Code Agent Harness 性能优化系统，JavaScript 构建，标星超8万，提供全方位的 Claude Code 增强能力。"
    },
    "https://github.com/anthropics/claude-code": {
        "title_zh": "anthropics/claude-code — 终端 Agentic 编程工具官方仓库",
        "full_summary": "Anthropic 官方 Claude Code 仓库，终端原生的 Agentic 编程工具，能理解代码库并通过自然语言执行复杂编程任务，标星超7.8万。"
    },
    "https://github.com/openai/codex": {
        "title_zh": "openai/codex — 终端轻量级 Coding Agent",
        "full_summary": "OpenAI 官方 Codex 仓库，Rust 构建的轻量级终端 Coding Agent，标星超6.5万，与 Claude Code 并列为最热门的终端 AI 编程 Agent。"
    },
    "https://github.com/farion1231/cc-switch": {
        "title_zh": "farion1231/cc-switch — Claude Code/Codex/OpenClaw 跨平台桌面全能助手",
        "full_summary": "cc-switch 是 Rust 构建的跨平台桌面工具，整合 Claude Code、Codex、OpenClaw 等主流 AI 编程工具，提供统一的 All-in-One 管理界面，标星超2.9万。"
    },
    "https://github.com/BloopAI/vibe-kanban": {
        "title_zh": "BloopAI/vibe-kanban — 让 Claude Code/Codex 效率提升10倍的看板工具",
        "full_summary": "vibe-kanban 是 Rust 构建的项目管理看板，专为 Claude Code、Codex 等 Coding Agent 设计，通过可视化任务管理让 AI 编程效率提升10倍，标星超2.3万。"
    },
    "https://github.com/davila7/claude-code-templates": {
        "title_zh": "davila7/claude-code-templates — Claude Code 配置与监控 CLI 工具",
        "full_summary": "Python 构建的 CLI 工具，提供 Claude Code 的配置模板管理和运行监控功能，帮助开发者快速配置和维护 Claude Code 工作环境，标星超2.3万。"
    },
    "https://github.com/iOfficeAI/AionUi": {
        "title_zh": "iOfficeAI/AionUi — 免费本地开源的 Gemini CLI/Claude Code 全天候协作应用",
        "full_summary": "AionUi 是免费、本地运行的开源 AI 协作应用，支持 Gemini CLI、Claude Code 等多个 AI 编程工具，提供7x24小时持续工作能力，TypeScript 构建，标星超1.9万。"
    },
    "https://github.com/router-for-me/CLIProxyAPI": {
        "title_zh": "router-for-me/CLIProxyAPI — 将 Gemini CLI/Claude Code/Codex 等封装为统一 API",
        "full_summary": "CLIProxyAPI 用 Go 构建，将 Gemini CLI、Claude Code、ChatGPT Codex、Qwen Code 等多个 CLI 工具统一封装为标准 API 接口，方便集成到各类工作流，标星超1.7万。"
    },
    "https://github.com/Kilo-Org/kilocode": {
        "title_zh": "Kilo-Org/kilocode — 一体化 Agentic 工程平台，快速构建和迭代",
        "full_summary": "Kilo 是 TypeScript 构建的全能 Agentic 工程平台，整合构建、发布和迭代能力，标星超1.6万，定位为 AI 时代的一站式工程开发解决方案。"
    },
    "https://github.com/coleam00/context-engineering-intro": {
        "title_zh": "coleam00/context-engineering-intro — 上下文工程才是真正让AI可靠工作的新Vibe Coding",
        "full_summary": "上下文工程（Context Engineering）是让 AI Coding Agent 真正可靠工作的核心方法，Python 构建，标星超1.2万，提供系统化的上下文管理入门指南。"
    },
    "https://github.com/liyupi/ai-guide": {
        "title_zh": "程序员鱼皮的 AI 资源大全 + Vibe Coding 零基础教程",
        "full_summary": "鱼皮整理的 AI 资源大全，涵盖大模型选择指南（DeepSeek/GPT/Gemini/Claude）、Vibe Coding 零基础教程，JavaScript 构建，标星超9700，是中文开发者社区最受欢迎的 AI 学习资源之一。"
    },
    "https://github.com/superset-sh/superset": {
        "title_zh": "superset-sh/superset — AI Agent 时代的 IDE，并行运行多个 Claude Code/Codex",
        "full_summary": "Superset 是专为 AI Agent 时代设计的 IDE，支持在同一台机器上并行运行 Claude Code、Codex 等多个 AI Agent，TypeScript 构建，标星超7200。"
    },
    "https://github.com/Godot4-Addons/ai_assistant_for_godot": {
        "title_zh": "Godot4-Addons/ai_assistant_for_godot — Godot 4 AI 编程助手插件",
        "full_summary": "GDScript 构建的 Godot 4 AI 编程助手插件，直接在 Godot 编辑器内集成 AI 代码辅助能力，标星21，是 Godot AI 开发生态的实用工具。"
    },
    "https://github.com/snougo/Godot-AI-Chat": {
        "title_zh": "snougo/Godot-AI-Chat — 在 Godot 编辑器内直接与 LLM 对话的插件",
        "full_summary": "Godot AI Chat 是 GDScript 构建的 Godot 插件，让开发者无需离开编辑器即可与大语言模型直接对话，标星13，适合需要 AI 辅助的 Godot 开发者。"
    },
}

with open('/Users/dada/vibe-coding-digest/digest_2026-03-17_raw.json', 'r') as f:
    data = json.load(f)

def apply_translations(items, translations):
    for item in items:
        url = item.get('url', '')
        if url in translations:
            t = translations[url]
            if 'title_zh' in t and not item.get('title_zh'):
                item['title_zh'] = t['title_zh']
            if 'full_summary' in t and not item.get('full_summary'):
                item['full_summary'] = t['full_summary']
    return items

data['m1'] = apply_translations(data['m1'], translations)
data['m2'] = apply_translations(data['m2'], translations)

with open('/Users/dada/vibe-coding-digest/digest_2026-03-17_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

m1_with_summary = sum(1 for item in data['m1'] if item.get('full_summary'))
m2_with_summary = sum(1 for item in data['m2'] if item.get('full_summary'))
print(f'M1 有摘要: {m1_with_summary}/{len(data["m1"])}')
print(f'M2 有摘要: {m2_with_summary}/{len(data["m2"])}')
print('翻译写入完成！')

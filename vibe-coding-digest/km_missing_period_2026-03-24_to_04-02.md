# 📚 KM 缺失期补录：AI + 游戏模块
> **缺失原因**：2026-03-24 / 03-26 / 03-28 / 03-31 / 04-02 共 5 天，KM MCP 工具因 Knot 本地 Agent 断连或 KM 服务不可用，导致日报未能抓取 KM 数据。
>
> **覆盖时间**：2026-03-24（周二）~ 2026-04-02（周四），共 10 天
>
> **本文收录**：AI + 游戏 / AI Coding 相关 KM 文章，按发布时间倒序排列
>
> **生成时间**：2026-04-08

---

## 🎮 AI + 游戏实践

---

#### [鹅厂游戏AI应用亮相！闪现美国湾区，揭秘GAME AI全景实践｜GDC](https://km.woa.com/articles/show/655929?jumpfrom=kmmcp)

> 📚 KM | 作者: yiruifeng | 阅读: 1972 | 热度: 760 | 标签: IEG · GDC · 游戏 · AI · 技术 | 2026-03-27

腾讯IEG游戏AI应用团队亲赴GDC（游戏开发者大会），在美国湾区展示了腾讯游戏AI的全景实践成果。文章以"游戏AI的实践主义"为主题，记录了出海游戏在AI技术应用上的真实探索——不追风口、不搞噱头，而是从玩家体验出发，将AI能力落地到游戏的核心玩法、内容生成和运营环节中。

---

#### [全球AI风暴下，我在GDC看到游戏行业的答案](https://km.woa.com/articles/show/656003?jumpfrom=kmmcp)

> 📚 KM | 作者: leahqiu / djdeng | 阅读: 69 | 热度: 57 | 标签: AI · 游戏 · GDC | 2026-03-27

作者亲赴GDC，在全球AI浪潮席卷游戏行业的背景下，记录了来自一线开发者的真实声音与应对策略。核心观点：**能定义游戏的，唯有游戏本身**——AI是工具，游戏性才是本质。文章观察了大厂与独立开发者在AI应用上的不同路径，以及游戏行业对AI的理性态度与边界判断。

---

#### [游戏行业没有AI的FOMO病](https://km.woa.com/articles/show/655966?jumpfrom=kmmcp)

> 📚 KM | 作者: djdeng / leahqiu | 阅读: 65 | 热度: 47 | 标签: AI · 游戏 · GDC | 2026-03-27

与"AI恐慌"相反，作者在GDC观察到游戏行业对AI整体保持理性克制——没有FOMO（错失恐惧症）。游戏开发者更关注的是：AI在哪些具体环节真正有用？在哪些地方会破坏游戏体验？文章提供了一个冷静的行业视角，适合对游戏×AI持长期主义思考的读者。

---

#### [CodeWiki，为游戏业务量身打造AI代码知识库！](https://km.woa.com/articles/show/656460?jumpfrom=kmmcp)

> 📚 KM | 作者: yizhangpeng | 阅读: 1967 | 热度: 1811 | 标签: SVN · 知识库 · AI · codewiki | 2026-04-02

CodeWiki 是专门为游戏研发团队打造的 AI 代码知识库工具，近期解决了两大核心痛点：

1. **SVN 项目场景**：游戏项目普遍使用 SVN 管理大型资产，CodeWiki 实现了对 SVN 仓库的智能索引与问答，开发者可直接用自然语言查询代码逻辑；
2. **UE 引擎学习场景**：针对 Unreal Engine 庞大的代码体量，CodeWiki 构建了专属知识库，大幅降低新人上手 UE 的学习成本。

该工具热度高达 1811，是本期 KM 热度最高的游戏相关文章。

---

#### [【技术学堂】PUBGM游戏智能AI伙伴PowNin的技术方案实践分享](https://km.woa.com/articles/show/656363?jumpfrom=kmmcp)

> 📚 KM | 作者: v_huihlili | 阅读: 94 | 热度: 85 | 标签: PUBG Mobile | 2026-04-01 | 📂 TEG学习互动社区

PUBG Mobile（绝地求生：大逃杀）团队分享了游戏内智能AI伙伴「PowNin」的完整技术方案。内容涵盖：AI伙伴的行为决策架构、与游戏引擎的集成方式、玩家交互设计，以及在大规模在线游戏环境下的性能优化策略。是少数来自腾讯游戏一线产品的 AI NPC 技术实践案例。

---

## 🎮 AI Coding / Vibe Coding 实践

---

#### [NTCompose Vibe Coding 不再盲写：让 AI 看见真机日志的 Harness Engineering 实践](https://km.woa.com/articles/show/656478?jumpfrom=kmmcp) ⭐KM推荐 🔥头条

> 📚 KM | 作者: veontang | 阅读: 175 | 热度: 159 | 标签: AI · Kuikly · NTCompose · Harness | 2026-04-02 | 📂 腾讯VATeam

AI 能写代码、能改代码，但在客户端开发调试时**看不到设备日志**——只能靠猜。这篇文章记录了如何通过设计多 Agent 分工、约束规则和反馈循环，经过 **8 轮迭代**做出了一个双平台（iOS/Android）实时日志采集 Skill，让 AI 从"盲写"变成根据真实运行数据来写代码。

核心方法论：
- **多 Agent 分工**：日志采集 Agent、代码生成 Agent、验证 Agent 各司其职
- **反馈闭环**：AI 写完代码 → 真机运行 → 日志回传 → AI 根据日志修正
- **Harness Engineering**：用约束规则防止 AI 在复杂客户端场景中"跑偏"

---

#### [不会写代码的我，用 Vibe Coding 把简历做成了网站（附保姆级搭建教程）](https://km.woa.com/articles/show/655891?jumpfrom=kmmcp)

> 📚 KM | 作者: joeyyyzhou | 阅读: 959 | 热度: 797 | 标签: Vibe Coding · 个人网站 · AI | 2026-03-26 | 📂 腾讯知点

零代码基础的作者，用几个下班后的晚上和 AI 对话，做出了一个个人简历网站。域名成本：8 块钱。全程没写一行代码。

文章详细记录了：选择哪个 AI 工具（Cursor/Claude）、如何描述需求、踩过哪些坑（部署、域名、样式问题）、以及对 Vibe Coding 的深度思考——**AI 降低了创作门槛，但提升了对"想清楚要什么"的要求**。附完整保姆级搭建教程，适合零基础读者参考。

---

#### [CDB AI 编程实践：0 Writing 驱动的 0 Coding 工作流](https://km.woa.com/articles/show/655909?jumpfrom=kmmcp)

> 📚 KM | 作者: marchzcma | 阅读: 37 | 热度: 19 | 标签: 编程 · 工作流 · AI | 2026-03-26

大家都在谈 AI coding，但真正的 0 coding 从未实现——因为**写代码的工作量只是换了个形式，变成了写文档的工作量**。

作者提出核心观点：**0 coding 的前提是 0 writing**。人的职责不是生产文档，而是产生意图；AI 负责将口语描述转化为结构化需求单、自动编码、同步知识库，信息在 AI 内部流转，不再经过人。

以 CDB 团队实践为例，通过 KnotClaw/WorkBuddy 两个 Agent 平台，结合覆盖需求录入、开发编排、代码规范、数据查询的专属 Skill 体系，将整个开发链路压缩为人工只需参与 **6 个节点**、其余全程由 AI 自驱完成的工作流。

---

#### [使用 codebuddy 纯 vibe coding 实现个人智能运维助手](https://km.woa.com/articles/show/655977?jumpfrom=kmmcp)

> 📚 KM | 作者: zeyangning | 阅读: 44 | 热度: 46 | 标签: AI Agent · eBPF · ReAct · SRE | 2026-03-27

完全用 Vibe Coding 方式（CodeBuddy + 自然语言描述），实现了一个功能完整的个人智能运维助手。技术亮点：

- **ReAct 多轮推理引擎**：驱动 Agent 自主思考与行动，支持"观察-思考-行动"循环
- **eBPF 内核追踪**：深入 Linux 系统底层，实现精准性能诊断
- **MCP 协议**：实现工具层解耦，方便扩展新诊断能力
- **向量知识库 + 长期记忆**：让诊断能力持续进化，不只是一次性工具

支持自动执行、人工确认、Copilot 协作三种交互模式，并通过 Web API 和 A2A 双协议对外提供服务。

---

#### [从 TAPD 到 MR：基于 VibeFlow 的 AI Coding 实践](https://km.woa.com/articles/show/656004?jumpfrom=kmmcp)

> 📚 KM | 作者: jinglezheng | 阅读: 153 | 热度: 113 | 标签: AI · TAPD · Coding | 2026-03-27 | 📂 腾讯广告研效

基于 VibeFlow 框架，探索从 TAPD 需求单到 MR（Merge Request）的全链路 AI Coding 实践。将 AI 介入点从"写代码"前移到"理解需求"阶段，实现需求拆解、代码生成、自动提交 MR 的一体化流程。

---

#### [AI 编程技术助力工作提效分享 —— Harness Engineering：从「感觉对了就行」到「在约束中全力奔跑」](https://km.woa.com/articles/show/655678?jumpfrom=kmmcp)

> 📚 KM | 作者: williamliao | 阅读: 97 | 热度: 54 | 标签: AICode · Harness · speckit | 2026-03-24

在 AI 编程工具爆发的今天，大多数开发者仍停留在「感觉对了就行」的 Vibe Coding 阶段——凭直觉提问、靠运气得到结果、用大量时间返工修正。AI 写出来的代码，像一匹没有缰绳的马：**跑得快，但方向不可控**。

本文分享一套经过实践验证的 AI 编程提效方法论，从角色锁定、思维链激活，到规格驱动开发（SDD）、Harness Engineering，系统性探讨如何为 AI 建立约束体系。文章里有可以直接跑的命令和代码。

---

#### [Vibe Coding 时代，研发内部汇报从 PPT 走向 HTML：我的实践判断](https://km.woa.com/articles/show/655651?jumpfrom=kmmcp)

> 📚 KM | 作者: houxiangcai | 阅读: 369 | 热度: 73 | 标签: AI · PPT · Vibe Coding · 可视化 | 2026-03-24 | 📂 腾讯云 CODING

当 AI 已显著降低了页面、图表和结构化可视化的生成与修改成本，HTML 在大多数内部项目汇报场景里已比 PPT 更适合作为默认呈现载体。

作者结合真实案例，重点讨论三个问题：
1. 为什么这个变化现在值得重新讨论（AI 降低了 HTML 制作成本）；
2. HTML 相比 PPT 的具体优势和边界（信息承载、后续修改、迭代、归档）；
3. 哪些内部场景适合优先采用 HTML，哪些场景仍然更适合保留 PPT。

---

## 🤖 AI Agent / Coding 通用（游戏相关性较弱，仅供参考）

---

#### [从 Claude Code 泄露源码看 Harness 设计哲学](https://km.woa.com/articles/show/656428?jumpfrom=kmmcp) ⭐KM推荐 🔥头条

> 📚 KM | 作者: charrli | 阅读: 3443 | 热度: 1483 | 2026-04-01 | 📂 CSIG质量部

基于 Claude Code CLI 泄漏的 512K 源码进行系统性架构拆解，配置 15 张手绘风格可视化图，带你从全景到细节，层层剥开这个工业级 AI Agent 的内核。

---

#### [从 Vibe Coding 到 Harness Engineering：AI 编程的三次范式跃迁](https://km.woa.com/articles/show/656308?jumpfrom=kmmcp)

> 📚 KM | 作者: luiszhu | 阅读: 113 | 热度: 97 | 2026-04-01 | 📂 数立方

AI 编程正在经历三次范式跃迁：从"自然语言写代码"的 **Vibe Coding**，到"结构化规格驱动"的 **Spec Coding**，再到"工程化驾驭 AI"的 **Harness Engineering**。当你理解了这条演进路径，就能找到在不同场景下驾驭 AI 的最优解。

---

#### [让 6 个 AI Agent 连写 4 天代码：4 亿 token 买来的 5 个教训](https://km.woa.com/articles/show/655612?jumpfrom=kmmcp)

> 📚 KM | 作者: raineywu | 阅读: 264 | 热度: 21 | 2026-03-24 | 📂 微信支付研发团队

6 个 AI Agent 组成开发团队，无人值守运行 4 天，迭代 13 个版本，烧掉 **4.2 亿 token**。测试用例从 50 涨到 218，18 个模块自动合入 master。这篇文章不讲代码，聊的是 5 个被真实故障逼出来的教训。

---

*本文档由 Knot AI 助手于 2026-04-08 补录生成，覆盖 KM MCP 不可用期间（2026-03-24 ~ 2026-04-02）的 AI+游戏相关文章。*

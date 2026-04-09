# Vibe Coding 每日资讯工作流 v0.5

> 最后更新：2026-03-12
> 负责人：seanyyao

---

## 🗺️ 整体流程

```
每天 11:00 自动触发
       ↓
  ┌─────────────────────────────────┐
  │  模块一：【AI + 游戏】           │
  │  严格按平台顺序穷尽抓取           │
  └─────────────────────────────────┘
       ↓
  ┌─────────────────────────────────┐
  │  模块二：【AI 通用】             │
  │  多渠道综合抓取                  │
  └─────────────────────────────────┘
       ↓
  过滤 & 去重
       ↓
  Claude Sonnet 4.6 翻译 & 摘要
       ↓
  Markdown 报告生成
       ↓
  企业微信推送
```

---

## 模块一：【AI + 游戏】

> **定义**：只搜索「游戏开发」分类下的 AI 相关资讯。
> 包括：AI/Vibe Coding 在游戏开发中的应用、行业内最新技术、工具使用 Tips、开发者经验分享。
> 覆盖引擎：**Unreal Engine / Unity / Godot**（三个均需覆盖）

### 平台搜索顺序（严格执行，不可跳过）

| 顺序 | 平台 | 语言策略 | 覆盖要求 | 状态 |
|------|------|----------|----------|------|
| **1** | 🏢 **KM（腾讯内部）** | 🇨🇳 中文为主 + 英文补充 | ⚠️ **穷尽** 24h | ✅ 可用 |
| **2** | 💬 **微信公众号** | 🇨🇳 中文为主 + 英文补充 | ⚠️ **穷尽** 24h | ✅ 运行中（搜狗微信搜索）|
| **3** | 🐦 **X (Twitter)** | 🌐 英文为主 + 中文补充 | ⚠️ **穷尽** 24h | ✅ 运行中（Playwright + Cookie）|
| **4** | 🤖 **Reddit** | 🌐 纯英文 | 尽量抓取 | ✅ 运行中（RSS Feed）|
| **5** | 📰 **HackerNews** | 🌐 纯英文 | 关键词过滤 | ✅ 运行中 |
| **6** | 📝 **Dev.to** | 🌐 纯英文 | 关键词过滤 | ✅ 运行中 |
| **7** | 📡 **RSS 聚合** | 🇨🇳/🌐 按来源区分 | 关键词过滤 | ✅ 运行中 |
| **8** | 🚀 **ProductHunt** | 🌐 纯英文 | 关键词过滤 | ✅ 运行中 |
| **9** | ⭐ **GitHub Trending** | 🌐 纯英文 | 关键词过滤，放最后 | ✅ 运行中 |

> 💡 **关键原则**：平台 1-3（KM / 微信公众号 / X）必须**穷尽**过去 24 小时内所有相关资讯，不得遗漏。平台 4-9 按关键词过滤即可。

---

## 🌐 按平台的关键词语言策略（v0.5 新增）

> 核心原则：**国内平台用中文+英文双语；国外平台优先英文；X 英文为主、中文补充（有中文用户群）**

---

### 平台 1：KM（中文为主 + 英文补充）

KM 是腾讯内部中文平台，作者以中文写作为主，但技术词汇（引擎名、工具名）常直接用英文。

```python
KEYWORDS_KM_MODULE1 = {
    "zh": [
        # 游戏引擎 × AI
        "游戏开发 AI", "AI 游戏开发", "游戏 AI 编程",
        "Unity AI", "Unity 人工智能", "Unity 智能编程",
        "Unreal AI", "UE5 AI", "虚幻引擎 AI",
        "Godot AI",
        # Vibe Coding / AI Coding 中文叫法
        "vibe coding", "AI 编程", "AI 辅助开发", "AI 辅助游戏开发",
        "智能编程", "AI 代码生成",
        # 工具名（中英混用）
        "Cursor 游戏", "Cursor Unity", "Cursor Unreal",
        "Claude 游戏开发", "Copilot 游戏",
        # 经验/教程类
        "游戏开发经验", "独立游戏 AI", "游戏开发 tips",
        "AI NPC", "程序化生成 AI",
    ],
    "en": [
        # 英文技术词补充（中文平台也会出现）
        "vibe coding game", "ai game development",
        "unity cursor", "unreal cursor", "godot cursor",
        "unity copilot", "unreal copilot",
        "llm game", "ai gamedev",
    ]
}
```

---

### 平台 2：微信公众号（中文为主 + 英文补充）

微信公众号以中文内容为主，但 AI 工具名称（Cursor/Claude/Copilot）通常直接用英文。

```python
KEYWORDS_WECHAT_MODULE1 = {
    "zh": [
        # 游戏开发 × AI
        "游戏开发 AI", "AI 游戏", "AI 游戏开发",
        "游戏 AI 工具", "游戏编程 AI",
        "Unity AI", "Unity 人工智能",
        "Unreal AI", "UE5 AI", "虚幻引擎 AI",
        "Godot AI",
        # Vibe Coding
        "vibe coding", "AI 编程助手", "AI 辅助编程",
        "AI 代码", "智能编程工具",
        # 工具名
        "Cursor 教程", "Cursor 使用", "Cursor 游戏",
        "Claude 编程", "Copilot 使用",
        # 独立游戏
        "独立游戏 AI", "独立游戏开发", "indie game AI",
        # 经验分享
        "游戏开发经验", "游戏开发 tips", "AI NPC 开发",
    ],
    "en": [
        "vibe coding", "cursor game", "claude game dev",
        "unity ai", "unreal ai", "godot ai",
        "ai game development",
    ]
}
```

---

### 平台 3：X / Twitter（英文为主 + 中文补充）

X 以英文用户为主，但有活跃的中文游戏开发者社区，需要兼顾。

```python
KEYWORDS_X_MODULE1 = {
    "en": [
        # 核心交叉词（优先搜索）
        "vibe coding game", "vibe coding unity", "vibe coding unreal", "vibe coding godot",
        "ai game dev", "ai game development", "ai gamedev",
        "cursor unity", "cursor unreal", "cursor godot",
        "claude unity", "claude unreal", "claude godot",
        "copilot unity", "copilot unreal", "copilot godot",
        "llm game dev", "llm unity", "llm unreal", "llm godot",
        # 工作流 & 经验
        "ai game workflow", "ai indie game", "ai npc",
        "game dev ai tips", "ai assisted game dev",
        "procedural generation ai",
        # hashtag 搜索
        "#vibecoding game", "#gamedev AI", "#indiedev AI",
        "#unity AI", "#unrealengine AI", "#godot AI",
        "#AIgamedev", "#vibecoding unity",
    ],
    "zh": [
        # 中文补充（X 上的中文游戏开发者）
        "游戏开发 AI", "vibe coding 游戏", "Unity AI 开发",
        "Unreal AI", "Godot AI", "AI 游戏编程",
        "Cursor 游戏开发",
    ]
}
```

---

### 平台 4：Reddit（纯英文）

Reddit 是英文社区，不需要中文关键词。

```python
KEYWORDS_REDDIT_MODULE1 = {
    "subreddits": [
        "r/gamedev", "r/Unity3D", "r/unrealengine", "r/godot",
        "r/indiegaming", "r/learnprogramming",
    ],
    "en": [
        "AI coding", "vibe coding", "cursor", "claude", "copilot",
        "LLM", "AI assistant", "AI workflow",
        "ai game", "ai npc", "procedural generation",
        "ai tools", "coding assistant",
    ]
}
```

---

### 平台 5：HackerNews（纯英文）

HN 以英文技术社区为主，搜索精准英文关键词。

```python
KEYWORDS_HN_MODULE1 = {
    "en": [
        "vibe coding game", "ai game development", "ai gamedev",
        "unity ai", "unreal ai", "godot ai",
        "cursor game", "claude game", "llm game",
        "ai indie game", "ai npc", "game ai tools",
        "vibe coding unity", "vibe coding unreal",
    ]
}
```

---

### 平台 6：Dev.to（纯英文）

Dev.to 英文技术博客平台，搜索英文关键词 + tag。

```python
KEYWORDS_DEVTO_MODULE1 = {
    "en": [
        "vibe coding game", "ai game dev", "unity ai",
        "unreal ai", "godot ai", "cursor game",
        "ai game development", "llm game",
        "indie game ai", "game dev ai workflow",
    ],
    "tags": [
        "gamedev", "unity", "unrealengine", "godot",
        "ai", "vibecoding", "cursor",
    ]
}
```

---

### 平台 7：RSS 聚合（按来源区分语言）

```python
RSS_SOURCES_MODULE1 = {
    "zh_feeds": [
        # 中文科技媒体
        "https://36kr.com/feed",           # 36氪
        "https://sspai.com/feed",           # 少数派
        "https://www.jiqizhixin.com/rss",   # 机器之心
        "https://gameinstitute.qq.com/rss", # 腾讯游戏学院（如有）
    ],
    "en_feeds": [
        # 英文游戏开发 & AI
        "https://www.gamedeveloper.com/rss.xml",
        "https://simonwillison.net/atom/everything/",
        "https://feeds.feedburner.com/oreilly/radar",
    ],
    "zh_keywords": [
        "游戏开发 AI", "AI 游戏", "Unity AI", "Unreal AI", "Godot AI",
        "vibe coding", "AI 编程", "游戏 AI 工具",
    ],
    "en_keywords": [
        "ai game", "vibe coding game", "unity ai", "unreal ai",
        "godot ai", "game dev ai", "ai gamedev",
    ]
}
```

---

### 平台 8：ProductHunt（纯英文）

```python
KEYWORDS_PH_MODULE1 = {
    "en": [
        "game", "unity", "unreal", "godot",
        "ai coding", "vibe coding", "game dev tool",
        "ai game", "indie game",
    ]
}
```

---

### 平台 9：GitHub Trending（纯英文，放最后）

```python
KEYWORDS_GITHUB_MODULE1 = {
    "en": [
        "unity ai coding assistant",
        "unreal engine ai coding",
        "godot ai assistant",
        "vibe coding game",
        "ai game development llm",
        "game dev ai tools",
        "unity llm", "unreal llm", "godot llm",
    ]
}
```

---

## 模块二：【AI 通用】关键词（按平台语言）

> 模块二不限游戏，但同样按平台语言差异化搜索。

### 国内平台（KM / 微信公众号）— 中文为主

```python
KEYWORDS_MODULE2_ZH = [
    # Vibe Coding / AI Coding
    "vibe coding", "AI 编程", "AI 辅助编程", "AI 代码助手",
    "智能编程", "AI IDE", "AI 开发工具",
    # 工具名
    "Cursor", "Cursor AI", "Cursor 教程", "Cursor 使用技巧",
    "Claude Code", "Windsurf", "Copilot",
    "bolt.new", "v0.dev",
    # 行业动态
    "大模型", "LLM", "GPT", "Claude", "Gemini",
    "AI Agent", "AI 工作流", "Agentic Coding",
    "OpenAI", "Anthropic",
    # 开发者生产力
    "AI 提效", "AI 开发效率", "程序员 AI",
]
```

### 国外平台（X / Reddit / HN / Dev.to / GitHub）— 英文为主

```python
KEYWORDS_MODULE2_EN = [
    # Vibe Coding / AI Coding 工具
    "vibe coding", "vibe-coding",
    "cursor ide", "cursor ai",
    "windsurf ide", "windsurf ai",
    "claude code",
    "ai agent ide", "agentic coding",
    "copilot agent", "github copilot agent",
    "bolt.new", "v0.dev",
    "devin ai", "codeium",
    "ai coding assistant", "llm coding",
    "ai pair programming", "coding agent",
    "ai ide", "ai coding",
    # 行业动态
    "claude", "gpt-4o", "gemini", "llm",
    "ai developer tools", "openai", "anthropic",
    # hashtag（X 专用）
    "#vibecoding", "#aicoding", "#cursorai", "#claudecode",
]
```

### X（英文为主 + 中文补充）

```python
KEYWORDS_MODULE2_X = {
    "en": KEYWORDS_MODULE2_EN,
    "zh": [
        "vibe coding", "AI 编程", "Cursor 使用", "Claude Code",
        "AI 开发工具", "大模型编程",
    ]
}
```

---

## 关键词策略汇总表

| 平台 | 语言策略 | 说明 |
|------|----------|------|
| 🏢 KM | 🇨🇳 中文 70% + 🌐 英文 30% | 腾讯内部，中文为主，技术词直接用英文 |
| 💬 微信公众号 | 🇨🇳 中文 80% + 🌐 英文 20% | 中文内容为主，工具名用英文 |
| 🐦 X (Twitter) | 🌐 英文 70% + 🇨🇳 中文 30% | 英文用户为主，兼顾中文开发者社区 |
| 🤖 Reddit | 🌐 纯英文 100% | 英文社区，无中文需求 |
| 📰 HackerNews | 🌐 纯英文 100% | 英文技术社区 |
| 📝 Dev.to | 🌐 纯英文 100% | 英文博客平台 |
| 📡 RSS | 🇨🇳/🌐 按来源区分 | 中文 Feed 用中文词，英文 Feed 用英文词 |
| 🚀 ProductHunt | 🌐 纯英文 100% | 英文产品社区 |
| ⭐ GitHub Trending | 🌐 纯英文 100% | 代码仓库，英文描述为主 |

---

## 报告输出结构

```markdown
# 🎮 AI 游戏开发 & Vibe Coding 每日资讯 — YYYY-MM-DD

## 📊 今日概况
| 模块 | 条数 |
|------|------|
| 🎮 模块一：AI + 游戏 | N 条 |
| 🤖 模块二：AI 通用  | N 条 |

---

## 🎮 模块一：AI + 游戏
> Unity / Unreal / Godot × AI/Vibe Coding

### 来自 KM（穷尽）

#### [文章标题](原文链接)
> 来源信息（平台 | 作者 | 阅读数等）

原文约 20% 字数的中文总结（提炼核心观点、方法论、结论，保留关键数据和技术细节）。

---

### 来自 微信公众号（穷尽）⏸️
（同上格式）

### 来自 X / Twitter（穷尽）⏸️
（同上格式）

### 来自 Reddit ⏸️
（同上格式）

### 来自 HackerNews / Dev.to / RSS / ProductHunt
（同上格式）

### 来自 GitHub Trending
（同上格式）

---

## 🤖 模块二：AI 通用
...（模块二保持原有格式：标题 + 来源 + 一句话摘要）

---
*抓取时间：11:00 | 过去 24 小时*
```

> ⚠️ **模块一文章格式规范（v0.6 新增）**
> - **标题**：使用 Markdown 超链接格式 `[标题](原文链接)`
> - **原文链接**：必须附上，方便直接跳转阅读
> - **总结**：字数约为原文的 **20%**，要求：
>   - 提炼核心观点、方法论、实操步骤、结论
>   - 保留关键数据、技术细节、工具名称
>   - 使用中文输出（原文为英文时翻译总结）
>   - 不得简单复述标题，需有实质性内容
> - 模块二不受此限制，保持原有一句话摘要格式

---

## 企业微信推送格式

```
🎮 AI游戏开发 & Vibe Coding 日报 [MM/DD]
共 N 条 | 🎮模块一:N条 🤖模块二:N条

── 🎮 AI+游戏 精选 ──
• [标题1]（来源：KM）
• [标题2]（来源：HN）
• [标题3]（来源：GitHub）

── 🤖 AI通用 精选 ──
• [标题1]
• [标题2]
```

---

## 📁 文件结构

```
/Users/dada/vibe-coding-digest/
├── digest.py                  # 主抓取 & 处理脚本
├── run_digest.sh              # cron 启动脚本
├── workflow-v0.5.md           # 本文件（当前工作流文档）
├── workflow-v0.4.md           # 上一版本
├── .env                       # API Key 配置（不提交 git）
├── digest_YYYY-MM-DD.md       # 每日报告
└── latest_summary.txt         # 最新推送摘要
```

---

## ✅ 已完成事项

- [x] **微信公众号**抓取模块（搜狗微信搜索，48h 时间窗口）
- [x] **X (Twitter)** 抓取模块（Playwright + Cookie 登录）
- [x] **Reddit** 抓取模块（RSS Feed，r/gamedev、r/Unity3D、r/unrealengine、r/godot 等）
- [x] 报告中按平台来源分组展示（模块一按平台顺序1-9）
- [x] 去重算法（跨平台同一 URL 去重）

---

## 📝 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v0.1 | 2026-03 | 初始版本，基础抓取框架 |
| v0.2 | 2026-03 | 新增 KM、科技媒体、GitHub Trending |
| v0.3 | 2026-03 | 确定关键词优先级（游戏×AI为P0），引擎覆盖 Unreal/Unity/Godot，模型改为 Claude Sonnet 4.6 |
| v0.4 | 2026-03-12 | 重构为两大模块：模块一（AI+游戏，严格平台顺序，KM/微信/X 穷尽24h）+ 模块二（AI通用）；GitHub Trending 移至最后 |
| v0.5 | 2026-03-12 | **新增按平台语言差异化关键词策略**：国内平台（KM/微信）中文为主+英文补充；X 英文为主+中文补充；Reddit/HN/Dev.to/GitHub 纯英文；RSS 按来源区分语言 |
| v0.6 | 2026-03-12 | **模块一输出格式升级**：每篇文章改为「标题+原文链接+原文约20%字数中文总结」；模块二保持原有一句话摘要格式 |

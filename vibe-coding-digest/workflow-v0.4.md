# Vibe Coding 每日资讯工作流 v0.4

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

| 顺序 | 平台 | 抓取方式 | 覆盖要求 | 状态 |
|------|------|----------|----------|------|
| **1** | 🏢 **KM（腾讯内部）** | KM MCP API | ⚠️ **穷尽** 11:00 前 24 小时内全部 | ✅ 可用 |
| **2** | 💬 **微信公众号** | 直接操作电脑（扫码登录） | ⚠️ **穷尽** 11:00 前 24 小时内全部 | ⏸️ 待完成 |
| **3** | 🐦 **X (Twitter)** | 直接操作电脑（登录账号） | ⚠️ **穷尽** 11:00 前 24 小时内全部 | ⏸️ 待完成 |
| **4** | 🤖 **Reddit** | 直接操作电脑 | 尽量抓取，不要求穷尽 | ⏸️ 待完成 |
| **5** | 📰 **HackerNews** | Algolia 免费 API | 关键词过滤 | ✅ 运行中 |
| **6** | 📝 **Dev.to** | 官方免费 API | 关键词过滤 | ✅ 运行中 |
| **7** | 📡 **RSS 聚合** | feedparser | 关键词过滤 | ✅ 运行中 |
| **8** | 🚀 **ProductHunt** | RSS | 关键词过滤 | ✅ 运行中 |
| **9** | ⭐ **GitHub Trending** | GitHub Search API | 关键词过滤，放最后 | ✅ 运行中 |

> 💡 **关键原则**：平台 1-3（KM / 微信公众号 / X）必须**穷尽**过去 24 小时内所有相关资讯，不得遗漏。平台 4-9 按关键词过滤即可。

---

### 模块一关键词

#### 核心交叉词（游戏引擎 × AI 工具）

```
引擎词：
  Unreal Engine / Unreal / UE5 / UE4
  Unity / Unity3D
  Godot

× AI 工具词：
  AI Coding / Vibe Coding / Cursor / Claude / Copilot
  MCP / Agent / LLM / GPT / Gemini

+ 场景词（任意一个）：
  game dev / game development / 游戏开发
  tips / tutorial / workflow / experience / devlog
  indie game / 独立游戏
```

#### 完整关键词列表

```python
KEYWORDS_MODULE1 = [
    # 游戏开发 + Vibe/AI Coding 直接交叉
    "vibe coding game", "ai game development", "ai game dev", "ai gamedev",
    "vibe coding unity", "vibe coding unreal", "vibe coding godot",
    "cursor game", "cursor unity", "cursor unreal", "cursor godot",
    "claude game", "claude unity", "claude unreal", "claude godot",
    "copilot game", "copilot unity", "copilot unreal", "copilot godot",
    "llm game development", "llm unity", "llm unreal", "llm godot",
    "ai game programming", "ai indie game",
    # 游戏引擎 + AI 工具
    "unity ai coding", "unity ai assistant", "unity copilot", "unity cursor",
    "unreal ai coding", "unreal ai assistant", "unreal copilot", "unreal cursor",
    "godot ai coding", "godot ai assistant", "godot copilot", "godot cursor",
    # 游戏开发者 AI 工作流 & 经验
    "game developer ai workflow", "indie game ai tools",
    "game programming ai tips", "ai assisted game development",
    "ai npc", "game ai tools", "procedural generation ai",
    # 中文关键词
    "游戏开发 ai", "ai 游戏开发", "unity ai", "unreal ai", "godot ai",
    "游戏 vibe coding", "ai 游戏编程", "游戏开发 cursor", "游戏开发 claude",
]
```

---

### 模块一抓取逻辑细节

#### 平台 1：KM（穷尽模式）

- 搜索方式：KM MCP `list-articles` + `hot-articles`
- 时间范围：过去 24 小时内（`created_after` 参数）
- 关键词：使用 `KEYWORDS_MODULE1` 全量搜索
- 翻页：**必须翻页至无更多结果**（穷尽）
- 排序：先按热度，再按时间

```
搜索组合（依次执行）：
  1. keywords=["游戏", "AI", "vibe coding", "Unity", "Unreal", "Godot"]
  2. keywords=["游戏开发", "cursor", "claude", "copilot"]
  3. keywords=["game dev", "ai coding", "vibe coding game"]
  4. hot-articles 近 2 天，过滤游戏相关
```

#### 平台 2：微信公众号（穷尽模式）⏸️

- 搜索方式：直接操作电脑，登录微信/公众号平台搜索
- 目标公众号类型：游戏开发类、AI 工具类、独立游戏开发者
- 时间范围：过去 24 小时内，**全量抓取**
- 待完成：需要扫码登录，后续单独处理

#### 平台 3：X / Twitter（穷尽模式）⏸️

- 搜索方式：直接操作电脑，登录 X 账号搜索
- 搜索词：`game dev AI`、`unity vibe coding`、`unreal cursor`、`godot AI` 等
- 时间范围：过去 24 小时内，**全量抓取**
- 待完成：需要登录账号，后续单独处理

#### 平台 4：Reddit ⏸️

- 目标 subreddit：`r/gamedev`、`r/Unity3D`、`r/unrealengine`、`r/godot`
- 搜索词：AI、vibe coding、cursor、claude、copilot
- 时间范围：过去 24 小时 `hot` + `new`
- 待完成：后续单独处理

#### 平台 5-8：HackerNews / Dev.to / RSS / ProductHunt

- 使用 `KEYWORDS_MODULE1` 关键词过滤
- 时间范围：过去 24 小时
- 按匹配度 + 热度排序

#### 平台 9：GitHub Trending（最后处理）

- 搜索组合：
  ```
  unity ai coding assistant
  unreal engine ai coding
  godot ai assistant
  vibe coding game
  ai game development llm
  ```
- 时间范围：近 7 天有更新的仓库
- 排序：Star 数降序

---

## 模块二：【AI 通用】

> **定义**：AI 相关的通用资讯，不限于游戏开发。
> 包括：Vibe Coding / AI Coding 工具动态、AI IDE 新功能、行业讨论、使用技巧。

### 平台搜索顺序

模块二不要求严格顺序，按资讯质量综合抓取：

| 平台 | 抓取方式 | 优先级 | 状态 |
|------|----------|--------|------|
| HackerNews | Algolia API | 高 | ✅ 运行中 |
| Dev.to | 官方 API | 高 | ✅ 运行中 |
| GitHub Trending | Search API | 高 | ✅ 运行中 |
| RSS（36kr / 少数派 / 机器之心 / Simon Willison 等） | feedparser | 中 | ✅ 运行中 |
| ProductHunt | RSS | 中 | ✅ 运行中 |
| KM（通用 AI 内容） | KM MCP | 中 | ✅ 运行中 |

### 模块二关键词

```python
KEYWORDS_MODULE2 = [
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
    "claude", "gpt-4", "gemini", "llm",
    "ai developer tools", "openai", "anthropic",
    # 中文
    "vibe coding", "ai 编程", "智能编程", "ai 开发工具",
    "大模型", "人工智能开发",
]
```

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
...

### 来自 微信公众号（穷尽）⏸️
...

### 来自 X / Twitter（穷尽）⏸️
...

### 来自 Reddit ⏸️
...

### 来自 HackerNews / Dev.to / RSS / ProductHunt
...

### 来自 GitHub Trending
...

---

## 🤖 模块二：AI 通用
...

---
*抓取时间：11:00 | 过去 24 小时*
```

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
├── workflow-v0.4.md           # 本文件（当前工作流文档）
├── workflow-v0.3.md           # 上一版本
├── .env                       # API Key 配置（不提交 git）
├── digest_YYYY-MM-DD.md       # 每日报告
└── latest_summary.txt         # 最新推送摘要
```

---

## ⏸️ 待完成事项

- [ ] **微信公众号**抓取模块（直接操作电脑，扫码登录）
- [ ] **X (Twitter)** 抓取模块（直接操作电脑，登录账号）
- [ ] **Reddit** 抓取模块（r/gamedev、r/Unity3D、r/unrealengine、r/godot）
- [ ] 报告中按平台来源分组展示（模块一需体现平台顺序）
- [ ] 去重算法优化

---

## 📝 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v0.1 | 2026-03 | 初始版本，基础抓取框架 |
| v0.2 | 2026-03 | 新增 KM、科技媒体、GitHub Trending |
| v0.3 | 2026-03 | 确定关键词优先级（游戏×AI为P0），引擎覆盖 Unreal/Unity/Godot，模型改为 Claude Sonnet 4.6 |
| v0.4 | 2026-03-12 | **重构为两大模块**：模块一（AI+游戏，严格平台顺序，KM/微信/X 穷尽24h）+ 模块二（AI通用）；GitHub Trending 移至模块一最后；报告结构按平台来源分组 |

# 🛠️ Work Assistant 工作辅助工作流

> 帮你随时查数据、看游戏新趋势、做竞品分析、解答设计问题——全平台联网获取数据

---

## 📁 目录结构

```
work-assistant/
├── assistant.py          # 🚀 主入口（供 Knot AI 直接调用）
├── scripts/
│   └── fetcher.py        # 各平台抓取器（底层模块）
├── config/
│   └── platforms.json    # 平台配置（鉴权/开关）
├── cache/                # 自动缓存（减少重复请求）
├── reports/              # 生成报告保存目录
└── README.md
```

---

## 🌐 支持平台

| 平台 | 类型 | 鉴权方式 | 用途 |
|------|------|----------|------|
| **Steam** | 游戏商店 | 无需（官方公开API） | 特惠/新游榜 |
| **SteamDB** | 游戏数据库 | 无需（SteamCharts + Steam API 组合）| 实时在线人数、历史趋势、打折、单游详情 |
| **itch.io** | 独立游戏 | 无需（JSON API） | 独立游戏趋势 |
| **Reddit** | 社区讨论 | 无需（RSS/API） | gamedev/indiegaming热帖 |
| **Hacker News** | 技术讨论 | 无需（官方API） | AI/游戏开发话题 |
| **X (Twitter)** | 社媒 | Cookie复用（accounts.db）| vibe coding / 游戏动态 |
| **Bilibili** | 视频 | 无需（公开API） | 独立游戏/AI编程热门视频 |
| **小红书** | 社区笔记 | Cookie注入（xhs_inject_cookies.py）| 独立游戏/游戏评测/设计趋势 |
| **YouTube** | 视频 | 无需（RSS） | GDC/游戏设计频道 |
| **KM** | 内部知识库 | mcporter-internal | 腾讯内部AI/游戏文章 |

---

## 🚀 快速使用

### 方式一：让 Knot 直接帮你查

直接用中文描述需求，例如：

- 「帮我查最近 Steam 上热门的独立游戏」
- 「看看 Reddit 上有什么 gamedev 话题在讨论」
- 「查一下最近关于 vibe coding 的 X 动态」
- 「Bilibili 独立游戏区最近有什么热门视频」
- 「HN 上有什么 AI 编程相关的热门讨论」

### 方式二：命令行直接运行

```bash
cd /data/workspace/ClawWorkFlows/work-assistant

# 游戏趋势（全平台，含 SteamDB）
python3 assistant.py 游戏趋势 --limit 10

# SteamDB 专项查询
python3 scripts/fetcher.py --source steamdb --type top --limit 20         # 实时在线人数 Top 20
python3 scripts/fetcher.py --source steamdb --type deals --limit 10       # 当前打折促销
python3 scripts/fetcher.py --source steamdb --type new --limit 10         # 新发售游戏
python3 scripts/fetcher.py --source steamdb --type app --keyword 1091500  # 单游详情（appid）
python3 scripts/fetcher.py --source steamdb --type search --keyword "roguelike" --limit 10  # 搜索

# 小红书（首次使用需注入 Cookie）
# 步骤1：编辑 scripts/xhs_inject_cookies.py，填入从浏览器复制的 Cookie
# 步骤2：运行注入脚本
python3 scripts/xhs_inject_cookies.py
# 步骤3：使用
python3 scripts/fetcher.py --source xhs --type search --keyword 独立游戏 --limit 20
python3 scripts/fetcher.py --source xhs --type hot --limit 20   # 发现页热门



# 关键词搜索（指定平台）
python3 assistant.py search --keyword "roguelike" --platforms steam reddit itch --limit 10

# 单平台查询
python3 scripts/fetcher.py --source steam --type trending --limit 20
python3 scripts/fetcher.py --source reddit --subreddit gamedev --limit 15
python3 scripts/fetcher.py --source bilibili --type search --keyword "独立游戏" --limit 10
python3 scripts/fetcher.py --source hn --query "game design" --limit 10
python3 scripts/fetcher.py --source x --query "indie game release" --limit 10
python3 scripts/fetcher.py --source itch --type top-rated --limit 20
python3 scripts/fetcher.py --source youtube --channel "GDC" --limit 10
```

---

## ⚙️ 配置说明

### X (Twitter) Cookie
自动复用 `../vibe-coding-digest/accounts.db`，无需重新登录。
若 Cookie 过期，可通过 vibe-coding-digest 中的 `x_login.py` 刷新。

### 预置 YouTube 频道
| 名称 | 内容 |
|------|------|
| GDC | 游戏开发者大会视频 |
| GameMaker's Toolkit | 游戏设计分析 |
| Brackeys | Unity 教程 |
| Extra Credits | 游戏设计深度讨论 |
| AI Explained | AI 前沿进展 |

新增频道：编辑 `scripts/fetcher.py` 中的 `YOUTUBE_CHANNELS` 字典

### Bilibili 分区
独立游戏、单机游戏、网络游戏、手机游戏、游戏资讯、科技、AI

---

## 🔄 缓存机制

所有抓取结果会自动缓存在 `cache/` 目录，有效期：
- X / HN 搜索：60 分钟
- Reddit / HN 热门 / Bilibili：30 分钟
- Steam / itch.io / YouTube：60~120 分钟

缓存到期后自动重新抓取，无需手动清理。

---

## 📋 常用 Reddit 社区

| 社区 | 内容 |
|------|------|
| r/gamedev | 游戏开发综合 |
| r/indiegaming | 独立游戏 |
| r/indiegamedev | 独立游戏开发 |
| r/gamedesign | 游戏设计 |
| r/LocalLLaMA | 本地大模型 |
| r/cursor_ai | Cursor AI 编程 |
| r/ClaudeAI | Claude 讨论 |
| r/MachineLearning | ML 研究 |

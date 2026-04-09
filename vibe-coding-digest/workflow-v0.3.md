# Vibe Coding 每日资讯工作流 v0.3

> 最后更新：2026-03-12
> 负责人：seanyyao

---

## 🗺️ 整体流程

```
每天 11:00 自动触发
       ↓
  模块一：任务调度
       ↓
  模块二：多源抓取
       ↓
  模块三：过滤 & 去重
       ↓
  模块四：AI 翻译 & 摘要
       ↓
  模块五：Markdown 报告生成
       ↓
  模块六：企业微信推送
```

---

## 模块一：任务调度

- 触发时间：每天 **11:00**（macOS cron）
- 入口脚本：`/Users/dada/vibe-coding-digest/run_digest.sh`

---

## 模块二：多源抓取

### 优先级说明

| 优先级 | 来源 | 抓取方式 | 状态 |
|--------|------|----------|------|
| 🔴 P0 | **KM（腾讯内部）** | KM MCP API | ✅ 运行中 |
| 🔴 P0 | HackerNews | Algolia 免费 API | ✅ 运行中 |
| 🔴 P0 | GitHub 搜索 + Trending | GitHub Search API | ✅ 运行中 |
| 🔴 P0 | Dev.to | 官方免费 API | ✅ 运行中 |
| 🟠 P1 | RSS 聚合 | feedparser | ✅ 运行中 |
| 🟠 P1 | ProductHunt | RSS | ✅ 运行中 |
| ⏸️ 待完成 | Reddit | 直接操作电脑 | 暂缓 |
| ⏸️ 待完成 | X (Twitter) | 直接操作电脑 | 暂缓 |
| ⏸️ 待完成 | 微信公众号 | 直接操作电脑 | 暂缓 |

### RSS 来源列表（P1）

**科技媒体**
- 36kr：`https://36kr.com/feed`
- 少数派：`https://sspai.com/feed`
- 机器之心：`https://www.jiqizhixin.com/rss`
- HackerNews RSS：`https://hnrss.org/frontpage`

**游戏开发专项**
- Game Developer：`https://www.gamedeveloper.com/rss.xml`
- Unity Blog：`https://blog.unity.com/rss`
- Unreal Engine Blog：`https://www.unrealengine.com/en-US/rss`
- Godot Blog：`https://godotengine.org/rss.xml`

---

## 模块三：关键词过滤 & 去重

### 关键词优先级

#### 🔴 P0 — 游戏开发 × AI（最高优先级，优先抓取）

```
游戏引擎关键词：
  unreal engine / unity / godot

× AI 工具关键词：
  ai coding / vibe coding / cursor / claude / copilot / mcp / agent

+ 场景词：
  game dev / game development / tips / tutorial / experience / devlog
```

**示例命中**：`"Using Cursor AI with Unreal Engine 5"` / `"Vibe coding a Godot game in 1 day"`

---

#### 🟠 P1 — AI Coding 通用

```
vibe coding / ai coding / cursor ide / windsurf / claude code /
github copilot / devin / replit agent / bolt.new / v0
```

---

#### 🟡 P2 — AI 行业动态（背景信息）

```
claude / gpt-4 / gemini / llm / ai agent / openai / anthropic /
large language model / foundation model
```

---

### 去重规则

- 24 小时内相同 URL → 跳过
- 标题相似度 > 80%（余弦相似度）→ 跳过
- 优先保留来源权重更高的版本（P0 > P1 > P2）

---

## 模块四：AI 翻译 & 摘要

- 模型：**Claude Sonnet 4.6**（`claude-sonnet-4-5` API）
- API Key：`ANTHROPIC_API_KEY`（配置在 `.env` 文件中）

### 每条资讯输出格式

```markdown
## [中文标题]

> 💡 一句话摘要（30字以内）

[原文约 20% 字数的中文总结内容]

🔗 [原文链接](url) | 来源：xxx | 热度：xxx
```

---

## 模块五：Markdown 报告生成

- 输出路径：`/Users/dada/vibe-coding-digest/digest_YYYY-MM-DD.md`

### 报告结构

```markdown
# 🎮 Vibe Coding 每日资讯 — YYYY-MM-DD

## 🔴 P0 游戏开发 × AI 精选（N 条）
...

## 🟠 P1 AI Coding 通用（N 条）
...

## 🟡 P2 AI 行业动态（N 条）
...
```

---

## 模块六：企业微信推送

- 推送内容：每个分区的标题 + 一句话摘要（精简版）
- 完整报告保存在本地 Markdown 文件中
- 推送通过「Knot消息通知」企业微信机器人发送

---

## 📁 文件结构

```
/Users/dada/vibe-coding-digest/
├── digest.py                  # 主抓取 & 处理脚本
├── run_digest.sh              # cron 启动脚本
├── workflow-v0.3.md           # 本文件（工作流文档）
├── .env                       # API Key 配置（不提交 git）
├── digest_2026-03-12.md       # 每日报告（示例）
└── digest_2026-03-11.md
```

---

## ⏸️ 待完成事项

- [ ] Reddit 抓取模块（直接操作电脑方案）
- [ ] X (Twitter) 抓取模块（直接操作电脑方案）
- [ ] 微信公众号抓取模块（直接操作电脑方案）
- [ ] 去重算法优化（当前为简单相似度匹配）
- [ ] 报告历史归档 & 搜索功能

---

## 📝 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v0.1 | 2026-03 | 初始版本，基础抓取框架 |
| v0.2 | 2026-03 | 新增 KM、科技媒体、GitHub Trending |
| v0.3 | 2026-03 | 确定关键词优先级（游戏开发×AI为P0），引擎覆盖 Unreal/Unity/Godot，模型改为 Claude Sonnet 4.6 |

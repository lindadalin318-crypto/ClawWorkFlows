# daily-game-idea 工作流

每日 **11:45** 自动生成 10 个全新游戏创意，通过 Knot 推送通知给用户。

---

## 目录结构

```
daily-game-idea/
├── generate_ideas.py     # 核心生成脚本（调用 AI 生成 10 个创意）
├── run_daily.py          # 定时任务入口（生成 + 推送）
├── latest_ideas.txt      # 最新一次的摘要（cron 读取用）
├── README.md             # 本文件
└── ideas/
    ├── ideas_2026-04-13.md   # 每日完整创意存档
    └── ...
```

---

## 创意来源维度

每次生成涵盖以下多个维度，随机混合：

| 维度 | 说明 |
|------|------|
| 🔀 玩法融合 | 两款经典游戏核心机制的组合，如 Flappy Bird × 三消 |
| 🌍 文化趋势融合 | 当前热点/社会现象/流行文化 + 游戏机制，如 AI打工人 × 塔防 |
| 🚀 爆款新方向 | 已有爆款的未验证变体，如羊了个羊的新形态 |
| 🙃 反直觉设计 | 颠覆玩家固有认知，如"越失败越强" |
| 💆 情绪驱动 | 以特定情绪（解压/治愈/紧张/仪式感）反推机制 |
| 🏙️ 真实世界映射 | 日常生活场景游戏化，如通勤/打卡/减肥 |

---

## 每个 Idea 的输出格式

```markdown
### 🎮 Idea N：[创意名称]
**来源维度**：[维度名称]
**一句话描述**：[吸引人的一句话]
**核心玩法**：[主要操作方式和循环，2-4句]
**差异化亮点**：[与已有游戏的本质区别]
**目标平台**：[手游/小游戏/PC独立游戏]
**参考原型**：[1-2个类似游戏作为参照]
```

---

## 手动运行

```bash
cd /data/workspace/ClawWorkFlows/daily-game-idea

# 仅生成创意（不推送）
python3 generate_ideas.py

# 生成 + 构建推送内容（完整流程）
python3 run_daily.py
```

---

## 定时任务

由 Knot cron 每日 **11:45（北京时间）** 自动执行，任务消息：

> 运行 `/data/workspace/ClawWorkFlows/daily-game-idea/run_daily.py`，读取输出中 `NOTIFY_BODY_START` 和 `NOTIFY_BODY_END` 之间的内容，以标题 `NOTIFY_TITLE` 对应的文本通过 notify 工具推送给用户。

---

## 依赖

- `knot-cli`（已安装，用于调用 AI）
- Python 3.8+（标准库，无需额外安装）

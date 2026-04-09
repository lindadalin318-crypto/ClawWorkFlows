#!/bin/bash
# 游戏舆情监控启动脚本

set -e
SCRIPT_DIR="/Users/dada/game-sentiment"
VENV="/Users/dada/vibe-coding-digest/venv"

echo "🎮 启动游戏舆情监控..."

# 激活 venv（复用 vibe-coding-digest 的虚拟环境）
source "$VENV/bin/activate"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 运行主脚本
python3 run_sentiment.py

echo "✅ 完成"

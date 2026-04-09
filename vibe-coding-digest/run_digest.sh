#!/bin/bash
# 🎮 AI Game Dev & Vibe Coding Digest - 启动脚本 v2.0
# 运行流程：
#   Step 1: 通过 KM MCP 抓取腾讯内部 KM 文章 → km_results.json
#   Step 2: 运行主脚本 digest.py（读取 km_results.json + 其他平台）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source "$SCRIPT_DIR/venv/bin/activate"

# 可选：设置 Claude API Key（如需 AI 摘要）
# export ANTHROPIC_API_KEY="your-key-here"

# 可选：设置 GitHub Token（提升 API 限额）
# export GITHUB_TOKEN="your-token-here"

echo "======================================================"
echo "🎮 AI Game Dev & Vibe Coding Digest"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================================"

# ── Step 1：KM MCP 数据抓取 ─────────────────────────────
# KM 数据由 Knot/OpenClaw 通过 MCP 工具实时抓取后写入 km_results.json
# 如果 km_results.json 存在且在 90 分钟内，则跳过重新抓取
KM_JSON="$SCRIPT_DIR/km_results.json"
KM_FRESH=false

if [ -f "$KM_JSON" ]; then
    # 检查文件是否在 90 分钟内
    FILE_AGE=$(( $(date +%s) - $(stat -f %m "$KM_JSON" 2>/dev/null || echo 0) ))
    if [ "$FILE_AGE" -lt 5400 ]; then
        echo "✅ KM 数据已存在（${FILE_AGE}秒前），跳过重新抓取"
        KM_FRESH=true
    fi
fi

if [ "$KM_FRESH" = false ]; then
    echo "📡 KM 数据需要更新，请通过 Knot/OpenClaw 执行 KM MCP 抓取"
    echo "   运行：python3 $SCRIPT_DIR/fetch_km_mcp.py"
    echo "   （或在 Knot 中触发 KM 抓取任务）"
    echo ""
    # 如果有 Knot CLI，可以在这里自动调用：
    # knot run fetch-km --output "$KM_JSON"
fi

# ── Step 2：运行主脚本 ──────────────────────────────────
echo ""
echo "🚀 启动 digest.py..."
python3 "$SCRIPT_DIR/digest.py"

echo ""
echo "======================================================"
echo "✅ 完成！报告已保存到 $SCRIPT_DIR/digest_$(date +%Y-%m-%d).md"
echo "======================================================"
echo ""
echo "⚠️  【重要】X/Twitter 和 Reddit 条目仍为英文原文"
echo "   请在 Knot 对话中告知 Claude："
echo "   「请读取 $SCRIPT_DIR/digest_$(date +%Y-%m-%d)_raw.json，翻译所有 X/Reddit 英文条目为中文，并重新生成报告」"
echo "======================================================"

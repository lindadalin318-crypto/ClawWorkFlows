# ============================================================
# 游戏舆情监控 - 配置文件
# ============================================================

# ---- 目标游戏配置（可随时修改）----
GAME_CONFIG = {
    "name": "洛克王国：世界",
    "name_aliases": ["洛克王国世界", "洛克王国", "roco kingdom", "洛克"],
    "developer": "腾讯",

    # 平台专属 ID
    "taptap_app_id": "188212",
    "bilibili_keywords": ["洛克王国世界", "洛克王国：世界"],

    # NGA 版块（游戏刚上线，若有专属版块后可更新 fid）
    "nga_fid": None,          # 暂无专属版块，用关键词搜索
    "nga_keywords": ["洛克王国世界", "洛克王国：世界"],

    # 小红书搜索关键词
    "xiaohongshu_keywords": ["洛克王国世界", "洛克王国：世界"],
}

# ---- 抓取参数 ----
FETCH_CONFIG = {
    "hours_lookback": 24,      # 只抓最近 N 小时的内容
    "max_items_per_source": 30, # 每个平台最多抓取条数
    "bilibili_max_videos": 20,  # B站最多抓取视频数
    "taptap_max_reviews": 10,   # TapTap API 单次 limit 最大值为 10
    "taptap_pages": 3,          # TapTap 抓取页数（10条/页 × 3页 = 30条）
    "nga_max_posts": 20,        # NGA 最多抓取帖子数
    "xhs_max_notes": 20,        # 小红书最多抓取笔记数
}

# ---- 输出目录 ----
OUTPUT_DIR = "/Users/dada/game-sentiment"

# ---- Playwright Profile（复用 vibe-coding-digest 的）----
PLAYWRIGHT_PROFILE = "/Users/dada/vibe-coding-digest/x_browser_profile"
XHS_PROFILE = "/Users/dada/game-sentiment/xhs_profile"

# ---- 报告模板 ----
REPORT_SECTIONS = [
    "overview",      # 今日舆情概览
    "hot_topics",    # 热点话题 Top10
    "complaints",    # 吐槽榜 Top10
    "memes",         # 玩家梗/流行词
    "praise",        # 好评亮点
    "platform_data", # 各平台数据摘要
]

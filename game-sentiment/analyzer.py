#!/usr/bin/env python3
"""
游戏舆情监控 - AI 分析模块
输入：原始抓取数据（raw_latest.json）
输出：结构化分析结果（analysis_latest.json）
"""

import json
import re
import logging
from datetime import datetime
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)


# ============================================================
# 情感分析（基于关键词规则，无需外部 API）
# ============================================================

POSITIVE_WORDS = [
    "好玩", "好评", "推荐", "喜欢", "感动", "童年", "回忆", "治愈", "可爱",
    "精彩", "满分", "完美", "棒", "赞", "开心", "快乐", "期待", "惊喜",
    "良心", "不氪金", "免费", "公平", "流畅", "优化好", "画质好", "好看",
    "好听", "好萌", "可爱", "有趣", "丰富", "精灵", "喜欢", "爱",
]

NEGATIVE_WORDS = [
    "难玩", "差评", "坑", "骗", "垃圾", "崩溃", "卡顿", "卡", "闪退",
    "bug", "BUG", "问题", "错误", "失望", "难受", "难", "烂", "垃圾",
    "太难", "不好", "差", "氪金", "充钱", "贵", "割韭菜", "毒瘤",
    "服务器", "登不上", "掉线", "延迟", "lag", "不平衡", "外挂",
    "退款", "删游", "劝退", "不推荐", "踩", "恶心", "吐槽",
]

COMPLAINT_PATTERNS = [
    r"(服务器|登录|闪退|卡顿|延迟|lag|掉线)[^，。！?]*",
    r"(bug|BUG|错误|崩溃)[^，。！?]*",
    r"(氪金|充钱|太贵|割韭菜)[^，。！?]*",
    r"(外挂|作弊|不平衡)[^，。！?]*",
    r"(画质|优化|帧率)[^，。！?]*差[^，。！?]*",
]

MEME_PATTERNS = [
    r"小洛克[^，。！?]*",
    r"御三家[^，。！?]*",
    r"精灵[^，。！?]{2,15}",
    r"学号[^，。！?]*",
    r"魔法[^，。！?]{2,10}",
]


def analyze_sentiment(text):
    """简单情感分析，返回 positive/negative/neutral 和分数"""
    if not text:
        return "neutral", 0

    text_lower = text.lower()
    pos_count = sum(1 for w in POSITIVE_WORDS if w in text)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w.lower() in text_lower)

    score = pos_count - neg_count
    if score > 0:
        return "positive", score
    elif score < 0:
        return "negative", score
    else:
        return "neutral", 0


def extract_keywords(texts, top_n=30):
    """提取高频关键词（简单分词）"""
    # 停用词
    stopwords = set([
        "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都",
        "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
        "会", "着", "没有", "看", "好", "自己", "这", "那", "里",
        "来", "她", "他", "它", "我们", "你们", "他们", "这个", "那个",
        "什么", "怎么", "为什么", "因为", "所以", "但是", "如果", "虽然",
        "可以", "可能", "应该", "还是", "已经", "现在", "时候", "时间",
        "游戏", "洛克", "王国", "世界",  # 游戏名本身不算关键词
    ])

    word_counter = Counter()
    for text in texts:
        if not text:
            continue
        # 提取 2-6 字的词组
        for n in [2, 3, 4]:
            for i in range(len(text) - n + 1):
                word = text[i:i+n]
                if word not in stopwords and re.match(r'^[\u4e00-\u9fff]+$', word):
                    word_counter[word] += 1

    return word_counter.most_common(top_n)


def extract_complaints(items):
    """提取吐槽内容"""
    complaints = []
    for item in items:
        text = item.get("content", "") + " " + item.get("title", "")
        sentiment, score = analyze_sentiment(text)
        if sentiment == "negative" or score < -1:
            for pattern in COMPLAINT_PATTERNS:
                matches = re.findall(pattern, text)
                for m in matches:
                    if len(m) > 3:
                        complaints.append({
                            "text": m.strip(),
                            "source": item.get("source", ""),
                            "url": item.get("url", ""),
                            "original": text[:100],
                        })
    return complaints


def extract_memes(items):
    """提取玩家梗/流行词"""
    meme_candidates = Counter()
    for item in items:
        text = item.get("content", "") + " " + item.get("title", "")
        for pattern in MEME_PATTERNS:
            matches = re.findall(pattern, text)
            for m in matches:
                m = m.strip()
                if 2 <= len(m) <= 20:
                    meme_candidates[m] += 1

    return [(k, v) for k, v in meme_candidates.most_common(20) if v >= 2]


def cluster_topics(items):
    """话题聚类（基于关键词）"""
    topic_keywords = {
        "服务器/登录问题": ["服务器", "登录", "掉线", "连接", "排队"],
        "精灵系统": ["精灵", "捕捉", "进化", "技能", "御三家"],
        "画质/优化": ["画质", "优化", "帧率", "卡顿", "流畅"],
        "剧情/世界观": ["剧情", "故事", "世界", "地图", "探索"],
        "PVP/战斗": ["战斗", "pvp", "PVP", "对战", "竞技", "平衡"],
        "氪金/付费": ["氪金", "充钱", "月卡", "皮肤", "道具"],
        "童年回忆": ["童年", "回忆", "情怀", "小时候", "怀旧"],
        "攻略/玩法": ["攻略", "教程", "怎么", "如何", "技巧"],
        "更新/活动": ["更新", "版本", "活动", "活动奖励", "新内容"],
        "社交/组队": ["组队", "好友", "社交", "公会", "一起"],
    }

    topic_counts = defaultdict(list)
    for item in items:
        text = (item.get("content", "") + " " + item.get("title", "")).lower()
        for topic, kws in topic_keywords.items():
            if any(kw.lower() in text for kw in kws):
                topic_counts[topic].append({
                    "title": item.get("title", "")[:50],
                    "source": item.get("source", ""),
                    "url": item.get("url", ""),
                    "sentiment": analyze_sentiment(text)[0],
                })

    # 按话题热度排序
    return sorted(
        [{"topic": k, "count": len(v), "items": v[:5]} for k, v in topic_counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )


def get_platform_stats(sources):
    """各平台数据统计"""
    stats = {}
    for src_name, items in sources.items():
        if not items:
            continue
        sentiments = [analyze_sentiment(i.get("content", "") + i.get("title", ""))[0] for i in items]
        pos = sentiments.count("positive")
        neg = sentiments.count("negative")
        neu = sentiments.count("neutral")
        total = len(sentiments)
        stats[src_name] = {
            "total": total,
            "positive": pos,
            "negative": neg,
            "neutral": neu,
            "sentiment_ratio": {
                "positive_pct": round(pos / total * 100, 1) if total else 0,
                "negative_pct": round(neg / total * 100, 1) if total else 0,
            }
        }
    return stats


# ============================================================
# 主分析函数
# ============================================================

def analyze(raw_data):
    """主分析入口"""
    sources = raw_data.get("sources", {})

    # 合并所有 items
    all_items = []
    for items in sources.values():
        all_items.extend(items)

    print(f"📊 分析 {len(all_items)} 条数据...")

    # 所有文本
    all_texts = [i.get("content", "") + " " + i.get("title", "") for i in all_items]

    # 执行分析
    result = {
        "game": raw_data.get("game", ""),
        "analyzed_at": datetime.now().isoformat(),
        "total_items": len(all_items),

        # 1. 各平台统计
        "platform_stats": get_platform_stats(sources),

        # 2. 整体情感分布
        "sentiment_overview": {
            "total": len(all_items),
            "positive": sum(1 for t in all_texts if analyze_sentiment(t)[0] == "positive"),
            "negative": sum(1 for t in all_texts if analyze_sentiment(t)[0] == "negative"),
            "neutral": sum(1 for t in all_texts if analyze_sentiment(t)[0] == "neutral"),
        },

        # 3. 热点话题
        "hot_topics": cluster_topics(all_items),

        # 4. 高频关键词
        "top_keywords": extract_keywords(all_texts, top_n=30),

        # 5. 吐槽榜
        "complaints": extract_complaints(all_items)[:20],

        # 6. 玩家梗
        "memes": extract_memes(all_items),

        # 7. 好评摘录（点赞最高的正面内容）
        "top_positive": sorted(
            [i for i in all_items if analyze_sentiment(
                i.get("content", "") + i.get("title", ""))[0] == "positive"],
            key=lambda x: int(str(x.get("likes", 0)).replace(",", "").replace("+", "") or 0),
            reverse=True,
        )[:10],

        # 8. 差评摘录（点赞最高的负面内容）
        "top_negative": sorted(
            [i for i in all_items if analyze_sentiment(
                i.get("content", "") + i.get("title", ""))[0] == "negative"],
            key=lambda x: int(str(x.get("likes", 0)).replace(",", "").replace("+", "") or 0),
            reverse=True,
        )[:10],
    }

    # 整体情感概述
    total = result["sentiment_overview"]["total"] or 1
    pos_pct = round(result["sentiment_overview"]["positive"] / total * 100, 1)
    neg_pct = round(result["sentiment_overview"]["negative"] / total * 100, 1)

    if pos_pct >= 60:
        overall = "🟢 整体正面"
    elif neg_pct >= 40:
        overall = "🔴 负面舆情较多，需关注"
    else:
        overall = "🟡 舆情中性，需持续观察"

    result["sentiment_overview"]["overall"] = overall
    result["sentiment_overview"]["positive_pct"] = pos_pct
    result["sentiment_overview"]["negative_pct"] = neg_pct

    print(f"✅ 分析完成")
    print(f"   情感概况: {overall} (正面{pos_pct}% / 负面{neg_pct}%)")
    print(f"   热点话题: {len(result['hot_topics'])} 个")
    print(f"   吐槽条目: {len(result['complaints'])} 条")
    print(f"   玩家梗词: {len(result['memes'])} 个")

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open("/Users/dada/game-sentiment/raw_latest.json", encoding="utf-8") as f:
        raw = json.load(f)
    result = analyze(raw)
    with open("/Users/dada/game-sentiment/analysis_latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("💾 分析结果已保存：analysis_latest.json")

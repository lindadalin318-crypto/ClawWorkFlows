#!/usr/bin/env python3
"""
translate_digest.py
读取 digest_{date}_raw.json，对 X/Twitter 和 Reddit 的英文条目：
1. 翻译标题为中文（title_zh）
2. 生成中文摘要（full_summary，约原文 20% 字数）
然后重新生成 digest_{date}.md 报告。

调用方式：
    python3 translate_digest.py [date]   # date 格式 YYYY-MM-DD，默认今天
"""

import json
import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def translate_with_claude(items_to_translate):
    """
    调用本地 claude CLI 批量翻译条目。
    返回 {url: {"title_zh": ..., "full_summary": ...}} 的字典。
    """
    if not items_to_translate:
        return {}

    # 构建翻译请求
    batch = []
    for i, item in enumerate(items_to_translate):
        batch.append({
            "idx": i,
            "url": item["url"],
            "title": item["title"],
            "summary": item.get("summary", ""),
            "source": item["source"],
        })

    prompt = f"""你是一个专业的翻译助手。请将以下来自 X/Twitter 和 Reddit 的英文内容翻译为中文。

要求：
1. title_zh：将原标题翻译为简洁的中文标题（不超过50字）
2. full_summary：基于原标题和摘要，生成约50-100字的中文摘要（原文约20%字数），要有实质内容

如果原文已经是中文或日文，title_zh 直接复制原标题，full_summary 生成中文摘要。
如果原文是广告/垃圾信息，title_zh 翻译即可，full_summary 写"（广告内容）"。

请严格按以下 JSON 格式返回，不要有任何其他文字：
[
  {{"idx": 0, "title_zh": "...", "full_summary": "..."}},
  ...
]

待翻译内容：
{json.dumps(batch, ensure_ascii=False, indent=2)}
"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=BASE_DIR,
        )
        output = result.stdout.strip()

        # 提取 JSON
        start = output.find("[")
        end = output.rfind("]") + 1
        if start == -1 or end == 0:
            print(f"  ⚠️  claude 返回格式异常，无法解析 JSON")
            print(f"  输出: {output[:200]}")
            return {}

        translations = json.loads(output[start:end])
        result_map = {}
        for t in translations:
            idx = t["idx"]
            if idx < len(batch):
                url = batch[idx]["url"]
                result_map[url] = {
                    "title_zh": t.get("title_zh", ""),
                    "full_summary": t.get("full_summary", ""),
                }
        return result_map

    except subprocess.TimeoutExpired:
        print("  ⚠️  claude CLI 超时")
        return {}
    except Exception as e:
        print(f"  ⚠️  翻译失败: {e}")
        return {}


def main():
    # 确定日期
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = datetime.now().strftime("%Y-%m-%d")

    raw_path = os.path.join(BASE_DIR, f"digest_{date}_raw.json")
    if not os.path.exists(raw_path):
        print(f"❌ 找不到 raw.json: {raw_path}")
        sys.exit(1)

    print(f"📖 读取 {raw_path}")
    with open(raw_path, encoding="utf-8") as f:
        data = json.load(f)

    m1_items = data["m1"]
    m2_items = data["m2"]
    all_items = m1_items + m2_items

    # 找出需要翻译的英文条目（X/Twitter 和 Reddit）
    need_translate = [
        item for item in all_items
        if (item["source"].startswith("X/Twitter") or item["source"].startswith("Reddit"))
        and not item.get("title_zh")  # 还没翻译过的
    ]

    print(f"🔤 需要翻译的条目: {len(need_translate)} 条")

    if need_translate:
        # 分批翻译（每批 15 条，避免 prompt 过长）
        BATCH_SIZE = 15
        all_translations = {}

        for i in range(0, len(need_translate), BATCH_SIZE):
            batch = need_translate[i:i + BATCH_SIZE]
            print(f"  🌐 翻译第 {i+1}-{min(i+BATCH_SIZE, len(need_translate))} 条...")
            translations = translate_with_claude(batch)
            all_translations.update(translations)
            print(f"  ✅ 本批翻译完成 {len(translations)} 条")

        # 将翻译结果写回 items
        url_to_item = {item["url"]: item for item in all_items}
        for url, trans in all_translations.items():
            if url in url_to_item:
                url_to_item[url]["title_zh"] = trans["title_zh"]
                url_to_item[url]["full_summary"] = trans["full_summary"]

        translated_count = sum(1 for t in all_translations.values() if t.get("title_zh"))
        print(f"\n✅ 翻译完成，成功翻译 {translated_count}/{len(need_translate)} 条")

        # 保存更新后的 raw.json
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 已更新 raw.json")
    else:
        print("  ✅ 所有条目已有中文翻译，跳过翻译步骤")

    # 重新生成报告
    print("\n📝 重新生成报告...")
    try:
        # 动态导入 digest.py 的 generate_report 函数
        sys.path.insert(0, BASE_DIR)
        import importlib.util
        spec = importlib.util.spec_from_file_location("digest", os.path.join(BASE_DIR, "digest.py"))
        digest_module = importlib.util.load_from_spec(spec)
        spec.loader.exec_module(digest_module)

        report = digest_module.generate_report(m1_items, m2_items)
        report_path = os.path.join(BASE_DIR, f"digest_{date}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已更新: {report_path}")

    except Exception as e:
        print(f"⚠️  重新生成报告失败: {e}")
        print("   请手动运行 digest.py 重新生成报告")


if __name__ == "__main__":
    main()

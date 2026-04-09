#!/usr/bin/env python3
"""从 /tmp/x_results.json 生成 X 预览 MD"""
import json
from datetime import datetime, timezone, timedelta

with open('/tmp/x_results.json') as f:
    results = json.load(f)

now = datetime.now(timezone(timedelta(hours=8)))

# 垃圾内容过滤：AI 生成的套话评论特征
SPAM_PATTERNS = [
    "Here's a high-quality",
    "Here's a high quality",
    "under 270 characters",
    "quote comment for",
    "reply comment for",
]

def is_spam(text):
    for p in SPAM_PATTERNS:
        if p.lower() in text.lower():
            return True
    return False

# 分类关键词
M1_KWS = {'vibe coding game', 'ai game dev', 'cursor unity'}
M2_KWS = {'vibe coding', 'cursor ide'}

# 去重 + 分类（M1 优先）
seen = set()
m1_unique, m2_unique = [], []

for r in results:
    url = r['url']
    text = r['text']
    if url in seen:
        continue
    if is_spam(text):
        continue
    seen.add(url)
    if r['kw'] in M1_KWS:
        m1_unique.append(r)
    else:
        m2_unique.append(r)

print(f'过滤后 M1: {len(m1_unique)} 条, M2: {len(m2_unique)} 条')

lines = []
lines.append('# 🐦 X/Twitter 抓取结果')
lines.append(f'> 生成时间：{now.strftime("%Y-%m-%d %H:%M")} CST | 共 {len(m1_unique)+len(m2_unique)} 条（已过滤垃圾内容）')
lines.append('')

def render_section(title, items):
    lines.append(f'## {title}（{len(items)} 条）')
    lines.append('')
    for i, r in enumerate(items, 1):
        text = r['text'].replace('\n', ' ').strip()
        pub = r['time'][:16].replace('T', ' ') if r.get('time') else '未知时间'
        kw = r.get('kw', '')
        author = r.get('author', 'Unknown')
        likes = r.get('likes', '0')
        lines.append(f'### {i}. @{author}')
        lines.append(f'> 🔍 `{kw}` | 🕐 {pub} UTC | ❤️ {likes}')
        lines.append('')
        lines.append(text[:300])
        lines.append('')
        lines.append(f'🔗 {r["url"]}')
        lines.append('')
        lines.append('---')
        lines.append('')

render_section('🎮 M1：AI + 游戏', m1_unique)
render_section('🤖 M2：AI 通用', m2_unique)

md_content = '\n'.join(lines)
out_path = '/Users/dada/vibe-coding-digest/x_preview.md'
with open(out_path, 'w') as f:
    f.write(md_content)
print(f'✅ 已生成 {out_path} ({len(md_content)} 字符)')

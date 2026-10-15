# -*- coding: utf-8 -*-
"""第 18 轮补丁：全局配色 Quiet Blue -> Airbnb（纯颜色替换）。
严格约束：不改 HTML 结构 / DOM / 交互逻辑 / 布局 / 字号 / 圆角 / 动画，
只做 CSS 颜色值（hex / rgba）与 CSS 注释文案的替换。
"""
import io, re, sys

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
raw = io.open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')

orig_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
orig_len = len(s.encode('utf-8'))

# ---------- 1) hex 颜色映射（大小写不敏感，全词匹配） ----------
HEX_MAP = [
    # —— 强调色：霓虹蓝系 -> Rausch 红系 ——
    ('#2563EB', '#FF385C'),   # Rausch Red（品牌唯一强调色）
    ('#1D4ED8', '#E00B41'),   # Deep Rausch（按压/深色变体）
    ('#3B82F6', '#FF385C'),
    ('#60A5FA', '#FFA3B5'),   # 浅 Rausch（渐变亮端）
    ('#93C5FD', '#FFC9D4'),
    ('#BFDBFE', '#FFDDE4'),
    ('#DBEAFE', '#FFE9ED'),
    ('#EFF6FF', '#FFF1F3'),   # 浅蓝底 -> 浅 Rausch 染色底
    # —— 中性文字：暖黑 + Airbnb 灰阶 ——
    ('#1A1A1A', '#222222'),   # Near Black
    ('#1F1F1F', '#222222'),
    ('#1F2937', '#222222'),
    ('#3F3F46', '#3F3F3F'),   # Focused Gray
    ('#374151', '#3F3F3F'),
    ('#4B5563', '#6A6A6A'),   # Secondary Gray
    ('#6B7280', '#6A6A6A'),
    ('#888888', '#6A6A6A'),
    ('#9CA3AF', '#929292'),   # Disabled
    # —— 边框 / 表面 ——
    ('#D6DAE0', '#C1C1C1'),   # Border Gray（悬停描边）
    ('#E5E7EB', '#EBEBEB'),   # 分割线灰
    ('#ECEEF1', '#EBEBEB'),
    ('#EEF1F5', '#EBEBEB'),
    ('#EAEAEA', '#F2F2F2'),   # Surface
    ('#F3F4F6', '#F2F2F2'),
    ('#F9FAFB', '#F7F7F7'),
    ('#F7F8FA', '#FFFFFF'),   # 画布：纯白
]

LOG = []
for old, new in HEX_MAP:
    pat = re.compile(re.escape(old) + r'\b', re.IGNORECASE)
    n = len(pat.findall(s))
    if n:
        s = pat.sub(new, s)
        LOG.append('%s -> %s  (%d 处)' % (old, new, n))

# ---------- 2) rgba 映射 ----------
RGBA_MAP = [
    ('rgba(37,99,235,',  'rgba(255,56,92,'),   # 蓝 -> Rausch
    ('rgba(17,24,39,',   'rgba(0,0,0,'),       # 冷黑阴影/线 -> 中性黑
    ('rgba(17,17,17,',   'rgba(0,0,0,'),
    ('rgba(247,248,250,.92)', 'rgba(255,255,255,.92)'),  # 导航毛玻璃 -> 白
]
for old, new in RGBA_MAP:
    n = s.count(old)
    if n:
        s = s.replace(old, new)
        LOG.append('%s -> %s  (%d 处)' % (old, new, n))

# ---------- 3) CSS 注释文案同步（不改任何规则） ----------
COMMENTS = [
    ('/* ---------- Mistral AI 设计令牌（暖象牙 / 阳光渐变 / 零圆角锐利几何） ---------- */',
     '/* ---------- Airbnb 设计令牌（纯白画布 / Rausch 红唯一强调 / 暖黑文字） ---------- */'),
    ('/* 霓虹蓝强调色（唯一 accent） */',
     '/* Rausch 红强调色（唯一 accent） */'),
    ('/* 高优先级提示：极细霓虹蓝左侧条（取代旧橙色描边） */',
     '/* 高优先级提示：极细 Rausch 红左侧条 */'),
    ('/* 已完成态：实心橙底白字 + 对勾图标 + 整卡降透明度表示已读 */',
     '/* 已完成态：实心 Rausch 红底白字 + 对勾图标 + 整卡降透明度表示已读 */'),
    ('/* —— 顶部标签筛选：橙色高亮块 transition:transform .3s 平滑滑动（不再生硬变色） —— */',
     '/* —— 顶部标签筛选：Rausch 红高亮块 transition:transform .3s 平滑滑动 —— */'),
]
for old, new in COMMENTS:
    if old in s:
        s = s.replace(old, new)
        LOG.append('注释: %s…' % new[4:24])

# ---------- 4) 写回与自检 ----------
out = s.replace('\n', '\r\n') if crlf else s
io.open(P, 'w', encoding='utf-8', newline='').write(out)

new_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
assert new_ids == orig_ids, '节点标记集合发生变化!'
assert len(new_ids) == 207, '节点标记数不是 207!'

print('== 替换日志 ==')
for l in LOG:
    print(' ', l)
print('节点标记: %d 个，集合守恒' % len(new_ids))
print('字节数: %d -> %d' % (orig_len, len(s.encode('utf-8'))))

# 残留扫描：旧主题色应清零
residue = ['#2563EB', '#1D4ED8', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE',
           '#DBEAFE', '#EFF6FF', '#1A1A1A', '#1F1F1F', '#1F2937', '#3F3F46',
           '#374151', '#4B5563', '#6B7280', '#888888', '#9CA3AF', '#D6DAE0',
           '#E5E7EB', '#ECEEF1', '#EEF1F5', '#EAEAEA', '#F3F4F6', '#F9FAFB',
           '#F7F8FA', 'rgba(37,99,235', 'rgba(17,24,39', 'rgba(17,17,17',
           'rgba(247,248,250']
bad = [t for t in residue
       if re.search(re.escape(t) + r'\b', s, re.IGNORECASE)]
print('旧色残留:', bad if bad else '清零')
sys.exit(1 if bad else 0)

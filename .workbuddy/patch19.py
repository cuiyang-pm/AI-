# -*- coding: utf-8 -*-
"""第 19 轮补丁：纯配色换肤 Airbnb Rausch 红 -> 现代学院风 / 勃艮第红。
严格约束：不改 HTML 结构 / DOM / 交互逻辑 / 布局 / 字号 / 圆角 / 动画，
只做 CSS 颜色值、:root 语义令牌与 CSS 注释的替换。
"""
import io, re, sys

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
raw = io.open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')

orig_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
orig_len = len(s.encode('utf-8'))
LOG = []

# ---------- 1) hex 全词映射（大小写不敏感） ----------
HEX_MAP = [
    # —— 强调色：Rausch 红系 -> 勃艮第红系 ——
    ('#FF385C', '#8B3A3A'),   # 勃艮第红（唯一 accent）
    ('#E00B41', '#6E2B2B'),   # 深勃艮第（按压/悬停变体）
    ('#FFA3B5', '#D3A5A5'),   # 浅勃艮第（渐变亮端）
    ('#FFC9D4', '#D9B3B3'),
    ('#FFDDE4', '#F4EAEA'),   # -> accent-light
    ('#FFE9ED', '#F4EAEA'),
    ('#FFF1F3', '#F4EAEA'),
    # —— 中性文字：暖灰学院风 ——
    ('#6A6A6A', '#7A7571'),   # text-secondary 暖灰
    ('#929292', '#A5A09B'),   # 弱化文字（暖灰）
    ('#3F3F3F', '#7A7571'),
    # —— 边框 / 表面 ——
    ('#EBEBEB', '#E8E4DF'),   # border-light 浅米色
    ('#C1C1C1', '#D8D2CB'),   # 悬停描边（暖一档）
    ('#F2F2F2', '#F1EEE9'),   # 中性浅暖表面（卡片内小标签底）
    ('#F7F7F7', '#F7F5F2'),   # 已读卡底
]
for old, new in HEX_MAP:
    pat = re.compile(re.escape(old) + r'\b', re.IGNORECASE)
    n = len(pat.findall(s))
    if n:
        s = pat.sub(new, s)
        LOG.append('%s -> %s  (%d 处)' % (old, new, n))

# ---------- 2) rgba 映射 ----------
RGBA_MAP = [
    ('rgba(255,56,92,', 'rgba(139,58,58,'),   # Rausch -> 勃艮第 (8B3A3A)
    ('rgba(0,0,0,',     'rgba(80,60,60,'),    # 中性阴影/线 -> 暖调基底 (503C3C)
]
for old, new in RGBA_MAP:
    n = s.count(old)
    if n:
        s = s.replace(old, new)
        LOG.append('%s... -> %s...  (%d 处)' % (old, new, n))

# ---------- 3) 定点替换（令牌值 / 规则级微调） ----------
TARGETED = [
    # 页面画布：米白（仅动令牌值，#FFFFFF 其余用途——卡片底/反白文字——不受影响）
    ('    --m-ivory:#FFFFFF;', '    --m-ivory:#F9F8F6;'),
    # 卡片阴影：按用户规格换几何与暖色基底
    ('    --shadow-card:0 2px 8px rgba(80,60,60,.04);',
     '    --shadow-card:0 4px 12px rgba(80,60,60,.04);'),
    # 重要度标签：accent-light 底 + accent-primary 字
    ('  .lvl-high{background:#F1EEE9;border:1px solid transparent;color:#7A7571}',
     '  .lvl-high{background:#F4EAEA;border:1px solid transparent;color:#8B3A3A}'),
    ('  .lvl-mid{background:#F1EEE9;border:1px solid transparent;color:#7A7571}',
     '  .lvl-mid{background:#F4EAEA;border:1px solid transparent;color:#8B3A3A}'),
    # 关键词标签：accent-light 底 + accent-primary 字（用户方案一）
    ('    color:#7A7571;\n    background:#F1EEE9;\n    border:1px solid transparent;border-radius:6px;',
     '    color:#8B3A3A;\n    background:#F4EAEA;\n    border:1px solid transparent;border-radius:6px;'),
    # 浓度条外框：border-light
    ('  .density-bar{height:4px;border-radius:2px;background:var(--blue-tint);overflow:hidden;margin-top:6px}',
     '  .density-bar{height:4px;border-radius:2px;background:#E8E4DF;overflow:hidden;margin-top:6px}'),
]
for old, new in TARGETED:
    n = s.count(old)
    if n != 1:
        print('FAIL 定点替换匹配 %d 处: %r' % (n, old[:60]))
        sys.exit(1)
    s = s.replace(old, new, 1)
    LOG.append('定点: %s…' % new.strip()[:44])

# ---------- 4) 注入用户指定的 :root 语义令牌块 ----------
ANCHOR = '    --shadow-deep:0 10px 24px rgba(80,60,60,.08);\n  }\n'
NEW_ROOT = ANCHOR + '''
  /* ---------- 勃艮第红 / 现代学院风语义令牌（第 19 轮） ---------- */
  :root{
    /* 页面背景：带一点暖调的米白色 */
    --bg-page:#F9F8F6;
    /* 卡片背景：纯白 */
    --bg-card:#FFFFFF;
    /* 主文字：深炭黑 */
    --text-main:#222222;
    /* 次要文字：暖灰色 */
    --text-secondary:#7A7571;
    /* 强调色：沉稳的勃艮第红 */
    --accent-primary:#8B3A3A;
    /* 强调色背景：极浅的豆沙色 */
    --accent-light:#F4EAEA;
    /* 分割线：浅米色 */
    --border-light:#E8E4DF;
    /* 阴影：暖调极轻阴影 */
    --shadow-card:0 4px 12px rgba(80,60,60,.04);
  }
'''
n = s.count(ANCHOR)
if n != 1:
    print('FAIL :root 注入锚点匹配 %d 处' % n)
    sys.exit(1)
s = s.replace(ANCHOR, NEW_ROOT, 1)
LOG.append('注入: :root 勃艮第红语义令牌块（9 个变量）')

# ---------- 5) CSS 注释文案同步 ----------
COMMENTS = [
    ('/* ---------- Airbnb 设计令牌（纯白画布 / Rausch 红唯一强调 / 暖黑文字） ---------- */',
     '/* ---------- 勃艮第红设计令牌（米白画布 / 勃艮第红唯一强调 / 暖黑文字） ---------- */'),
    ('/* Rausch 红强调色（唯一 accent） */',
     '/* 勃艮第红强调色（唯一 accent） */'),
    ('/* 高优先级提示：极细 Rausch 红左侧条 */',
     '/* 高优先级提示：极细勃艮第红左侧条 */'),
    ('/* 已完成态：实心 Rausch 红底白字 + 对勾图标 + 整卡降透明度表示已读 */',
     '/* 已完成态：实心勃艮第红底白字 + 对勾图标 + 整卡降透明度表示已读 */'),
    ('/* —— 顶部标签筛选：Rausch 红高亮块 transition:transform .3s 平滑滑动 —— */',
     '/* —— 顶部标签筛选：勃艮第红高亮块 transition:transform .3s 平滑滑动 —— */'),
]
for old, new in COMMENTS:
    if old in s:
        s = s.replace(old, new, 1)
        LOG.append('注释: %s' % new[4:26])

# ---------- 6) 写回与自检 ----------
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

# 残留扫描：旧 Rausch 系应清零
residue = ['#FF385C', '#E00B41', '#FFA3B5', '#FFC9D4', '#FFDDE4', '#FFE9ED',
           '#FFF1F3', '#6A6A6A', '#929292', '#3F3F3F', '#EBEBEB', '#C1C1C1',
           '#F2F2F2', '#F7F7F7', 'rgba(255,56,92', 'rgba(0,0,0']
bad = [t for t in residue if t in s]
print('旧色残留:', bad if bad else '清零')
sys.exit(1 if bad else 0)

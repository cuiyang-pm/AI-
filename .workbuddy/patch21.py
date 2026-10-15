# -*- coding: utf-8 -*-
"""第 21 轮补丁：细节质感增强（纯 CSS 覆盖层，不改结构 / 交互 / 布局）
1. 板块分布：数字旁 40×4px 迷你进度条（浅灰轨道 + 勃艮第红填充，比例 = 条数×20%）
2. 新闻卡片：极轻悬浮阴影 0 2px 10px rgba(0,0,0,.03) + 微弱米白底色 rgba(249,248,246,.8)
3. 阅读进度：「N / 3 篇已读」数字加粗；进度条升级「充电电池」质感（细描边 + 内高光 + 填充光泽）
"""
import sys

PATH = r"C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html"

with open(PATH, "r", encoding="utf-8", newline="") as f:
    raw = f.read()

crlf = "\r\n" in raw
text = raw.replace("\r\n", "\n")

def sub(old, new, label):
    global text
    n = text.count(old)
    if n != 1:
        print("FAIL [%s]: anchor count = %d" % (label, n))
        sys.exit(1)
    text = text.replace(old, new, 1)
    print("OK  [%s]" % label)

CSS = """
  /* ============================================================
     第 21 轮 · 细节质感增强（纯 CSS 覆盖，不改结构 / 交互 / 布局）
     ============================================================ */

  /* —— 1. 板块分布迷你进度条：数字右侧 40×4px 圆角条，
        浅灰轨道 var(--border-light) + 勃艮第红填充 var(--accent-primary)，
        填充比例 = 今日条数 × 20%（3→60%、1→20%，满值封顶），--bw 由渲染钩子写入 —— */
  .titem::after{display:none} /* 收起第 20 轮的行底柱状条，升级为数字旁迷你条 */
  .tright::after{
    content:"";flex:0 0 40px;width:40px;height:4px;border-radius:2px;
    background:linear-gradient(90deg,var(--accent-primary) calc(var(--bw,0)*20%),var(--border-light) 0);
  }
  .titem[aria-disabled="true"] .tright::after{opacity:.45}

  /* —— 2. 新闻卡片：极轻悬浮阴影 + 微弱米白底色，与纯白面板形成极细腻区分 —— */
  .news{background:rgba(249,248,246,.8);box-shadow:0 2px 10px rgba(0,0,0,.03)}

  /* —— 3a. 「N / 3 篇已读」数字加粗提色 —— */
  .pd b{font-weight:600;color:var(--text-main)}

  /* —— 3b. 进度条「充电电池」质感：极细描边 + 顶部内高光 + 填充层光泽 ——
        （box-sizing:border-box，高度含描边；padding-top 同步 -2px 保持面板不溢出） */
  .progress{padding-top:6px;gap:5px}
  .pbar{
    height:5px;border-radius:3px;
    background:#EFECE8;
    border:1px solid rgba(80,60,60,.14);
    box-shadow:inset 0 1px 1px rgba(255,255,255,.85),inset 0 -1px 1px rgba(80,60,60,.06);
  }
  .pbar-fill{
    border-radius:2px;
    background-color:var(--accent-primary);
    background-image:linear-gradient(180deg,rgba(255,255,255,.30),rgba(255,255,255,0) 50%);
  }

"""

ANCHOR = "  /* —— 装饰层移动端收敛 —— */"
sub(ANCHOR, CSS + ANCHOR, "r21-layer")

out = text.replace("\n", "\r\n") if crlf else text
with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out)

print("DONE. bytes =", len(out.encode("utf-8")), "| CRLF =", crlf)

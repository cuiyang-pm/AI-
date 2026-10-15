# -*- coding: utf-8 -*-
"""第 20b 轮补丁：面板纵向密度收紧
为新增装饰元素（主编短评 / 浓度圆环 / 微型柱状图 / 已阅印章）腾出纵向空间，
确保「今日阅读进度 + 已阅印章」完整落在 900px 画板内。
只收紧间距 / 字号，不改结构与交互。
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
  /* —— 第 20b 轮 · 面板纵向密度收紧：为新增装饰元素腾出空间，
        确保「今日阅读进度 + 已阅印章」完整落在画板内（只收间距 / 字号） —— */
  .panel{gap:6px;padding:16px 20px}
  .phead h2{font-size:20px}
  .phead .en{margin-top:3px}
  .panel > .hero ~ div{padding-top:10px}
  .hero{padding:10px 14px}
  .hero-numwrap{gap:5px}
  .hero .num{font-size:40px;letter-spacing:-1.2px}
  .density{gap:8px}
  .density-bar{
    flex:0 0 24px;width:24px;height:24px;
    -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 3px));
            mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 3px));
  }
  .hero-numwrap::after{margin-top:5px;font-size:11.5px;line-height:1.5}
  .tlist{margin-top:6px!important}
  .titem{margin-bottom:4px;padding:2px 8px}
  .kw{margin-top:6px!important}
  .kw span{padding:3px 9px;font-size:11.5px}
  .kwcap{margin-top:5px}
  .progress{padding-top:8px;gap:6px}
  .pinfo .pt::after{width:24px;height:24px;font-size:9px;letter-spacing:1px;text-indent:1px}

"""

ANCHOR = "  /* —— 装饰层移动端收敛 —— */"
sub(ANCHOR, CSS + ANCHOR, "squeeze-layer")

out = text.replace("\n", "\r\n") if crlf else text
with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out)

print("DONE. bytes =", len(out.encode("utf-8")), "| CRLF =", crlf)

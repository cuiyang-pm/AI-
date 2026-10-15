# -*- coding: utf-8 -*-
"""第 20 轮补丁：装饰性视觉增强（纯装饰层，不改结构 / 交互 / 布局）
- 右上角期刊胶囊（CSS ::after）
- 卡片顶部 1px 渐变细线（::before）
- 卡片底部阅读进度条（::after，已读 scaleX 0->100%）
- 主编短评便利贴（hero ::after）
- 浓度圆环（conic-gradient + mask，视觉等同 SVG 环，零 DOM 改动）
- 板块分布微型柱状图（titem::after，--bw 由 renderPanel 写入）
- 来源小圆点胶囊（src::before）
- 左右分区竖向渐变微线（main::before）
- 已阅印章（pt::after，.progress.is-full 点亮）
- 主体点状网格纹理（main 背景）
附加 JS 仅三行渲染钩子：is-full / --dp / --bw（不改变任何交互逻辑）
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

# ---------- 1. JS 渲染钩子（三行，纯附加） ----------
sub(
    """    readFill.style.width = pct + '%';
    readCount.textContent = done;
""",
    """    readFill.style.width = pct + '%';
    readCount.textContent = done;
    // 装饰钩子：进度 100% 时点亮「已阅」印章（不改任何交互逻辑）
    var progBox = readFill.closest('.progress');
    if (progBox) progBox.classList.toggle('is-full', pct >= 100);
""",
    "js-hook is-full",
)

sub(
    """    densityFill.style.width = pctW + '%';
""",
    """    densityFill.style.width = pctW + '%';
    densityBox.style.setProperty('--dp', pctW); /* 装饰钩子：浓度圆环角度 */
""",
    "js-hook --dp",
)

sub(
    """      li.querySelector('.tnum').textContent = tb;
""",
    """      li.querySelector('.tnum').textContent = tb;
      li.style.setProperty('--bw', tb); /* 装饰钩子：微型柱状图长度 */
""",
    "js-hook --bw",
)

# ---------- 2. CSS 装饰层（插在 reduced-motion 块之前） ----------
CSS = """
  /* ============================================================
     第 20 轮 · 装饰性视觉增强（只加装饰，不改结构 / 交互 / 布局）
     ============================================================ */

  /* —— 1. 右上角期刊胶囊：极细边框浅灰胶囊，填堵大标题行右侧空白，增加期刊感 —— */
  .hero-head::after{
    content:"VOL. 013 · 09 / 16 · WED";
    margin-left:auto;flex:0 0 auto;
    font-family:var(--font-mono);font-size:11px;font-weight:400;letter-spacing:1.2px;
    color:#A5A09B;white-space:nowrap;
    border:1px solid var(--border-light);border-radius:999px;
    padding:6px 14px;background:rgba(255,255,255,.55);
  }

  /* —— 2. 卡片顶部 1px 渐变细线：两端透明、中间勃艮第红，作为卡片的顶部分割 —— */
  .news::before{
    content:"";position:absolute;left:0;right:0;top:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--accent-primary) 50%,transparent);
    opacity:.55;pointer-events:none;
  }
  /* 头条卡原 4px 实色顶条一并统一为渐变细线（更轻盈） */
  .card-feat::before{
    height:1px;border-radius:12px 12px 0 0;
    background:linear-gradient(90deg,transparent,var(--accent-primary) 50%,transparent);
    opacity:.9;
  }

  /* —— 3. 卡片底部阅读进度条：默认 0%，点「标记已读」后 scaleX 0 -> 100%，勃艮第红渐变 —— */
  .news::after{
    content:"";position:absolute;left:0;right:0;bottom:0;height:2px;
    background:linear-gradient(90deg,#D3A5A5,var(--accent-primary));
    transform:scaleX(0);transform-origin:left center;
    transition:transform .55s cubic-bezier(.22,.72,.2,1);
    border-radius:0 0 12px 12px;pointer-events:none;z-index:1;
  }
  .news.done::after{transform:scaleX(1)}

  /* —— 4. 主编短评（便利贴）：13 / TODAY'S SELECTED 下方的一行斜体短句，前带引言引号 —— */
  .hero-numwrap::after{
    content:"\\201C 今日模型竞争白热化，Google 双发抢占心智。\\201D";
    display:block;margin-top:10px;
    font-size:12px;font-style:italic;font-weight:400;line-height:1.6;letter-spacing:0;
    color:#7A7571;
  }

  /* —— 5. 浓度圆环：与 SVG 环同款视觉（浅灰底环 + 勃艮第红进度），
        用 conic-gradient + donut mask 实现，零 DOM 改动，--dp 由渲染钩子写入 —— */
  .density{display:flex;align-items:center;gap:10px}
  .density-label{flex:1;min-width:0}
  .density-bar{
    flex:0 0 30px;width:30px;height:30px;margin-top:0;
    border-radius:50%;
    background:conic-gradient(var(--accent-primary) calc(var(--dp,44)*1%),#E8E4DF 0);
    -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3.5px),#000 calc(100% - 3.5px));
            mask:radial-gradient(farthest-side,transparent calc(100% - 3.5px),#000 calc(100% - 3.5px));
  }
  .density-bar span{display:none}
  .density.down .density-bar,
  .density.flat .density-bar{background:conic-gradient(#A5A09B calc(var(--dp,44)*1%),#E8E4DF 0)}

  /* —— 6. 板块分布微型柱状图：每行底部一条极细浅色条，长度与今日条数成正比（--bw） —— */
  .titem{position:relative}
  .titem::after{
    content:"";position:absolute;left:8px;bottom:-5px;height:3px;border-radius:2px;
    width:calc(var(--bw,0) * 100% / 7);
    max-width:calc(100% - 16px);min-width:0;
    background:var(--accent-light);
    pointer-events:none;
  }
  .titem[aria-disabled="true"]::after{opacity:.5}

  /* —— 7. 来源胶囊：小圆点 + 浅灰底圆角胶囊，增加卡片细节 —— */
  .src{
    display:inline-flex;align-items:center;gap:6px;min-width:0;max-width:75%;
    background:#F1EEE9;border:1px solid transparent;border-radius:999px;
    padding:3px 10px;
  }
  .src::before{
    content:"";flex:0 0 5px;width:5px;height:5px;border-radius:50%;
    background:#A5A09B;
  }

  /* —— 8. 左右分区装饰微线：两端透明、中间浅灰的竖向渐变细线，分隔「阅读区 / 数据区」 —— */
  .main{position:relative}
  .main::before{
    content:"";position:absolute;top:6px;bottom:6px;right:421px;width:1px;
    background:linear-gradient(180deg,transparent,var(--border-light) 40%,var(--border-light) 60%,transparent);
    pointer-events:none;
  }

  /* —— 9. 已阅印章：阅读进度旁的小圆章，进度 100% 时点亮为勃艮第红 —— */
  .pinfo .pt{display:flex;align-items:center;gap:8px}
  .pinfo .pt::after{
    content:"已阅";
    width:30px;height:30px;border-radius:50%;
    display:grid;place-items:center;
    font-size:10px;font-style:normal;letter-spacing:2px;text-indent:2px;
    color:#A5A09B;border:1px solid var(--border-light);background:transparent;
    transition:color .3s,border-color .3s,background .3s;
  }
  .progress.is-full .pt::after{
    color:var(--accent-primary);border-color:var(--accent-primary);background:var(--accent-light);
  }

  /* —— 10. 主体点状网格纹理：极低对比度圆点，让背景不再是死板的色块 —— */
  .main{
    background-image:radial-gradient(var(--border-light) 1px,transparent 1px);
    background-size:20px 20px;
  }

  /* —— 装饰层移动端收敛 —— */
  @media (max-width:860px){
    .main::before{display:none}
    .hero-head::after{margin-left:0}
  }

"""

ANCHOR = "  @media (prefers-reduced-motion:reduce){"
sub(ANCHOR, CSS + ANCHOR, "css-layer")

out = text.replace("\n", "\r\n") if crlf else text
with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out)

print("DONE. bytes =", len(out.encode("utf-8")), "| CRLF =", crlf)

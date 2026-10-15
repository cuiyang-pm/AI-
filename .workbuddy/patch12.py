# -*- coding: utf-8 -*-
"""
第 12 轮改造补丁：重做右侧「今日趋势」面板
① 板块分布 -> 纯垂直列表（左分类名 / 右今日数 + 昨日增减箭头）
② 热点关键词 -> 统一圆角胶囊 + flex-wrap 流式 + 点击按压缩放
③ 阅读进度 -> 删圆形进度环，改轻量线性条（灰底/橙前景/6px/圆角3px）+ "1/3 篇已读"
④ 整体降噪 -> 去面板外框，只留极浅左分割线；数据文字统一 12px / #4B5563
⑤ 375px 小屏响应式加固
所有 207 个 data-page-node-id 全部复用保留（含被删圆环的 SVG 内部标记）。
"""
import io, sys

P = r"C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html"
s = io.open(P, encoding="utf-8").read()
n0 = s.count("data-page-node-id")
log = []

def splice(start, end, new, label):
    global s
    i = s.index(start)
    j = s.index(end, i) + len(end)
    s = s[:i] + new + s[j:]
    log.append(label)

def rep(old, new, label, count=1):
    global s
    got = s.count(old)
    assert got == count, "%s: expect %d got %d" % (label, count, got)
    s = s.replace(old, new)
    log.append(label)

def cut(start, end, new, label):
    """替换 [start, end) 区间，end 之后的内容原样保留"""
    global s
    i = s.index(start)
    j = s.index(end, i)
    s = s[:i] + new + s[j:]
    log.append(label)


# =====================================================================
# 1) 右侧面板整段 CSS 重写（从面板注释头到 .ghost:focus-visible 结束）
# =====================================================================
NEW_CSS = u"""  /* ============ 右侧趋势面板（降噪版：去外框 + 极浅左分割线 + 安静的数据排版） ============ */
  .panel{
    height:100%;display:flex;flex-direction:column;gap:18px;
    padding:2px 0 2px 24px;
    border:none;
    border-left:1px solid var(--line-light);
    border-radius:0;
    background:transparent;
    box-shadow:none;
    animation:rise .6s cubic-bezier(.22,.72,.2,1) .1s backwards;
  }
  .phead{padding-bottom:0;border-bottom:none}
  .phead h2{font-family:var(--font-display);font-size:22px;font-weight:400;line-height:1.2;letter-spacing:-.3px;color:var(--ink)}
  .phead .en{
    font-family:var(--font-sans);font-size:12px;font-weight:400;letter-spacing:2px;
    color:#4B5563;text-transform:uppercase;margin-top:6px;
  }

  .hero{display:flex;align-items:flex-end;gap:10px}
  .hero .num{font-family:var(--font-mono);font-size:32px;font-weight:400;line-height:1;letter-spacing:-1px;color:#4B5563}
  .hero .unit{font-size:12px;font-weight:400;color:#4B5563;line-height:1.6;padding-bottom:2px}
  .hero .unit b{display:block;font-family:var(--font-mono);font-size:12px;color:#4B5563;font-weight:400}

  .block-title{
    display:flex;align-items:baseline;justify-content:space-between;gap:10px;
    font-family:var(--font-sans);font-size:12px;font-weight:400;
    letter-spacing:2px;color:#4B5563;text-transform:uppercase;
  }
  .legend{display:flex;gap:10px;font-family:var(--font-sans);font-size:11px;font-weight:400;letter-spacing:0;color:#4B5563;text-transform:none}
  .legend span{display:inline-flex;align-items:center;gap:4px;white-space:nowrap}
  .legend em{display:inline-block;width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent}
  .legend .l-up{border-bottom:6px solid #E5484D}
  .legend .l-down{border-top:6px solid #16A34A}

  /* —— 板块分布：纯垂直列表（左分类名 / 右今日数 + 昨日增减箭头），无线条，靠 margin 分隔 —— */
  .tlist{list-style:none;display:flex;flex-direction:column}
  .titem{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:11px}
  .titem:last-child{margin-bottom:0}
  .tleft{min-width:0;display:flex;align-items:center}
  .tname{font-size:12px;font-weight:400;color:#4B5563;line-height:1.4;letter-spacing:0;overflow-wrap:break-word}
  .tright{display:flex;align-items:baseline;gap:8px;flex:0 0 auto}
  .tnum{font-family:var(--font-mono);font-size:12px;font-weight:400;color:#4B5563}
  .tdelta{
    display:inline-flex;align-items:center;justify-content:flex-end;gap:1px;
    min-width:32px;font-family:var(--font-mono);font-size:12px;font-style:normal;font-weight:400;letter-spacing:.2px;
  }
  .tdelta.up{color:#E5484D}
  .tdelta.down{color:#16A34A}
  .tdelta.flat{color:#9CA3AF}
  .tdelta .arw,.tdelta .dl{font-style:normal}
  .tdelta.flat .dl:empty{display:none}

  /* —— 热点关键词：统一圆角胶囊 + 自然流式换行 + 点击按压缩放 —— */
  .kw{display:flex;flex-wrap:wrap;gap:8px}
  .kw span{
    font-family:var(--font-sans);font-size:12px;font-weight:400;letter-spacing:0;
    color:#4B5563;
    background:#F3F4F6;
    border:none;border-radius:20px;
    padding:6px 13px;cursor:pointer;max-width:100%;overflow-wrap:anywhere;
    transition:background .2s,transform .18s cubic-bezier(.2,.8,.2,1);
  }
  .kw span.hot{background:#FFF7ED}
  .kw span:hover{background:#E5E7EB}
  .kw span.hot:hover{background:#FFEDD5}
  .kw span:active{transform:scale(.94)}
  .kw span.kwpop{animation:kwPop .3s cubic-bezier(.34,1.56,.64,1)}
  @keyframes kwPop{0%{transform:scale(1)}42%{transform:scale(.9)}100%{transform:scale(1)}}
  .kwcap{display:flex;align-items:center;gap:14px;margin-top:10px;font-size:11px;font-weight:400;letter-spacing:0;color:#4B5563}
  .kwcap .kc{display:inline-flex;align-items:center;gap:5px}
  .kwcap em{display:inline-block;width:10px;height:10px;border-radius:20px}
  .kwcap .kd-today{background:#FFF7ED;box-shadow:inset 0 0 0 1px rgba(250,82,15,.28)}
  .kwcap .kd-yest{background:#F3F4F6}
  .kwcap .kt{font-style:normal}
  .kwcap .kmore{margin-left:auto;color:#9CA3AF}

  /* —— 阅读进度：轻量线性条（灰底 / 橙前景 / 6px / 圆角 3px），取代原有圆形进度环 —— */
  .progress{
    margin-top:auto;padding-top:16px;
    border-top:1px solid var(--line-light);
    display:flex;flex-direction:column;gap:10px;
  }
  .pinfo{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .pinfo .pt{font-size:12px;font-weight:400;letter-spacing:0;color:#4B5563}
  .pbar{height:6px;border-radius:3px;background:#E5E7EB;overflow:hidden}
  .pbar-fill{
    display:block;height:100%;width:0;border-radius:3px;
    background:var(--m-orange);
    transition:width .55s cubic-bezier(.22,.72,.2,1);
  }
  .pd{font-size:12px;font-weight:400;color:#4B5563;line-height:1.6}
  .pd b{font-family:var(--font-mono);font-size:12px;font-weight:400;color:#4B5563}
  .ghost{
    cursor:pointer;flex:0 0 auto;
    font-family:var(--font-sans);font-size:12px;font-weight:400;letter-spacing:0;text-transform:none;
    color:#4B5563;background:transparent;
    border:1px solid #E5E7EB;border-radius:20px;
    padding:4px 12px;
    transition:background .2s,border-color .2s,color .2s;
  }
  .ghost:hover{background:#FFF7ED;border-color:rgba(250,82,15,.35);color:#C2410C}
  .ghost:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}"""

splice(
    u"  /* ============ 右侧趋势面板（Mistral 白卡变体：最大对比 + 金色描边） ============ */",
    u"  .ghost:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}",
    NEW_CSS,
    "CSS: 右侧面板整段重写",
)

# =====================================================================
# 2) 移动端面板覆盖（去左分割线 / 改顶部细线）
# =====================================================================
rep(
    u"    .right{width:auto;flex:none;margin-top:14px}\n    .panel{height:auto}",
    u"    .right{width:auto;flex:none;margin-top:18px;padding-top:18px;border-top:1px solid var(--line-light)}\n"
    u"    .panel{height:auto;padding:0;border-left:none;gap:16px}",
    "CSS: 移动端 .right/.panel 覆盖",
)

# =====================================================================
# 3) 新增 ≤420px 小屏加固块（插在顶部滚动进度条注释前）
# =====================================================================
SMALL = u"""  /* ============================================================
     小屏（≤420px，覆盖 375px）：再收一档边距，标签强制换行不溢出
     ============================================================ */
  @media (max-width:420px){
    .nav{padding:10px 12px}
    .hero-band{padding:18px 12px 16px}
    .main{padding:12px 12px 0}
    .card-feat{padding:14px}
    .news:not(.card-feat){padding:14px}
    .ndesc{overflow-wrap:anywhere}
    .nstat{gap:6px}
    .nstat span{max-width:100%;white-space:normal;overflow-wrap:anywhere}
    .nfoot{gap:4px 8px}
    .src{font-size:11.5px}
    .titem{gap:8px;margin-bottom:10px}
    .tname{font-size:12px}
    .kw{gap:7px}
    .kw span{padding:5px 11px}
    .kwcap{gap:10px}
    .kwcap .kmore{display:none}
    .footbar{padding:14px 12px 18px}
  }

"""
rep(
    u"  /* 顶部滚动进度条：2px 橙色渐变，随页面滚动 0% → 100% */",
    SMALL + u"  /* 顶部滚动进度条：2px 橙色渐变，随页面滚动 0% → 100% */",
    "CSS: 新增 ≤420px 小屏加固块",
)

# =====================================================================
# 4) HTML：板块分布图例 -> 增减箭头说明
# =====================================================================
rep(
    u'<span data-page-node-id="0qezLTocWZ1HUpLor1kgW8"><em class="l-today" data-page-node-id="ftirrGZUXxXUKNCZYVSPqA"></em>今日</span>\n'
    u'              <span data-page-node-id="NR76ISECHnzsilrSElF5x5"><em class="l-yest" data-page-node-id="lrGIhqR4J9i1MEgP3FMqD8"></em>昨日</span>',
    u'<span data-page-node-id="0qezLTocWZ1HUpLor1kgW8"><em class="l-up" data-page-node-id="ftirrGZUXxXUKNCZYVSPqA"></em>较昨日增</span>\n'
    u'              <span data-page-node-id="NR76ISECHnzsilrSElF5x5"><em class="l-down" data-page-node-id="lrGIhqR4J9i1MEgP3FMqD8"></em>减</span>',
    "HTML: 板块分布图例改为增减说明",
)

# =====================================================================
# 5) HTML：板块分布 -> 垂直列表（换掉 bars 柱状图，保留全部 40 个节点标记）
# =====================================================================
# (分类名, 今日数, 方向, 增减值, [row, ttrack, tname, tval, tnum, tdelta, todaybar, yestbar])
ROWS = [
    (u"模型发布/更新", u"3", u"up", u"1", ["E8sqPUNxpHRzUf95Hj8ype", "HL9Pb5i56GktatqfEY9Vt9", "JjL3HYxj9QBRNYzCDaB2V2", "7qFAHTNcdVIktlacKn8yd4", "H41B67PgLJANimKWGNBRAE", "z2n2UnQYABUMOxGEwoO9J8", "9fwThM90QR886illX7GmRm", "0z8UEw5pDICaDertDR38td"]),
    (u"产品发布/更新", u"2", u"up", u"1", ["KqVVH44Lhj9HZhSaBZzaAW", "l8XlYgZpFdnaVDufy98oP8", "dAKNgVq8kJ0oZL79AnpFar", "udI14yVoNgQFIZqrtZzHaX", "YcZiHaV5R3Ipb77iMUKa1Y", "SlTl5aIEGtXyqbrN7A5gGH", "Ni7Nf7YEhkKQ3G3pLCPD1W", "rZG25vIEQDDMhcaklK5Nmx"]),
    (u"行业动态", u"1", u"flat", u"", ["USgHMYNYxlgYPZLg3VGoES", "TVW970kjjxclwaBpCEKSmd", "GQy4VlrCxtyUoXF6DtT5V0", "qxVQ3ZEweGMfVvI3QVZGFV", "0csa13aolzGFla9BOvFy5E", "iLcWjtn5XCkz861N9aBO6B", "82FoS0U3STfGsrhpEre245", "Roy25x2q1cfBHqPEuCKJuL"]),
    (u"技巧与观点", u"7", u"up", u"3", ["MqpaFqdxFzws4iGAZBFvWl", "HibWFfq9ObmqpPizs1OG8f", "ttXI3QNAO1aKezKJywRQGc", "CDbftzslvTupx96vEgqIiL", "WgbYPWvmlvxrLibzJ0GdHp", "F5RqDqqjloABizgtlfWk8U", "BEyASPhBqBlOrHx2NEZRnv", "i8ECa0NQe5x7ctQrbg2Gzl"]),
    (u"论文研究", u"0", u"down", u"1", ["2vgtwaqc5ZMj7F4gtFdBAX", "AqUOgF2jHPgt7RGrb34xD3", "bFkL4r8P7iA94SxvGV23ID", "vVXZtgl1qyxNVDMNOWHqfG", "DOOwPR1RSMu8rqJTYozrgj", "7U2AKXYm42lkTBpY1tTeZy", "cmZzri9ooNLg4G1NofzJM7", "pQ8j7fdS5477Q0rbelANaS"]),
]
ARROW = {u"up": u"\u2191", u"down": u"\u2193", u"flat": u"\u2014"}

rows_html = []
for name, num, d, val, ids in ROWS:
    row_id, track_id, name_id, tval_id, tnum_id, tdelta_id, tbar1_id, tbar2_id = ids
    rows_html.append(
        u'            <li class="titem" data-page-node-id="%s">\n'
        u'              <span class="tleft" data-page-node-id="%s"><span class="tname" data-page-node-id="%s">%s</span></span>\n'
        u'              <span class="tright" data-page-node-id="%s"><b class="tnum" data-page-node-id="%s">%s</b>'
        u'<em class="tdelta %s" data-page-node-id="%s"><span class="arw" data-page-node-id="%s">%s</span>'
        u'<span class="dl" data-page-node-id="%s">%s</span></em></span>\n'
        u'            </li>'
        % (row_id, track_id, name_id, name, tval_id, tnum_id, num,
           d, tdelta_id, tbar1_id, ARROW[d], tbar2_id, val)
    )

NEW_BARS = (
    u'          <ul class="tlist" style="margin-top:12px" data-page-node-id="DSUiFgd79ba1jnulJFEsrH">\n'
    + u"\n".join(rows_html)
    + u"\n          </ul>\n        </div>\n\n"
)

splice(
    u'          <div class="bars" style="margin-top:14px" data-page-node-id="DSUiFgd79ba1jnulJFEsrH">',
    u'        <div data-page-node-id="EoEHN12iHp13zCPUHIcnHB">',
    NEW_BARS + u'        <div data-page-node-id="EoEHN12iHp13zCPUHIcnHB">',
    "HTML: 板块分布改为垂直列表",
)

# =====================================================================
# 6) HTML：热点关键词后补一枚图例（承接被删圆环的 5 个 SVG 内部节点标记）
# =====================================================================
KWCAP = (
    u'          </div>\n'
    u'          <div class="kwcap" data-page-node-id="jyGRyDJLVOSSJnJm56RD0V">\n'
    u'            <span class="kc" data-page-node-id="coNITb6rLaVeKipTxHtUxF"><em class="kdot kd-today" data-page-node-id="53HxSJS2X2wzcDGbRS2PvC"></em><i class="kt" data-page-node-id="GJbnRpJqvYXHJr6VAjAssD">今日高热</i></span>\n'
    u'            <span class="kc" data-page-node-id="Aw3rxGhQLhGUSyLMsFPIsF"><em class="kdot kd-yest" data-page-node-id="xjxqyuZcgy0FDeZDWFxD3B"></em><i class="kt" data-page-node-id="54qc4T0OKlivH00UCxpqya">常态关注</i></span>\n'
    u'            <span class="kmore" data-page-node-id="oBV50TDRcMPu0iQyYmw5yj">共 8 个</span>\n'
    u'          </div>\n'
)
rep(
    u'<span data-page-node-id="bWCI40We7suHgAQdtdhwxz">CobbleDB</span>\n          </div>\n',
    u'<span data-page-node-id="bWCI40We7suHgAQdtdhwxz">CobbleDB</span>\n' + KWCAP,
    "HTML: 热点关键词补图例",
)

# =====================================================================
# 7) HTML：阅读进度 -> 线性条（删圆环 SVG，保留其余全部节点标记）
# =====================================================================
NEW_PROG = (
    u'        <div class="progress" data-page-node-id="tUeFyMGUIHaDDEQuJZj0J0">\n'
    u'          <div class="pinfo" data-page-node-id="BKYRbncEhHbB8x8GGhOvwN">\n'
    u'            <div class="pt" data-page-node-id="qOJz42HFtXQ8uV3IDgBDmA">今日阅读进度</div>\n'
    u'            <button class="ghost" id="resetBtn" type="button" data-page-node-id="VrjZHmXfmb27PHljsuRdbE">重置进度</button>\n'
    u'          </div>\n'
    u'          <div class="pbar" data-page-node-id="SGkLKUWcmneSWvccyBSNQN"><span class="pbar-fill" id="readFill" data-page-node-id="0fWrcjVhniqbXx9EmTtkxu"></span></div>\n'
    u'          <div class="pd" data-page-node-id="z5lredz891eOcCx6Z50uzh"><span data-page-node-id="B4Cdjl2o7YUy4FvegfIetD"><b id="readCount" data-page-node-id="Q8zCtHICz1a3l2Y5Nv8aNK">0</b><span data-page-node-id="Dl93i4YvCEMZp01QqpOJgg"> / 3 篇已读</span></span></div>\n'
    u'        </div>'
)
splice(
    u'        <div class="progress" data-page-node-id="tUeFyMGUIHaDDEQuJZj0J0">',
    u'\n\n      </div>\n    </aside>',
    NEW_PROG + u'\n\n      </div>\n    </aside>',
    "HTML: 阅读进度改线性条",
)

# =====================================================================
# 8) JS：移除圆环逻辑，改更新线性条宽度
# =====================================================================
OLD_JS = u"""  var cards = Array.prototype.slice.call(document.querySelectorAll('.news'));
  var ringFg = document.getElementById('ringFg');
  var ringPct = document.getElementById('ringPct');
  var readCount = document.getElementById('readCount');
  var resetBtn = document.getElementById('resetBtn');

  var CIRC = 2 * Math.PI * 40; // r = 40 -> 251.33
  ringFg.style.strokeDasharray = CIRC.toFixed(2);

  var state = cards.map(function () { return false; });"""
NEW_JS = u"""  var cards = Array.prototype.slice.call(document.querySelectorAll('.news'));
  var readFill = document.getElementById('readFill');
  var readCount = document.getElementById('readCount');
  var resetBtn = document.getElementById('resetBtn');

  var state = cards.map(function () { return false; });"""
rep(OLD_JS, NEW_JS, "JS: 去掉圆环初始化")

rep(
    u"""    ringFg.style.strokeDashoffset = (CIRC * (1 - pct / 100)).toFixed(2);
    ringPct.textContent = pct;
    readCount.textContent = done;""",
    u"""    readFill.style.width = pct + '%';
    readCount.textContent = done;""",
    "JS: render() 改驱动线性条",
)

# =====================================================================
# 9) JS：新增关键词胶囊点击按压动画
# =====================================================================
rep(
    u"""  render();
  applyFilter('all');
})();""",
    u"""  /* ---------- 6. 热点关键词胶囊：点击按压缩放回弹 ---------- */
  Array.prototype.slice.call(document.querySelectorAll('.kw span')).forEach(function (el) {
    el.addEventListener('click', function () {
      el.classList.remove('kwpop');
      void el.offsetWidth;                 // 强制重排，连点也能重播动画
      el.classList.add('kwpop');
    });
    el.addEventListener('animationend', function () { el.classList.remove('kwpop'); });
  });

  render();
  applyFilter('all');
})();""",
    "JS: 关键词胶囊按压动画",
)

# =====================================================================
io.open(P, "w", encoding="utf-8").write(s)
n1 = s.count("data-page-node-id")
print("OK  patches=%d" % len(log))
for x in log:
    print("  - " + x)
print("node-id: %d -> %d" % (n0, n1))
print("size: %d -> %d bytes" % (len(io.open(P, encoding="utf-8").read()), len(s)))

# -*- coding: utf-8 -*-
"""第 13 轮定点补丁：顶部标签滑动指示器 + 右侧「13 条精选」数据仪表盘重塑。"""
import io, sys, re

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
raw = open(P, 'rb').read()
print('raw crlf: %d  lf-only: %d' % (raw.count(b'\r\n'), raw.count(b'\n') - raw.count(b'\r\n')))
s = raw.decode('utf-8')
orig_len = len(raw)
LOG = []


def cut(old, new, label):
    global s
    # 源文件为 CRLF 行尾：把补丁里的 LF 统一升级为 CRLF 再匹配
    old = old.replace('\n', '\r\n')
    new = new.replace('\n', '\r\n')
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: matched %d' % (label, n))
        sys.exit(1)
    s = s.replace(old, new, 1)
    LOG.append(label)
    print('OK   %s' % label)


# ============================================================
# 1) CSS —— 顶部标签筛选区：橙色滑块 + 数字微型徽章
# ============================================================
cut(
    u"""  .hero-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
  .hero-tab{
    background:var(--white);color:var(--gray-700);
    border:1px solid var(--line);
    padding:5px 14px;border-radius:0;
    font-size:13px;font-weight:400;letter-spacing:.3px;
  }
  .hero-tab.active{background:var(--m-orange);border-color:var(--m-orange);color:var(--white)}
""",
    u"""  /* —— 顶部标签筛选：橙色高亮块 transition:transform .3s 平滑滑动（不再生硬变色） —— */
  .hero-tabs{position:relative;display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
  .tab-ind{
    position:absolute;left:0;top:0;z-index:0;
    width:0;height:0;background:var(--m-orange);border-radius:0;
    opacity:0;pointer-events:none;
    transition:transform .3s cubic-bezier(.22,.72,.2,1),
               width .3s cubic-bezier(.22,.72,.2,1),
               height .3s ease,opacity .24s ease;
    will-change:transform,width;
  }
  .tab-ind.ready{opacity:1}
  .hero-tab{
    position:relative;z-index:1;
    cursor:pointer;border:1px solid transparent;border-radius:0;
    background:transparent;color:var(--gray-700);
    font-family:var(--font-sans);
    padding:5px 14px;
    font-size:13px;font-weight:400;letter-spacing:.3px;white-space:nowrap;
    display:inline-flex;align-items:center;gap:6px;
    transition:color .3s ease;
  }
  .hero-tab:hover{color:var(--ink)}
  .hero-tab.active{color:var(--white)}
  .hero-tab:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}
  /* 数字微型徽章：未选中=浅灰底深灰字 / 选中=白底橙字 */
  .tbadge{
    display:inline-flex;align-items:center;justify-content:center;
    min-width:19px;height:19px;padding:0 6px;border-radius:20px;
    font-family:var(--font-mono);font-size:11px;font-weight:600;line-height:1;letter-spacing:0;
    background:#F3F4F6;color:#4B5563;
    transition:background .3s ease,color .3s ease;
  }
  .hero-tab.active .tbadge{background:var(--white);color:#EA580C}
  .tunit{font-size:12px;color:var(--gray-500);transition:color .3s ease}
  .hero-tab.active .tunit{color:rgba(255,255,255,.82)}
""",
    "CSS: 顶部标签滑动指示器 + 数字徽章",
)

# ============================================================
# 2) CSS —— 重要程度分段控件：同步改为浅橙滑块
# ============================================================
cut(
    u"""  .segmented{
    display:inline-flex;align-items:center;gap:2px;
    padding:3px;border-radius:0;
    background:var(--white);
    border:1px solid var(--line);
  }
  .seg{
    cursor:pointer;border:none;background:transparent;
    font-family:var(--font-sans);font-size:13px;font-weight:400;letter-spacing:.3px;
    color:var(--gray-700);white-space:nowrap;
    padding:6px 14px;border-radius:0;
    display:inline-flex;align-items:center;gap:6px;
    transition:background .2s,color .2s;
  }
  .seg:hover{color:var(--ink);background:rgba(127,99,21,.08)}
  .seg b{font-family:var(--font-mono);font-size:11px;font-weight:400;color:var(--gray-500)}
  .seg.active{background:#FFF7ED;color:#EA580C}
  .seg.active:hover{background:#FFEDD5;color:#C2410C}
  .seg.active b{color:#C2410C}
  .seg:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}
  .seg.active{animation:seg-spread .45s ease}
  @keyframes seg-spread{
    from{box-shadow:0 0 0 0 rgba(234,88,12,.28)}
    to{box-shadow:0 0 0 12px rgba(234,88,12,0)}
  }
""",
    u"""  .segmented{
    position:relative;
    display:inline-flex;align-items:center;gap:2px;
    padding:3px;border-radius:0;
    background:var(--white);
    border:1px solid var(--line);
  }
  /* 浅橙滑块：与顶部标签区同一套滑动语言 */
  .seg-ind{
    position:absolute;left:0;top:0;z-index:0;
    width:0;height:0;background:#FFF7ED;border-radius:0;
    opacity:0;pointer-events:none;
    transition:transform .3s cubic-bezier(.22,.72,.2,1),
               width .3s cubic-bezier(.22,.72,.2,1),
               height .3s ease,opacity .24s ease;
    will-change:transform,width;
  }
  .seg-ind.ready{opacity:1}
  .seg{
    position:relative;z-index:1;
    cursor:pointer;border:none;background:transparent;
    font-family:var(--font-sans);font-size:13px;font-weight:400;letter-spacing:.3px;
    color:var(--gray-700);white-space:nowrap;
    padding:6px 14px;border-radius:0;
    display:inline-flex;align-items:center;gap:6px;
    transition:background .2s,color .3s ease;
  }
  .seg:hover{color:var(--ink);background:rgba(127,99,21,.08)}
  .seg b{font-family:var(--font-mono);font-size:11px;font-weight:400;color:var(--gray-500)}
  .seg.active{color:#EA580C}
  .seg.active:hover{background:transparent;color:#C2410C}
  .seg.active b{color:#C2410C}
  .seg:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}
""",
    "CSS: 分段控件浅橙滑块",
)

# ============================================================
# 3) CSS —— 卡片区：淡入淡出过渡 + 板块筛选单列 + 空态
# ============================================================
cut(
    u"""  .cards{flex:1;min-height:0;display:grid;gap:10px;align-items:start}
""",
    u"""  .cards{
    flex:1;min-height:0;display:grid;gap:10px;align-items:start;
    opacity:1;transform:translateY(0);
    transition:opacity .3s ease,transform .3s ease;
  }
  /* 切换筛选时列表淡出 → 换内容 → 淡入 */
  .cards.is-fade{opacity:0;transform:translateY(8px)}
""",
    "CSS: 卡片区淡入淡出过渡",
)

cut(
    u"""  .cards[data-view="mid"]{grid-template-columns:1fr;grid-template-rows:auto}
  .cards[data-view="mid"] .news[data-card="3"]{grid-column:1;grid-row:1}
""",
    u"""  .cards[data-view="mid"]{grid-template-columns:1fr;grid-template-rows:auto}
  .cards[data-view="mid"] .news[data-card="3"]{grid-column:1;grid-row:1}

  /* 板块标签激活时统一单列，避免单张卡片被双列栅格甩到一侧 */
  .cards.cat-narrow{grid-template-columns:1fr;grid-template-rows:auto}
  .cards.cat-narrow .news{grid-column:1;grid-row:auto}

  /* 板块无对应精读卡片时的空态占位 */
  .cards-empty{
    grid-column:1 / -1;
    display:flex;flex-direction:column;align-items:flex-start;gap:12px;
    padding:24px 22px;
    background:var(--white);
    border-left:4px solid #EA580C;
    animation:rise .4s cubic-bezier(.22,.72,.2,1) backwards;
  }
  .cards-empty[hidden]{display:none}
  .cards-empty .ce-t{font-size:13.5px;font-weight:400;line-height:1.6;color:#4B5563}
  .cards-empty .ce-btn{
    cursor:pointer;border:1px solid #E5E7EB;border-radius:20px;background:transparent;
    font-family:var(--font-sans);font-size:12px;font-weight:400;letter-spacing:0;color:#4B5563;
    padding:5px 14px;
    transition:background .2s,border-color .2s,color .2s;
  }
  .cards-empty .ce-btn:hover{background:#FFF7ED;border-color:rgba(250,82,15,.35);color:#C2410C}
  .cards-empty .ce-btn:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}
""",
    "CSS: 板块单列布局 + 空态",
)

# ============================================================
# 4) CSS —— 右侧「13 条精选」超大数字数据仪表盘
# ============================================================
cut(
    u"""  .hero{display:flex;align-items:flex-end;gap:10px}
  .hero .num{font-family:var(--font-mono);font-size:32px;font-weight:400;line-height:1;letter-spacing:-1px;color:#4B5563}
  .hero .unit{font-size:12px;font-weight:400;color:#4B5563;line-height:1.6;padding-bottom:2px}
  .hero .unit b{display:block;font-family:var(--font-mono);font-size:12px;color:#4B5563;font-weight:400}
""",
    u"""  /* —— 今日趋势 · 13 条精选：独立数据仪表盘（超大数字 + 说明 + 环比胶囊） —— */
  .hero{
    display:flex;align-items:center;gap:14px;
    padding:18px 16px;
    background:var(--white);
    border-left:4px solid #EA580C;
  }
  .hero-numwrap{display:flex;flex-direction:column;gap:3px;min-width:0}
  .hero .num{
    font-family:var(--font-mono);
    font-size:36px;font-weight:700;line-height:1;
    letter-spacing:-1.5px;color:#EA580C;
  }
  .hero .unit{
    font-size:12px;font-weight:400;letter-spacing:.5px;
    color:#4B5563;line-height:1.3;
  }
  .hero-pill{
    margin-left:auto;flex:0 0 auto;
    display:inline-flex;align-items:center;gap:4px;
    background:#FFF7ED;color:#EA580C;
    font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:0;
    padding:5px 11px;border-radius:20px;white-space:nowrap;
    transition:background .2s ease;
  }
  .hero-pill .arw{font-size:11px;font-weight:700;line-height:1}
""",
    "CSS: 精选资讯数据仪表盘",
)

# ============================================================
# 5) CSS —— 小屏适配（860px / 420px）
# ============================================================
cut(
    u"""    .hero-tabs{margin-top:12px;gap:6px}
    .hero-tab{font-size:12px;padding:4px 11px}
""",
    u"""    .hero-tabs{margin-top:12px;gap:6px}
    .hero-tab{font-size:12px;padding:4px 11px}
    .hero{padding:16px 14px;gap:12px}
    .hero .num{font-size:32px}
""",
    "CSS: 860px 小屏 hero 适配",
)

cut(
    u"""    .kwcap .kmore{display:none}
    .footbar{padding:14px 12px 18px}
""",
    u"""    .kwcap .kmore{display:none}
    .hero-tab{font-size:11.5px;padding:4px 9px;gap:5px}
    .tbadge{min-width:17px;height:17px;padding:0 5px;font-size:10px}
    .hero{padding:14px 12px;gap:10px}
    .hero .num{font-size:30px}
    .hero-pill{font-size:11.5px;padding:4px 9px}
    .footbar{padding:14px 12px 18px}
""",
    "CSS: 420px 小屏 hero / badge 适配",
)

# ============================================================
# 6) HTML —— 顶部标签筛选区
# ============================================================
cut(
    u"""    <div class="hero-tabs">
      <span class="hero-tab active">精选 13 条</span>
      <span class="hero-tab">模型发布 3</span>
      <span class="hero-tab">产品更新 2</span>
      <span class="hero-tab">行业动态 1</span>
      <span class="hero-tab">观点技巧 7</span>
    </div>
""",
    u"""    <div class="hero-tabs" id="catTabs">
      <span class="tab-ind" id="tabInd" aria-hidden="true"></span>
      <button class="hero-tab active" type="button" data-cat="all" aria-pressed="true">精选<b class="tbadge">13</b><span class="tunit">条</span></button>
      <button class="hero-tab" type="button" data-cat="模型发布" aria-pressed="false">模型发布<b class="tbadge">3</b></button>
      <button class="hero-tab" type="button" data-cat="产品发布" aria-pressed="false">产品更新<b class="tbadge">2</b></button>
      <button class="hero-tab" type="button" data-cat="行业动态" aria-pressed="false">行业动态<b class="tbadge">1</b></button>
      <button class="hero-tab" type="button" data-cat="观点技巧" aria-pressed="false">观点技巧<b class="tbadge">7</b></button>
    </div>
""",
    "HTML: 顶部标签改为可点击筛选器",
)

# ============================================================
# 7) HTML —— 分段控件加 id + 滑块
# ============================================================
cut(
    u"""        <div class="segmented" role="group" aria-label="按重要程度筛选新闻">
          <button class="seg active" type="button" data-filter="all" aria-pressed="true">全部<b>3</b></button>
""",
    u"""        <div class="segmented" id="segmented" role="group" aria-label="按重要程度筛选新闻">
          <span class="seg-ind" id="segInd" aria-hidden="true"></span>
          <button class="seg active" type="button" data-filter="all" aria-pressed="true">全部<b>3</b></button>
""",
    "HTML: 分段控件加滑块",
)

# ============================================================
# 8) HTML —— 右侧「13 条精选」仪表盘
# ============================================================
cut(
    u"""        <div class="hero" data-page-node-id="otg5Img00BxuDmRg6aCOKM">
          <div class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>
          <div class="unit" data-page-node-id="BHnaBikreQtxtydu4KCcv1">条精选资讯<b data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH">较昨日 ▲44%</b></div>
        </div>
""",
    u"""        <div class="hero" data-page-node-id="otg5Img00BxuDmRg6aCOKM">
          <div class="hero-numwrap" data-page-node-id="BHnaBikreQtxtydu4KCcv1">
            <div class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>
            <div class="unit">精选资讯</div>
          </div>
          <span class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH">较昨日 <span class="arw">↑</span> 44%</span>
        </div>
""",
    "HTML: 精选资讯仪表盘结构",
)

# ============================================================
# 9) HTML —— 三张卡片补 data-cat
# ============================================================
cut(
    u"""<article class="news card-feat" data-card="1" data-lvl="high\"""",
    u"""<article class="news card-feat" data-card="1" data-lvl="high" data-cat="模型发布\"""",
    "HTML: 卡片1 data-cat",
)
cut(
    u"""<article class="news" data-card="2" data-lvl="high\"""",
    u"""<article class="news" data-card="2" data-lvl="high" data-cat="产品发布\"""",
    "HTML: 卡片2 data-cat",
)
cut(
    u"""<article class="news" data-card="3" data-lvl="mid\"""",
    u"""<article class="news" data-card="3" data-lvl="mid" data-cat="行业动态\"""",
    "HTML: 卡片3 data-cat",
)

# ============================================================
# 10) HTML —— 卡片区空态占位
# ============================================================
cut(
    u"""          </button>
        </article>
        </div>

      </div>
    </div>
""",
    u"""          </button>
        </article>
        </div>

        <div class="cards-empty" id="cardsEmpty" hidden>
          <p class="ce-t">该板块今日的内容为短讯速览，暂未生成精读卡片。</p>
          <button class="ce-btn" type="button" id="emptyReset">回到全部精选</button>
        </div>

      </div>
    </div>
""",
    "HTML: 卡片区空态",
)

# ============================================================
# 11) JS —— 组合筛选 + 滑动指示器 + 淡入淡出
# ============================================================
cut(
    u"""  /* ---------- 3. 重要程度筛选（全部 / 高优先级 / 中优先级） ---------- */
  var segs = Array.prototype.slice.call(document.querySelectorAll('.seg'));
  var cardsWrap = document.querySelector('.cards');
  var filterCount = document.getElementById('filterCount');

  function applyFilter(view) {
    var shown = 0;
    cards.forEach(function (card) {
      // 筛选是「视图层」操作：只改变可见性，不触碰已读状态
      var match = (view === 'all') || (card.getAttribute('data-lvl') === view);
      card.hidden = !match;
      if (match) shown += 1;
    });
    cardsWrap.setAttribute('data-view', view);
    segs.forEach(function (b) {
      var on = b.getAttribute('data-filter') === view;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    filterCount.textContent = '显示 ' + shown + ' / ' + cards.length + ' 条';
  }

  segs.forEach(function (b) {
    b.addEventListener('click', function () {
      applyFilter(b.getAttribute('data-filter'));
    });
  });
""",
    u"""  /* ---------- 3. 筛选：板块标签（顶部）× 重要程度（分段控件）组合过滤 ---------- */
  var segs = Array.prototype.slice.call(document.querySelectorAll('.seg'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.hero-tab'));
  var cardsWrap = document.querySelector('.cards');
  var filterCount = document.getElementById('filterCount');
  var cardsEmpty = document.getElementById('cardsEmpty');
  var emptyReset = document.getElementById('emptyReset');

  var catFilter = 'all';   // 板块：all / 模型发布 / 产品发布 / 行业动态 / 观点技巧
  var lvlFilter = 'all';   // 重要程度：all / high / mid

  /* 3.1 滑动指示器：高亮块以 transition:transform .3s 平滑滑到当前标签位置 */
  function makeIndicator(wrap, ind, sel) {
    if (!wrap || !ind) return function () {};
    return function (immediate) {
      var btn = wrap.querySelector(sel);
      if (!btn) return;
      var w = btn.offsetWidth + 'px';
      var h = btn.offsetHeight + 'px';
      var t = 'translate(' + btn.offsetLeft + 'px,' + btn.offsetTop + 'px)';
      if (immediate) {
        // 首屏 / 窗口尺寸变化：直接落位，不播滑动动画
        ind.style.transition = 'none';
        ind.style.width = w;
        ind.style.height = h;
        ind.style.transform = t;
        void ind.offsetWidth;
        ind.style.transition = '';
      } else {
        ind.style.width = w;
        ind.style.height = h;
        ind.style.transform = t;
      }
      ind.classList.add('ready');
    };
  }
  var placeCat = makeIndicator(document.getElementById('catTabs'), document.getElementById('tabInd'), '.hero-tab.active');
  var placeLvl = makeIndicator(document.getElementById('segmented'), document.getElementById('segInd'), '.seg.active');
  function placeAll(immediate) { placeCat(immediate); placeLvl(immediate); }

  /* 3.2 应用视图：组合过滤，只改变可见性，不触碰已读状态 */
  function applyView() {
    var shown = 0;
    cards.forEach(function (card) {
      var okCat = (catFilter === 'all') || (card.getAttribute('data-cat') === catFilter);
      var okLvl = (lvlFilter === 'all') || (card.getAttribute('data-lvl') === lvlFilter);
      var match = okCat && okLvl;
      card.hidden = !match;
      if (match) shown += 1;
    });
    cardsWrap.setAttribute('data-view', lvlFilter);
    cardsWrap.classList.toggle('cat-narrow', catFilter !== 'all');
    tabs.forEach(function (b) {
      var on = b.getAttribute('data-cat') === catFilter;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    segs.forEach(function (b) {
      var on = b.getAttribute('data-filter') === lvlFilter;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    cardsEmpty.hidden = shown > 0;
    filterCount.textContent = '显示 ' + shown + ' / ' + cards.length + ' 条';
  }

  /* 3.3 切换动效：列表淡出 → 换内容 → 淡入（opacity / transform .3s ease） */
  var fadeTimer = null;
  function switchView(mutate) {
    if (fadeTimer) { clearTimeout(fadeTimer); fadeTimer = null; }
    cardsWrap.classList.add('is-fade');
    fadeTimer = setTimeout(function () {
      fadeTimer = null;
      mutate();
      cardsWrap.classList.remove('is-fade');
    }, 170);
  }

  /* 3.4 事件绑定 */
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = b.getAttribute('data-cat');
      if (next === catFilter) return;
      catFilter = next;
      switchView(function () { applyView(); placeCat(false); });
    });
  });

  segs.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = b.getAttribute('data-filter');
      if (next === lvlFilter) return;
      lvlFilter = next;
      switchView(function () { applyView(); placeLvl(false); });
    });
  });

  if (emptyReset) {
    emptyReset.addEventListener('click', function () {
      catFilter = 'all';
      switchView(function () { applyView(); placeCat(false); });
    });
  }

  window.addEventListener('resize', function () { placeAll(true); });
""",
    "JS: 组合筛选 + 滑块 + 淡入淡出",
)

# ============================================================
# 12) JS —— 初始化
# ============================================================
cut(
    u"""  render();
  applyFilter('all');
})();
""",
    u"""  render();
  applyView();
  placeAll(true);

  // 字体 / 窗口就绪后再校准一次指示器位置（避免字体替换导致宽度偏差）
  window.addEventListener('load', function () { placeAll(true); });
  if (document.fonts && document.fonts.ready && document.fonts.ready.then) {
    document.fonts.ready.then(function () { placeAll(true); });
  }
})();
""",
    "JS: 初始化",
)

# ============================================================
# 落盘 + 自检
# ============================================================
ids = re.findall(r'data-page-node-id="([^"]+)"', s)
new_len = len(s.encode('utf-8'))
print('\n---- 自检 ----')
print('node ids: %d (unique %d)' % (len(ids), len(set(ids))))
print('bytes: %d -> %d' % (orig_len, new_len))
print('patches applied: %d' % len(LOG))

if len(ids) != 207 or len(set(ids)) != 207:
    print('!! 节点标记数量异常，已放弃写入')
    sys.exit(1)
if 'applyFilter' in s:
    print('!! 仍存在旧函数名 applyFilter，已放弃写入')
    sys.exit(1)

open(P, 'wb').write(s.encode('utf-8'))
print('written -> %s' % P)

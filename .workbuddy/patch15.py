# -*- coding: utf-8 -*-
"""第 15 轮补丁：精选筛选 Tab × 板块联动筛选 × 标签过滤器改版 × filterState 统一状态树。
锚点切片替换，保留全部 207 个 data-page-node-id。"""
import io, sys, re, collections

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
s = io.open(P, encoding='utf-8', newline='').read()
s = s.replace('\r\n', '\n')          # 统一为 LF 处理，写回时还原 CRLF
orig_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
LOG = []


def cut(start, end, repl, label):
    """替换 [start..end]（含两端）为 repl"""
    global s
    i = s.find(start)
    assert i >= 0, 'start not found: ' + label
    j = s.find(end, i + len(start))
    assert j >= 0, 'end not found: ' + label
    s = s[:i] + repl + s[j + len(end):]
    LOG.append(label)
    print('OK   ' + label)


def rep(old, new, label):
    global s
    n = s.count(old)
    assert n == 1, 'match %d for %s' % (n, label)
    s = s.replace(old, new, 1)
    LOG.append(label)
    print('OK   ' + label)


# ============ CSS ============

# C1 分段控件：纯色滑块 -> 传统描边标签过滤器
rep(u'''  .segmented{
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
  .seg:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}''',
    u'''  .segmented{
    display:inline-flex;align-items:center;flex-wrap:wrap;gap:8px;
    padding:0;border:none;background:transparent;
  }
  /* 传统标签过滤器：描边胶囊 + 浅橙选中（不再用纯色滑块） */
  .seg{
    cursor:pointer;border:1px solid #E5E7EB;border-radius:20px;background:transparent;
    font-family:var(--font-sans);font-size:12.5px;font-weight:400;letter-spacing:.3px;
    color:#4B5563;white-space:nowrap;
    padding:5px 13px;
    display:inline-flex;align-items:center;gap:6px;
    transition:background .25s ease,border-color .25s ease,color .25s ease,box-shadow .25s ease;
  }
  .seg:hover{color:#C2410C;border-color:rgba(250,82,15,.45);background:#FFF7ED}
  .seg b{font-family:var(--font-mono);font-size:11px;font-weight:400;color:#9CA3AF;transition:color .25s ease}
  .seg.active{background:#FFF7ED;border-color:#EA580C;color:#EA580C}
  .seg.active:hover{background:#FFF7ED;border-color:#EA580C;color:#C2410C}
  .seg.active b{color:#EA580C}
  .seg:focus-visible{outline:2px solid var(--m-orange);outline-offset:2px}''',
    u'C1 分段控件改为描边标签过滤器')

# C2 顶部标签「精选」半选态（与板块同时生效时的 AND 提示）
rep(u'''  .hero-tab.active .tunit{color:rgba(255,255,255,.82)}''',
    u'''  .hero-tab.active .tunit{color:rgba(255,255,255,.82)}
  /* 「精选」与板块同时生效时的半选态：橙色文字提示 AND 组合 */
  .hero-tab.semi{color:#EA580C}
  .hero-tab.semi .tbadge{background:#FFF7ED;color:#EA580C}
  .hero-tab.semi .tunit{color:#EA580C}''',
    u'C2 hero-tab 半选态样式')

# C3 环比胶囊降/平变体
rep(u'''  .hero-pill .arw{font-size:11px;font-weight:700;line-height:1}''',
    u'''  .hero-pill .arw{font-size:11px;font-weight:700;line-height:1}
  /* 环比胶囊随筛选结果变色：降为绿 / 持平为灰（涨红跌绿） */
  .hero-pill.down{background:#ECFDF5;color:#16A34A}
  .hero-pill.flat{background:#F3F4F6;color:#4B5563}''',
    u'C3 环比胶囊降/平变体')

# C4 板块行变可点击筛选器（悬停 / 选中 / 禁用三态）
rep(u'''  .titem{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:11px}
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
  .tdelta.flat .dl:empty{display:none}''',
    u'''  .titem{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-left:-8px;margin-right:-8px;margin-bottom:11px;padding:3px 8px;border-radius:8px;cursor:pointer;transition:background .2s ease}
  .titem:last-child{margin-bottom:0}
  /* 板块行即筛选器：悬停浅橙 / 选中橙字 / 零结果禁用（再点当前项取消） */
  .titem:hover{background:rgba(255,247,237,.75)}
  .titem:focus-visible{outline:2px solid var(--m-orange);outline-offset:1px}
  .titem[aria-pressed="true"]{background:#FFF7ED}
  .titem[aria-pressed="true"] .tname{color:#EA580C;font-weight:600}
  .titem[aria-pressed="true"] .tnum{color:#EA580C;font-weight:700}
  .titem[aria-disabled="true"]{opacity:.45;cursor:default}
  .titem[aria-disabled="true"]:hover{background:transparent}
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
  .tdelta.flat .dl:empty{display:none}''',
    u'C4 板块行可点击三态样式')

# C5 图例提示「点击行可筛选」
rep(u'''  .legend .l-down{border-top:6px solid #16A34A}''',
    u'''  .legend .l-down{border-top:6px solid #16A34A}
  .legend .l-hint{color:#9CA3AF}''',
    u'C5 图例提示样式')

# C6 小屏板块行触控区
rep(u'''    .titem{gap:8px;margin-bottom:10px}''',
    u'''    .titem{gap:8px;margin-bottom:10px;padding:2px 6px;margin-left:-6px;margin-right:-6px}''',
    u'C6 小屏板块行触控区')

# ============ HTML ============

# H1 顶部标签：新增「全部」scope，精选改为 featured 筛选（徽章动态化）
rep(u'''      <button class="hero-tab active" type="button" data-cat="all" aria-pressed="true">精选<b class="tbadge">13</b><span class="tunit">条</span></button>
      <button class="hero-tab" type="button" data-cat="模型发布" aria-pressed="false">模型发布<b class="tbadge">3</b></button>
      <button class="hero-tab" type="button" data-cat="产品发布" aria-pressed="false">产品更新<b class="tbadge">2</b></button>
      <button class="hero-tab" type="button" data-cat="行业动态" aria-pressed="false">行业动态<b class="tbadge">1</b></button>
      <button class="hero-tab" type="button" data-cat="观点技巧" aria-pressed="false">观点技巧<b class="tbadge">7</b></button>''',
    u'''      <button class="hero-tab active" type="button" data-scope="all" aria-pressed="true">全部<b class="tbadge">13</b><span class="tunit">条</span></button>
      <button class="hero-tab" type="button" data-scope="featured" aria-pressed="false">精选<b class="tbadge">3</b><span class="tunit">条</span></button>
      <button class="hero-tab" type="button" data-scope="模型发布" aria-pressed="false">模型发布<b class="tbadge">3</b></button>
      <button class="hero-tab" type="button" data-scope="产品发布" aria-pressed="false">产品更新<b class="tbadge">2</b></button>
      <button class="hero-tab" type="button" data-scope="行业动态" aria-pressed="false">行业动态<b class="tbadge">1</b></button>
      <button class="hero-tab" type="button" data-scope="观点技巧" aria-pressed="false">观点技巧<b class="tbadge">7</b></button>''',
    u'H1 顶部标签改为 scope 语义并新增「全部」')

# H2 移除分段滑块
rep(u'''          <span class="seg-ind" id="segInd" aria-hidden="true"></span>
          <button class="seg active"''',
    u'''          <button class="seg active"''',
    u'H2 移除 seg-ind 滑块')

# H3 面板大数字 / 环比胶囊挂 id（保留节点标记在前）
rep(u'''<div class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>''',
    u'''<div id="heroNum" class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>''',
    u'H3a heroNum 挂 id')
rep(u'''<span class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH">''',
    u'''<span id="heroPill" class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH">''',
    u'H3b heroPill 挂 id')

# H4 板块行挂 data-board + 键盘可达
rep(u'''<li class="titem" data-page-node-id="E8sqPUNxpHRzUf95Hj8ype">''',
    u'''<li class="titem" data-board="模型发布" role="button" tabindex="0" aria-pressed="false" data-page-node-id="E8sqPUNxpHRzUf95Hj8ype">''',
    u'H4a 板块行 模型发布')
rep(u'''<li class="titem" data-page-node-id="KqVVH44Lhj9HZhSaBZzaAW">''',
    u'''<li class="titem" data-board="产品发布" role="button" tabindex="0" aria-pressed="false" data-page-node-id="KqVVH44Lhj9HZhSaBZzaAW">''',
    u'H4b 板块行 产品发布')
rep(u'''<li class="titem" data-page-node-id="USgHMYNYxlgYPZLg3VGoES">''',
    u'''<li class="titem" data-board="行业动态" role="button" tabindex="0" aria-pressed="false" data-page-node-id="USgHMYNYxlgYPZLg3VGoES">''',
    u'H4c 板块行 行业动态')
rep(u'''<li class="titem" data-page-node-id="MqpaFqdxFzws4iGAZBFvWl">''',
    u'''<li class="titem" data-board="观点技巧" role="button" tabindex="0" aria-pressed="false" data-page-node-id="MqpaFqdxFzws4iGAZBFvWl">''',
    u'H4d 板块行 观点技巧')
rep(u'''<li class="titem" data-page-node-id="2vgtwaqc5ZMj7F4gtFdBAX">''',
    u'''<li class="titem" data-board="论文研究" role="button" aria-disabled="true" data-page-node-id="2vgtwaqc5ZMj7F4gtFdBAX">''',
    u'H4e 板块行 论文研究（禁用）')

# H5 图例加可点击提示
rep(u'''<span data-page-node-id="NR76ISECHnzsilrSElF5x5"><em class="l-down" data-page-node-id="lrGIhqR4J9i1MEgP3FMqD8"></em>减</span>''',
    u'''<span data-page-node-id="NR76ISECHnzsilrSElF5x5"><em class="l-down" data-page-node-id="lrGIhqR4J9i1MEgP3FMqD8"></em>减</span>
              <span class="l-hint">点击行可筛选</span>''',
    u'H5 图例点击提示')

# H6 空态文案改为通用筛选组合语境
rep(u'''<p class="ce-t">该板块今日的内容为短讯速览，暂未生成精读卡片。</p>''',
    u'''<p class="ce-t">当前筛选组合下暂无精读卡片，试试放宽条件或回到全部精选。</p>''',
    u'H6 空态文案')

# ============ JS：第 3 节整体重写为 filterState + renderList ============

NEW_JS = u'''  /* ---------- 3. 筛选：统一 filterState 状态树 + renderList 单一渲染出口 ---------- */
  var segs = Array.prototype.slice.call(document.querySelectorAll('.seg'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.hero-tab'));
  var cardsWrap = document.querySelector('.cards');
  var filterCount = document.getElementById('filterCount');
  var cardsEmpty = document.getElementById('cardsEmpty');
  var emptyReset = document.getElementById('emptyReset');
  var titems = Array.prototype.slice.call(document.querySelectorAll('.titem[data-board]'));
  var heroNum = document.getElementById('heroNum');
  var heroPill = document.getElementById('heroPill');

  /* 3.0 今日数据模型：13 条精选的板块 / 重要程度 / 精读标记 / 昨日在榜。
     与右侧面板静态统计一一对应（模型发布3 产品发布2 行业动态1 观点技巧7 论文研究0；昨日共 9 条 -> ↑44%）。
     ghost 条目今日已不在榜，仅参与「昨日」基数。 */
  var NEWS = [
    { cat:'模型发布', lvl:'high', featured:true,  yest:0 },   /* Gemini 3.8 Live（精读卡 1） */
    { cat:'模型发布', lvl:'mid',  featured:false, yest:1 },   /* StepAudio 3 */
    { cat:'模型发布', lvl:'low',  featured:false, yest:1 },
    { cat:'产品发布', lvl:'high', featured:true,  yest:0 },   /* Apple Intelligence（精读卡 2） */
    { cat:'产品发布', lvl:'mid',  featured:false, yest:1 },   /* Vidu S2 */
    { cat:'行业动态', lvl:'mid',  featured:true,  yest:1 },   /* CobbleDB（精读卡 3） */
    { cat:'观点技巧', lvl:'high', featured:false, yest:1 },   /* 呼吁协调放缓前沿开发 */
    { cat:'观点技巧', lvl:'mid',  featured:false, yest:1 },   /* DeepSeek IPO */
    { cat:'观点技巧', lvl:'mid',  featured:false, yest:1 },   /* Codex 智能体 */
    { cat:'观点技巧', lvl:'low',  featured:false, yest:1 },
    { cat:'观点技巧', lvl:'low',  featured:false, yest:0 },
    { cat:'观点技巧', lvl:'low',  featured:false, yest:0 },
    { cat:'观点技巧', lvl:'low',  featured:false, yest:0 },
    { cat:'论文研究', lvl:'low',  featured:false, yest:1, ghost:true }
  ];

  /* 3.0b 唯一事实来源：三个单选维度之间逻辑与（AND）
     featured -> 只看精读精选；board -> 板块；lvl -> 重要程度 */
  var filterState = { featured:false, board:'all', lvl:'all' };

  function matchNews(pred) {
    var n = 0;
    NEWS.forEach(function (it) { if (!it.ghost && pred(it)) n++; });
    return n;
  }
  function yestNews(pred) {
    var n = 0;
    NEWS.forEach(function (it) { if (pred(it) && it.yest) n++; });
    return n;
  }
  function lvlOk(it) { return filterState.lvl === 'all' || it.lvl === filterState.lvl; }
  function inSlice(it) { return lvlOk(it) && (!filterState.featured || it.featured); }
  function boardOk(cat) { return filterState.board === 'all' || cat === filterState.board; }

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
  function placeAll(immediate) { placeCat(immediate); }

  /* 3.2 renderList：主列表唯一渲染出口（可见性 / 布局 / 空态 / 计数 / 分段徽章） */
  function renderList() {
    var shown = 0;
    cards.forEach(function (card) {
      var match = boardOk(card.getAttribute('data-cat'))
        && (filterState.lvl === 'all' || card.getAttribute('data-lvl') === filterState.lvl);
      card.hidden = !match;
      if (match) shown += 1;
    });
    cardsWrap.setAttribute('data-view', filterState.lvl);
    cardsWrap.classList.toggle('cat-narrow', filterState.board !== 'all');
    cardsEmpty.hidden = shown > 0;
    filterCount.textContent = '显示 ' + shown + ' / ' + cards.length + ' 条';
    segs.forEach(function (b) {
      var L = b.getAttribute('data-filter');
      var n = cards.filter(function (c) {
        return boardOk(c.getAttribute('data-cat'))
          && (L === 'all' || c.getAttribute('data-lvl') === L);
      }).length;
      b.querySelector('b').textContent = n;
      var on = filterState.lvl === L;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  /* 3.3 renderPanel：右侧面板数字随筛选结果动态重算（今日条数 vs 昨日基数） */
  function renderPanel() {
    var t = matchNews(function (it) { return inSlice(it) && boardOk(it.cat); });
    var y = yestNews(function (it) { return inSlice(it) && boardOk(it.cat); });
    heroNum.textContent = t;
    var tone, body;
    if (y === 0) {
      tone = t > 0 ? 'up' : 'flat';
      body = t > 0 ? '<span class="arw">↑</span> 新增' : '— 持平';
    } else {
      var p = Math.round((t - y) / y * 100);
      if (p > 0) { tone = 'up'; body = '<span class="arw">↑</span> ' + p + '%'; }
      else if (p < 0) { tone = 'down'; body = '<span class="arw">↓</span> ' + Math.abs(p) + '%'; }
      else { tone = 'flat'; body = '— 持平'; }
    }
    heroPill.innerHTML = '较昨日 ' + body;
    heroPill.classList.toggle('down', tone === 'down');
    heroPill.classList.toggle('flat', tone === 'flat');
    titems.forEach(function (li) {
      var cat = li.getAttribute('data-board');
      var tb = matchNews(function (it) { return inSlice(it) && it.cat === cat; });
      var yb = yestNews(function (it) { return inSlice(it) && it.cat === cat; });
      li.querySelector('.tnum').textContent = tb;
      var d = tb > yb ? { c:'up', a:'↑', n:String(tb - yb) }
            : tb < yb ? { c:'down', a:'↓', n:String(yb - tb) }
            : { c:'flat', a:'—', n:'' };
      var em = li.querySelector('.tdelta');
      em.className = 'tdelta ' + d.c;
      em.querySelector('.arw').textContent = d.a;
      em.querySelector('.dl').textContent = d.n;
      var active = filterState.board === cat;
      li.classList.toggle('active', active);
      li.setAttribute('aria-pressed', active ? 'true' : 'false');
      li.setAttribute('aria-disabled', (tb === 0 && !active) ? 'true' : 'false');
    });
  }

  /* 3.4 renderTabs：顶部标签选中态 + 徽章数字（徽章 = 若点击该标签将得到的条数） */
  function renderTabs() {
    var activeKey = filterState.board !== 'all' ? filterState.board
                  : (filterState.featured ? 'featured' : 'all');
    tabs.forEach(function (b) {
      var key = b.getAttribute('data-scope');
      var on = key === activeKey;
      var semi = key === 'featured' && filterState.featured && filterState.board !== 'all';
      b.classList.toggle('active', on);
      b.classList.toggle('semi', semi);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var n;
      if (key === 'all') n = matchNews(lvlOk);
      else if (key === 'featured') n = matchNews(function (it) { return it.featured && lvlOk(it); });
      else n = matchNews(function (it) { return it.cat === key && lvlOk(it); });
      b.querySelector('.tbadge').textContent = n;
    });
  }

  function renderAll() { renderList(); renderPanel(); renderTabs(); }

  /* 3.5 切换动效：列表淡出 → 统一重渲染 → 淡入（opacity / transform .3s ease） */
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

  /* 3.6 事件绑定：各维度独立单选，再次点击当前项即取消；维度间自动 AND 叠加 */
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      var key = b.getAttribute('data-scope');
      if (key === 'all') {
        if (!filterState.featured && filterState.board === 'all') return;
        filterState.featured = false;
        filterState.board = 'all';
      } else if (key === 'featured') {
        filterState.featured = !filterState.featured;
      } else {
        filterState.board = (filterState.board === key) ? 'all' : key;
      }
      switchView(function () { renderAll(); placeCat(false); });
    });
  });

  titems.forEach(function (li) {
    var activate = function () {
      if (li.getAttribute('aria-disabled') === 'true') return;
      var cat = li.getAttribute('data-board');
      filterState.board = (filterState.board === cat) ? 'all' : cat;
      switchView(function () { renderAll(); placeCat(false); });
    };
    li.addEventListener('click', activate);
    li.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); activate(); }
    });
  });

  segs.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = b.getAttribute('data-filter');
      if (next === filterState.lvl) return;
      filterState.lvl = next;
      switchView(function () { renderAll(); });
    });
  });

  if (emptyReset) {
    emptyReset.addEventListener('click', function () {
      filterState.featured = false;
      filterState.board = 'all';
      switchView(function () { renderAll(); placeCat(false); });
    });
  }

  window.addEventListener('resize', function () { placeAll(true); });'''

cut(u'''  /* ---------- 3. 筛选：板块标签（顶部）× 重要程度（分段控件）组合过滤 ---------- */''',
    u'''  window.addEventListener('resize', function () { placeAll(true); });''',
    NEW_JS,
    u'JS 第 3 节重写为 filterState + renderList/renderPanel/renderTabs')

# J2 初始化调用改为 renderAll
rep(u'''  render();
  applyView();
  placeAll(true);''',
    u'''  render();
  renderAll();
  placeAll(true);''',
    u'J2 初始化调用 renderAll')

# ============ 写回与自检 ============
s = s.replace('\n', '\r\n')          # 还原 CRLF 行尾
io.open(P, 'w', encoding='utf-8', newline='').write(s)

ids = re.findall(r'data-page-node-id="([^"]+)"', s)
c = collections.Counter(ids)
dup = {k: v for k, v in c.items() if v > 1}
print('')
print('patches applied: %d' % len(LOG))
print('node ids: %d (before %d), unique %d' % (len(ids), len(orig_ids), len(set(ids))))
print('duplicates: %s' % (dup if dup else 'none'))
print('bytes: %d' % len(s.encode('utf-8')))
if len(ids) != 207 or dup:
    print('!!! NODE ID MISMATCH - restoring backup')
    io.open(P, 'w', encoding='utf-8', newline='').write(
        io.open(r'C:\Users\lenovo\Desktop\test2\.workbuddy\index.before-r15.html', encoding='utf-8', newline='').read())
    sys.exit(1)
print('ALL OK')

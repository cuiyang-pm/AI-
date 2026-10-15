# -*- coding: utf-8 -*-
"""第 16 轮改造：头部标题区（无衬线大标题 + LIVE 荧光绿胶囊）+ 右侧趋势面板轻盈卡片化。
锚点切片替换，保留全部 207 个 data-page-node-id。文件为 CRLF 行尾：读入归一化 LF，写回还原 CRLF。"""
import io, re, sys

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
raw = io.open(P, encoding='utf-8', newline='').read()
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n') if crlf else raw
orig_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
LOG = []

def cut(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: matched %d' % (label, n)); sys.exit(1)
    s = s.replace(old, new, 1)
    LOG.append(label); print('OK   %s' % label)

# ============ A. 导航 .live 状态标签 -> 深色底荧光绿胶囊（pulse 2s 呼吸灯） ============
cut(u'''  .live{
    display:inline-flex;align-items:center;gap:7px;
    font-family:var(--font-sans);font-size:11px;font-weight:400;letter-spacing:1.5px;
    color:var(--gray-500);text-transform:uppercase;
  }
  .live i{width:7px;height:7px;border-radius:0;background:var(--m-orange);animation:pulse 2.4s ease-out infinite}
  @keyframes pulse{
    0%{box-shadow:0 0 0 0 rgba(250,82,15,.35)}
    70%{box-shadow:0 0 0 7px rgba(250,82,15,0)}
    100%{box-shadow:0 0 0 0 rgba(250,82,15,0)}
  }''',
u'''  .live{
    display:inline-flex;align-items:center;gap:7px;flex:0 0 auto;
    background:#1A1A1A;color:#CCFF00;
    font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.5px;
    padding:6px 14px;border-radius:100px;white-space:nowrap;
  }
  .live i{width:6px;height:6px;border-radius:50%;background:#CCFF00;animation:pulse 2s infinite}
  @keyframes pulse{
    0%{box-shadow:0 0 0 0 rgba(204,255,0,.45)}
    70%{box-shadow:0 0 0 7px rgba(204,255,0,0)}
    100%{box-shadow:0 0 0 0 rgba(204,255,0,0)}
  }''',
'A. .live 荧光绿胶囊 + pulse 呼吸灯')

# ============ B. Hero 大标题：无衬线 38px/700/#1A1A1A/-0.5px + 副标题 14px/#888 + 8px 间距 ============
cut(u'''  .hero-band h1{
    margin-top:6px;
    font-family:"Noto Serif SC","Source Han Serif SC","STSong","SimSun",serif;
    font-size:32px;font-weight:600;line-height:1.2;letter-spacing:4px;
    color:#1F2937;
  }
  .hero-band h1::after{
    content:"";display:block;width:76px;height:4px;margin-top:10px;
    background:linear-gradient(90deg,#ffd900 0%,#ffa110 48%,#fa520f 100%);
  }
  .hero-band h1 .accent{color:#1F2937}
  .hero-sub{
    margin-top:7px;
    font-size:16px;font-weight:400;line-height:1.5;letter-spacing:0;
    color:var(--gray-700);
  }''',
u'''  .hero-head{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:6px}
  .hero-band h1{
    font-family:var(--font-sans);
    font-size:38px;font-weight:700;line-height:1.15;letter-spacing:-.5px;
    color:#1A1A1A;
  }
  .hero-band h1 .accent{color:#1A1A1A}
  .hero-sub{
    margin-top:8px;
    font-size:14px;font-weight:400;line-height:1.5;letter-spacing:0;
    color:#888888;
  }''',
'B. Hero 标题区排版（无衬线紧致现代）')

# ============ C. 面板容器：#F9F9FB 轻盈卡片（16px 圆角 / 24px 内边距 / 无边框阴影） ============
cut(u'''  .panel{
    height:100%;display:flex;flex-direction:column;gap:18px;
    padding:2px 0 2px 24px;
    border:none;
    border-left:1px solid var(--line-light);
    border-radius:0;
    background:transparent;
    box-shadow:none;
    animation:rise .6s cubic-bezier(.22,.72,.2,1) .1s backwards;
  }''',
u'''  .panel{
    height:100%;display:flex;flex-direction:column;gap:18px;
    padding:24px;
    border:none;
    border-radius:16px;
    background:#F9F9FB;
    box-shadow:none;
    animation:rise .6s cubic-bezier(.22,.72,.2,1) .1s backwards;
  }''',
'C. 面板容器轻盈卡片化')

# ============ D. 核心数据区：超大 48px 数字 + TODAY'S SELECTED + 今日资讯浓度渐变条 ============
cut(u'''  /* —— 今日趋势 · 13 条精选：独立数据仪表盘（超大数字 + 说明 + 环比胶囊） —— */
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
  /* 环比胶囊随筛选结果变色：降为绿 / 持平为灰（涨红跌绿） */
  .hero-pill.down{background:#ECFDF5;color:#16A34A}
  .hero-pill.flat{background:#F3F4F6;color:#4B5563}''',
u'''  /* —— 今日趋势 · 核心数据：超大数字 + TODAY'S SELECTED + 今日资讯浓度渐变条 —— */
  .hero{display:block;padding:0;background:transparent;border:none}
  .hero-numwrap{display:flex;flex-direction:column;gap:10px;min-width:0}
  .hero-numrow{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
  .hero .num{
    font-family:var(--font-sans);
    font-size:48px;font-weight:700;line-height:1;
    letter-spacing:-1.5px;color:#1A1A1A;
  }
  .hero .unit{
    font-size:12px;font-weight:400;letter-spacing:1px;
    color:#9CA3AF;line-height:1.3;text-transform:uppercase;
  }
  .density{min-width:0}
  .density-label{display:flex;align-items:baseline;gap:6px;font-size:12px;font-weight:400;color:#6B7280;line-height:1.4}
  .hero-pill{
    display:inline-flex;align-items:center;gap:2px;
    font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:0;
    color:#4F46E5;white-space:nowrap;
  }
  .hero-pill .arw{font-size:11px;font-weight:700;line-height:1}
  /* 浓度随筛选结果变色：降为绿 / 持平为灰 */
  .density-label .hero-pill.down{color:#16A34A}
  .density-label .hero-pill.flat{color:#6B7280}
  .density-bar{height:4px;border-radius:2px;background:#E0E7FF;overflow:hidden;margin-top:6px}
  .density-bar span{
    display:block;height:100%;width:0;border-radius:2px;
    background:linear-gradient(90deg,#E0E7FF 0%,#4F46E5 100%);
    transition:width .55s cubic-bezier(.22,.72,.2,1),background .3s ease;
  }
  .density.down .density-bar span{background:linear-gradient(90deg,#D1FAE5,#16A34A)}
  .density.flat .density-bar span{background:#9CA3AF}''',
'D. 核心数据区：48px 大数字 + 浓度渐变条')

# ============ E. 区块标题：14px / 600 / 深灰 ============
cut(u'''  .block-title{
    display:flex;align-items:baseline;justify-content:space-between;gap:10px;
    font-family:var(--font-sans);font-size:12px;font-weight:400;
    letter-spacing:2px;color:#4B5563;text-transform:uppercase;
  }''',
u'''  .block-title{
    display:flex;align-items:baseline;justify-content:space-between;gap:10px;
    font-family:var(--font-sans);font-size:14px;font-weight:600;
    letter-spacing:0;color:#1F2937;text-transform:none;
  }''',
'E. 板块分布/热点关键词标题 14px 600')

# ============ F. 板块行三态：中性灰系（悬停 / 选中 / 禁用） ============
cut(u'''  /* 板块行即筛选器：悬停浅橙 / 选中橙字 / 零结果禁用（再点当前项取消） */
  .titem:hover{background:rgba(255,247,237,.75)}
  .titem:focus-visible{outline:2px solid var(--m-orange);outline-offset:1px}
  .titem[aria-pressed="true"]{background:#FFF7ED}
  .titem[aria-pressed="true"] .tname{color:#EA580C;font-weight:600}
  .titem[aria-pressed="true"] .tnum{color:#EA580C;font-weight:700}
  .titem[aria-disabled="true"]{opacity:.45;cursor:default}
  .titem[aria-disabled="true"]:hover{background:transparent}''',
u'''  /* 板块行即筛选器：悬停浅灰 / 选中深灰标签反色 / 零结果禁用（再点当前项取消） */
  .titem:hover{background:rgba(17,17,17,.04)}
  .titem:focus-visible{outline:2px solid #4F46E5;outline-offset:1px}
  .titem[aria-pressed="true"]{background:rgba(17,17,17,.05)}
  .titem[aria-pressed="true"] .tname{color:#1A1A1A;font-weight:600}
  .titem[aria-pressed="true"] .tnum{background:#1A1A1A;color:#FFFFFF}
  .titem[aria-disabled="true"]{opacity:.45;cursor:default}
  .titem[aria-disabled="true"]:hover{background:transparent}''',
'F. 板块行三态改中性灰系')

# ============ G. 今日数字改微小圆角标签（#EAEAEA 底 / 深灰字） ============
cut(u'''  .tnum{font-family:var(--font-mono);font-size:12px;font-weight:400;color:#4B5563}''',
u'''  .tnum{font-family:var(--font-sans);font-size:12px;font-weight:600;color:#3F3F46;background:#EAEAEA;border-radius:6px;padding:2px 9px;min-width:26px;text-align:center;line-height:1.5}''',
'G. tnum 数字改圆角小标签')

# ============ H. 热点关键词：极简描边标签（透明底 / 1px 深灰边框 / 悬停反色） ============
cut(u'''  /* —— 热点关键词：统一圆角胶囊 + 自然流式换行 + 点击按压缩放 —— */
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
  .kw span:active{transform:scale(.94)}''',
u'''  /* —— 热点关键词：极简描边标签（透明底 / 1px 深灰边框 / 圆角 6px / 悬停深灰底白字） —— */
  .kw{display:flex;flex-wrap:wrap;gap:8px}
  .kw span{
    font-family:var(--font-sans);font-size:12px;font-weight:400;letter-spacing:0;
    color:#374151;
    background:transparent;
    border:1px solid #4B5563;border-radius:6px;
    padding:4px 10px;cursor:pointer;max-width:100%;overflow-wrap:anywhere;
    transition:background .2s,color .2s,border-color .2s,transform .18s cubic-bezier(.2,.8,.2,1);
  }
  .kw span:hover{background:#374151;border-color:#374151;color:#FFFFFF}
  .kw span:active{transform:scale(.94)}''',
'H. 关键词改描边标签 + 悬停反色')

# ============ I. 关键词图例：双底色区分已无意义，隐藏图例项保留「共 8 个」 ============
cut(u'''  .kwcap{display:flex;align-items:center;gap:14px;margin-top:10px;font-size:11px;font-weight:400;letter-spacing:0;color:#4B5563}''',
u'''  .kwcap{display:flex;align-items:center;gap:14px;margin-top:10px;font-size:11px;font-weight:400;letter-spacing:0;color:#4B5563}
  .kwcap .kc{display:none}''',
'I. 隐藏关键词双底色图例项')

# ============ J. 阅读进度：极细 2px / 深灰填充 ============
cut(u'''  .pbar{height:6px;border-radius:3px;background:#E5E7EB;overflow:hidden}
  .pbar-fill{
    display:block;height:100%;width:0;border-radius:3px;
    background:var(--m-orange);
    transition:width .55s cubic-bezier(.22,.72,.2,1);
  }''',
u'''  .pbar{height:2px;border-radius:1px;background:#E5E7EB;overflow:hidden}
  .pbar-fill{
    display:block;height:100%;width:0;border-radius:1px;
    background:#4B5563;
    transition:width .55s cubic-bezier(.22,.72,.2,1);
  }''',
'J. 阅读进度条 2px 深灰')

# ============ K. 860 断点：标题/副标题/状态胶囊收窄 ============
cut(u'''    .hero-band h1{font-size:32px;line-height:1.2;letter-spacing:4px;word-break:keep-all}
    .hero-sub{margin-top:8px;font-size:15.5px;line-height:1.5}''',
u'''    .hero-band h1{font-size:32px;line-height:1.2;letter-spacing:-.5px;word-break:keep-all}
    .hero-sub{margin-top:8px;font-size:14px;line-height:1.5}
    .live{font-size:11px;padding:5px 11px}''',
'K. 860 断点标题排版')

# ============ L. 860 断点：hero 数据区字号 ============
cut(u'''    .hero{padding:16px 14px;gap:12px}
    .hero .num{font-size:32px}''',
u'''    .hero-head{gap:12px}
    .hero .num{font-size:40px}''',
'L. 860 断点大数字 40px')

# ============ M. 860 断点：面板卡片化（去顶部细线，自带卡片底） ============
cut(u'''    .right{width:auto;flex:none;margin-top:18px;padding-top:18px;border-top:1px solid var(--line-light)}
    .panel{height:auto;padding:0;border-left:none;gap:16px}''',
u'''    .right{width:auto;flex:none;margin-top:18px;padding-top:0;border-top:none}
    .panel{height:auto;padding:20px;gap:16px}''',
'M. 860 断点面板卡片')

# ============ N. 420 断点：大数字 / 浓度说明 / 关键词收窄 ============
cut(u'''    .kw span{padding:5px 11px}''',
u'''    .kw span{padding:3px 8px}''',
'N1. 420 关键词内边距')
cut(u'''    .hero{padding:14px 12px;gap:10px}
    .hero .num{font-size:30px}
    .hero-pill{font-size:11.5px;padding:4px 9px}''',
u'''    .hero .num{font-size:34px}
    .hero .unit{font-size:11px}''',
'N2. 420 大数字 34px')

# ============ O. 导航：LIVE 与「今日 13 条精选」合并进 Hero 状态胶囊，导航去重 ============
cut(u'''      <span class="live" data-page-node-id="WhLSD8GN4cFJpTeSNLeUKu"><i data-page-node-id="B9gro87HSA9uDjOvn5namS"></i>LIVE</span>
      <button class="nav-cta" type="button">今日 13 条精选</button>
''',
u'',
'O. 导航移除重复的 LIVE 与精选按钮')

# ============ P. Hero 标题行：标题左 + 状态胶囊紧挨右侧 ============
cut(u'''    <h1 data-page-node-id="vY7r0bAOTjHHBJyda1zHYP">AI 行业<span class="accent">日报</span></h1>
    <p class="hero-sub">3分钟，追上今天所有AI大事。</p>''',
u'''    <div class="hero-head">
      <h1 data-page-node-id="vY7r0bAOTjHHBJyda1zHYP">AI 行业<span class="accent">日报</span></h1>
      <span class="live" data-page-node-id="WhLSD8GN4cFJpTeSNLeUKu"><i data-page-node-id="B9gro87HSA9uDjOvn5namS"></i>LIVE · 今日 13 条精选</span>
    </div>
    <p class="hero-sub">3分钟，追上今天所有AI大事。</p>''',
'P. Hero 标题行加状态胶囊')

# ============ Q. 面板核心数据 HTML：48px 数字 + TODAY'S SELECTED + 浓度渐变条 ============
cut(u'''        <div class="hero" data-page-node-id="otg5Img00BxuDmRg6aCOKM">
          <div class="hero-numwrap" data-page-node-id="BHnaBikreQtxtydu4KCcv1">
            <div id="heroNum" class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>
            <div class="unit">精选资讯</div>
          </div>
          <span id="heroPill" class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH">较昨日 <span class="arw">↑</span> 44%</span>
        </div>''',
u'''        <div class="hero" data-page-node-id="otg5Img00BxuDmRg6aCOKM">
          <div class="hero-numwrap" data-page-node-id="BHnaBikreQtxtydu4KCcv1">
            <div class="hero-numrow">
              <div id="heroNum" class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>
              <span class="unit">TODAY'S SELECTED</span>
            </div>
            <div class="density" id="densityBox">
              <div class="density-label">今日资讯浓度 <span id="heroPill" class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH"><span class="arw">↑</span> 44%</span></div>
              <div class="density-bar"><span id="densityFill" style="width:44%"></span></div>
            </div>
          </div>
        </div>''',
'Q. 面板核心数据 HTML 重排')

# ============ R. JS：新增 densityFill / densityBox 引用 ============
cut(u'''  var heroNum = document.getElementById('heroNum');
  var heroPill = document.getElementById('heroPill');''',
u'''  var heroNum = document.getElementById('heroNum');
  var heroPill = document.getElementById('heroPill');
  var densityFill = document.getElementById('densityFill');
  var densityBox = document.getElementById('densityBox');''',
'R. JS 新增 density 引用')

# ============ S. JS：renderPanel 同步浓度条宽度与色调 ============
cut(u'''    heroPill.innerHTML = '较昨日 ' + body;
    heroPill.classList.toggle('down', tone === 'down');
    heroPill.classList.toggle('flat', tone === 'flat');''',
u'''    heroPill.innerHTML = body;
    var pctW = y > 0 ? Math.min(Math.abs(Math.round((t - y) / y * 100)), 100) : (t > 0 ? 100 : 0);
    densityFill.style.width = pctW + '%';
    densityBox.classList.toggle('down', tone === 'down');
    densityBox.classList.toggle('flat', tone === 'flat');''',
'S. JS renderPanel 浓度条联动')

# ============ 写回与自检 ============
new_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
assert len(new_ids) == 207 and len(set(new_ids)) == 207, 'node-id broken: %d/%d' % (len(new_ids), len(set(new_ids)))
assert set(new_ids) == set(orig_ids), 'node-id set changed!'
if crlf:
    s = s.replace('\n', '\r\n')
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('\nALL %d patches applied; node-ids conserved (207 unique).' % len(LOG))
print('bytes: %d' % len(s.encode('utf-8')))

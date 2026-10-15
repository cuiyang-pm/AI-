# -*- coding: utf-8 -*-
"""第 17 轮：全局 Quiet Blue 换肤（浅灰白基调 / 霓虹蓝唯一强调色 / 12px 圆角轻阴影）"""
import io, re, sys

P = r'C:\Users\lenovo\Desktop\test2\ai-daily-dashboard\index.html'
s = io.open(P, encoding='utf-8', newline='').read()
s = s.replace('\r\n', '\n')  # CRLF -> LF 归一化，写回时还原
orig_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
LOG = []

def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: matched %d' % (label, n))
        sys.exit(1)
    s = s.replace(old, new, 1)
    LOG.append(label)
    print('OK   %s' % label)

# ---------- R1a 色板：橙金系 -> 蓝灰系 ----------
rep(u'''    --m-orange:#fa520f;
    --m-flame:#fb6424;
    --m-block:#ff8105;
    --m-sun-900:#ff8a00;
    --m-sun-700:#ffa110;
    --m-sun-500:#ffb83e;
    --m-sun-300:#ffd06a;
    --m-gold:#ffe295;
    --m-yellow:#ffd900;
    --m-ivory:#fffaeb;
    --m-cream:#fff0c2;''',
u'''    /* 霓虹蓝强调色（唯一 accent） */
    --blue:#2563EB;
    --blue-deep:#1D4ED8;
    --blue-soft:#DBEAFE;
    --blue-tint:#EFF6FF;
    --m-orange:#2563EB;
    --m-flame:#1D4ED8;
    --m-block:#3B82F6;
    --m-sun-900:#3B82F6;
    --m-sun-700:#2563EB;
    --m-sun-500:#60A5FA;
    --m-sun-300:#93C5FD;
    --m-gold:#BFDBFE;
    --m-yellow:#60A5FA;
    --m-ivory:#F7F8FA;
    --m-cream:#EEF1F5;''', 'R1a 色板主色')

rep(u'''    --ink:#1f1f1f;
    --ink-strong:#1f1f1f;
    --gray-700:#3d3d3d;
    --gray-600:#3d3d3d;
    --gray-500:#7f6315;
    --charcoal:#1f1f1f;''',
u'''    --ink:#1A1A1A;
    --ink-strong:#1A1A1A;
    --gray-700:#374151;
    --gray-600:#4B5563;
    --gray-500:#888888;
    --charcoal:#1A1A1A;''', 'R1b 中性色')

rep(u'''    --surface-2:rgba(127,99,21,.08);
    --line:rgba(127,99,21,.15);
    --line-light:rgba(127,99,21,.08);''',
u'''    --surface-2:rgba(17,24,39,.04);
    --line:rgba(17,24,39,.10);
    --line-light:rgba(17,24,39,.06);''', 'R1c 线与表面')

rep(u'''    --bg-surface:var(--m-cream);''',
u'''    --bg-surface:var(--white);''', 'R1d bg-surface')

rep(u'''    --tint-brand:rgba(250,82,15,.10);
    --tint-brand-line:rgba(250,82,15,.35);
    --tint-orange:rgba(250,82,15,.10);
    --tint-orange-line:rgba(250,82,15,.35);
    --tint-green:var(--white);
    --tint-green-line:rgba(127,99,21,.28);''',
u'''    --tint-brand:rgba(37,99,235,.08);
    --tint-brand-line:rgba(37,99,235,.30);
    --tint-orange:rgba(37,99,235,.08);
    --tint-orange-line:rgba(37,99,235,.30);
    --tint-green:var(--white);
    --tint-green-line:rgba(17,24,39,.15);''', 'R1e tint 系')

rep(u'''    /* Mistral 字体体系：Arial 全家桶，raw clarity */
    --font-sans:Arial,'Helvetica Neue',Helvetica,'PingFang SC','Microsoft YaHei',sans-serif;
    --font-display:Arial,'Helvetica Neue',Helvetica,'PingFang SC','Microsoft YaHei',sans-serif;''',
u'''    /* 字体体系：系统无衬线（Inter / PingFang SC），拉开字重对比 */
    --font-sans:'Inter','PingFang SC','Helvetica Neue','Microsoft YaHei',Arial,sans-serif;
    --font-display:'Inter','PingFang SC','Helvetica Neue','Microsoft YaHei',Arial,sans-serif;''', 'R1f 字体')

rep(u'''    /* Mistral 圆角：一切归零，锐利建筑感 */
    --r-badge:0px;
    --r-btn:0px;
    --r-nav:0px;
    --r-card:0px;
    --r-panel:0px;
    --r-pill:0px;''',
u'''    /* 圆角体系：卡片与模块统一 12px */
    --r-badge:6px;
    --r-btn:10px;
    --r-nav:0px;
    --r-card:12px;
    --r-panel:12px;
    --r-pill:999px;''', 'R1g 圆角')

rep(u'''    /* Mistral 阴影体系：标志性金色多层暖影 */
    --shadow-subtle:none;
    --shadow-ambient:rgba(127,99,21,.14) 0px 10px 28px;
    --shadow-card:-8px 16px 39px rgba(127,99,21,.12),-33px 64px 72px rgba(127,99,21,.10),-73px 144px 97px rgba(127,99,21,.06);
    --shadow-deep:rgba(127,99,21,.16) 0px 16px 44px;''',
u'''    /* 阴影体系：极轻阴影，轻盈感 */
    --shadow-subtle:0 2px 8px rgba(0,0,0,.04);
    --shadow-ambient:0 2px 8px rgba(0,0,0,.04);
    --shadow-card:0 2px 8px rgba(0,0,0,.04);
    --shadow-deep:0 10px 24px rgba(0,0,0,.08);''', 'R1h 阴影')

# ---------- R2 画板阴影 ----------
rep(u'box-shadow:0 0 0 1px var(--line),rgba(127,99,21,.18) 0 24px 60px;',
u'box-shadow:0 0 0 1px var(--line),0 24px 60px rgba(17,24,39,.08);', 'R2 画板阴影')

# ---------- R3 导航底色 ----------
rep(u'background:rgba(255,250,235,.92);',
u'background:rgba(247,248,250,.92);', 'R3 导航底色')

# ---------- R4 Logo 渐变 -> 纯霓虹蓝 ----------
rep(u'background:linear-gradient(135deg,#ffd900 0%,#ffa110 45%,#fa520f 100%);',
u'background:var(--blue);', 'R4 Logo')

# ---------- R5 状态胶囊：黑底荧光绿 -> 浅蓝底蓝字蓝点 ----------
rep(u'''    background:#1A1A1A;color:#CCFF00;
    font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.5px;
    padding:6px 14px;border-radius:100px;white-space:nowrap;
  }
  .live i{width:6px;height:6px;border-radius:50%;background:#CCFF00;animation:pulse 2s infinite}
  @keyframes pulse{
    0%{box-shadow:0 0 0 0 rgba(204,255,0,.45)}
    70%{box-shadow:0 0 0 7px rgba(204,255,0,0)}
    100%{box-shadow:0 0 0 0 rgba(204,255,0,0)}
  }''',
u'''    background:var(--blue-tint);color:var(--blue);
    font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.3px;
    padding:6px 14px;border-radius:999px;white-space:nowrap;
  }
  .live i{width:6px;height:6px;border-radius:50%;background:var(--blue);animation:pulse 2s infinite}
  @keyframes pulse{
    0%{box-shadow:0 0 0 0 rgba(37,99,235,.35)}
    70%{box-shadow:0 0 0 6px rgba(37,99,235,0)}
    100%{box-shadow:0 0 0 0 rgba(37,99,235,0)}
  }''', 'R5 状态胶囊')

# ---------- R6 Hero 辉光 ----------
rep(u'background:radial-gradient(circle,rgba(255,161,16,.10) 0%,rgba(250,82,15,.05) 40%,transparent 70%);',
u'background:radial-gradient(circle,rgba(37,99,235,.07) 0%,rgba(37,99,235,.03) 40%,transparent 70%);', 'R6 辉光')

# ---------- R7 滑块 ----------
rep(u'width:0;height:0;background:var(--m-orange);border-radius:0;',
u'width:0;height:0;background:var(--blue);border-radius:999px;', 'R7 滑块')

# ---------- R8 徽章选中色 ----------
rep(u'.hero-tab.active .tbadge{background:var(--white);color:#EA580C}',
u'.hero-tab.active .tbadge{background:var(--white);color:var(--blue)}', 'R8 徽章选中')

# ---------- R9 半选态 ----------
rep(u'''  .hero-tab.semi{color:#EA580C}
  .hero-tab.semi .tbadge{background:#FFF7ED;color:#EA580C}
  .hero-tab.semi .tunit{color:#EA580C}''',
u'''  .hero-tab.semi{color:var(--blue)}
  .hero-tab.semi .tbadge{background:var(--blue-tint);color:var(--blue)}
  .hero-tab.semi .tunit{color:var(--blue)}''', 'R9 半选态')

# ---------- R10 摘要卡 ----------
rep(u'''    border:none;border-left:4px solid #EA580C;
    border-radius:0;
    background:var(--white);
    box-shadow:none;''',
u'''    border:1px solid #ECEEF1;border-left:3px solid var(--blue);
    border-radius:12px;
    background:var(--white);
    box-shadow:var(--shadow-card);''', 'R10 摘要卡')

# ---------- R11 摘要符号圆点化 ----------
rep(u'''    width:7px;height:7px;background:var(--m-orange);
  }''',
u'''    width:7px;height:7px;border-radius:50%;background:var(--blue);
  }''', 'R11 摘要符号')

rep(u'.sec-head .dot{width:8px;height:8px;border-radius:0;background:var(--m-orange);flex:0 0 8px}',
u'.sec-head .dot{width:8px;height:8px;border-radius:50%;background:var(--blue);flex:0 0 8px}', 'R11b 区块圆点')

# ---------- R12 芯片胶囊 ----------
rep(u'''    border:1px solid var(--line);border-radius:0;
    padding:5px 12px;background:var(--white);''',
u'''    border:1px solid var(--line);border-radius:999px;
    padding:5px 12px;background:var(--white);''', 'R12 芯片')

# ---------- R13 分段控件 ----------
rep(u'.seg:hover{color:#C2410C;border-color:rgba(250,82,15,.45);background:#FFF7ED}',
u'.seg:hover{color:var(--blue-deep);border-color:rgba(37,99,235,.45);background:var(--blue-tint)}', 'R13a seg hover')
rep(u'''  .seg.active{background:#FFF7ED;border-color:#EA580C;color:#EA580C}
  .seg.active:hover{background:#FFF7ED;border-color:#EA580C;color:#C2410C}
  .seg.active b{color:#EA580C}''',
u'''  .seg.active{background:var(--blue-tint);border-color:var(--blue);color:var(--blue)}
  .seg.active:hover{background:var(--blue-tint);border-color:var(--blue);color:var(--blue-deep)}
  .seg.active b{color:var(--blue)}''', 'R13b seg active')

# ---------- R14 新闻卡片 ----------
rep(u'''    border:1px solid rgba(234,88,12,.22);
    border-radius:8px;
    background:linear-gradient(to left,#fed7aa,#fff7ed);
    box-shadow:0 4px 6px -1px rgba(0,0,0,.1),0 2px 4px -2px rgba(0,0,0,.1);''',
u'''    border:1px solid #ECEEF1;
    border-radius:12px;
    background:var(--white);
    box-shadow:var(--shadow-card);''', 'R14a 卡片基底')
rep(u'''  .news:hover{
    transform:translateY(-4px);
    border-color:rgba(234,88,12,.45);
    box-shadow:0 14px 22px -6px rgba(234,88,12,.18),0 6px 10px -4px rgba(0,0,0,.08);
  }''',
u'''  .news:hover{
    transform:translateY(-4px);
    border-color:#D6DAE0;
    box-shadow:0 12px 24px rgba(0,0,0,.08);
  }
  /* 高优先级提示：极细霓虹蓝左侧条（取代旧橙色描边） */
  .news[data-lvl="high"]{border-left:3px solid var(--blue)}''', 'R14b 卡片悬停+蓝条')
rep(u'''  .card-feat{
    padding:16px;
    border:none;
    border-radius:8px;
    box-shadow:var(--shadow-card);
  }''',
u'''  .card-feat{
    padding:16px;
    border:none;border-left:3px solid var(--blue);
    border-radius:12px;
    box-shadow:var(--shadow-card);
  }''', 'R14c 头条卡')

# ---------- R15 头条顶部条 ----------
rep(u'''    border-radius:8px 8px 0 0;
    background:linear-gradient(90deg,#ffd900 0%,#ffa110 48%,#fa520f 100%);''',
u'''    border-radius:12px 12px 0 0;
    background:var(--blue);''', 'R15 头条顶条')

# ---------- R16 重要程度标签 ----------
rep(u'''  .lvl i{width:5px;height:5px;border-radius:0;background:currentColor}
  .lvl-high{background:var(--m-orange);border:1px solid var(--m-orange);color:var(--white)}
  .lvl-mid{background:var(--white);border:1px solid rgba(234,88,12,.25);color:#9A3412}''',
u'''  .lvl i{width:5px;height:5px;border-radius:50%;background:currentColor}
  .lvl-high{background:#F3F4F6;border:1px solid transparent;color:#4B5563}
  .lvl-mid{background:#F3F4F6;border:1px solid transparent;color:#4B5563}''', 'R16 等级标签')

# ---------- R17 分类标签 ----------
rep(u'''    border:1px solid var(--line);background:var(--white);
    border-radius:0;padding:3px 11px;''',
u'''    border:1px solid transparent;background:#F3F4F6;
    border-radius:6px;padding:3px 11px;''', 'R17 分类标签')

# ---------- R18 滚动条 ----------
rep(u'background:rgba(234,88,12,.25);border-radius:40px',
u'background:rgba(37,99,235,.30);border-radius:40px', 'R18 滚动条')

# ---------- R19 统计标签 ----------
rep(u'''    background:var(--white);border:1px solid var(--line);
    border-radius:0;padding:5px 11px;''',
u'''    background:#F3F4F6;border:1px solid transparent;
    border-radius:6px;padding:5px 11px;''', 'R19 统计标签')
rep(u'.card-feat .nstat span{font-size:12.5px;padding:6px 12px;background:var(--white)}',
u'.card-feat .nstat span{font-size:12.5px;padding:6px 12px;background:#F3F4F6}', 'R19b 头条统计')

# ---------- R20 完成按钮 ----------
rep(u'''    color:#EA580C;background-color:#FFF7ED;
    border-style:solid;border-width:2px;border-color:rgba(255,255,255,.6);
    border-radius:40px;padding:12px 24px;
    box-shadow:-4px -2px 16px 0px #ffffff,4px 2px 16px 0px rgba(234,88,12,.15);
    transition:.2s;
  }
  .done-btn:hover{color:#C2410C;background-color:#FFEDD5;box-shadow:-2px -1px 8px 0px #ffffff,2px 1px 8px 0px rgba(234,88,12,.3)}''',
u'''    color:var(--blue);background-color:var(--blue-tint);
    border-style:solid;border-width:1px;border-color:var(--blue-tint);
    border-radius:40px;padding:12px 24px;
    box-shadow:0 2px 8px rgba(0,0,0,.04);
    transition:.2s;
  }
  .done-btn:hover{color:var(--blue-deep);background-color:var(--blue-soft);box-shadow:0 6px 16px rgba(37,99,235,.18)}''', 'R20a 按钮')
rep(u'.done-btn:focus-visible{outline:2px solid #EA580C;outline-offset:2px}',
u'.done-btn:focus-visible{outline:2px solid var(--blue);outline-offset:2px}', 'R20b 焦点')
rep(u'''    background:linear-gradient(to left,#fed7aa,#ffedd5);
    box-shadow:inset 0 0 0 1px rgba(234,88,12,.35);
  }
  .card-feat.done{box-shadow:inset 0 0 0 1px rgba(234,88,12,.35),var(--shadow-card)}
  .news.done .done-btn{
    color:#FFFFFF;background-color:#EA580C;border-color:rgba(255,255,255,.55);
    box-shadow:0 4px 10px -2px rgba(234,88,12,.45);
  }
  .news.done .done-btn:hover{color:#FFFFFF;background-color:#C2410C}''',
u'''    background:#F9FAFB;
    box-shadow:inset 0 0 0 1px rgba(17,24,39,.08);
  }
  .card-feat.done{box-shadow:inset 0 0 0 1px rgba(17,24,39,.08),var(--shadow-card)}
  .news.done .done-btn{
    color:#FFFFFF;background-color:var(--blue);border-color:var(--blue);
    box-shadow:0 4px 10px -2px rgba(37,99,235,.45);
  }
  .news.done .done-btn:hover{color:#FFFFFF;background-color:var(--blue-deep)}''', 'R20c 已读态')

# ---------- R21 对勾徽章 ----------
rep(u'width:26px;height:26px;border-radius:0;',
u'width:26px;height:26px;border-radius:50%;', 'R21 对勾徽章')

# ---------- R22 空态 ----------
rep(u'''    background:var(--white);
    border-left:4px solid #EA580C;''',
u'''    background:var(--white);
    border:1px solid #ECEEF1;border-left:3px solid var(--blue);
    border-radius:12px;box-shadow:var(--shadow-card);''', 'R22a 空态')
rep(u'.cards-empty .ce-btn:hover{background:#FFF7ED;border-color:rgba(250,82,15,.35);color:#C2410C}',
u'.cards-empty .ce-btn:hover{background:var(--blue-tint);border-color:rgba(37,99,235,.35);color:var(--blue)}', 'R22b 空态按钮')

# ---------- R23 面板容器：纯白 + 细分割线 ----------
rep(u'''    padding:24px;
    border:none;
    border-radius:16px;
    background:#F9F9FB;
    box-shadow:none;''',
u'''    padding:24px;gap:14px;
    border:1px solid #ECEEF1;
    border-radius:12px;
    background:var(--white);
    box-shadow:var(--shadow-card);''', 'R23a 面板容器')
rep(u'''.phead{padding-bottom:0;border-bottom:none}''',
u'''.phead{padding-bottom:0;border-bottom:none}
  /* 模块间用极细灰分割线区分（板块分布 / 热点关键词） */
  .panel > .hero ~ div{border-top:1px solid var(--line-light);padding-top:14px}''', 'R23b 分割线')

# ---------- R24 核心数据独立小卡 ----------
rep(u'.hero{display:block;padding:0;background:transparent;border:none}',
u'.hero{display:block;padding:14px 16px;background:var(--white);border:1px solid #ECEEF1;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.04)}', 'R24 指标小卡')

# ---------- R25 浓度条 ----------
rep(u'''    color:#4F46E5;white-space:nowrap;''',
u'''    color:var(--blue);white-space:nowrap;''', 'R25a 浓度值')
rep(u'.density-label .hero-pill.down{color:#16A34A}',
u'.density-label .hero-pill.down{color:#6B7280}', 'R25b 浓度降')
rep(u'.density-bar{height:4px;border-radius:2px;background:#E0E7FF;overflow:hidden;margin-top:6px}',
u'.density-bar{height:4px;border-radius:2px;background:var(--blue-tint);overflow:hidden;margin-top:6px}', 'R25c 浓度槽')
rep(u'background:linear-gradient(90deg,#E0E7FF 0%,#4F46E5 100%);',
u'background:linear-gradient(90deg,#60A5FA 0%,#2563EB 100%);', 'R25d 浓度填充')
rep(u'.density.down .density-bar span{background:linear-gradient(90deg,#D1FAE5,#16A34A)}',
u'.density.down .density-bar span{background:#9CA3AF}', 'R25e 浓度降条')

# ---------- R26 增减配色：升=霓虹蓝 / 降=灰 ----------
rep(u'''  .legend .l-up{border-bottom:6px solid #E5484D}
  .legend .l-down{border-top:6px solid #16A34A}''',
u'''  .legend .l-up{border-bottom:6px solid #2563EB}
  .legend .l-down{border-top:6px solid #9CA3AF}''', 'R26a 图例')
rep(u'''  .tdelta.up{color:#E5484D}
  .tdelta.down{color:#16A34A}''',
u'''  .tdelta.up{color:#2563EB}
  .tdelta.down{color:#9CA3AF}''', 'R26b 增减')
rep(u'.titem:focus-visible{outline:2px solid #4F46E5;outline-offset:1px}',
u'.titem:focus-visible{outline:2px solid var(--blue);outline-offset:1px}', 'R26c 焦点')

# ---------- R27 关键词：浅灰底 + 悬停霓虹蓝 ----------
rep(u'''    background:transparent;
    border:1px solid #4B5563;border-radius:6px;''',
u'''    background:#F3F4F6;
    border:1px solid transparent;border-radius:6px;''', 'R27a 关键词底')
rep(u'.kw span:hover{background:#374151;border-color:#374151;color:#FFFFFF}',
u'.kw span:hover{background:var(--blue);border-color:var(--blue);color:#FFFFFF}', 'R27b 关键词悬停')
rep(u'.kwcap .kd-today{background:#FFF7ED;box-shadow:inset 0 0 0 1px rgba(250,82,15,.28)}',
u'.kwcap .kd-today{background:var(--blue-tint);box-shadow:inset 0 0 0 1px rgba(37,99,235,.25)}', 'R27c 图例点')

# ---------- R28 阅读进度条 ----------
rep(u'''    background:#4B5563;
    transition:width .55s cubic-bezier(.22,.72,.2,1);''',
u'''    background:var(--blue);
    transition:width .55s cubic-bezier(.22,.72,.2,1);''', 'R28 进度条')

# ---------- R29 重置按钮 ----------
rep(u'.ghost:hover{background:#FFF7ED;border-color:rgba(250,82,15,.35);color:#C2410C}',
u'.ghost:hover{background:var(--blue-tint);border-color:rgba(37,99,235,.35);color:var(--blue)}', 'R29 重置按钮')

# ---------- R30 页脚 ----------
rep(u'''    background:linear-gradient(90deg,#ffd900 0%,#ffe295 20%,#ffa110 42%,#ff8105 62%,#fb6424 82%,#fa520f 100%);
    border-top:none;
    font-size:12px;font-weight:400;color:rgba(31,31,31,.85);letter-spacing:.3px;
  }
  .footbar a{color:var(--ink);text-decoration:underline;text-underline-offset:2px}
  .footbar a:hover{color:var(--white)}''',
u'''    background:var(--ink);
    border-top:none;
    font-size:12px;font-weight:400;color:rgba(255,255,255,.75);letter-spacing:.3px;
  }
  .footbar a{color:#FFFFFF;text-decoration:underline;text-underline-offset:2px}
  .footbar a:hover{color:#93C5FD}''', 'R30a 页脚')
rep(u'.footbar .keys b{color:var(--ink);font-weight:400}',
u'.footbar .keys b{color:#FFFFFF;font-weight:400}', 'R30b 页脚键名')

# ---------- R31 滚动进度条 ----------
rep(u'background:linear-gradient(90deg,#ffa110,#fa520f);',
u'background:var(--blue);', 'R31 滚动进度条')

# ---------- R32 面板标题字重 ----------
rep(u".phead h2{font-family:var(--font-display);font-size:22px;font-weight:400;line-height:1.2;letter-spacing:-.3px;color:var(--ink)}",
u".phead h2{font-family:var(--font-display);font-size:22px;font-weight:700;line-height:1.2;letter-spacing:-.3px;color:var(--ink)}", 'R32 面板标题')

# ---------- 写回与自检（还原 CRLF 行尾） ----------
io.open(P, 'w', encoding='utf-8', newline='\r\n').write(s)
new_ids = re.findall(r'data-page-node-id="([^"]+)"', s)
assert orig_ids == new_ids, 'node ids changed!'
print('\nALL %d patches applied; node ids intact (%d)' % (len(LOG), len(new_ids)))
left = [c for c in ['#EA580C','#FFF7ED','#fa520f','#ffa110','#ffd900','#CCFF00','#E5484D','#16A34A','#4F46E5','#E0E7FF','#D1FAE5','#C2410C','#9A3412','fed7aa','fff7ed','ffedd5','127,99,21','250,82,15','204,255,0','234,88,12','#fb6424','#ff8105','#ffe295','#ffd06a','#ffb83e','#ff8a00','#fff0c2','#fffaeb'] if c in s]
print('legacy colors left:', left if left else 'none')

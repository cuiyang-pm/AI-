import { JSDOM } from "file:///C:/Users/lenovo/.workbuddy/binaries/node/workspace/node_modules/jsdom/lib/api.js";
import fs from "fs";

const FILE = "C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html";
const html = fs.readFileSync(FILE, "utf8");
const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true });
const win = dom.window;
const doc = win.document;

let pass = 0, fail = 0;
const ok = (n, c, extra = "") => {
  c ? pass++ : fail++;
  console.log(`${c ? "PASS" : "FAIL"}  ${n}${extra ? "  -> " + extra : ""}`);
};
const click = (el) =>
  el.dispatchEvent(new win.MouseEvent("click", { bubbles: true, cancelable: true }));
const key = (k) =>
  win.dispatchEvent(new win.KeyboardEvent("keydown", { key: k, bubbles: true }));

const cards = [...doc.querySelectorAll(".news")];
const btns = [...doc.querySelectorAll(".done-btn")];
const readCount = doc.getElementById("readCount");
const readFill = doc.getElementById("readFill");
const resetBtn = doc.getElementById("resetBtn");
const segs = [...doc.querySelectorAll(".seg")];
const cardsWrap = doc.querySelector(".cards");
const filterCount = doc.getElementById("filterCount");

// 十二轮后：圆形进度环 -> 线性进度条，进度以条宽百分比表达
const pctNum = () => Math.round(parseFloat(readFill.style.width || "0"));
const fillNum = () => parseFloat(readFill.style.width || "0");
const visible = () => cards.filter((c) => !c.hidden);
const segBy = (f) => segs.find((b) => b.getAttribute("data-filter") === f);

// 十三轮起：切换筛选带 170ms 淡出 + 300ms 淡入过渡，断言需等动效落定
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const clickSeg = async (b) => { click(b); await sleep(240); };

const tabs = [...doc.querySelectorAll(".hero-tab")];
const tabBy = (c) => tabs.find((b) => b.getAttribute("data-scope") === c);
const clickTab = async (b) => { click(b); await sleep(240); };
const tabInd = doc.getElementById("tabInd");
const cardsEmpty = doc.getElementById("cardsEmpty");
const heroBox = doc.querySelector(".hero");

console.log("=== 1. 页面结构 ===");
ok("三条新闻卡片", cards.length === 3, `got ${cards.length}`);
ok("每张卡片都有重要程度标签", doc.querySelectorAll(".news .lvl").length === 3);
ok("每张卡片都有阅读完成按钮", btns.length === 3);
ok("卡片的新闻链接指向 AIHOT 详情页",
  cards.every((c) => /^https:\/\/aihot\.news\/items\//.test(c.querySelector(".ntitle a").href)));
ok("卡片的链接都开了新窗口",
  cards.every((c) => c.querySelector(".ntitle a").target === "_blank"));

console.log("\n=== 2. 初始状态 ===");
ok("初始进度 0%", pctNum() === 0, `got ${pctNum()}`);
ok("初始已读 0 条", readCount.textContent === "0");
ok("初始线性进度条宽度为 0%", fillNum() === 0, `w=${readFill.style.width}`);
ok("初始没有卡片处于已完成态", doc.querySelectorAll(".news.done").length === 0);
ok("按钮初始文案为「标记阅读完成」",
  btns.every((b) => b.querySelector("span").textContent === "标记阅读完成"));

console.log("\n=== 3. 单卡点击：未读 -> 已读 ===");
click(btns[0]);
ok("卡片 1 获得 done 类", cards[0].classList.contains("done"));
ok("卡片 2 未受影响", !cards[1].classList.contains("done"));
ok("卡片 1 按钮文案变为「已完成」",
  btns[0].querySelector("span").textContent === "已完成",
  `got "${btns[0].querySelector("span").textContent}"`);
ok("卡片 1 右上角小对勾出现（done-badge 元素存在）",
  !!cards[0].querySelector(".done-badge svg"));
ok("进度更新为 33%", pctNum() === 33, `got ${pctNum()}`);
ok("已读计数为 1", readCount.textContent === "1");
ok("线性进度条已部分填充 (33%)", Math.abs(fillNum() - 33) < 0.6, `w=${readFill.style.width}`);

console.log("\n=== 4. 反向操作：再次点击应可取消 ===");
click(btns[0]);
ok("卡片 1 已取消 done 类", !cards[0].classList.contains("done"));
ok("进度回退为 0%", pctNum() === 0, `got ${pctNum()}`);
ok("已读计数回退为 0", readCount.textContent === "0");

console.log("\n=== 5. 三卡全读 ===");
btns.forEach((b) => click(b));
ok("三张卡片全部 done", doc.querySelectorAll(".news.done").length === 3);
ok("进度达到 100%", pctNum() === 100, `got ${pctNum()}`);
ok("已读计数为 3", readCount.textContent === "3");
ok("线性进度条填满 100%", Math.abs(fillNum() - 100) < 0.6, `w=${readFill.style.width}`);

console.log("\n=== 6. 重置（先复位状态，避免残留导致假失败） ===");
click(resetBtn);
ok("重置后进度回到 0%", pctNum() === 0, `got ${pctNum()}`);
ok("重置后无卡片为 done", doc.querySelectorAll(".news.done").length === 0);
ok("重置后按钮文案复原",
  btns.every((b) => b.querySelector("span").textContent === "标记阅读完成"));

console.log("\n=== 7. 键盘快捷键 1 / 2 / 3（状态已在第 6 步清空） ===");
["1", "2", "3"].forEach((k) => key(k));
ok("按 1/2/3 三张卡片全部标记完成", doc.querySelectorAll(".news.done").length === 3);
ok("键盘操作后进度为 100%", pctNum() === 100, `got ${pctNum()}`);
click(resetBtn);
ok("（复位）重置后进度回到 0%", pctNum() === 0, `got ${pctNum()}`);

console.log("\n=== 8. 内容完整性 & 版式 ===");
ok("顶部标题为「AI 行业日报」", doc.querySelector(".titles .nav-name").textContent.trim() === "AI 行业日报");
ok("Hero 大标题存在", doc.querySelector(".hero-band h1").textContent.trim() === "AI 行业日报");
ok("Hero 副标题正确",
  doc.querySelector(".hero-sub").textContent.trim() === "3分钟，追上今天所有AI大事。",
  `got "${doc.querySelector(".hero-sub").textContent.trim()}"`);
ok("存在顶部导航栏（含数据窗口标签）", !!doc.querySelector(".nav .window-tag"));
ok("Hero 标题行有状态胶囊（浅蓝底 + 蓝字 + 蓝点呼吸灯，iOS 风格）",
  !!doc.querySelector(".hero-head .live i")
  && /\.live\{[\s\S]*?background:var\(--blue-tint\);color:var\(--blue\)[\s\S]*?border-radius:999px/.test(html)
  && /\.live i\{width:6px;height:6px;border-radius:50%;background:var\(--blue\);animation:pulse 2s infinite\}/.test(html)
  && doc.querySelector(".hero-head .live").textContent.includes("今日 13 条精选"));
ok("存在今日重点摘要区块", !!doc.querySelector(".summary") && doc.querySelector(".sec-head h2").textContent.includes("今日重点摘要"));
ok("存在右侧今日趋势面板", !!doc.querySelector(".panel") && doc.querySelector(".phead h2").textContent.trim() === "今日趋势");
ok("趋势面板含 5 行板块数据（垂直列表）", doc.querySelectorAll(".titem").length === 5);
ok("每行 = 分类名 + 今日数字 + 昨日增减箭头",
  doc.querySelectorAll(".tname").length === 5
  && doc.querySelectorAll(".tnum").length === 5
  && doc.querySelectorAll(".tdelta").length === 5);
ok("横向细条柱状图已移除", doc.querySelectorAll(".tbar, .ttrack, .bars").length === 0);
ok("趋势面板含关键词标签", doc.querySelectorAll(".kw span").length >= 6);
ok("有页脚数据来源署名", !!doc.querySelector(".footbar a"));

console.log("\n=== 9. 三条卡片层级区分（第一条最大） ===");
ok("恰好一张头条大卡", doc.querySelectorAll(".news.card-feat").length === 1);
ok("头条大卡就是第 1 张", cards[0].classList.contains("card-feat"));
ok("另两张包在堆叠容器里", doc.querySelectorAll(".col-stack .news").length === 2
  && doc.querySelector(".cards > .col-stack").children.length === 2);
ok("头条卡标题层级标签为 h3 且带大标题类", cards[0].querySelector("h3.ntitle") !== null);
ok("三张卡片都有重要程度标签", doc.querySelectorAll(".news .lvl").length === 3);
ok("三张卡片都有右上角对勾位", doc.querySelectorAll(".news > .done-badge").length === 3);

console.log("\n=== 10. 新增功能：重要程度筛选 ===");
ok("存在三个筛选按钮", segs.length === 3, `got ${segs.length}`);
ok("三个按钮文案为 全部 / 高优先级 / 中优先级",
  segs.map((b) => b.textContent.replace(/\d+/g, "").trim()).join("|")
  === "全部|高优先级|中优先级",
  `got "${segs.map((b) => b.textContent.trim()).join(" / ")}"`);
ok("筛选栏位于新闻卡片上方（DOM 顺序在 .cards 之前）",
  !!(doc.querySelector(".filterbar") &&
     (doc.querySelector(".filterbar").compareDocumentPosition(cardsWrap) & 4)),
  "DOCUMENT_POSITION_FOLLOWING");

// —— 默认「全部」——
ok("[全部] 三张卡片都可见", visible().length === 3, `got ${visible().length}`);
ok("[全部] 全部按钮为选中态", segBy("all").classList.contains("active")
  && segBy("all").getAttribute("aria-pressed") === "true");
ok("[全部] 容器 data-view=all", cardsWrap.getAttribute("data-view") === "all");
ok("[全部] 计数文案为「显示 3 / 3 条」", filterCount.textContent.trim() === "显示 3 / 3 条",
  `got "${filterCount.textContent.trim()}"`);

// —— 高优先级 ——
await clickSeg(segBy("high"));
ok("[高优先级] 仅显示 2 张高优先级卡片", visible().length === 2
  && visible().every((c) => c.getAttribute("data-lvl") === "high"),
  `visible=${visible().map((c) => c.getAttribute("data-card")).join(",")}`);
ok("[高优先级] 中优先级卡片被隐藏", cards[2].hidden === true);
ok("[高优先级] 按钮高亮切换到高优先级", segBy("high").classList.contains("active")
  && !segBy("all").classList.contains("active")
  && !segBy("mid").classList.contains("active"));
ok("[高优先级] 容器 data-view=high（布局随之切换）", cardsWrap.getAttribute("data-view") === "high");
ok("[高优先级] 计数文案为「显示 2 / 3 条」", filterCount.textContent.trim() === "显示 2 / 3 条",
  `got "${filterCount.textContent.trim()}"`);

// —— 中优先级 ——
await clickSeg(segBy("mid"));
ok("[中优先级] 仅显示 1 张中优先级卡片", visible().length === 1
  && visible()[0].getAttribute("data-lvl") === "mid",
  `visible=${visible().map((c) => c.getAttribute("data-card")).join(",")}`);
ok("[中优先级] 两张高优先级卡片被隐藏", cards[0].hidden && cards[1].hidden);
ok("[中优先级] 按钮高亮切换到中优先级", segBy("mid").classList.contains("active")
  && !segBy("all").classList.contains("active")
  && !segBy("high").classList.contains("active"));
ok("[中优先级] 计数文案为「显示 1 / 3 条」", filterCount.textContent.trim() === "显示 1 / 3 条",
  `got "${filterCount.textContent.trim()}"`);

// —— 回到全部 ——
await clickSeg(segBy("all"));
ok("[全部] 恢复显示全部三张卡片", visible().length === 3);
ok("[全部] 按钮高亮回到全部", segBy("all").classList.contains("active")
  && !segBy("high").classList.contains("active")
  && !segBy("mid").classList.contains("active"));

console.log("\n=== 11. 冲突检查 A：筛选不得破坏「阅读完成」状态 ===");
click(resetBtn);
await clickSeg(segBy("all"));
click(btns[2]);                                   // 先读第 3 条（中优先级）
ok("标记第 3 条已读后进度 33%", pctNum() === 33, `got ${pctNum()}`);
await clickSeg(segBy("high"));                             // 把第 3 条筛掉
ok("筛掉后该卡片仍保留 done 类（状态未被清空）", cards[2].classList.contains("done"));
ok("筛选不改动阅读进度（仍为 33%）", pctNum() === 33, `got ${pctNum()}`);
ok("筛选不改动已读计数（仍为 1）", readCount.textContent === "1");
await clickSeg(segBy("all"));                              // 筛回来
ok("筛回后仍然处于已完成态", cards[2].classList.contains("done")
  && btns[2].querySelector("span").textContent === "已完成");
ok("筛回后进度仍为 33%", pctNum() === 33, `got ${pctNum()}`);
click(resetBtn);
ok("重置可清除被筛选期间标记的已读状态", pctNum() === 0
  && doc.querySelectorAll(".news.done").length === 0);

console.log("\n=== 12. 冲突检查 B：键盘快捷键不得误改隐藏卡片 ===");
await clickSeg(segBy("mid"));                              // 只显示第 3 张
key("1");                                         // 第 1 张已隐藏 -> 应被忽略
key("2");                                         // 第 2 张已隐藏 -> 应被忽略
ok("对已隐藏卡片按 1/2 不产生任何已读状态",
  readCount.textContent === "0" && doc.querySelectorAll(".news.done").length === 0,
  `read=${readCount.textContent}`);
key("3");                                         // 第 3 张可见 -> 正常生效
ok("对可见卡片按 3 正常标记完成", cards[2].classList.contains("done") && pctNum() === 33,
  `pct=${pctNum()}`);
ok("隐藏卡片未被键盘污染", !cards[0].classList.contains("done") && !cards[1].classList.contains("done"));
click(resetBtn);
await clickSeg(segBy("all"));
ok("（复位）回到全部 + 进度清零", visible().length === 3 && pctNum() === 0, `pct=${pctNum()}`);

console.log("\n=== 13. 筛选视角下的阅读进度口径 ===");
ok("进度分母固定为今日全部 3 条（筛选只改可见性）",
  doc.querySelector(".progress .pd").textContent.includes("/ 3 篇已读"),
  `got "${doc.querySelector(".progress .pd").textContent.trim()}"`);
await clickSeg(segBy("high"));
btns.filter((_, i) => !cards[i].hidden).forEach((b) => click(b));
ok("高优先级视角下读完可见的 2 条 -> 67%（2/3 四舍五入）", pctNum() === 67, `got ${pctNum()}`);
await clickSeg(segBy("all"));
ok("切回全部时第 3 条仍为未读", !cards[2].classList.contains("done"));
click(resetBtn);
await clickSeg(segBy("all"));

console.log("\n=== 14. 新增：移动端流式布局（CSS 层） ===");
ok("存在 860px 移动端媒体查询", html.includes("@media (max-width:860px)"));
ok("移动端新闻卡片改为单列 (display:block)",
  /@media \(max-width:860px\)[\s\S]*?\.cards\{display:block/.test(html));
ok("移动端主栅格改为纵向堆叠（趋势面板落到新闻列表下方）",
  /@media \(max-width:860px\)[\s\S]*?\.main\{display:block/.test(html));
ok("移动端取消 1600px 固定画布 (transform:none!important)",
  /@media \(max-width:860px\)[\s\S]*?\.stage\{[\s\S]*?transform:none!important/.test(html));
ok("移动端 Hero 标题保持 32px 规格不挤压",
  /@media \(max-width:860px\)[\s\S]*?\.hero-band h1\{font-size:32px/.test(html));
ok("移动端筛选控件铺满整行不换行",
  /@media \(max-width:860px\)[\s\S]*?\.segmented\{display:flex;width:100%\}/.test(html));
ok("移动端阅读完成按钮统一为整行按钮",
  /@media \(max-width:860px\)[\s\S]*?\.news:not\(\.card-feat\) \.done-btn,[\s\S]*?position:static/.test(html));
ok("视图专属排版仅桌面端生效 (min-width:861px)",
  html.includes("@media (min-width:861px)"));

console.log("\n=== 15. 新增：窄屏缩放分支（JS 层） ===");
const stage = doc.getElementById("stage");
const setW = (w) => Object.defineProperty(win, "innerWidth", { value: w, configurable: true });
const fire = () => win.dispatchEvent(new win.Event("resize"));
try {
  setW(390); fire();
  ok("390px 视口下清除整体缩放 (transform 为空)", stage.style.transform === "",
    `got "${stage.style.transform}"`);
  setW(1600); fire();
  ok("恢复桌面宽度后重新按 16:9 缩放",
    stage.style.transform.startsWith("scale("), `got "${stage.style.transform}"`);
  setW(861); fire();
  ok("861px 仍走桌面缩放分支", stage.style.transform.startsWith("scale("));
  setW(860); fire();
  ok("860px 切换为移动流式分支", stage.style.transform === "");
  setW(1600); fire();
} catch (e) {
  ok("jsdom 支持 innerWidth 重定义（跳过该组断言）", false, e.message);
}

console.log("\n=== 16. 新增：Airbnb 风格令牌（第 18 轮换肤） ===");
ok("勃艮第红强调色 #8B3A3A 存在（唯一 accent）", html.includes("#8B3A3A"));
ok("米白画布页底 #F9F8F6（学院风暖调）", html.includes("--m-ivory:#F9F8F6"));
ok("主文字色 #222222（暖黑）", html.includes("--ink:#222222"));
ok("旧橙金色系已全部清除（禁用荧光绿/亮橙/纯红）",
  !html.includes("#fa520f") && !html.includes("#ffa110") && !html.includes("#ffd900")
  && !html.includes("#CCFF00") && !html.includes("#EA580C") && !html.includes("#FFF7ED")
  && !html.includes("#E5484D") && !html.includes("127,99,21") && !html.includes("250,82,15"));
ok("旧进度环渐变已换为阳光系（无旧 MiniMax 色）",
  !html.includes("#1456f0") && !html.includes("#3daeff") && !html.includes("#ea5ec1"));
ok("旧 MiniMax / Stripe / Intercom 令牌已清除",
  !html.includes("#181e25") && !html.includes("#e8ffea") && !html.includes("#f0f0f0") &&
  !html.includes("#533afd") && !html.includes("#f6f9fc") &&
  !html.includes("#faf9f6") && !html.includes("#ff5600"));
ok("旧阳光渐变已全部移除", !/linear-gradient\(90deg,#ffd900/.test(html) && !html.includes("#ffa110"));
ok("头条卡带阳光渐变发丝线 (::before)", /\.card-feat::before/.test(html));
ok("暖调极轻阴影（0 4px 12px rgba(80,60,60,.04)）", html.includes("--shadow-card:0 4px 12px rgba(80,60,60,.04)"));
ok("页脚为深灰纯色收尾带", /\.footbar\{[\s\S]*?background:var\(--ink\)/.test(html));
ok("统一 12px 圆角体系", html.includes("--r-card:12px") && html.includes("--r-panel:12px") && html.includes("--r-badge:6px"));
ok("大写字母间距标签体系（letter-spacing:2px）", (html.match(/letter-spacing:2px/g) || []).length >= 5);

console.log("\n=== 17. 新增：新拟态卡片与暖橙按钮 ===");
ok("正文滚动区 max-height:120px + overflow-y:auto", html.includes("max-height:120px;overflow-y:auto"));
ok("头条正文 flex 滚动区（min-height:0）", /\.card-feat \.ndesc\{[^}]*min-height:0[^}]*overflow-y:auto/.test(html));
ok("按钮 40px 胶囊 + 12px 24px 内边距", html.includes("border-radius:40px;padding:12px 24px"));
ok("按钮 Rausch 红染色配色（--blue-tint 底 / --blue 字）", /\.done-btn\{[\s\S]*?color:var\(--blue\);background-color:var\(--blue-tint\)/.test(html));
ok("按钮极轻阴影", /\.done-btn\{[\s\S]*?box-shadow:0 4px 12px rgba\(80,60,60,\.04\)/.test(html));
ok("按钮 hover/active 态齐全", html.includes(".done-btn:hover{color:var(--blue-deep);background-color:var(--blue-soft)") && html.includes(".done-btn:active{box-shadow:none}"));
ok("已完成态实心蓝底白字按钮", html.includes("color:#FFFFFF;background-color:var(--blue);border-color:var(--blue)"));
ok("新闻卡片纯白底 + 12px 圆角", /\.news\{[\s\S]*?border-radius:12px;[\s\S]*?background:var\(--white\)/.test(html));
ok("小卡正文行数截断已移除（交给滚动）", !/\.news:not\(\.card-feat\) \.ndesc\{[^}]*line-clamp/.test(html));
ok("移动端按钮缩小版 padding:10px 24px", html.includes("padding:10px 24px;font-size:13px"));

console.log("\n=== 18. 新增：App 化 UI 与交互动效 ===");
ok("摘要改为 3 行要点列表（蓝色圆点符号）", /\.sumlist li::before\{[^}]*border-radius:50%;background:var\(--blue\)/.test(html) && (html.match(/<li[ >]/g) || []).length >= 3);
ok("要点列表保留来源节点标记", html.includes('<ul class="sumlist" data-page-node-id='));
ok("卡片高度自适应（行轨道 auto + align-items:start）", html.includes("grid-template-rows:auto auto") && html.includes("align-items:start"));
ok("卡片悬浮 transition all .3s ease", html.includes("transition:all .3s ease"));
ok("悬浮上浮 4px + 阴影加深", html.includes("transform:translateY(-4px)") && /\.news:hover\{[\s\S]*?box-shadow:0 12px 24px rgba\(80,60,60,\.08\)/.test(html));
ok("高优先级卡片用极细蓝色左侧条提示（取代橙色描边）", /\.news\[data-lvl="high"\]\{border-left:3px solid var\(--blue\)\}/.test(html));
ok("已读整卡降透明度 0.6", html.includes("opacity:.6;") && /\.news\.done\{[^}]*opacity/.test(html));
ok("完成按钮显示对勾图标（不再隐藏）", !html.includes(".news.done .done-btn svg{display:none}") && html.includes(".news.done .done-btn svg{stroke:#FFFFFF}"));
ok("顶部 2px 霓虹蓝滚动进度条（CSS+节点+JS）", html.includes('#scrollProgress') && html.includes("height:2px;width:0") && html.includes("updateScrollProgress") && /#scrollProgress\{[\s\S]*?background:var\(--blue\)/.test(html));
ok("分段控件改为传统标签过滤器（描边胶囊，无纯色滑块）",
  !html.includes("segInd") && !html.includes("seg-ind")
  && /\.seg\{[\s\S]*?cursor:pointer;border:1px solid #E8E4DF;border-radius:20px/.test(html));

console.log("\n=== 19. 新增：今日趋势面板重做（垂直列表 / 胶囊关键词 / 线性进度） ===");
click(resetBtn);
await clickSeg(segBy("all"));

// —— ① 板块分布：垂直列表 ——
ok("板块分布为垂直列表（ul.tlist > li.titem）",
  !!doc.querySelector("ul.tlist") && doc.querySelectorAll("ul.tlist > li.titem").length === 5);
ok("每行左侧为中文分类名",
  [...doc.querySelectorAll(".titem .tname")].map((e) => e.textContent.trim()).join("|")
  === "模型发布/更新|产品发布/更新|行业动态|技巧与观点|论文研究");
ok("每行右侧为今日数字 + 昨日增减箭头",
  doc.querySelectorAll(".titem .tright > .tnum").length === 5
  && doc.querySelectorAll(".titem .tright > .tdelta").length === 5);
ok("增加用 ↑ 且为勃艮第红 #8B3A3A（学院风强调色口径）",
  doc.querySelectorAll(".tdelta.up").length === 3 && html.includes(".tdelta.up{color:#8B3A3A}"));
ok("减少用 ↓ 且为暖灰 #A5A09B（不再用红绿）",
  doc.querySelectorAll(".tdelta.down").length === 1 && html.includes(".tdelta.down{color:#A5A09B}"));
ok("持平行用灰 — 表示（不误报成增减）",
  doc.querySelectorAll(".tdelta.flat").length === 1
  && doc.querySelectorAll(".tdelta.flat")[0].textContent.trim() === "—"
  && html.includes(".tdelta.flat{color:#A5A09B}"));
ok("增减数值口径与昨日一致（技巧与观点 7 vs 4 -> ↑3）",
  doc.querySelectorAll(".tdelta")[3].textContent.replace(/\s+/g, "") === "↑3",
  `got "${doc.querySelectorAll(".tdelta")[3].textContent.trim()}"`);
ok("列表无横线（仅允许 border-radius，无实线边框），改用 margin-bottom 分隔",
  !/\.titem\{[^}]*border-(top|bottom|left|right)[^}]*\}/.test(html)
  && /\.titem\{[^}]*margin-bottom:11px/.test(html));

// —— ② 热点关键词：极简描边标签 ——
ok("关键词为豆沙色底圆角标签（#F4EAEA 底 / 勃艮第红字 / 圆角 6px）",
  /\.kw span\{[\s\S]*?background:#F4EAEA;[\s\S]*?border:1px solid transparent;border-radius:6px/.test(html));
ok("悬停时 Rausch 红底 + 白字反色", /\.kw span:hover\{background:var\(--blue\);border-color:var\(--blue\);color:#FFFFFF\}/.test(html));
ok("关键词文字统一 12px 勃艮第红", /\.kw span\{[\s\S]*?font-size:12px;[\s\S]*?color:#8B3A3A/.test(html));
ok("关键词为 flex-wrap 自然流式布局", /\.kw\{display:flex;flex-wrap:wrap/.test(html));
ok("关键词点击有按压缩放动画（keyframes + JS）",
  html.includes("@keyframes kwPop") && html.includes("addEventListener('animationend'"));
click(doc.querySelector(".kw span"));
ok("点击关键词后挂上 kwpop 动画类", doc.querySelector(".kw span").classList.contains("kwpop"));

// —— ③ 阅读进度：线性条取代圆环 ——
ok("圆形进度环已彻底删除",
  !doc.getElementById("ringFg") && !doc.getElementById("ringPct") && !html.includes("ringGrad"));
ok("线性进度条规格：高 2px / 圆角 1px（极细）", /\.pbar\{height:2px;border-radius:1px/.test(html));
ok("进度条灰底 + Rausch 红填充",
  html.includes("background:#E8E4DF;overflow:hidden")
  && /\.pbar-fill\{[\s\S]*?background:var\(--blue\)/.test(html));
ok("进度条旁有「N / 3 篇已读」文字说明",
  /\d+\s*\/\s*3\s*篇已读/.test(doc.querySelector(".progress .pd").textContent),
  `got "${doc.querySelector(".progress .pd").textContent.trim()}"`);
click(btns[0]);
ok("标记 1 条后线性条宽度为 33%", Math.abs(fillNum() - 33) < 0.6, `w=${readFill.style.width}`);
ok("文字同步为「1 / 3 篇已读」",
  doc.querySelector(".progress .pd").textContent.replace(/\s+/g, " ").trim().startsWith("1 / 3 篇已读"));
click(resetBtn);
ok("重置后线性条归零", fillNum() === 0, `w=${readFill.style.width}`);

// —— ④ 整体视觉：轻盈卡片化 ——
ok("面板为纯白卡片（12px 圆角 / 24px 内边距 / 极细描边 / 极轻阴影）",
  /\.panel\{[\s\S]*?padding:24px;[\s\S]*?border:1px solid #E8E4DF;[\s\S]*?border-radius:12px;[\s\S]*?background:var\(--white\);[\s\S]*?box-shadow:var\(--shadow-card\)/.test(html));
ok("面板不再有左分割线（旧降噪样式已移除）", !/border-left:1px solid var\(--line-light\)/.test(html.match(/\.panel\{[^}]*\}/)[0]));
ok("数据文字统一 12px 深灰（列表名 / 进度标签）",
  /\.tname\{font-size:12px;font-weight:400;color:#7A7571/.test(html)
  && /\.pinfo \.pt\{font-size:12px;font-weight:400;letter-spacing:0;color:#7A7571\}/.test(html));
ok("今日数字为微小圆角标签（#F1EEE9 底 / 暖灰字 / 6px 圆角）",
  /\.tnum\{font-family:var\(--font-sans\);font-size:12px;font-weight:600;color:#7A7571;background:#F1EEE9;border-radius:6px/.test(html));
ok("面板大数字：48px / 700 / #222222（无衬线）",
  /\.hero \.num\{[\s\S]*?font-size:48px;font-weight:700;[\s\S]*?color:#222222/.test(html));

// —— ⑤ 375px 小屏响应式 ——
ok("新增 ≤420px 小屏媒体查询", html.includes("@media (max-width:420px)"));
ok("小屏标签强制换行不溢出（max-width + overflow-wrap）",
  /@media \(max-width:420px\)[\s\S]*?\.nstat span\{max-width:100%;white-space:normal;overflow-wrap:anywhere\}/.test(html));
ok("小屏关键词描边标签同步收窄", /@media \(max-width:420px\)[\s\S]*?\.kw span\{padding:3px 8px\}/.test(html));
ok("375px 下摘要胶囊也改为换行不再横滑", /@media \(max-width:420px\)[\s\S]*?\.chips\{flex-wrap:wrap;overflow-x:visible\}/.test(html));
ok("小屏移动端面板为独立卡片（自带内边距，无旧分割线）",
  /@media \(max-width:860px\)[\s\S]*?\.panel\{height:auto;padding:20px/.test(html));

// —— ⑥ 编辑器节点标记守恒 ——
ok("207 个 data-page-node-id 全部保留且无重复",
  (html.match(/data-page-node-id/g) || []).length === 207
  && new Set(html.match(/data-page-node-id="[^"]+"/g)).size === 207);

console.log("\n=== 20. 新增：顶部标签滑动指示器 + 核心数据浓度仪表 ===");
await clickSeg(segBy("all"));

// jsdom 无布局引擎（offsetWidth 恒为 0），注入模拟尺寸后触发 resize 让指示器真实落位
const stubBox = (el, w, x, h, y) => {
  Object.defineProperty(el, "offsetWidth", { get: () => w, configurable: true });
  Object.defineProperty(el, "offsetLeft", { get: () => x, configurable: true });
  Object.defineProperty(el, "offsetHeight", { get: () => h, configurable: true });
  Object.defineProperty(el, "offsetTop", { get: () => y, configurable: true });
};
tabs.forEach((b, i) => stubBox(b, 46 + i * 22, i * 74, 26, 0));
segs.forEach((b, i) => stubBox(b, 62 + i * 14, i * 78, 30, 3));
fire();

// —— ① 顶部标签筛选区：滑动指示器 + 数字徽章 ——
ok("顶部标签为 6 个可点击 button（全部 / 精选 / 4 板块）",
  tabs.length === 6 && tabs.every((b) => b.tagName === "BUTTON"));
ok("标签文案与筛选维度一一对应",
  tabs.map((b) => b.textContent.replace(/\d+/g, "").replace(/\s+/g, "")).join("|")
  === "全部条|精选条|模型发布|产品更新|行业动态|观点技巧",
  `got "${tabs.map((b) => b.textContent.trim()).join(" / ")}"`);
ok("标签后的数字都是独立微型徽章 .tbadge（初始 13/3/3/2/1/7）",
  tabs.every((b) => b.querySelector(".tbadge"))
  && tabs.map((b) => b.querySelector(".tbadge").textContent).join(",") === "13,3,3,2,1,7",
  `got "${tabs.map((b) => b.querySelector(".tbadge") && b.querySelector(".tbadge").textContent).join(",")}"`);
ok("选中态徽章为白底 Rausch 红字",
  /\.hero-tab\.active \.tbadge\{background:var\(--white\);color:var\(--blue\)\}/.test(html));
ok("未选中态徽章为浅灰底深灰字",
  /\.tbadge\{[\s\S]*?background:#F1EEE9;color:#7A7571/.test(html));
ok("存在 Rausch 红滑动指示器 .tab-ind 且已完成首屏定位",
  !!tabInd && tabInd.classList.contains("ready") && tabInd.style.transform.startsWith("translate("),
  `transform=${tabInd.style.transform}`);
ok("指示器位移使用 transform 过渡 .3s（非生硬变色）",
  /\.tab-ind\{[\s\S]*?transition:transform \.3s cubic-bezier/.test(html));
ok("旧的「选中即变色」写法已移除", !/\.hero-tab\.active\{background:var\(--m-orange\)/.test(html));

const t0 = tabInd.style.transform;
await clickTab(tabBy("模型发布"));
ok("点击标签后指示器平滑滑动（transform 改变）", tabInd.style.transform !== t0,
  `${t0} -> ${tabInd.style.transform}`);
ok("标签选中态随之切换",
  tabBy("模型发布").classList.contains("active")
  && !tabBy("all").classList.contains("active")
  && tabBy("模型发布").getAttribute("aria-pressed") === "true"
  && tabBy("all").getAttribute("aria-pressed") === "false");
ok("列表淡出淡入过渡（opacity / transform .3s ease）",
  /\.cards\{[\s\S]*?transition:opacity \.3s ease,transform \.3s ease/.test(html)
  && html.includes(".cards.is-fade{opacity:0;transform:translateY(8px)}")
  && html.includes("function switchView"));

// —— ② 板块筛选真实生效 ——
ok("[模型发布] 只剩该板块卡片", visible().length === 1
  && visible()[0].getAttribute("data-cat") === "模型发布",
  `visible=${visible().map((c) => c.getAttribute("data-card")).join(",")}`);
ok("[模型发布] 容器加 cat-narrow 单列类", cardsWrap.classList.contains("cat-narrow"));
ok("[模型发布] 计数文案同步更新", filterCount.textContent.trim() === "显示 1 / 3 条",
  `got "${filterCount.textContent.trim()}"`);
ok("有卡片时不显示空态", cardsEmpty.hidden === true);

// —— ③ 空态：该板块暂无精读卡片 ——
await clickTab(tabBy("观点技巧"));
ok("[观点技巧] 无匹配卡片时展示空态占位", visible().length === 0 && cardsEmpty.hidden === false);
ok("空态提供「回到全部精选」按钮", doc.getElementById("emptyReset") !== null);
click(doc.getElementById("emptyReset"));
await sleep(240);
ok("点击空态按钮回到全部精选", visible().length === 3
  && tabBy("all").classList.contains("active") && cardsEmpty.hidden === true,
  `visible=${visible().length}`);

// —— ④ 板块 × 重要程度 组合过滤 ——
await clickTab(tabBy("产品发布"));
await clickSeg(segBy("mid"));
ok("板块 ∩ 优先级交集为空时进入空态", visible().length === 0 && cardsEmpty.hidden === false);
await clickSeg(segBy("high"));
ok("产品发布 ∩ 高优先级 = 第 2 张卡片", visible().length === 1
  && visible()[0].getAttribute("data-card") === "2");
await clickTab(tabBy("all"));
await clickSeg(segBy("all"));
ok("（复位）回到全部板块 + 全部优先级", visible().length === 3
  && cardsWrap.getAttribute("data-view") === "all"
  && !cardsWrap.classList.contains("cat-narrow"));
ok("组合筛选不改动阅读进度", pctNum() === 0, `pct=${pctNum()}`);

// —— ⑤ 分段控件改为传统标签过滤器（第 15 轮） ——
ok("优先级筛选为描边胶囊标签（无纯色滑块）",
  !doc.getElementById("segInd") && /\.seg\{[\s\S]*?cursor:pointer;border:1px solid #E8E4DF;border-radius:20px/.test(html));
ok("标签选中态为浅 Rausch 染色底 + 红描边 + 红字",
  /\.seg\.active\{background:var\(--blue-tint\);border-color:var\(--blue\);color:var\(--blue\)\}/.test(html));
ok("标签有平滑过渡（transition 含 border-color / background）",
  /\.seg\{[^}]*transition:background \.25s ease,border-color \.25s ease/.test(html));

// —— ⑥ 核心数据区：超大数字 + TODAY'S SELECTED + 今日资讯浓度渐变条（第 16 轮） ——
ok("数字 13：48px / 700 / #222222 紧贴右侧 12px 浅灰 TODAY'S SELECTED",
  /\.hero \.num\{[\s\S]*?font-size:48px;font-weight:700;[\s\S]*?color:#222222/.test(html)
  && /<span class="unit">TODAY'S SELECTED<\/span>/.test(html)
  && /\.hero-numrow\{display:flex;align-items:baseline/.test(html));
ok("浓度标签：今日资讯浓度 + 环比值（默认 ↑ 44%，Rausch 红）",
  doc.querySelector(".density-label").textContent.includes("今日资讯浓度")
  && heroBox.querySelector(".hero-pill").textContent.replace(/\s+/g, " ").trim() === "↑ 44%"
  && /\.hero-pill\{[\s\S]*?color:var\(--blue\)/.test(html),
  `got "${heroBox.querySelector(".hero-pill").textContent.replace(/\s+/g, " ").trim()}"`);
ok("浓度条：4px 高 / 2px 圆角 / #E8E4DF 外框 + 勃艮第红渐变填充",
  /\.density-bar\{height:4px;border-radius:2px;background:#E8E4DF/.test(html)
  && /\.density-bar span\{[\s\S]*?background:linear-gradient\(90deg,#D3A5A5 0%,#8B3A3A 100%\)/.test(html));
ok("核心数据为独立白色指标小卡（12px 圆角 + 细描边）",
  /\.hero\{display:block;padding:14px 16px;background:var\(--white\);border:1px solid #E8E4DF;border-radius:12px/.test(html));
ok("核心数据区保留原有 3 个编辑器节点标记",
  html.includes('<div class="hero" data-page-node-id="otg5Img00BxuDmRg6aCOKM">')
  && html.includes('<div class="hero-numwrap" data-page-node-id="BHnaBikreQtxtydu4KCcv1">')
  && html.includes('class="num" data-page-node-id="qnfodBoSloXw2ryvHjRpHB">13</div>')
  && html.includes('class="hero-pill" data-page-node-id="Kn3MYAO1DVQVuAdcnzrAiH"'));
ok("小屏 420px 下标签 / 徽章 / 大数字同步收窄",
  /@media \(max-width:420px\)[\s\S]*?\.tbadge\{min-width:17px;height:17px/.test(html)
  && /@media \(max-width:420px\)[\s\S]*?\.hero \.num\{font-size:34px\}/.test(html));

console.log("\n=== 21. 新增：精选筛选 × 板块联动 × filterState 统一状态树 ===");
click(resetBtn);
await clickSeg(segBy("all"));
await clickTab(tabBy("all"));

ok("存在统一 filterState 状态树与 renderList 渲染出口（需求四）",
  html.includes("var filterState") && html.includes("function renderList")
  && html.includes("function renderAll") && !html.includes("var catFilter"));
ok("板块分布行可点击（role=button + 键盘可达 + 数据维度）",
  [...doc.querySelectorAll(".titem[data-board]")].length === 5
  && [...doc.querySelectorAll(".titem[data-board]")].every((li) => li.getAttribute("role") === "button")
  && [...doc.querySelectorAll(".titem[data-board]")].filter((li) => li.getAttribute("tabindex") === "0").length === 4);
ok("板块行 hover / 选中 / 禁用三态样式齐全（中性灰系）",
  /\.titem:hover\{background:rgba\(80,60,60,\.04\)\}/.test(html)
  && /\.titem\[aria-pressed="true"\]\{background:rgba\(80,60,60,\.05\)\}/.test(html)
  && /\.titem\[aria-disabled="true"\]\{opacity:\.45;cursor:default\}/.test(html));

const titems = [...doc.querySelectorAll(".titem[data-board]")];
const tBy = (c) => titems.find((li) => li.getAttribute("data-board") === c);
const heroNumEl = doc.getElementById("heroNum");
const heroPillEl = doc.getElementById("heroPill");
const densityFillEl = doc.getElementById("densityFill");
const tabBadge = (c) => tabBy(c).querySelector(".tbadge").textContent;
const pillTxt = () => heroPillEl.textContent.replace(/\s+/g, " ").trim();

// —— ① 精选筛选（需求一） ——
await clickTab(tabBy("featured"));
ok("[精选] Tab 高亮且徽章动态变为 3（精读精选条数）",
  tabBy("featured").classList.contains("active") && tabBadge("featured") === "3",
  `got ${tabBadge("featured")}`);
ok("[精选] 面板大数字动态更新为 3", heroNumEl.textContent === "3", `got ${heroNumEl.textContent}`);
ok("[精选] 环比浓度动态重算（今日 3 vs 昨日 1 -> ↑ 200%，浓度条充满 100%）",
  pillTxt() === "↑ 200%" && densityFillEl.style.width === "100%", `got "${pillTxt()}" / ${densityFillEl.style.width}`);
ok("[精选] 三张精读卡片仍全部可见", visible().length === 3);
ok("[精选] 板块分布数量按精选口径重算（模型发布 1 / 观点技巧 0）",
  tBy("模型发布").querySelector(".tnum").textContent === "1"
  && tBy("观点技巧").querySelector(".tnum").textContent === "0");

// —— ② 板块联动筛选 + 逻辑与（需求二） ——
click(tBy("模型发布")); await sleep(240);
ok("[精选×模型发布] AND 叠加：只剩第 1 张卡片", visible().length === 1
  && visible()[0].getAttribute("data-card") === "1",
  `visible=${visible().map((c) => c.getAttribute("data-card")).join(",")}`);
ok("[精选×模型发布] 面板大数字更新为 1", heroNumEl.textContent === "1");
ok("[精选×模型发布] 顶部「精选」进入半选态（橙色文字提示 AND）",
  tabBy("featured").classList.contains("semi")
  && tabBy("模型发布").classList.contains("active"));
ok("[精选×模型发布] 面板行选中态同步（aria-pressed）",
  tBy("模型发布").getAttribute("aria-pressed") === "true");
ok("[精选×模型发布] 分段徽章随板块动态收窄（全部 1 / 中优先级 0）",
  segBy("all").querySelector("b").textContent === "1"
  && segBy("mid").querySelector("b").textContent === "0");
click(tBy("模型发布")); await sleep(240);
ok("再点当前板块行取消筛选（回到精选视角）", visible().length === 3
  && tBy("模型发布").getAttribute("aria-pressed") === "false"
  && heroNumEl.textContent === "3");

// —— ③ 板块行键盘可达 ——
tBy("行业动态").dispatchEvent(new win.KeyboardEvent("keydown", { key: "Enter", bubbles: true, cancelable: true }));
await sleep(240);
ok("板块行支持 Enter 激活筛选", visible().length === 1
  && visible()[0].getAttribute("data-card") === "3",
  `visible=${visible().map((c) => c.getAttribute("data-card")).join(",")}`);
click(tBy("行业动态")); await sleep(240);

// —— ④ 顶部板块标签与面板行联动（同一维度双向同步） ——
await clickTab(tabBy("产品发布"));
ok("顶部板块标签切换后面板行同步选中（AND 保留精选维度）",
  tBy("产品发布").getAttribute("aria-pressed") === "true"
  && visible().length === 1 && visible()[0].getAttribute("data-card") === "2");
await clickTab(tabBy("产品发布"));   // 再点当前 -> 取消
ok("再点顶部当前板块标签取消筛选", filterCount.textContent.trim() === "显示 3 / 3 条",
  `got "${filterCount.textContent.trim()}"`);

// —— ⑤ 零结果板块禁用 ——
ok("今日 0 条的「论文研究」行禁用（aria-disabled）",
  tBy("论文研究").getAttribute("aria-disabled") === "true");
click(tBy("论文研究"));
ok("禁用行点击不产生任何筛选效果", heroNumEl.textContent === "3" && visible().length === 3);

// —— ⑥ 复位 ——
await clickTab(tabBy("all"));
await clickSeg(segBy("all"));
ok("（复位）全部视角：面板数字回到 13 / ↑44% / 浓度条 44%",
  heroNumEl.textContent === "13" && pillTxt() === "↑ 44%" && densityFillEl.style.width === "44%",
  `got ${heroNumEl.textContent} / ${pillTxt()} / ${densityFillEl.style.width}`);
ok("（复位）板块行今日数量复原（3/2/1/7/0）",
  titems.map((li) => li.querySelector(".tnum").textContent).join(",") === "3,2,1,7,0");
ok("（复位）分段徽章复原 3/2/1",
  segs.map((b) => b.querySelector("b").textContent).join(",") === "3,2,1");

console.log("\n=== 22. 全局换肤校验（第 17 轮 Quiet Blue -> 第 18 轮 Airbnb） ===");
ok("面板模块间用极细灰分割线区分", /\.panel > \.hero ~ div\{border-top:1px solid var\(--line-light\);padding-top:14px\}/.test(html));
ok("重要度标签统一豆沙色底勃艮第红字（学院风）",
  /\.lvl-high\{background:#F4EAEA;border:1px solid transparent;color:#8B3A3A\}/.test(html)
  && /\.lvl-mid\{background:#F4EAEA;border:1px solid transparent;color:#8B3A3A\}/.test(html));
ok("系统无衬线字体（Inter / PingFang SC 优先）", /--font-sans:'Inter','PingFang SC'/.test(html));
ok("面板标题字重拉开对比（700）", /\.phead h2\{[^}]*font-weight:700/.test(html));
ok("分类/统计标签统一浅灰底 6px 圆角",
  /\.cat\{[^}]*border-radius:6px/.test(html) && /\.nstat span\{[\s\S]*?background:#F1EEE9;[\s\S]*?border-radius:6px/.test(html));
ok("已完成态整卡浅灰化（不再橙色渐变）",
  /\.news\.done\{[\s\S]*?background:#F7F5F2/.test(html) && !html.includes("fed7aa"));
ok("勃艮第红呼吸灯 pulse 光晕（rgba(139,58,58)）", html.includes("rgba(139,58,58,.35)") && html.includes("animation:pulse 2s infinite"));

console.log(`\n===== 结果: ${pass} PASS / ${fail} FAIL =====`);
process.exit(fail ? 1 : 0);

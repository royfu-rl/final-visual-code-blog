// 交付前自查：把 index.html 的某一段截下来。
//   node --experimental-websocket scripts/shot.mjs '#web/verified' '2.1 Overview' out.png [高度上限]
// 第 2 个参数是锚文字，脚本找到含该文字的标题，截它到下一个同级标题之间的内容。
// 必须用 captureBeyondViewport + 文档坐标 clip：scrollIntoView 不会移动截图窗口。
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const CHROME = '/root/.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell';
const ROOT = resolve(import.meta.dirname, '..');
const [hash, anchor, out, maxH = '6000', openAll] = process.argv.slice(2);
const PORT = 9400 + (process.pid % 300);

const chrome = spawn(CHROME, [`--remote-debugging-port=${PORT}`, '--headless', '--no-sandbox',
  '--disable-gpu', '--hide-scrollbars', '--window-size=1600,1200',
  `file://${ROOT}/${hash.includes('.html') ? hash : 'index.html' + hash}`], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const until = async (fn, tries = 60) => {
  for (let i = 0; i < tries; i++) { try { return await fn(); } catch { await sleep(500); } }
  throw new Error('timeout');
};

const target = await until(async () => {
  const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
  const page = list.find((t) => t.type === 'page' && t.webSocketDebuggerUrl);
  if (!page) throw new Error('no page');
  return page;
});

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => { ws.onopen = r; });
let id = 0;
const pending = new Map();
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
};
const send = (method, params = {}) => new Promise((res, rej) => {
  const n = ++id;
  pending.set(n, (m) => (m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)));
  ws.send(JSON.stringify({ id: n, method, params }));
});

await send('Page.enable');
await sleep(2500);                                  // SPA 渲染 + 字体
if (openAll) {                                      // 折叠块默认关着，要看里面就先展开
  await send('Runtime.evaluate', { expression: "document.querySelectorAll('details').forEach(d=>d.open=true)" });
  await sleep(800);
}

const expr = `(() => {
  const want = ${JSON.stringify(anchor)};
  const hs = [...document.querySelectorAll('.doc h1,.doc h2,.doc h3,.doc h4')]
    .filter(h => h.offsetParent !== null);
  const i = hs.findIndex(h => h.textContent.includes(want));
  if (i < 0) {                                      // 不是标题：退回「含这段文字的折叠块」
    const d = [...document.querySelectorAll('.doc details')]
      .find(e => e.querySelector('summary')?.textContent.includes(want));
    if (!d) return null;
    const b = d.getBoundingClientRect();
    return { x: Math.max(0, b.left + scrollX - 8), y: b.top + scrollY - 8, w: b.width + 16, h: b.height + 16 };
  }
  const a = hs[i], lvl = +a.tagName[1];
  const end = hs.slice(i + 1).find(h => +h.tagName[1] <= lvl);
  const top = a.getBoundingClientRect().top + scrollY - 12;
  const bot = end ? end.getBoundingClientRect().top + scrollY - 8
                  : document.documentElement.scrollHeight;
  const box = a.closest('.doc').getBoundingClientRect();
  return { x: Math.max(0, box.left + scrollX - 8), y: top,
           w: Math.min(box.width + 16, 1600), h: bot - top };
})()`;
const { result } = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
if (!result.value) { chrome.kill(); throw new Error(`页面里没找到标题「${anchor}」`); }
const r = result.value;
const h = Math.min(r.h, +maxH);

const shot = await send('Page.captureScreenshot', {
  format: 'png', captureBeyondViewport: true,
  clip: { x: r.x, y: r.y, width: r.w, height: h, scale: 1 },
});
mkdirSync(dirname(resolve(out)), { recursive: true });
writeFileSync(resolve(out), Buffer.from(shot.data, 'base64'));
console.log(`${out}  ${Math.round(r.w)}x${Math.round(h)}${r.h > h ? `  (原高 ${Math.round(r.h)}，已截断)` : ''}`);
ws.close();
chrome.kill();


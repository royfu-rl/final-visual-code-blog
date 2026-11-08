// 把本地 html 渲染成截图，给「数据样例」卡片用（站点作品没有官方缩略图时）。
//   node --experimental-websocket scripts/render_page.mjs <in.html|url> <out.png> [宽] [高] [等待毫秒]
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const CHROME = '/root/.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell';
const [src, out, W = '900', H = '600', wait = '2500'] = process.argv.slice(2);
// file:// 也直接放行：本地路径带 #hash 时 resolve() 会把 hash 当成文件名的一部分。
const url = /^(https?|file):/.test(src) ? src : `file://${resolve(src)}`;
const PORT = 9700 + (process.pid % 200);

const args = [`--remote-debugging-port=${PORT}`, '--headless', '--no-sandbox', '--disable-gpu',
  '--hide-scrollbars', `--window-size=${W},${H}`];
if (process.env.https_proxy) args.push(`--proxy-server=${process.env.https_proxy}`);
const chrome = spawn(CHROME, [...args, url], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 60 && !target; i++) {
  try {
    const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    target = list.find((t) => t.type === 'page' && t.webSocketDebuggerUrl);
  } catch { /* 还没起来 */ }
  if (!target) await sleep(500);
}
if (!target) { chrome.kill(); throw new Error('chrome 没起来'); }

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => { ws.onopen = r; });
let id = 0; const pending = new Map();
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const send = (method, params = {}) => new Promise((res, rej) => {
  const n = ++id;
  pending.set(n, (m) => (m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)));
  ws.send(JSON.stringify({ id: n, method, params }));
});

await send('Page.enable');
await sleep(+wait);
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
mkdirSync(dirname(resolve(out)), { recursive: true });
writeFileSync(resolve(out), Buffer.from(shot.data, 'base64'));
console.log(`${out}  ${W}x${H}`);
ws.close();
chrome.kill();


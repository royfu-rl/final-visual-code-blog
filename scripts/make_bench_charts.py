#!/usr/bin/env python3
"""data/header_bench.json -> assets/figures/header-bench.html（总页开头的 6 个 benchmark 面板）。

用法：python3 scripts/make_bench_charts.py && python3 scripts/make_total.py
  - 版式照 critic-blog 页头那组图（再往上是 KAT-Coder 博客的 pro-bench）：每个 benchmark 一个面板，
    我们的模型（hi）蓝色高亮排第一，其余灰色按分数从高到低；柱顶是厂商 logo
  - 每个面板自带坐标范围（min / max / ticks）和小数位（fmt），Elo 类榜单从非零起画，dom 里写明单位
  - 面板只画有分数的模型；hi 模型没分数时画「待补」
  - 高度通过 postMessage({type:'kc-height'}) 报给总页，iframe 自动贴合
"""
import base64, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / 'data/header_bench.json'
OUT = ROOT / 'assets/figures/header-bench.html'

PAGE = r'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual Coding — benchmarks</title>
<!-- 生成文件，别手改：data/header_bench.json + scripts/make_bench_charts.py -->
<style>
  :root{
    --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    --ink:#1a1a1a;--muted:#9a9aa0;--muted2:#b8b8be;--border:#e6e6e6;
    --accent:#2f6bff;--accent-deep:#1b3fae;
  }
  *{box-sizing:border-box;}
  body{margin:0;background:transparent;font-family:var(--font);color:var(--ink);
    -webkit-font-smoothing:antialiased;padding:4px 2px;display:flex;justify-content:center;}
  .card{width:100%;max-width:1340px;}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  @media (max-width:860px){.grid{grid-template-columns:repeat(2,1fr);}}
  @media (max-width:620px){.grid{grid-template-columns:1fr;}}
  .panel{min-width:0;background:#fafafb;border:1px solid var(--border);border-radius:12px;padding:12px 12px 6px;}
  .panel-name{font-size:12.5px;font-weight:600;color:var(--ink);line-height:1.3;text-decoration:none;}
  a.panel-name:hover{color:var(--accent);}
  .panel-dom{font-size:11px;font-weight:500;color:var(--muted2);margin-left:5px;}
  .note{font-size:12.5px;color:var(--muted);margin:14px 0 0;line-height:1.5;max-width:900px;}
  svg text{font-family:var(--font);}
  .barrect{transition:y .5s cubic-bezier(.22,.61,.36,1),height .5s cubic-bezier(.22,.61,.36,1);}
  .grp:hover .barrect{filter:brightness(1.05);}
  @media (prefers-reduced-motion:reduce){.barrect{transition:none;}}
  #tip{position:fixed;z-index:50;pointer-events:none;background:#111;color:#fff;border-radius:8px;
    padding:8px 11px;font-size:12.5px;line-height:1.5;box-shadow:0 6px 20px rgba(0,0,0,.25);
    opacity:0;transition:opacity .12s;white-space:nowrap;}
  #tip .t-cat{font-weight:600;margin-bottom:2px;} #tip .t-dim{color:#cfcfd4;}
</style>
</head>
<body>
<div class="card">
  <div class="grid" id="grid"></div>
  <p class="note" id="note"></p>
</div>
<div id="tip"></div>
<script>
const DATA  = __DATA__;
const LOGOS = __LOGOS__;

const tip=document.getElementById("tip");
function showTip(html,e){tip.innerHTML=html;tip.style.opacity=1;moveTip(e);}
function moveTip(e){const pad=14;let x=e.clientX+pad,y=e.clientY+pad;const r=tip.getBoundingClientRect();
  if(x+r.width>innerWidth)x=e.clientX-r.width-pad;if(y+r.height>innerHeight)y=e.clientY-r.height-pad;
  tip.style.left=x+"px";tip.style.top=y+"px";}
function hideTip(){tip.style.opacity=0;}
const NS="http://www.w3.org/2000/svg";
const el=(n,a)=>{const x=document.createElementNS(NS,n);for(const k in a)x.setAttribute(k,a[k]);return x;};

// models with a score, ours (hi) first even without one, the rest by score high → low
const bars=p=>DATA.models.flatMap(m=>{
  const c=p.scores[m.key], v=typeof c==="object"&&c?c.v:c;
  return v==null&&!m.hi?[]:[{...m,value:v,missing:v==null,meta:(c&&c.meta)||m.meta}];
}).sort((a,b)=>(!!b.hi-!!a.hi)||((b.value??0)-(a.value??0)));

let UID=0;
function renderPanel(p){
  const W=320,H=258,padL=34,padR=10,padT=26,padB=74, lo=p.min, hi=p.max, fmt=v=>v.toFixed(p.fmt);
  const baseY=H-padB, topY=padT, plotH=baseY-topY, y=v=>baseY-((v-lo)/(hi-lo))*plotH;
  const bs=bars(p), slot=(W-padL-padR)/bs.length, barW=Math.min(26,slot*0.56), uid=++UID;

  const wrap=document.createElement("div");wrap.className="panel";
  const name=p.source?`<a class="panel-name" href="${p.source}" target="_blank" rel="noopener">${p.name}</a>`:`<span class="panel-name">${p.name}</span>`;
  wrap.innerHTML=name+(p.dom?`<span class="panel-dom">${p.dom}</span>`:"");
  const svg=el("svg",{viewBox:`0 0 ${W} ${H}`,width:"100%",style:"display:block;margin-top:8px;overflow:visible",role:"img","aria-label":p.name});
  svg.innerHTML=`<defs>
    <linearGradient id="hl${uid}" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="var(--accent)"/><stop offset="100%" stop-color="var(--accent-deep)"/></linearGradient>
    <linearGradient id="gr${uid}" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#d4d4d4"/><stop offset="100%" stop-color="#b3b3b3"/></linearGradient>
    <clipPath id="rr${uid}" clipPathUnits="objectBoundingBox"><rect width="1" height="1" rx=".24"/></clipPath></defs>`;

  p.ticks.forEach((t,i)=>{
    svg.appendChild(el("line",{x1:padL,x2:W-padR,y1:y(t),y2:y(t),stroke:"#e6e6e6","stroke-width":1,opacity:i===0?.9:.55}));
    const lab=el("text",{x:padL-6,y:y(t)+3.5,"text-anchor":"end","font-size":10,fill:"#9a9aa0"});lab.textContent=t;svg.appendChild(lab);
  });
  svg.appendChild(el("line",{x1:padL,x2:padL,y1:topY-4,y2:baseY,stroke:"#d8d8dc","stroke-width":1}));
  svg.appendChild(el("line",{x1:padL,x2:W-padR,y1:baseY,y2:baseY,stroke:"#c8c8ce","stroke-width":1}));

  bs.forEach((b,i)=>{
    const cx=padL+slot*(i+0.5), ty=b.missing?baseY:y(b.value), h=baseY-ty;
    const g=el("g",{class:"grp"});
    const r=el("rect",{class:"barrect",x:cx-barW/2,y:baseY,width:barW,height:0,rx:3,fill:`url(#${b.hi?"hl":"gr"}${uid})`});
    g.appendChild(r);
    if(!b.missing) requestAnimationFrame(()=>requestAnimationFrame(()=>{r.setAttribute("y",ty);r.setAttribute("height",Math.max(0,h));}));

    const fs=Math.min(10.5,slot*0.36);   // 柱子多时数字缩小，免得相邻两个数挤在一起
    const sc=el("text",{x:cx,y:b.missing?baseY-6:ty-6,"text-anchor":"middle","font-size":b.missing?Math.min(9.5,fs):fs,"font-family":"var(--mono)",
      "font-weight":b.hi?700:600,fill:b.missing?"var(--accent)":b.hi?"var(--accent-deep)":"#6b7280"});
    sc.textContent=b.missing?"待补":fmt(b.value);g.appendChild(sc);

    if(!b.missing&&LOGOS[b.logo]&&h>20){
      const s=12;
      g.appendChild(el("image",{href:LOGOS[b.logo],x:cx-s/2,y:ty+5,width:s,height:s,"clip-path":`url(#rr${uid})`}));
    }
    const lyb=baseY+9;
    const t=el("text",{x:cx,y:lyb,"text-anchor":"end","font-size":9,"font-weight":b.hi?700:500,
      fill:b.hi?"var(--accent)":"#5b6270",transform:`rotate(-45 ${cx} ${lyb})`});
    t.textContent=b.label;g.appendChild(t);

    const hit=el("rect",{x:cx-slot/2,y:topY-6,width:slot,height:plotH+10,fill:"transparent"});
    const tipHtml=`<div class="t-cat">${b.label} · ${p.name}</div><b>${b.missing?"待补":fmt(b.value)}</b>`+
      (b.meta?` <span class="t-dim">· ${b.meta}</span>`:"");
    hit.addEventListener("mousemove",e=>showTip(tipHtml,e));hit.addEventListener("mouseleave",hideTip);
    g.appendChild(hit);svg.appendChild(g);
  });
  wrap.appendChild(svg);
  return wrap;
}

const grid=document.getElementById("grid");
DATA.panels.forEach(p=>grid.appendChild(renderPanel(p)));
const note=document.getElementById("note");if(DATA.note)note.textContent=DATA.note;else note.remove();
addEventListener("scroll",hideTip,true);

// report our height so the parent page can fit the iframe; srcdoc runs early, so report a few more times
const card=document.querySelector(".card");
const report=()=>parent.postMessage({type:"kc-height",h:card.getBoundingClientRect().height+10},"*");
new ResizeObserver(report).observe(card);
addEventListener("load",report);[0,300,1000,2500].forEach(t=>setTimeout(report,t));
</script>
</body>
</html>
'''


def main():
    spec = json.loads(SPEC.read_text())
    logos = {m['logo']: 'data:image/png;base64,' + base64.b64encode((ROOT / f'assets/logos/{m["logo"]}.png').read_bytes()).decode()
             for m in spec['models']}
    data = {k: spec[k] for k in ('models', 'panels', 'note')}
    html = PAGE.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__LOGOS__', json.dumps(logos))
    OUT.write_text(html)
    print(f'{OUT.relative_to(ROOT)}  {len(spec["panels"])} panels  {len(html) // 1024} KB')


if __name__ == '__main__':
    main()


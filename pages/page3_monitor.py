import streamlit as st
import streamlit.components.v1 as components

def render():
    st.markdown("""
    <style>
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffb300;
        letter-spacing: 6px;
        text-shadow: 0 0 30px #ffb300, 0 0 60px rgba(255,179,0,0.3);
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #5a3a00;
        letter-spacing: 4px;
        margin-bottom: 1.5rem;
    }
    </style>
    <div class="page-title">PERFORMANCE MONITOR</div>
    <div class="page-subtitle">REAL-TIME FPGA TELEMETRY — RESOURCE UTILIZATION & TRADING METRICS</div>
    """, unsafe_allow_html=True)

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');
body { background:#020408; font-family:'Share Tech Mono',monospace; color:#c0e8f8; overflow:hidden; }

.grid {
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: auto 1fr 1fr;
    gap:10px;
    padding:10px;
    height:100vh;
}

.kpi-row { grid-column:1/-1; display:flex; gap:10px; }
.kpi {
    flex:1;
    background:rgba(4,12,24,0.95);
    border:1px solid rgba(255,179,0,0.2);
    border-radius:3px;
    padding:10px 14px;
    position:relative;
    overflow:hidden;
}
.kpi::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, var(--ac), transparent);
}
.kpi-label { font-size:0.55rem; letter-spacing:3px; color:#4a4a00; margin-bottom:2px; }
.kpi-val   { font-size:1.4rem; font-family:'Orbitron',monospace; font-weight:700; }
.kpi-sub   { font-size:0.58rem; color:#3a3a00; margin-top:2px; }
.kpi-delta { font-size:0.65rem; position:absolute; top:10px; right:10px; }

.panel {
    background:rgba(4,12,24,0.95);
    border:1px solid rgba(255,179,0,0.15);
    border-radius:3px;
    padding:10px;
    position:relative;
    overflow:hidden;
}
.panel-title {
    font-size:0.6rem; letter-spacing:3px; color:#6a5000; margin-bottom:8px;
    border-bottom:1px solid rgba(255,179,0,0.1); padding-bottom:6px;
}

canvas.chart { width:100%; display:block; }
</style>
</head>
<body>
<div class="grid" id="grid">

  <div class="kpi-row" id="kpi-row">
    <div class="kpi" style="--ac:#00e5ff">
      <div class="kpi-label">CLOCK FREQUENCY</div>
      <div class="kpi-val" id="k0" style="color:#00e5ff;text-shadow:0 0 12px #00e5ff">250.00</div>
      <div class="kpi-sub">MHz — STABLE</div>
    </div>
    <div class="kpi" style="--ac:#00ff88">
      <div class="kpi-label">TOTAL ORDERS</div>
      <div class="kpi-val" id="k1" style="color:#00ff88;text-shadow:0 0 12px #00ff88">0</div>
      <div class="kpi-sub">SESSION TOTAL</div>
      <div class="kpi-delta" id="k1d" style="color:#00ff88">▲ +284/s</div>
    </div>
    <div class="kpi" style="--ac:#ffb300">
      <div class="kpi-label">P50 LATENCY</div>
      <div class="kpi-val" id="k2" style="color:#ffb300;text-shadow:0 0 12px #ffb300">44</div>
      <div class="kpi-sub">nanoseconds</div>
    </div>
    <div class="kpi" style="--ac:#ff1744">
      <div class="kpi-label">P99 LATENCY</div>
      <div class="kpi-val" id="k3" style="color:#ff1744;text-shadow:0 0 12px #ff1744">52</div>
      <div class="kpi-sub">nanoseconds</div>
    </div>
    <div class="kpi" style="--ac:#00e5ff">
      <div class="kpi-label">FPGA TEMP</div>
      <div class="kpi-val" id="k4" style="color:#00e5ff;text-shadow:0 0 12px #00e5ff">71°C</div>
      <div class="kpi-sub">WITHIN LIMITS</div>
    </div>
    <div class="kpi" style="--ac:#00ff88">
      <div class="kpi-label">PNL TODAY</div>
      <div class="kpi-val" id="k5" style="color:#00ff88;text-shadow:0 0 12px #00ff88">$0</div>
      <div class="kpi-sub">USD — SIMULATED</div>
      <div class="kpi-delta" id="k5d" style="color:#00ff88">▲</div>
    </div>
    <div class="kpi" style="--ac:#ffb300">
      <div class="kpi-label">WIN RATE</div>
      <div class="kpi-val" id="k6" style="color:#ffb300;text-shadow:0 0 12px #ffb300">64.2%</div>
      <div class="kpi-sub">ROLLING 1000 TRADES</div>
    </div>
    <div class="kpi" style="--ac:#ff1744">
      <div class="kpi-label">RISK EXPOSURE</div>
      <div class="kpi-val" id="k7" style="color:#ff1744;text-shadow:0 0 12px #ff1744">$1.2M</div>
      <div class="kpi-sub">NET POSITION</div>
    </div>
  </div>

  <!-- Row 2 -->
  <div class="panel" style="grid-column:1/3">
    <div class="panel-title">FPGA RESOURCE UTILIZATION</div>
    <canvas class="chart" id="c-util" height="160"></canvas>
  </div>
  <div class="panel" style="grid-column:3/5">
    <div class="panel-title">LATENCY OVER TIME (ns)</div>
    <canvas class="chart" id="c-lat" height="160"></canvas>
  </div>

  <!-- Row 3 -->
  <div class="panel" style="grid-column:1/2">
    <div class="panel-title">ORDER BOOK DEPTH</div>
    <canvas class="chart" id="c-book" height="150"></canvas>
  </div>
  <div class="panel" style="grid-column:2/3">
    <div class="panel-title">MSG TYPES BREAKDOWN</div>
    <canvas class="chart" id="c-pie" height="150"></canvas>
  </div>
  <div class="panel" style="grid-column:3/5">
    <div class="panel-title">PNL CURVE — CUMULATIVE (SIMULATED USD)</div>
    <canvas class="chart" id="c-pnl" height="150"></canvas>
  </div>

</div>

<script>
// ── Utility ────────────────────────────────────────────────
const $ = id => document.getElementById(id);
function lerp(a,b,t){return a+(b-a)*t;}

function resizeCanvas(canvas) {
  const parent = canvas.parentElement;
  canvas.width  = parent.clientWidth - 20;
  canvas.height = parseInt(canvas.getAttribute('height'));
}

// ── State ──────────────────────────────────────────────────
let totalOrders = 0;
let pnl = 0;
const pnlHistory   = Array.from({length:120}, (_,i)=>Math.sin(i*0.15)*500 + i*8);
const latHistory   = Array.from({length:120}, ()=>42 + Math.random()*12);
const tputHistory  = Array.from({length:120}, ()=>1.5+Math.random()*0.8);

const RESOURCES = [
  { label:'LUTs',    used:73, color:'#00e5ff' },
  { label:'FFs',     used:61, color:'#00ff88' },
  { label:'BRAM',    used:68, color:'#ffb300' },
  { label:'DSP',     used:91, color:'#ff1744' },
  { label:'IO',      used:45, color:'#cc44ff' },
  { label:'GT',      used:82, color:'#00e5ff' },
];
const resTargets = RESOURCES.map(r=>r.used);
const resCurrent = RESOURCES.map(r=>r.used * (0.9 + Math.random()*0.2));

// ── Draw Resource Utilization ──────────────────────────────
function drawUtil(t) {
  const canvas = $('c-util');
  resizeCanvas(canvas);
  const ctx = canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);

  const barH = Math.min(22, (H-20)/(RESOURCES.length+1));
  const labelW = 40, barX = labelW+10, maxW = W-barX-50;

  RESOURCES.forEach((r,i) => {
    const y = 10 + i*(barH+6);
    const pct = resCurrent[i];
    const bw  = (pct/100)*maxW;
    const pulse = 0.7+0.3*Math.sin(t*2+i);

    // Label
    ctx.fillStyle = '#4a4a4a';
    ctx.font = '8px Share Tech Mono,monospace';
    ctx.textAlign='right';
    ctx.fillText(r.label, labelW, y+barH*0.65);

    // Background track
    ctx.fillStyle = 'rgba(255,255,255,0.04)';
    ctx.fillRect(barX, y, maxW, barH);

    // Fill
    const grad = ctx.createLinearGradient(barX,0,barX+bw,0);
    grad.addColorStop(0, r.color+'44');
    grad.addColorStop(1, r.color+'cc');
    ctx.fillStyle = grad;
    ctx.save();
    ctx.shadowColor = r.color;
    ctx.shadowBlur  = 8*pulse;
    ctx.fillRect(barX, y, bw, barH);
    ctx.restore();

    // Shimmer
    const shimX = barX + (t*60 + i*30)%maxW;
    const shimG = ctx.createLinearGradient(shimX-15, 0, shimX+15, 0);
    shimG.addColorStop(0,'transparent');
    shimG.addColorStop(0.5,'rgba(255,255,255,0.12)');
    shimG.addColorStop(1,'transparent');
    ctx.fillStyle=shimG;
    ctx.fillRect(barX, y, bw, barH);

    // Tick marks
    [25,50,75].forEach(tick => {
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth=1;
      ctx.beginPath();
      ctx.moveTo(barX+tick/100*maxW, y);
      ctx.lineTo(barX+tick/100*maxW, y+barH);
      ctx.stroke();
    });

    // Value label
    ctx.fillStyle = r.color;
    ctx.font = `bold 9px Share Tech Mono,monospace`;
    ctx.textAlign='left';
    ctx.fillText(`${pct.toFixed(0)}%`, barX+bw+5, y+barH*0.65);
  });
}

// ── Draw Latency Chart ─────────────────────────────────────
function drawLat(t) {
  const canvas=$('c-lat');
  resizeCanvas(canvas);
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);

  const padL=36, padB=18, padT=8;
  const cW=W-padL-8, cH=H-padB-padT;
  const minV=30, maxV=80;

  // Grid
  [30,40,50,60,70,80].forEach(v=>{
    const gy = padT + cH - (v-minV)/(maxV-minV)*cH;
    ctx.strokeStyle='rgba(255,179,0,0.07)';
    ctx.setLineDash([3,5]);
    ctx.beginPath(); ctx.moveTo(padL,gy); ctx.lineTo(padL+cW,gy); ctx.stroke();
    ctx.fillStyle='#3a3a00'; ctx.font='7px Share Tech Mono,monospace'; ctx.textAlign='right';
    ctx.fillText(v+'ns', padL-3, gy+3);
  });
  ctx.setLineDash([]);

  // Area fill
  const pts = latHistory.map((v,i)=>({
    x: padL + i/latHistory.length*cW,
    y: padT + cH - (v-minV)/(maxV-minV)*cH
  }));
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(pts[0].x, padT+cH);
  pts.forEach(p=>ctx.lineTo(p.x,p.y));
  ctx.lineTo(pts[pts.length-1].x, padT+cH);
  ctx.closePath();
  const aG = ctx.createLinearGradient(0,padT,0,padT+cH);
  aG.addColorStop(0,'rgba(255,179,0,0.3)');
  aG.addColorStop(1,'rgba(255,179,0,0.02)');
  ctx.fillStyle=aG;
  ctx.fill();
  ctx.restore();

  // Line
  ctx.save();
  ctx.beginPath();
  pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
  ctx.strokeStyle='#ffb300';
  ctx.lineWidth=1.5;
  ctx.shadowColor='#ffb300';
  ctx.shadowBlur=8;
  ctx.stroke();
  ctx.restore();

  // Current dot
  const last = pts[pts.length-1];
  ctx.save();
  ctx.beginPath(); ctx.arc(last.x,last.y,4,0,Math.PI*2);
  ctx.fillStyle='#ffb300'; ctx.shadowColor='#ffb300'; ctx.shadowBlur=16;
  ctx.fill();
  ctx.restore();
}

// ── Order Book ─────────────────────────────────────────────
let bookBids = Array.from({length:10},(_,i)=>({px:182.30-i*0.01, qty:100+Math.random()*500}));
let bookAsks = Array.from({length:10},(_,i)=>({px:182.36+i*0.01, qty:100+Math.random()*500}));

function drawBook(t) {
  const canvas=$('c-book');
  resizeCanvas(canvas);
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);

  const midX=W/2;
  const maxQty=800;
  const rowH=(H-20)/10;

  for(let i=0;i<10;i++){
    const bid=bookBids[i], ask=bookAsks[i];
    const by=10+i*rowH;

    // Bid bar (left side)
    const bw = Math.min(bid.qty/maxQty*(midX-50),midX-50);
    ctx.fillStyle='rgba(0,255,136,0.15)';
    ctx.fillRect(midX-50-bw, by, bw, rowH-2);
    ctx.save(); ctx.shadowColor='#00ff88'; ctx.shadowBlur=4;
    ctx.fillStyle='#00ff88'; ctx.font='7px Share Tech Mono,monospace';
    ctx.textAlign='right'; ctx.fillText(bid.px.toFixed(2), midX-55, by+rowH*0.65);
    ctx.restore();

    // Ask bar (right side)
    const aw = Math.min(ask.qty/maxQty*(midX-50),midX-50);
    ctx.fillStyle='rgba(255,23,68,0.15)';
    ctx.fillRect(midX+50, by, aw, rowH-2);
    ctx.save(); ctx.shadowColor='#ff1744'; ctx.shadowBlur=4;
    ctx.fillStyle='#ff1744'; ctx.font='7px Share Tech Mono,monospace';
    ctx.textAlign='left'; ctx.fillText(ask.px.toFixed(2), midX+55, by+rowH*0.65);
    ctx.restore();
  }

  // Mid label
  ctx.fillStyle='#ffb300'; ctx.font='bold 8px Share Tech Mono,monospace';
  ctx.textAlign='center'; ctx.fillText('MID', midX, H-4);
}

// ── Pie chart ──────────────────────────────────────────────
const PIE_DATA = [
  {label:'QUOTE', val:52, color:'#00e5ff'},
  {label:'TRADE', val:24, color:'#00ff88'},
  {label:'ORDER', val:15, color:'#ffb300'},
  {label:'CANCEL',val:9,  color:'#ff1744'},
];

function drawPie(t) {
  const canvas=$('c-pie');
  resizeCanvas(canvas);
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);

  const cx=W*0.38, cy=H/2, r=Math.min(W*0.28,H*0.4);
  let angle=-Math.PI/2;
  const total=PIE_DATA.reduce((s,d)=>s+d.val,0);

  PIE_DATA.forEach((d,i) => {
    const sweep = (d.val/total)*Math.PI*2;
    const pulse = 0.95 + 0.05*Math.sin(t*2+i);
    ctx.save();
    ctx.shadowColor=d.color; ctx.shadowBlur=12*pulse;
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.arc(cx,cy,r*pulse,angle,angle+sweep);
    ctx.closePath();
    ctx.fillStyle=d.color+'bb';
    ctx.fill();
    ctx.strokeStyle='#020408'; ctx.lineWidth=2; ctx.stroke();
    ctx.restore();
    angle+=sweep;
  });

  // Inner circle
  ctx.fillStyle='#020408'; ctx.beginPath(); ctx.arc(cx,cy,r*0.4,0,Math.PI*2); ctx.fill();
  ctx.fillStyle='#ffb300'; ctx.font='bold 10px Orbitron,monospace';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('MSG', cx,cy-5);
  ctx.fillStyle='#4a4a00'; ctx.font='7px Share Tech Mono,monospace'; ctx.fillText('TYPES', cx, cy+8);
  ctx.textBaseline='alphabetic';

  // Legend
  const lx=W*0.72, ly=H*0.15;
  PIE_DATA.forEach((d,i)=>{
    const y=ly+i*22;
    ctx.fillStyle=d.color; ctx.fillRect(lx,y,10,8);
    ctx.fillStyle='#4a4a4a'; ctx.font='7px Share Tech Mono,monospace';
    ctx.textAlign='left'; ctx.fillText(`${d.label} ${d.val}%`, lx+14, y+8);
  });
}

// ── PNL Curve ──────────────────────────────────────────────
function drawPnl(t) {
  const canvas=$('c-pnl');
  resizeCanvas(canvas);
  const ctx=canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  ctx.clearRect(0,0,W,H);

  const padL=50, padB=16, padT=8;
  const cW=W-padL-8, cH=H-padB-padT;
  const minV=Math.min(...pnlHistory)*1.1;
  const maxV=Math.max(...pnlHistory)*1.1;
  const range=maxV-minV || 1;

  // Zero line
  const zeroY = padT + cH - (0-minV)/range*cH;
  ctx.strokeStyle='rgba(255,255,255,0.08)'; ctx.setLineDash([4,4]); ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(padL,zeroY); ctx.lineTo(padL+cW,zeroY); ctx.stroke();
  ctx.setLineDash([]);

  const pts = pnlHistory.map((v,i)=>({
    x: padL + i/(pnlHistory.length-1)*cW,
    y: padT + cH - (v-minV)/range*cH,
    v,
  }));

  // Area
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(pts[0].x, padT+cH);
  pts.forEach(p=>ctx.lineTo(p.x,p.y));
  ctx.lineTo(pts[pts.length-1].x, padT+cH);
  ctx.closePath();
  const aG=ctx.createLinearGradient(0,padT,0,padT+cH);
  aG.addColorStop(0,'rgba(0,255,136,0.35)');
  aG.addColorStop(1,'rgba(0,255,136,0.02)');
  ctx.fillStyle=aG; ctx.fill();
  ctx.restore();

  // Line
  ctx.save();
  ctx.beginPath();
  pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
  ctx.strokeStyle='#00ff88'; ctx.lineWidth=1.5;
  ctx.shadowColor='#00ff88'; ctx.shadowBlur=8; ctx.stroke();
  ctx.restore();

  // Axis labels
  ctx.fillStyle='#1a5a3a'; ctx.font='7px Share Tech Mono,monospace'; ctx.textAlign='right';
  [minV,0,maxV].forEach(v=>{
    const gy=padT+cH-(v-minV)/range*cH;
    ctx.fillText('$'+Math.round(v).toLocaleString(), padL-3, gy+3);
  });

  // Current value
  const last=pts[pts.length-1];
  ctx.save();
  ctx.beginPath(); ctx.arc(last.x,last.y,4,0,Math.PI*2);
  ctx.fillStyle='#00ff88'; ctx.shadowColor='#00ff88'; ctx.shadowBlur=16; ctx.fill();
  ctx.restore();
  ctx.fillStyle='#00ff88'; ctx.font='bold 9px Share Tech Mono,monospace';
  ctx.textAlign='left';
  ctx.fillText('$'+Math.round(last.v).toLocaleString(), last.x-20, last.y-8);
}

// ── State updates ──────────────────────────────────────────
let lastUpdate=0, lastBook=0, lastPnl=0, startTime=null;

function frame(ts) {
  if(!startTime) startTime=ts;
  const t=(ts-startTime)/1000;

  // Animate resources
  RESOURCES.forEach((r,i)=>{
    resCurrent[i]=lerp(resCurrent[i], resTargets[i]*(0.92+Math.sin(t*0.3+i)*0.08), 0.02);
  });

  drawUtil(t);
  drawLat(t);
  drawBook(t);
  drawPie(t);
  drawPnl(t);

  if(ts-lastUpdate>600){
    totalOrders+=Math.floor(Math.random()*180+100);
    $('k1').textContent=totalOrders.toLocaleString();

    pnl += (Math.random()-0.42)*200;
    $('k5').textContent='$'+Math.round(pnl).toLocaleString();
    $('k5d').textContent = pnl>=0 ? '▲ +'+Math.abs(Math.round(Math.random()*500)).toLocaleString() : '▼ -'+Math.abs(Math.round(Math.random()*200)).toLocaleString();
    $('k5d').style.color = pnl>=0?'#00ff88':'#ff1744';
    $('k5').style.color  = pnl>=0?'#00ff88':'#ff1744';

    $('k2').textContent=42+Math.floor(Math.random()*6);
    $('k3').textContent=48+Math.floor(Math.random()*10);
    $('k4').textContent=(69+Math.random()*4).toFixed(1)+'°C';
    $('k6').textContent=(62+Math.random()*5).toFixed(1)+'%';
    $('k7').textContent='$'+(0.8+Math.random()*0.8).toFixed(1)+'M';

    latHistory.shift(); latHistory.push(42+Math.random()*14);
    lastUpdate=ts;
  }

  if(ts-lastBook>400){
    bookBids.forEach(b=>{ b.qty=Math.max(50, b.qty+(Math.random()-0.5)*80); });
    bookAsks.forEach(a=>{ a.qty=Math.max(50, a.qty+(Math.random()-0.5)*80); });
    lastBook=ts;
  }

  if(ts-lastPnl>300){
    const last=pnlHistory[pnlHistory.length-1];
    pnlHistory.shift();
    pnlHistory.push(last+(Math.random()-0.42)*150);
    lastPnl=ts;
  }

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
</body>
</html>
""", height=740, scrolling=False)

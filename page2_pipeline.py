import streamlit as st
import streamlit.components.v1 as components

def render():
    st.markdown("""
    <style>
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00ff88;
        letter-spacing: 6px;
        text-shadow: 0 0 30px #00ff88, 0 0 60px rgba(0,255,136,0.3);
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #1a5a3a;
        letter-spacing: 4px;
        margin-bottom: 1.5rem;
    }
    </style>
    <div class="page-title">ORDER FLOW PIPELINE</div>
    <div class="page-subtitle">SUB-MICROSECOND ORDER PROCESSING — MARKET DATA INGESTION TO EXECUTION</div>
    """, unsafe_allow_html=True)

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');
body { background:#020408; font-family:'Share Tech Mono',monospace; color:#c0e8f8; overflow:hidden; }

.top-bar {
    display:flex; justify-content:space-between; align-items:center;
    padding:8px 20px;
    border-bottom:1px solid rgba(0,255,136,0.15);
    background:rgba(0,10,20,0.9);
}
.top-metric { text-align:center; }
.top-metric-label { font-size:0.55rem; color:#1a5a3a; letter-spacing:3px; }
.top-metric-val   { font-size:1.1rem; color:#00ff88; font-family:'Orbitron',monospace; text-shadow:0 0 12px #00ff88; }

.msg-log {
    position:absolute;
    bottom:0; left:0; right:0;
    height:90px;
    background:rgba(2,8,16,0.95);
    border-top:1px solid rgba(0,255,136,0.15);
    padding:8px 16px;
    overflow:hidden;
}
.log-title { font-size:0.55rem; color:#1a5a3a; letter-spacing:3px; margin-bottom:4px; }
.log-line  { font-size:0.62rem; color:#2a7a5a; line-height:1.7; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.log-line.new { color:#00ff88; }
</style>
</head>
<body>

<div class="top-bar">
  <div class="top-metric"><div class="top-metric-label">MSG INGRESS</div><div class="top-metric-val" id="m-ingress">1.94M/s</div></div>
  <div class="top-metric"><div class="top-metric-label">PIPELINE STAGES</div><div class="top-metric-val">8</div></div>
  <div class="top-metric"><div class="top-metric-label">END-TO-END LATENCY</div><div class="top-metric-val" id="m-lat">47 ns</div></div>
  <div class="top-metric"><div class="top-metric-label">ORDERS/SEC</div><div class="top-metric-val" id="m-ord">284K</div></div>
  <div class="top-metric"><div class="top-metric-label">FILL RATE</div><div class="top-metric-val" id="m-fill">98.2%</div></div>
  <div class="top-metric"><div class="top-metric-label">REJECTS</div><div class="top-metric-val" id="m-rej" style="color:#ff1744">0.04%</div></div>
</div>

<canvas id="c"></canvas>

<div class="msg-log">
  <div class="log-title">PIPELINE EVENT LOG — LIVE</div>
  <div id="log-container"></div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');

function resize() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight - 56 - 90;
}
resize();

// ── Pipeline stage definitions ─────────────────────────────
const STAGES = [
  { id:'eth',   label:'ETH RX',         sublabel:'100G MAC',          color:'#00e5ff', x:0   },
  { id:'dec',   label:'DECODER',        sublabel:'FIX/ITCH/OUCH',     color:'#00e5ff', x:0.12 },
  { id:'nrm',   label:'NORMALIZE',      sublabel:'MSG PARSING',       color:'#00e5ff', x:0.24 },
  { id:'flt',   label:'FILTER',         sublabel:'SYMBOL ROUTING',    color:'#00ff88', x:0.36 },
  { id:'ob',    label:'ORDER BOOK',     sublabel:'BID/ASK UPDATE',    color:'#ff1744', x:0.48 },
  { id:'stg',   label:'STRATEGY',       sublabel:'SIGNAL DETECT',     color:'#00ff88', x:0.60 },
  { id:'rm',    label:'RISK CHECK',     sublabel:'PRE-TRADE CTRL',    color:'#ffb300', x:0.72 },
  { id:'tx',    label:'ORDER TX',       sublabel:'FIX/OUCH OUT',      color:'#00e5ff', x:0.84 },
];

// ── Animated message tokens ────────────────────────────────
const MSG_TYPES = [
  { type:'QUOTE',  color:'#00e5ff', prob:0.5  },
  { type:'TRADE',  color:'#00ff88', prob:0.25 },
  { type:'ORDER',  color:'#ffb300', prob:0.15 },
  { type:'CANCEL', color:'#ff1744', prob:0.10 },
];

const messages = [];
let msgId = 0;

function spawnMsg() {
  const r = Math.random();
  let acc = 0, chosen = MSG_TYPES[0];
  for(const m of MSG_TYPES) { acc+=m.prob; if(r<acc){chosen=m;break;} }
  messages.push({
    id: msgId++,
    type: chosen.type,
    color: chosen.color,
    stage: 0,
    stageT: 0,
    speed: 0.018 + Math.random()*0.012,
    lane: 0.2 + Math.random()*0.6,
    dead: false,
    reject: Math.random() < 0.004,
  });
}

// Seed
for(let i=0;i<12;i++) {
  const m = {id:msgId++,type:'QUOTE',color:'#00e5ff',stage:Math.floor(Math.random()*8),stageT:Math.random(),speed:0.018+Math.random()*0.012,lane:0.2+Math.random()*0.6,dead:false,reject:false};
  messages.push(m);
}

// ── Log ────────────────────────────────────────────────────
const logLines = [];
const logContainer = document.getElementById('log-container');
const LOG_PREFIXES = ['[SYM:AAPL]','[SYM:TSLA]','[SYM:SPY]','[SYM:QQQ]','[SYM:NVDA]','[SYM:AMZN]'];
const LOG_MSGS = [
  'QUOTE received bid=182.34 ask=182.36 qty=500',
  'ORDER BOOK updated depth=12 levels',
  'STRATEGY TRIGGER: spread < threshold',
  'RISK CHECK passed: pos_limit OK',
  'BUY ORDER submitted qty=100 limit=182.35',
  'FILL confirmed qty=100 px=182.35 venue=NASDAQ',
  'CANCEL ACK received oid=7829541',
];

function addLog(msg) {
  const ts = new Date().toISOString().slice(11,23);
  const sym = LOG_PREFIXES[Math.floor(Math.random()*LOG_PREFIXES.length)];
  logLines.unshift(`${ts} ${sym} ${msg}`);
  if(logLines.length > 4) logLines.pop();
  logContainer.innerHTML = logLines.map((l,i) => `<div class="log-line${i===0?' new':''}">${l}</div>`).join('');
}

let lastLog = 0;

// ── Drawing ────────────────────────────────────────────────
function stageX(s) { return s.x * canvas.width + (1/STAGES.length)*canvas.width*0.5; }
const STAGE_W = () => canvas.width / STAGES.length * 0.72;
const STAGE_H = 90;
const PIPE_Y  = () => canvas.height * 0.38;

function drawPipeline(t) {
  const py = PIPE_Y();
  const sw  = STAGE_W();

  // Pipeline backbone
  const x0 = stageX(STAGES[0]);
  const x1 = stageX(STAGES[STAGES.length-1]);
  ctx.save();
  ctx.strokeStyle = 'rgba(0,229,255,0.08)';
  ctx.lineWidth = STAGE_H * 1.4;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(x0, py);
  ctx.lineTo(x1, py);
  ctx.stroke();
  ctx.restore();

  STAGES.forEach((s, i) => {
    const sx = stageX(s);
    const sy = py - STAGE_H/2;
    const pulse = 0.6 + 0.4*Math.sin(t*2.5 + i*0.7);

    // Block bg
    ctx.save();
    ctx.shadowColor = s.color;
    ctx.shadowBlur  = 20*pulse;
    ctx.strokeStyle = s.color;
    ctx.lineWidth   = 1.5;
    ctx.strokeRect(sx - sw/2, sy, sw, STAGE_H);
    ctx.restore();

    const g = ctx.createLinearGradient(sx-sw/2, sy, sx-sw/2, sy+STAGE_H);
    g.addColorStop(0, 'rgba(6,20,40,0.97)');
    g.addColorStop(1, 'rgba(2,8,20,0.99)');
    ctx.fillStyle = g;
    ctx.fillRect(sx-sw/2+1, sy+1, sw-2, STAGE_H-2);

    // Top accent bar
    ctx.fillStyle = s.color + '55';
    ctx.fillRect(sx-sw/2+2, sy+2, sw-4, 3);

    // Stage number
    ctx.fillStyle = s.color + '40';
    ctx.font = `bold ${Math.max(20, sw*0.35)}px 'Orbitron',monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(String(i+1).padStart(2,'0'), sx, py + 6);

    // Labels
    ctx.save();
    ctx.shadowColor = s.color;
    ctx.shadowBlur  = 8;
    ctx.fillStyle = '#e0f4ff';
    ctx.font = `bold ${Math.max(9, sw*0.13)}px 'Share Tech Mono',monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(s.label, sx, sy + 20);
    ctx.fillStyle = s.color + 'bb';
    ctx.font = `${Math.max(7.5, sw*0.10)}px 'Share Tech Mono',monospace`;
    ctx.fillText(s.sublabel, sx, sy + 34);
    ctx.restore();

    // Latency badge
    const ns = [4,3,5,2,8,6,4,5][i];
    ctx.fillStyle = 'rgba(0,0,0,0.7)';
    ctx.fillRect(sx - 20, sy + STAGE_H - 20, 40, 16);
    ctx.save();
    ctx.shadowColor = s.color;
    ctx.shadowBlur  = 6;
    ctx.fillStyle = s.color;
    ctx.font = `${Math.max(7,sw*0.09)}px 'Share Tech Mono',monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(`${ns} ns`, sx, sy + STAGE_H - 9);
    ctx.restore();

    // Arrow to next
    if(i < STAGES.length-1) {
      const nx = stageX(STAGES[i+1]);
      const ax = sx + sw/2 + 2;
      const ay = py;
      ctx.save();
      ctx.strokeStyle = s.color + '60';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(nx - sw/2 - 2, ay);
      ctx.stroke();
      // Arrowhead
      ctx.fillStyle = s.color + '60';
      ctx.beginPath();
      ctx.moveTo(nx - sw/2 - 2, ay);
      ctx.lineTo(nx - sw/2 - 8, ay - 5);
      ctx.lineTo(nx - sw/2 - 8, ay + 5);
      ctx.fill();
      ctx.restore();
    }
  });
}

function drawMessages(t) {
  const py = PIPE_Y();
  const sw = STAGE_W();

  messages.forEach(m => {
    if(m.dead) return;
    const si = Math.min(m.stage, STAGES.length-1);
    const s  = STAGES[si];
    const ns = si+1 < STAGES.length ? STAGES[si+1] : null;

    let x, y;
    if(ns) {
      const x0 = stageX(s);
      const x1 = stageX(ns);
      x = x0 + (x1-x0) * m.stageT;
    } else {
      x = stageX(s) + sw/2 * m.stageT * 1.5;
    }
    const laneOff = (m.lane - 0.5) * STAGE_H * 0.55;
    y = py + laneOff;

    // Trail
    ctx.save();
    ctx.beginPath();
    const trailLen = 24;
    for(let i=0;i<trailLen;i++) {
      const frac = i/trailLen;
      const tx2 = x - frac*18;
      const alpha = (1-frac)*0.5;
      ctx.fillStyle = m.color + Math.floor(alpha*255).toString(16).padStart(2,'0');
      ctx.beginPath();
      ctx.arc(tx2, y, 2*(1-frac*0.6), 0, Math.PI*2);
      ctx.fill();
    }
    ctx.restore();

    // Particle
    ctx.save();
    ctx.shadowColor = m.color;
    ctx.shadowBlur  = 16;
    ctx.fillStyle   = m.color;
    ctx.beginPath();
    ctx.arc(x, y, m.reject ? 5 : 3.5, 0, Math.PI*2);
    ctx.fill();
    ctx.restore();

    // Label badge
    ctx.save();
    ctx.font = '7px Share Tech Mono,monospace';
    ctx.fillStyle = m.color + 'cc';
    ctx.textAlign = 'center';
    ctx.fillText(m.type, x, y - 10);
    ctx.restore();
  });
}

// ── Throughput waterfall chart ─────────────────────────────
const historyLen = 80;
const throughputHistory = Array.from({length:historyLen}, ()=>0.7+Math.random()*0.3);

function drawThroughput(t) {
  const W = canvas.width;
  const H = canvas.height;
  const chartX = W*0.04;
  const chartY = H*0.64;
  const chartW = W*0.42;
  const chartH = H*0.28;

  // bg
  ctx.fillStyle = 'rgba(0,10,20,0.7)';
  ctx.strokeStyle = 'rgba(0,255,136,0.15)';
  ctx.lineWidth = 1;
  ctx.fillRect(chartX, chartY, chartW, chartH);
  ctx.strokeRect(chartX, chartY, chartW, chartH);

  // Title
  ctx.save();
  ctx.fillStyle = '#00ff88';
  ctx.font = '9px Share Tech Mono,monospace';
  ctx.fillText('MSG THROUGHPUT — 1s WINDOW', chartX+8, chartY+12);
  ctx.restore();

  // Grid lines
  for(let g=0;g<=4;g++) {
    const gy = chartY + chartH*0.15 + (chartH*0.78)*g/4;
    ctx.save();
    ctx.strokeStyle = 'rgba(0,255,136,0.07)';
    ctx.setLineDash([3,5]);
    ctx.beginPath(); ctx.moveTo(chartX+4, gy); ctx.lineTo(chartX+chartW-4, gy); ctx.stroke();
    ctx.restore();
    ctx.fillStyle = '#1a5a3a';
    ctx.font = '7px Share Tech Mono,monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`${((4-g)*500/1000).toFixed(1)}M`, chartX+40, gy+3);
  }

  // Bars
  const bw = (chartW - 50) / historyLen;
  throughputHistory.forEach((v, i) => {
    const bh = v * (chartH*0.78);
    const bx = chartX + 44 + i * bw;
    const by = chartY + chartH*0.15 + (chartH*0.78) - bh;
    const alpha = 0.3 + (i/historyLen)*0.7;
    ctx.fillStyle = `rgba(0,255,136,${alpha*0.7})`;
    ctx.fillRect(bx, by, Math.max(bw-1,1), bh);
    if(i === historyLen-1) {
      ctx.save();
      ctx.shadowColor = '#00ff88';
      ctx.shadowBlur  = 8;
      ctx.fillStyle   = '#00ff88';
      ctx.fillRect(bx, by, Math.max(bw-1,1), bh);
      ctx.restore();
    }
  });
}

// ── Latency histogram ─────────────────────────────────────
function drawLatencyHist(t) {
  const W = canvas.width;
  const H = canvas.height;
  const chartX = W*0.54;
  const chartY = H*0.64;
  const chartW = W*0.42;
  const chartH = H*0.28;

  ctx.fillStyle = 'rgba(0,10,20,0.7)';
  ctx.strokeStyle = 'rgba(255,179,0,0.15)';
  ctx.lineWidth = 1;
  ctx.fillRect(chartX, chartY, chartW, chartH);
  ctx.strokeRect(chartX, chartY, chartW, chartH);

  ctx.save();
  ctx.fillStyle = '#ffb300';
  ctx.font = '9px Share Tech Mono,monospace';
  ctx.fillText('END-TO-END LATENCY DISTRIBUTION (ns)', chartX+8, chartY+12);
  ctx.restore();

  const bins = [2,5,12,24,38,52,44,30,18,10,6,3,1];
  const maxBin = Math.max(...bins);
  const bw = (chartW-50) / bins.length;
  const buckets = [30,35,40,42,44,46,48,50,52,55,60,70,80];

  bins.forEach((v,i) => {
    const bh = (v/maxBin) * (chartH*0.72);
    const bx = chartX + 44 + i*bw;
    const by = chartY + chartH*0.15 + chartH*0.72 - bh;
    const highlight = i>=3 && i<=7;
    ctx.save();
    if(highlight) { ctx.shadowColor='#ffb300'; ctx.shadowBlur=10; }
    ctx.fillStyle = highlight ? '#ffb300cc' : '#ffb30055';
    ctx.fillRect(bx, by, Math.max(bw-2,2), bh);
    ctx.restore();

    ctx.fillStyle = '#4a4a0a';
    ctx.font = '6px Share Tech Mono,monospace';
    ctx.textAlign = 'center';
    ctx.fillText(buckets[i], bx+bw/2, chartY+chartH-6);
  });

  // P99 line
  const p99x = chartX + 44 + 8*bw;
  ctx.save();
  ctx.strokeStyle = '#ff1744';
  ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  ctx.beginPath();
  ctx.moveTo(p99x, chartY+chartH*0.15);
  ctx.lineTo(p99x, chartY+chartH*0.87);
  ctx.stroke();
  ctx.fillStyle = '#ff1744';
  ctx.font = '7px Share Tech Mono,monospace';
  ctx.fillText('P99', p99x+2, chartY+chartH*0.2);
  ctx.restore();
}

// ── Grid bg ────────────────────────────────────────────────
function drawGrid() {
  ctx.save();
  ctx.strokeStyle = 'rgba(0,80,50,0.08)';
  ctx.lineWidth = 0.5;
  for(let x=0;x<canvas.width;x+=32){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke();}
  for(let y=0;y<canvas.height;y+=32){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke();}
  ctx.restore();
}

// ── Update ─────────────────────────────────────────────────
let lastSpawn=0, lastTput=0, lastStat=0;
let startTime=null;

function frame(ts) {
  if(!startTime) startTime=ts;
  const t=(ts-startTime)/1000;

  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#020408';
  ctx.fillRect(0,0,canvas.width,canvas.height);

  drawGrid();
  drawPipeline(t);
  drawMessages(t);
  drawThroughput(t);
  drawLatencyHist(t);

  // Advance messages
  messages.forEach(m => {
    if(m.dead) return;
    m.stageT += m.speed;
    if(m.stageT >= 1) {
      m.stageT = 0;
      m.stage++;
      if(m.stage >= STAGES.length) m.dead = true;
    }
  });

  // Remove dead, spawn new
  const alive = messages.filter(m=>!m.dead);
  if(alive.length > 60) {
    const oldest = alive.indexOf(alive.find(m=>m.dead===false));
    messages.splice(0, messages.length-50);
  }
  if(ts-lastSpawn>180) { spawnMsg(); lastSpawn=ts; }

  // Update throughput history
  if(ts-lastTput>200) {
    throughputHistory.shift();
    throughputHistory.push(0.5 + 0.5*Math.random());
    lastTput=ts;
  }

  // Update stats
  if(ts-lastStat>800) {
    document.getElementById('m-ingress').textContent=(1.8+Math.random()*0.4).toFixed(2)+'M/s';
    document.getElementById('m-lat').textContent=(44+Math.floor(Math.random()*8))+' ns';
    document.getElementById('m-ord').textContent=Math.floor(270+Math.random()*30)+'K';
    document.getElementById('m-fill').textContent=(97+Math.random()*2).toFixed(1)+'%';
    lastStat=ts;
  }

  // Log
  if(ts-lastLog>1400) {
    addLog(LOG_MSGS[Math.floor(Math.random()*LOG_MSGS.length)]);
    lastLog=ts;
  }

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
</body>
</html>
""", height=700, scrolling=False)

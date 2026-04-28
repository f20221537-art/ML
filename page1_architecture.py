import streamlit as st
import streamlit.components.v1 as components

def render():
    st.markdown("""
    <style>
    .page-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 900;
        color: #00e5ff;
        letter-spacing: 6px;
        text-shadow: 0 0 30px #00e5ff, 0 0 60px rgba(0,229,255,0.3);
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #2a6a8a;
        letter-spacing: 4px;
        margin-bottom: 2rem;
    }
    </style>
    <div class="page-title">FPGA ARCHITECTURE</div>
    <div class="page-subtitle">XILINX VIRTEX ULTRASCALE+ VU9P — HFT TRADING ACCELERATOR</div>
    """, unsafe_allow_html=True)

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#020408; font-family:'Share Tech Mono',monospace; overflow-x:hidden; }
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

canvas { display:block; }

.overlay {
    position:absolute; top:0; left:0; width:100%; pointer-events:none;
}

.stats-row {
    display:flex; gap:12px; padding:10px 16px; flex-wrap:wrap;
}
.stat-card {
    background:rgba(0,20,40,0.9);
    border:1px solid rgba(0,229,255,0.2);
    border-radius:4px;
    padding:8px 16px;
    min-width:130px;
    flex:1;
}
.stat-label { font-size:0.55rem; color:#2a6a8a; letter-spacing:3px; }
.stat-value { font-size:1.1rem; color:#00e5ff; font-family:'Orbitron',monospace; font-weight:700; text-shadow:0 0 10px #00e5ff; }
.stat-unit  { font-size:0.55rem; color:#1a4a6a; }

.legend {
    display:flex; gap:16px; padding:6px 16px; flex-wrap:wrap;
}
.legend-item { display:flex; align-items:center; gap:6px; font-size:0.6rem; color:#4a7a9a; letter-spacing:1px; }
.legend-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
</style>
</head>
<body>

<div class="stats-row">
  <div class="stat-card">
    <div class="stat-label">LOGIC CELLS</div>
    <div class="stat-value" id="s-lc">2.586M</div>
    <div class="stat-unit">UTILIZATION 73%</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">DSP SLICES</div>
    <div class="stat-value" id="s-dsp">6,840</div>
    <div class="stat-unit">ACTIVE 91%</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">BRAM BLOCKS</div>
    <div class="stat-value" id="s-bram">4,320</div>
    <div class="stat-unit">USED 68%</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">CLOCK SPEED</div>
    <div class="stat-value" id="s-clk">250</div>
    <div class="stat-unit">MHz</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">LATENCY</div>
    <div class="stat-value" id="s-lat">47</div>
    <div class="stat-unit">NANOSECONDS</div>
  </div>
</div>

<canvas id="c"></canvas>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#00e5ff;box-shadow:0 0 6px #00e5ff"></div>DATA PATH SIGNAL</div>
  <div class="legend-item"><div class="legend-dot" style="background:#00ff88;box-shadow:0 0 6px #00ff88"></div>CONTROL SIGNAL</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffb300;box-shadow:0 0 6px #ffb300"></div>CLOCK DISTRIBUTION</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ff1744;box-shadow:0 0 6px #ff1744"></div>MEMORY ACCESS</div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');

function resize() {
  canvas.width  = window.innerWidth;
  canvas.height = Math.max(window.innerHeight - 140, 480);
}
resize();
window.addEventListener('resize', () => { resize(); });

// ── Color palette ─────────────────────────────────────────
const C = {
  bg:      '#020408',
  panel:   '#060d14',
  border:  'rgba(0,229,255,0.18)',
  cyan:    '#00e5ff',
  green:   '#00ff88',
  amber:   '#ffb300',
  red:     '#ff1744',
  muted:   '#1a3a5a',
  text:    '#7ab4cc',
  textHi:  '#c0e8f8',
};

// ── Block layout (fractional coords) ─────────────────────
const BLOCKS = [
  // ── Top row: external interfaces ──────────────────────────────
  { id:'eth',   label:'100G ETHERNET\nMAC/PHY',   col:0,  row:0, w:2, h:1.4, color:C.cyan,  type:'io' },
  { id:'pcie',  label:'PCIe Gen4 x16\nHOST IFACE',col:2,  row:0, w:2, h:1.4, color:C.green, type:'io' },
  { id:'qdma',  label:'QDMA ENGINE\nDMA CTRL',    col:4,  row:0, w:2, h:1.4, color:C.green, type:'io' },
  { id:'clk',   label:'CLOCK MGMT\n250/500 MHz',  col:6,  row:0, w:2, h:1.4, color:C.amber, type:'clk'},

  // ── Middle row: processing cores ──────────────────────────────
  { id:'mdp',   label:'MARKET DATA\nPREPROC',     col:0,  row:1.8, w:2, h:1.6, color:C.cyan,  type:'proc' },
  { id:'norm',  label:'MSG NORMALIZER\nFIX/ITCH',  col:2,  row:1.8, w:2, h:1.6, color:C.cyan,  type:'proc' },
  { id:'ob',    label:'ORDER BOOK\nENGINE x8',     col:4,  row:1.8, w:2, h:1.6, color:C.red,   type:'mem'  },
  { id:'strat', label:'STRATEGY\nARBITRAGE',       col:6,  row:1.8, w:2, h:1.6, color:C.green, type:'proc' },

  // ── Bottom row: output ────────────────────────────────────────
  { id:'rm',    label:'RISK MGMT\nPRE-TRADE',      col:0,  row:3.8, w:2, h:1.6, color:C.amber, type:'risk' },
  { id:'oe',    label:'ORDER ENTRY\nFIX ENGINE',    col:2,  row:3.8, w:2, h:1.6, color:C.cyan,  type:'proc' },
  { id:'hbm',   label:'HBM2E MEMORY\n16 GB 460GB/s',col:4, row:3.8, w:2, h:1.6, color:C.red,   type:'mem'  },
  { id:'mon',   label:'PERF MONITOR\nTELEMETRY',   col:6,  row:3.8, w:2, h:1.6, color:C.amber, type:'io'   },
];

// ── Connections (from, to, color) ──────────────────────────
const EDGES = [
  ['eth',  'mdp',   C.cyan ],
  ['pcie', 'qdma',  C.green],
  ['qdma', 'strat', C.green],
  ['clk',  'norm',  C.amber],
  ['clk',  'ob',    C.amber],
  ['mdp',  'norm',  C.cyan ],
  ['norm', 'ob',    C.cyan ],
  ['ob',   'strat', C.red  ],
  ['strat','rm',    C.green],
  ['rm',   'oe',    C.amber],
  ['oe',   'eth',   C.cyan ],
  ['ob',   'hbm',   C.red  ],
  ['hbm',  'ob',    C.red  ],
  ['mon',  'strat', C.amber],
  ['oe',   'mon',   C.amber],
];

// ── Animated signal particles ─────────────────────────────
const particles = [];

function makeParticle(edge) {
  const [fromId, toId, color] = edge;
  particles.push({ fromId, toId, color, t: Math.random(), speed: 0.004 + Math.random()*0.004 });
}

// Seed particles
EDGES.forEach(e => {
  const n = 2 + Math.floor(Math.random()*3);
  for (let i=0;i<n;i++) makeParticle(e);
});

// ── Layout helpers ────────────────────────────────────────
let COLS = 8, ROWS = 5.4;
let PAD, CW, CH, OX, OY;

function layout() {
  const W = canvas.width, H = canvas.height;
  PAD = Math.min(W, H) * 0.04;
  const availW = W - PAD*2, availH = H - PAD*2 - 20;
  CW = availW / COLS;
  CH = availH / ROWS;
  OX = PAD;
  OY = PAD + 10;
}

function blockRect(b) {
  return {
    x: OX + b.col * CW + 4,
    y: OY + b.row * CH + 4,
    w: b.w  * CW - 8,
    h: b.h  * CH - 8,
  };
}

function blockCenter(id) {
  const b = BLOCKS.find(b=>b.id===id);
  const r = blockRect(b);
  return { x: r.x + r.w/2, y: r.y + r.h/2 };
}

// ── Draw helpers ──────────────────────────────────────────
function glow(color, blur=18) {
  ctx.shadowColor = color;
  ctx.shadowBlur  = blur;
}
function noGlow() { ctx.shadowBlur = 0; }

function drawBlock(b, t) {
  const r = blockRect(b);
  const pulse = 0.7 + 0.3 * Math.sin(t * 2 + b.col + b.row);

  // Outer glow
  ctx.save();
  ctx.shadowColor = b.color;
  ctx.shadowBlur  = 16 * pulse;
  ctx.strokeStyle = b.color;
  ctx.lineWidth   = 1.5;
  ctx.strokeRect(r.x, r.y, r.w, r.h);
  ctx.restore();

  // Fill
  const grad = ctx.createLinearGradient(r.x, r.y, r.x, r.y+r.h);
  grad.addColorStop(0, 'rgba(6,18,36,0.95)');
  grad.addColorStop(1, 'rgba(2,8,20,0.98)');
  ctx.fillStyle = grad;
  ctx.fillRect(r.x+1, r.y+1, r.w-2, r.h-2);

  // Corner accents
  const accentLen = Math.min(r.w, r.h) * 0.18;
  ctx.save();
  ctx.strokeStyle = b.color;
  ctx.lineWidth = 2;
  glow(b.color, 8);
  [
    [r.x, r.y, 1, 1], [r.x+r.w, r.y, -1, 1],
    [r.x, r.y+r.h, 1, -1], [r.x+r.w, r.y+r.h, -1, -1]
  ].forEach(([cx,cy,dx,dy]) => {
    ctx.beginPath();
    ctx.moveTo(cx + dx*accentLen, cy);
    ctx.lineTo(cx, cy);
    ctx.lineTo(cx, cy + dy*accentLen);
    ctx.stroke();
  });
  ctx.restore();

  // Type icon / activity bars
  const barW = 3, barGap = 5, barCount = 5;
  const barTotalW = barCount*(barW+barGap)-barGap;
  const barX0 = r.x + r.w - barTotalW - 8;
  const barMaxH = 16;
  const barY = r.y + 10;
  for(let i=0;i<barCount;i++) {
    const h = (0.3 + 0.7*Math.abs(Math.sin(t*3 + i*0.8 + b.col))) * barMaxH;
    ctx.fillStyle = b.color + '88';
    ctx.fillRect(barX0 + i*(barW+barGap), barY + barMaxH - h, barW, h);
  }

  // Label
  ctx.save();
  ctx.shadowColor = b.color;
  ctx.shadowBlur = 6;
  ctx.fillStyle = '#c0e8f8';
  ctx.font = `bold ${Math.max(9, CW*0.08)}px 'Share Tech Mono',monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const lines = b.label.split('\n');
  const lineH = Math.max(11, CW*0.1);
  const startY = r.y + r.h/2 - (lines.length-1)*lineH/2;
  lines.forEach((ln, i) => {
    ctx.fillStyle = i===0 ? '#e0f4ff' : b.color + 'cc';
    ctx.font = i===0
      ? `bold ${Math.max(9,CW*0.08)}px 'Share Tech Mono',monospace`
      : `${Math.max(7,CW*0.065)}px 'Share Tech Mono',monospace`;
    ctx.fillText(ln, r.x + r.w/2, startY + i*lineH);
  });
  ctx.restore();
}

function drawEdge(fromId, toId, color, t) {
  const A = blockCenter(fromId), B = blockCenter(toId);
  const dx = B.x-A.x, dy = B.y-A.y;
  const dist = Math.sqrt(dx*dx+dy*dy);

  ctx.save();
  ctx.beginPath();
  const cp1x = A.x + dx*0.35 + (dy>0?0:-dy*0.1);
  const cp1y = A.y + dy*0.15;
  const cp2x = B.x - dx*0.35;
  const cp2y = B.y - dy*0.15;
  ctx.moveTo(A.x, A.y);
  ctx.bezierCurveTo(cp1x,cp1y, cp2x,cp2y, B.x,B.y);

  ctx.strokeStyle = color + '30';
  ctx.lineWidth = 1.5;
  ctx.shadowColor = color;
  ctx.shadowBlur = 4;
  ctx.stroke();
  ctx.restore();
}

function drawParticle(p, t) {
  const A = blockCenter(p.fromId), B = blockCenter(p.toId);
  const dx = B.x-A.x, dy = B.y-A.y;
  const cp1x = A.x + dx*0.35; const cp1y = A.y + dy*0.15;
  const cp2x = B.x - dx*0.35; const cp2y = B.y - dy*0.15;

  // Cubic bezier point
  const tt = p.t;
  const mt = 1-tt;
  const px = mt*mt*mt*A.x + 3*mt*mt*tt*cp1x + 3*mt*tt*tt*cp2x + tt*tt*tt*B.x;
  const py = mt*mt*mt*A.y + 3*mt*mt*tt*cp1y + 3*mt*tt*tt*cp2y + tt*tt*tt*B.y;

  ctx.save();
  ctx.beginPath();
  ctx.arc(px, py, 3, 0, Math.PI*2);
  ctx.fillStyle = p.color;
  ctx.shadowColor = p.color;
  ctx.shadowBlur = 12;
  ctx.fill();

  // Tail
  ctx.beginPath();
  ctx.arc(px, py, 6, 0, Math.PI*2);
  ctx.fillStyle = p.color + '30';
  ctx.shadowBlur = 0;
  ctx.fill();
  ctx.restore();
}

// ── Background grid ───────────────────────────────────────
function drawGrid() {
  ctx.save();
  ctx.strokeStyle = 'rgba(0,60,90,0.15)';
  ctx.lineWidth = 0.5;
  const step = 32;
  for(let x=0;x<canvas.width;x+=step) {
    ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke();
  }
  for(let y=0;y<canvas.height;y+=step) {
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke();
  }
  ctx.restore();
}

// ── Scanline overlay ──────────────────────────────────────
function drawScanlines(t) {
  ctx.save();
  const scanY = (t * 60) % canvas.height;
  const grad = ctx.createLinearGradient(0, scanY-40, 0, scanY+40);
  grad.addColorStop(0, 'transparent');
  grad.addColorStop(0.5, 'rgba(0,229,255,0.025)');
  grad.addColorStop(1, 'transparent');
  ctx.fillStyle = grad;
  ctx.fillRect(0, scanY-40, canvas.width, 80);
  ctx.restore();
}

// ── Flicker random stat ────────────────────────────────────
let lastFlicker = 0;
function flickerStats(ts) {
  if(ts - lastFlicker < 1200) return;
  lastFlicker = ts;
  const el = document.getElementById('s-lat');
  if(el) el.textContent = (44 + Math.floor(Math.random()*8)).toString();
}

// ── Main loop ─────────────────────────────────────────────
let startTime = null;
function frame(ts) {
  if(!startTime) startTime = ts;
  const t = (ts - startTime) / 1000;

  layout();
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // BG
  ctx.fillStyle = C.bg;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  drawGrid();
  drawScanlines(t);

  // Edges
  EDGES.forEach(([a,b,c]) => drawEdge(a,b,c,t));

  // Particles
  particles.forEach(p => {
    p.t += p.speed;
    if(p.t > 1) {
      p.t = 0;
      p.speed = 0.003 + Math.random()*0.005;
    }
    drawParticle(p, t);
  });

  // Blocks
  BLOCKS.forEach(b => drawBlock(b, t));

  flickerStats(ts);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
</body>
</html>
""", height=650, scrolling=False)

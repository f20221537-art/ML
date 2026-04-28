# ⚡ FPGA-Based HFT Simulator

A visually stunning browser-based simulation of an **FPGA High-Frequency Trading** accelerator system — built with Streamlit and Canvas animations.

---

## 🖥️ Pages

### Page 1 — FPGA Architecture Overview
Animated block diagram of the Xilinx VU9P FPGA internals:
- All major hardware blocks (Ethernet MAC, PCIe, Order Book Engine, Strategy Core, HBM2E)
- Animated signal particles flowing between modules
- Real-time activity bars on each block
- Corner-accent neon styling with scanline overlay

### Page 2 — Order Flow Pipeline
8-stage pipeline from raw market data to order execution:
- Animated message tokens (QUOTE / TRADE / ORDER / CANCEL) flowing through stages
- Per-stage latency badges
- Live throughput waterfall bar chart
- Latency distribution histogram with P99 marker
- Live event log console

### Page 3 — Live Performance Monitor
Full telemetry dashboard:
- 8 live KPI cards (Clock, Orders, P50/P99 Latency, Temp, PnL, Win Rate, Risk)
- FPGA resource utilization bars (LUTs, FFs, BRAM, DSP, IO, GT) with shimmer animation
- Latency-over-time area chart
- Order book depth visualization (bid/ask)
- Message type pie chart
- Cumulative PnL curve

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fpga-hft-sim.git
cd fpga-hft-sim

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
fpga-hft-sim/
├── app.py                   # Main entry point & sidebar nav
├── requirements.txt
├── README.md
└── pages/
    ├── __init__.py
    ├── page1_architecture.py   # FPGA chip block diagram
    ├── page2_pipeline.py       # Order flow pipeline animation
    └── page3_monitor.py        # Live performance dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + HTML5 Canvas (via `components.html`) |
| Animations | Vanilla JS `requestAnimationFrame` |
| Fonts | Google Fonts — Orbitron + Share Tech Mono |
| Deployment | Streamlit Community Cloud / Docker |

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set **Main file path** to `app.py`
4. Deploy!

---

## 📌 Notes

- All data is **simulated** — no real market connections
- Designed for fullscreen (1280px+ width recommended)
- All animations run at 60fps via Canvas `requestAnimationFrame`
- No additional Python packages beyond Streamlit needed

---

> Built for the FPGA HFT project — simulating sub-microsecond trading architecture

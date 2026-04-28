import streamlit as st

st.set_page_config(
    page_title="FPGA HFT Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

:root {
    --neon-green:  #00ff88;
    --neon-cyan:   #00e5ff;
    --neon-amber:  #ffb300;
    --neon-red:    #ff1744;
    --bg-deep:     #020408;
    --bg-card:     #060d14;
    --bg-panel:    #0a1628;
    --border-glow: rgba(0,229,255,0.25);
    --text-primary:#e0f4ff;
    --text-muted:  #5a7a99;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background: #030b14 !important;
    border-right: 1px solid var(--border-glow);
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Sidebar nav label */
.sidebar-logo {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 900;
    color: var(--neon-cyan) !important;
    letter-spacing: 3px;
    text-align: center;
    padding: 1rem 0 0.5rem;
    text-shadow: 0 0 20px var(--neon-cyan);
}
.sidebar-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted) !important;
    text-align: center;
    letter-spacing: 4px;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">FPGA//HFT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">SIMULATION ENGINE v2.4</div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "NAVIGATE",
        ["⚡  Architecture Overview", "📊  Order Flow Pipeline", "🔥  Live Performance Monitor"],
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-family:Share Tech Mono;font-size:0.65rem;color:#2a4a6a;line-height:1.8;'>
    SYSTEM STATUS: ONLINE<br>
    CLOCK FREQ: 250 MHz<br>
    LATENCY: 47 ns<br>
    THROUGHPUT: 2.1M msg/s<br>
    FPGA: Xilinx VU9P<br>
    BUILD: 2024.2
    </div>
    """, unsafe_allow_html=True)

# ── Page Router ───────────────────────────────────────────────────────────────
if "Architecture" in page:
    from pages.page1_architecture import render
    render()
elif "Order Flow" in page:
    from pages.page2_pipeline import render
    render()
elif "Performance" in page:
    from pages.page3_monitor import render
    render()

"""
CivicLens AI - Main Application Entry Point
Home page with hero section, features, and navigation.
"""

import streamlit as st
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, seed_demo_data

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CivicLens AI — Smart Civic Problem Detection",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/civiclens-ai",
        "Report a bug": None,
        "About": "CivicLens AI — Hackathon Demo v1.0"
    }
)

# ─── Initialize DB ────────────────────────────────────────────────────────────

init_db()
seed_demo_data()

# ─── Global CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Dark background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1321 50%, #0a0e1a 100%);
    color: #e8eaf6;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1321 0%, #111827 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #a5b4fc;
}

/* ── Custom cards ── */
.cl-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin: 8px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.cl-card:hover {
    border-color: rgba(99, 102, 241, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-value {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.8rem;
    color: #9ca3af;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Severity badges ── */
.badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600; }
.badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600; }
.badge-low    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600; }

/* ── Status badges ── */
.status-open       { background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.25);  border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; }
.status-inprogress { background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; }
.status-resolved   { background: rgba(34,197,94,0.1);  color: #4ade80; border: 1px solid rgba(34,197,94,0.25);  border-radius: 20px; padding: 3px 10px; font-size: 0.75rem; }

/* ── Gradient headings ── */
.gradient-text {
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* ── Hero section ── */
.hero-section {
    text-align: center;
    padding: 60px 20px 40px;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(167,139,250,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.8rem;
    color: #a78bfa;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin: 16px 0;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.2rem;
    color: #9ca3af;
    max-width: 600px;
    margin: 0 auto 40px;
    line-height: 1.7;
}

/* ── Feature cards ── */
.feature-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 16px;
    padding: 28px 24px;
    height: 100%;
    transition: all 0.3s ease;
}
.feature-card:hover {
    border-color: rgba(99,102,241,0.4);
    box-shadow: 0 4px 24px rgba(99,102,241,0.12);
    transform: translateY(-3px);
}
.feature-icon {
    font-size: 2.2rem;
    margin-bottom: 12px;
}
.feature-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e8eaf6;
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 0.85rem;
    color: #6b7280;
    line-height: 1.6;
}

/* ── Score ring ── */
.score-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    font-size: 1.8rem;
    font-weight: 900;
    border: 4px solid;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    border: none !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.3) !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #a78bfa) !important;
    border-radius: 4px;
}

/* ── Divider ── */
.cl-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 24px 0;
}

/* ── Demo tag ── */
.demo-tag {
    background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(251,191,36,0.1));
    border: 1px solid rgba(245,158,11,0.4);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.8rem;
    color: #fbbf24;
    font-weight: 600;
    display: inline-block;
}

/* ── Charts ── */
.js-plotly-plot .plotly {
    background: transparent !important;
}

/* ── Tables ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e8eaf6 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 12px !important;
}

/* ── Sidebar nav ── */
.sidebar-logo {
    text-align: center;
    padding: 16px 0 8px;
    border-bottom: 1px solid rgba(99,102,241,0.15);
    margin-bottom: 16px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1321; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.7); }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2rem;">🏙️</div>
        <div style="font-weight:800;font-size:1.1rem;color:#a5b4fc;margin-top:4px;">CivicLens AI</div>
        <div style="font-size:0.7rem;color:#6b7280;margin-top:2px;">Smart Civic Reporting</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Navigation")
    st.page_link("app.py", label="🏠 Home", icon=None)
    st.page_link("pages/1_Report_Problem.py", label="📸 Report Problem", icon=None)
    st.page_link("pages/2_Dashboard.py", label="📊 Admin Dashboard", icon=None)
    st.page_link("pages/3_Report_Details.py", label="🔍 Report Details", icon=None)

    st.divider()

    st.markdown("### ℹ️ About")
    st.markdown("""
    <div style="font-size:0.78rem;color:#6b7280;line-height:1.6;">
    CivicLens AI uses computer vision and intelligent scoring to convert civic problem photos into actionable government reports.
    <br><br>
    <span style="color:#fbbf24;font-weight:600;">⚡ Demo Mode Active</span><br>
    Sample data pre-loaded for demonstration.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size:0.7rem;color:#374151;text-align:center;">
    Built for Hackathon 2026<br>
    CivicLens AI v1.0
    </div>
    """, unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🏆 Hackathon 2026 · AI for Good</div>
    <div class="hero-title">CivicLens AI</div>
    <div class="hero-subtitle">
        Upload a photo of any civic problem — potholes, garbage, broken streetlights —
        and our AI instantly converts it into a structured, prioritized government report.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CTA Buttons ──────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1.5, 1.5, 1])
with col1:
    if st.button("📸  Report a Problem", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Report_Problem.py")
with col2:
    if st.button("📊  View Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")

# ─── Live Stats Bar ───────────────────────────────────────────────────────────

from database import get_stats
stats = get_stats()

st.markdown("<hr class='cl-divider'>", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{stats['total']}</div>
        <div class="metric-label">Total Reports</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="background:linear-gradient(135deg,#ef4444,#f87171);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{stats['high']}</div>
        <div class="metric-label">High Priority</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="background:linear-gradient(135deg,#f59e0b,#fbbf24);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{stats['medium']}</div>
        <div class="metric-label">Medium Priority</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="background:linear-gradient(135deg,#22c55e,#4ade80);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{stats['low']}</div>
        <div class="metric-label">Low Priority</div>
    </div>""", unsafe_allow_html=True)
with m5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{stats['avg_score']}</div>
        <div class="metric-label">Avg Priority Score</div>
    </div>""", unsafe_allow_html=True)

# ─── Feature Cards ────────────────────────────────────────────────────────────

st.markdown("<hr class='cl-divider'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;font-weight:800;color:#e8eaf6;'>How CivicLens AI Works</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#6b7280;margin-bottom:28px;'>From photo to actionable report in seconds</p>", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
features = [
    ("📸", "Upload Photo", "Snap or upload a photo of any civic problem — pothole, garbage, broken streetlight, water leakage, or open drain."),
    ("🧠", "AI Analysis", "Our vision AI instantly detects the problem type, estimates severity, and generates relevant tags with confidence scores."),
    ("🎯", "Priority Scoring", "A transparent 5-factor scoring formula (0–100) ranks each report by urgency, safety risk, and public impact."),
    ("📊", "Live Dashboard", "All reports flow into an interactive admin dashboard with charts, maps, filters, and real-time civic intelligence."),
]
for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

# ─── Problem Categories ────────────────────────────────────────────────────────

st.markdown("<hr class='cl-divider'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;font-weight:800;color:#e8eaf6;'>Detected Problem Categories</h2>", unsafe_allow_html=True)

categories_display = [
    ("🚧", "Road Damage", "#FF4B4B"),
    ("🗑️", "Garbage Overflow", "#FFA500"),
    ("💡", "Broken Streetlight", "#FFD700"),
    ("💧", "Water Leakage", "#00B4D8"),
    ("🧱", "Damaged Pavement", "#8B8B8B"),
    ("🕳️", "Open Drain", "#CD853F"),
    ("🏗️", "Broken Infrastructure", "#6C757D"),
]

cols = st.columns(7)
for col, (icon, name, color) in zip(cols, categories_display):
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:16px 8px;border:1px solid {color}30;border-radius:12px;
                    background:linear-gradient(135deg,{color}15,{color}05);transition:all 0.3s;">
            <div style="font-size:1.8rem;">{icon}</div>
            <div style="font-size:0.72rem;color:#9ca3af;margin-top:6px;font-weight:500;">{name}</div>
        </div>""", unsafe_allow_html=True)

# ─── How Priority Works ───────────────────────────────────────────────────────

st.markdown("<hr class='cl-divider'>", unsafe_allow_html=True)

col_a, col_b = st.columns([1.2, 1])
with col_a:
    st.markdown("""
    <h3 style='font-weight:800;color:#e8eaf6;'>🎯 Transparent Priority Scoring</h3>
    <p style='color:#6b7280;font-size:0.9rem;'>Every score is explained — no black boxes.</p>
    """, unsafe_allow_html=True)

    factors = [
        ("Severity Weight", "40 pts max", "#ef4444", 40),
        ("Duplicate Reports", "20 pts max", "#f59e0b", 20),
        ("Category Risk", "15 pts max", "#a78bfa", 15),
        ("Safety Risk", "15 pts max", "#60a5fa", 15),
        ("Location Importance", "10 pts max", "#34d399", 10),
    ]
    for name, pts, color, val in factors:
        st.markdown(f"""
        <div style="margin:8px 0;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:0.85rem;color:#d1d5db;font-weight:500;">{name}</span>
                <span style="font-size:0.8rem;color:{color};font-weight:600;">{pts}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:6px;">
                <div style="background:{color};width:{val}%;height:6px;border-radius:4px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <h3 style='font-weight:800;color:#e8eaf6;'>🔍 Duplicate Detection</h3>
    <p style='color:#6b7280;font-size:0.9rem;'>Prevents redundant reports from clogging the system.</p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="cl-card" style="margin-top:8px;">
        <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;">
            <span style="font-size:1.4rem;">🗂️</span>
            <div>
                <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;">Category Matching</div>
                <div style="color:#6b7280;font-size:0.8rem;">Same civic problem type</div>
            </div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;">
            <span style="font-size:1.4rem;">📍</span>
            <div>
                <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;">Location Proximity</div>
                <div style="color:#6b7280;font-size:0.8rem;">Haversine distance &lt; 500 meters</div>
            </div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:12px;">
            <span style="font-size:1.4rem;">📈</span>
            <div>
                <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;">Priority Boost</div>
                <div style="color:#6b7280;font-size:0.8rem;">Each duplicate adds 5 pts to priority score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Demo Data Notice ──────────────────────────────────────────────────────────

st.markdown("<hr class='cl-divider'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:20px;">
    <div class="demo-tag">⚡ DEMO MODE ACTIVE — 7 sample reports pre-loaded for demonstration</div>
    <div style="color:#6b7280;font-size:0.8rem;margin-top:12px;">
        All reports marked [DEMO] are synthetic data for hackathon presentation purposes only.
        Real deployments would connect to live civic databases and government APIs.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center;padding:24px 0 8px;color:#374151;font-size:0.78rem;">
    CivicLens AI — Built with ❤️ for Hackathon 2026 · Powered by Streamlit & Python
</div>
""", unsafe_allow_html=True)

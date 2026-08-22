"""
CivicLens AI - Admin Dashboard Page
Interactive analytics dashboard with charts, maps, and report table.
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import (
    get_all_reports, get_stats, get_category_distribution,
    get_severity_distribution, get_reports_over_time,
    get_location_data, get_priority_distribution
)

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Admin Dashboard — CivicLens AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1321 50%, #0a0e1a 100%); color: #e8eaf6; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1321 0%, #111827 100%); border-right: 1px solid rgba(99,102,241,0.2); }
.metric-card { background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.08)); border: 1px solid rgba(99,102,241,0.25); border-radius: 14px; padding: 18px; text-align: center; }
.metric-value { font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.metric-label { font-size: 0.72rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }
.chart-container { background: rgba(255,255,255,0.02); border: 1px solid rgba(99,102,241,0.12); border-radius: 16px; padding: 16px; margin: 8px 0; }
.section-header { font-size: 1.1rem; font-weight: 700; color: #e8eaf6; margin: 0 0 12px; display: flex; align-items: center; gap: 8px; }
.badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius: 20px; padding: 2px 8px; font-size: 0.72rem; font-weight: 700; }
.badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 20px; padding: 2px 8px; font-size: 0.72rem; font-weight: 700; }
.badge-low    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  border-radius: 20px; padding: 2px 8px; font-size: 0.72rem; font-weight: 700; }
.stButton > button { border-radius: 10px !important; font-weight: 600 !important; }
.stSelectbox > div > div, .stTextInput > div > div > input, .stMultiSelect > div > div {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 8px !important; color: #e8eaf6 !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ─────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#9ca3af", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#9ca3af")),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)")
)

SEVERITY_COLORS = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#22c55e"}
CATEGORY_COLORS = {
    "Road Damage": "#FF4B4B",
    "Garbage Overflow": "#FFA500",
    "Broken Streetlight": "#FFD700",
    "Water Leakage": "#00B4D8",
    "Damaged Pavement": "#8B8B8B",
    "Open Drain": "#CD853F",
    "Broken Infrastructure": "#6C757D"
}

# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px;border-bottom:1px solid rgba(99,102,241,0.15);margin-bottom:16px;">
        <div style="font-size:2rem;">🏙️</div>
        <div style="font-weight:800;font-size:1.1rem;color:#a5b4fc;">CivicLens AI</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("### 🧭 Navigation")
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Report_Problem.py", label="📸 Report Problem")
    st.page_link("pages/2_Dashboard.py", label="📊 Admin Dashboard")
    st.page_link("pages/3_Report_Details.py", label="🔍 Report Details")
    st.divider()

    st.markdown("### 🎛️ Filters")
    filter_severity = st.selectbox("Severity", ["All", "HIGH", "MEDIUM", "LOW"], key="dash_sev")
    filter_category = st.selectbox("Category", ["All", "Road Damage", "Garbage Overflow", "Broken Streetlight",
                                                  "Water Leakage", "Damaged Pavement", "Open Drain", "Broken Infrastructure"], key="dash_cat")
    filter_status = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved"], key="dash_status")
    search_term = st.text_input("🔍 Search", placeholder="keyword...", key="dash_search")
    sort_by = st.selectbox("Sort By", ["created_at", "priority_score", "duplicate_count"], key="dash_sort")
    sort_order = st.selectbox("Order", ["DESC", "ASC"], key="dash_order")

    st.divider()
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# ─── Load Data ────────────────────────────────────────────────────────────────

filters = {
    "severity": filter_severity,
    "category": filter_category,
    "status": filter_status,
    "search": search_term,
    "sort": sort_by,
    "order": sort_order
}

stats = get_stats()
all_reports = get_all_reports(filters)
cat_dist = get_category_distribution()
sev_dist = get_severity_distribution()
time_data = get_reports_over_time()
loc_data = get_location_data()
priority_scores = get_priority_distribution()

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="padding:16px 0 8px;display:flex;align-items:center;justify-content:space-between;">
    <div>
        <div style="font-size:2rem;font-weight:900;background:linear-gradient(135deg,#fff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            📊 Admin Dashboard
        </div>
        <div style="color:#6b7280;font-size:0.9rem;margin-top:2px;">Real-time civic intelligence overview</div>
    </div>
</div>
<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);margin:8px 0 20px;">
""", unsafe_allow_html=True)

# ─── KPI Metrics ─────────────────────────────────────────────────────────────

m1, m2, m3, m4, m5, m6 = st.columns(6)
metrics = [
    (str(stats["total"]), "Total Reports", "linear-gradient(135deg,#6366f1,#a78bfa)"),
    (str(stats["high"]), "High Priority", "linear-gradient(135deg,#ef4444,#f87171)"),
    (str(stats["medium"]), "Medium Priority", "linear-gradient(135deg,#f59e0b,#fbbf24)"),
    (str(stats["low"]), "Low Priority", "linear-gradient(135deg,#22c55e,#4ade80)"),
    (str(stats["avg_score"]), "Avg Score", "linear-gradient(135deg,#6366f1,#60a5fa)"),
    (str(stats["open"]), "Open Issues", "linear-gradient(135deg,#ef4444,#f87171)"),
]
for col, (val, label, grad) in zip([m1, m2, m3, m4, m5, m6], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="background:{grad};-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.9rem;">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

# ─── Row 1: Pie + Bar + Histogram ─────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
ch1, ch2, ch3 = st.columns(3)

# Category Pie
with ch1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🥧 Problem Categories</div>', unsafe_allow_html=True)
    if cat_dist:
        df_cat = pd.DataFrame(cat_dist)
        colors = [CATEGORY_COLORS.get(c, "#6366f1") for c in df_cat["category"]]
        fig = go.Figure(go.Pie(
            labels=df_cat["category"],
            values=df_cat["cnt"],
            hole=0.5,
            marker=dict(colors=colors, line=dict(color="#0d1321", width=2)),
            textinfo="percent+label",
            textfont=dict(size=10, color="#e8eaf6"),
            hovertemplate="<b>%{label}</b><br>%{value} reports (%{percent})<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280, showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data yet")
    st.markdown('</div>', unsafe_allow_html=True)

# Severity Bar
with ch2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Severity Distribution</div>', unsafe_allow_html=True)
    if sev_dist:
        df_sev = pd.DataFrame(sev_dist)
        # Ensure order HIGH > MEDIUM > LOW
        order = ["HIGH", "MEDIUM", "LOW"]
        df_sev["severity"] = pd.Categorical(df_sev["severity"], categories=order, ordered=True)
        df_sev = df_sev.sort_values("severity")
        colors = [SEVERITY_COLORS.get(s, "#6366f1") for s in df_sev["severity"]]
        fig = go.Figure(go.Bar(
            x=df_sev["severity"],
            y=df_sev["cnt"],
            marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)", width=0)),
            text=df_sev["cnt"],
            textposition="outside",
            textfont=dict(color="#e8eaf6", size=11),
            hovertemplate="<b>%{x}</b><br>%{y} reports<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280, bargap=0.3)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data yet")
    st.markdown('</div>', unsafe_allow_html=True)

# Priority Histogram
with ch3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Priority Distribution</div>', unsafe_allow_html=True)
    if priority_scores:
        fig = go.Figure(go.Histogram(
            x=priority_scores,
            nbinsx=10,
            marker=dict(
                color=priority_scores,
                colorscale=[[0, "#22c55e"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                cmin=0,
                cmax=100,
                line=dict(color="rgba(0,0,0,0)", width=0)
            ),
            hovertemplate="Score: %{x}<br>Count: %{y}<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=280,
                          xaxis_title="Priority Score", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data yet")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Row 2: Time Series + Map ─────────────────────────────────────────────────

ch4, ch5 = st.columns([1.2, 1])

# Reports over time
with ch4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Reports Over Time</div>', unsafe_allow_html=True)
    if time_data:
        df_time = pd.DataFrame(time_data)
        df_time["date"] = pd.to_datetime(df_time["date"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_time["date"],
            y=df_time["cnt"],
            mode="lines+markers",
            line=dict(color="#6366f1", width=2.5, shape="spline"),
            marker=dict(size=6, color="#a78bfa", line=dict(color="#fff", width=1)),
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.08)",
            hovertemplate="%{x|%d %b %Y}: %{y} reports<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=260, xaxis_title="Date", yaxis_title="Reports")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No time data yet")
    st.markdown('</div>', unsafe_allow_html=True)

# Location Map
with ch5:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🗺️ Location Heatmap</div>', unsafe_allow_html=True)
    if loc_data:
        df_loc = pd.DataFrame(loc_data)
        df_loc = df_loc[df_loc["latitude"] != 0]
        if not df_loc.empty:
            fig = px.scatter_mapbox(
                df_loc,
                lat="latitude",
                lon="longitude",
                color="severity",
                size="priority_score",
                size_max=20,
                hover_name="location_name",
                hover_data={"category": True, "priority_score": True, "severity": True, "latitude": False, "longitude": False},
                color_discrete_map=SEVERITY_COLORS,
                zoom=10,
                height=260
            )
            fig.update_layout(
                mapbox_style="carto-darkmatter",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(bgcolor="rgba(13,19,33,0.8)", font=dict(color="#9ca3af"))
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No location data with GPS coordinates")
    else:
        st.info("No location data yet")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Recent Reports Table ─────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

col_head, col_export = st.columns([2, 1])
with col_head:
    st.markdown('<div class="section-header">📋 Recent Reports</div>', unsafe_allow_html=True)

# Prepare table data
if all_reports:
    df = pd.DataFrame(all_reports)

    # CSV Export
    with col_export:
        csv_df = df[["id", "category", "severity", "priority_score", "location_name", "status", "duplicate_count", "created_at"]].copy()
        csv_data = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export CSV",
            data=csv_data,
            file_name=f"civiclens_reports_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Display table
    for report in all_reports[:20]:
        sev = report["severity"]
        badge_class = f"badge-{sev.lower()}"
        status = report["status"]
        status_class = "status-" + status.lower().replace(" ", "")
        score = report["priority_score"]
        score_color = "#ef4444" if score >= 80 else ("#f59e0b" if score >= 50 else "#22c55e")
        cat = report["category"]
        cat_icon = {"Road Damage": "🚧", "Garbage Overflow": "🗑️", "Broken Streetlight": "💡",
                    "Water Leakage": "💧", "Damaged Pavement": "🧱", "Open Drain": "🕳️",
                    "Broken Infrastructure": "🏗️"}.get(cat, "📍")
        demo_tag = '<span style="background:rgba(245,158,11,0.1);color:#fbbf24;border:1px solid rgba(245,158,11,0.25);border-radius:4px;padding:1px 5px;font-size:0.65rem;">DEMO</span>' if report.get("is_demo") else ""
        created = report["created_at"][:10] if report["created_at"] else ""

        with st.container():
            rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([0.5, 2.5, 1, 1, 1, 1])
            with rc1:
                st.markdown(f"<div style='font-size:1.4rem;padding-top:4px;'>{cat_icon}</div>", unsafe_allow_html=True)
            with rc2:
                st.markdown(f"""
                <div style="padding:2px 0;">
                    <div style="font-weight:600;color:#e8eaf6;font-size:0.88rem;">#{report['id']} {cat} {demo_tag}</div>
                    <div style="color:#6b7280;font-size:0.75rem;margin-top:1px;">📍 {report['location_name'][:45]}{'...' if len(report.get('location_name',''))>45 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
            with rc3:
                st.markdown(f"<div style='padding:4px 0;'><span class='{badge_class}'>{sev}</span></div>", unsafe_allow_html=True)
            with rc4:
                st.markdown(f"<div style='font-weight:700;color:{score_color};font-size:0.9rem;padding-top:4px;'>{score}/100</div>", unsafe_allow_html=True)
            with rc5:
                st.markdown(f"""<div style="padding:3px 0;">
                    <span style="background:rgba(255,255,255,0.05);color:#9ca3af;border-radius:20px;padding:2px 8px;font-size:0.72rem;">
                        {'Open' if status=='Open' else ('⏳ In Progress' if status=='In Progress' else '✅ Resolved')}
                    </span></div>""", unsafe_allow_html=True)
            with rc6:
                if st.button("View", key=f"view_{report['id']}", use_container_width=True):
                    st.session_state["selected_report_id"] = report["id"]
                    st.switch_page("pages/3_Report_Details.py")

        st.markdown("<hr style='border:none;height:1px;background:rgba(255,255,255,0.03);margin:2px 0;'>", unsafe_allow_html=True)

    if len(all_reports) > 20:
        st.markdown(f"<div style='text-align:center;color:#6b7280;font-size:0.8rem;padding:8px;'>Showing 20 of {len(all_reports)} reports. Use filters to narrow results.</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:48px;color:#4b5563;">
        <div style="font-size:3rem;">📭</div>
        <div style="font-size:1rem;font-weight:600;margin-top:12px;color:#6b7280;">No reports match your filters</div>
        <div style="font-size:0.8rem;color:#374151;margin-top:6px;">Try adjusting the filters in the sidebar</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Most Common Problem ──────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
info1, info2, info3 = st.columns(3)
with info1:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.05));border:1px solid rgba(99,102,241,0.2);border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;">🏆 Most Common Problem</div>
        <div style="font-weight:700;color:#a78bfa;font-size:1.1rem;margin-top:8px;">{stats['most_common']}</div>
    </div>""", unsafe_allow_html=True)
with info2:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(34,197,94,0.08),rgba(16,185,129,0.04));border:1px solid rgba(34,197,94,0.2);border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;">✅ Resolved Issues</div>
        <div style="font-weight:700;color:#4ade80;font-size:1.1rem;margin-top:8px;">{stats['resolved']}/{stats['total']}</div>
    </div>""", unsafe_allow_html=True)
with info3:
    resolution_rate = round((stats["resolved"] / stats["total"] * 100) if stats["total"] > 0 else 0, 1)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(96,165,250,0.08),rgba(59,130,246,0.04));border:1px solid rgba(96,165,250,0.2);border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;">📈 Resolution Rate</div>
        <div style="font-weight:700;color:#60a5fa;font-size:1.1rem;margin-top:8px;">{resolution_rate}%</div>
    </div>""", unsafe_allow_html=True)

"""
CivicLens AI - Report Details Page
Full report view with image, priority breakdown, status update, and PDF export.
"""

import streamlit as st
import sys
import os
import io
import json
from datetime import datetime
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import get_report_by_id, get_all_reports, update_report_status
from priority_engine import get_score_label, get_score_breakdown_text
from ai_analyzer import CATEGORIES

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Report Details — CivicLens AI",
    page_icon="🔍",
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
.cl-card { background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); border: 1px solid rgba(99,102,241,0.2); border-radius: 16px; padding: 24px; margin: 8px 0; }
.detail-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.detail-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
.detail-value { font-size: 0.9rem; color: #e8eaf6; font-weight: 600; }
.badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.badge-low    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.stButton > button { border-radius: 10px !important; font-weight: 600 !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(99,102,241,0.2) !important; border-radius: 8px !important; color: #e8eaf6 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

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

    # Report selector
    st.markdown("### 📋 Select Report")
    all_reports = get_all_reports()
    if all_reports:
        report_options = {f"#{r['id']} — {r['category']} ({r['severity']})": r["id"] for r in all_reports}
        selected_label = st.selectbox("Choose a report", list(report_options.keys()), label_visibility="collapsed")
        if st.button("Load Report", use_container_width=True, type="primary"):
            st.session_state["selected_report_id"] = report_options[selected_label]
            st.rerun()

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="padding:16px 0 8px;">
    <div style="font-size:2rem;font-weight:900;background:linear-gradient(135deg,#fff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        🔍 Report Details
    </div>
    <div style="color:#6b7280;font-size:0.9rem;">Full civic report view with AI analysis and priority breakdown</div>
</div>
<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);margin:8px 0 20px;">
""", unsafe_allow_html=True)

# ─── Load Report ──────────────────────────────────────────────────────────────

report_id = st.session_state.get("selected_report_id")

if not report_id:
    # Default to latest report
    if all_reports:
        report_id = all_reports[0]["id"]
    else:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px;color:#6b7280;">
            <div style="font-size:4rem;">📭</div>
            <div style="font-size:1.2rem;font-weight:600;margin-top:16px;">No Reports Found</div>
            <div style="font-size:0.9rem;margin-top:8px;">Submit your first civic report to see details here.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📸 Submit First Report", type="primary"):
            st.switch_page("pages/1_Report_Problem.py")
        st.stop()

report = get_report_by_id(report_id)

if not report:
    st.error(f"Report #{report_id} not found.")
    st.stop()

# ─── Parse breakdown ──────────────────────────────────────────────────────────

try:
    breakdown = json.loads(report.get("priority_breakdown") or "{}")
except Exception:
    breakdown = {}

score = report["priority_score"]
score_label, score_color = get_score_label(score)
severity = report["severity"]
category = report["category"]
cat_meta = CATEGORIES.get(category, {"icon": "📍", "color": "#6366f1"})
tags = [t.strip() for t in (report.get("tags") or "").split(",") if t.strip()]
demo_label = " · [DEMO DATA]" if report.get("is_demo") else ""

# ─── Report Header Banner ──────────────────────────────────────────────────────

sev_badge = {
    "HIGH": "🔴 HIGH",
    "MEDIUM": "🟡 MEDIUM",
    "LOW": "🟢 LOW"
}.get(severity, severity)
sev_color = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#22c55e"}.get(severity, "#6366f1")

st.markdown(f"""
<div style="background:linear-gradient(135deg,{cat_meta['color']}18,{cat_meta['color']}06);
            border:1px solid {cat_meta['color']}30;border-radius:16px;padding:20px 24px;margin-bottom:16px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div style="display:flex;align-items:center;gap:14px;">
            <span style="font-size:2.8rem;">{cat_meta['icon']}</span>
            <div>
                <div style="font-size:1.6rem;font-weight:800;color:#e8eaf6;">{category}</div>
                <div style="font-size:0.8rem;color:#6b7280;margin-top:3px;">
                    Report #{report['id']}{demo_label} · 📍 {report['location_name']} · 🕐 {report['created_at'][:16]}
                </div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="text-align:center;">
                <div style="font-size:0.65rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">Severity</div>
                <div style="font-weight:700;color:{sev_color};font-size:0.95rem;margin-top:2px;">{sev_badge}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:0.65rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">Status</div>
                <div style="font-weight:700;color:#a78bfa;font-size:0.9rem;margin-top:2px;">{report['status']}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:0.65rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">Priority</div>
                <div style="font-weight:800;color:{score_color};font-size:1.3rem;margin-top:2px;">{score}/100</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Main Content ─────────────────────────────────────────────────────────────

col_left, col_right = st.columns([1.5, 1])

with col_left:
    # Image Display
    img_path = report.get("image_path", "")
    if img_path and os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, caption=f"📷 {category} — {report['location_name']}", use_container_width=True)
    else:
        # Placeholder for demo images
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{cat_meta['color']}12,{cat_meta['color']}05);
                    border:2px dashed {cat_meta['color']}40;border-radius:12px;
                    height:280px;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;text-align:center;">
            <div style="font-size:4rem;">{cat_meta['icon']}</div>
            <div style="color:#6b7280;font-size:0.85rem;margin-top:12px;">{category}</div>
            <div style="color:#374151;font-size:0.75rem;margin-top:4px;">Image stored at: {img_path or 'N/A'}</div>
        </div>""", unsafe_allow_html=True)

    # Description
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="cl-card">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:10px;">✏️ Description</div>
        <div style="font-size:0.9rem;color:#d1d5db;line-height:1.7;">{report.get('description','No description provided.')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Tags
    if tags:
        tag_html = " ".join([
            f"<span style='background:rgba(99,102,241,0.12);color:#a78bfa;border:1px solid rgba(99,102,241,0.25);border-radius:20px;padding:3px 10px;font-size:0.75rem;margin:2px;display:inline-block;'>#{t}</span>"
            for t in tags
        ])
        st.markdown(f"""
        <div class="cl-card" style="padding:16px 20px;">
            <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;font-weight:700;margin-bottom:8px;">🏷️ Tags</div>
            <div>{tag_html}</div>
        </div>""", unsafe_allow_html=True)

    # Recommended Action
    st.markdown(f"""
    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:12px;padding:16px 20px;margin:8px 0;">
        <div style="font-size:0.72rem;color:#fbbf24;text-transform:uppercase;font-weight:700;letter-spacing:0.08em;margin-bottom:8px;">⚡ Recommended Action</div>
        <div style="font-size:0.9rem;color:#e8eaf6;line-height:1.6;">{report.get('recommended_action','No recommendation available.')}</div>
    </div>""", unsafe_allow_html=True)

with col_right:
    # Priority Score Ring
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{score_color}15,{score_color}05);border:1px solid {score_color}35;
                border-radius:16px;padding:24px;text-align:center;margin-bottom:12px;">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">🎯 Civic Priority Score</div>
        <div style="position:relative;width:130px;height:130px;border-radius:50%;border:6px solid {score_color};
                    margin:0 auto 16px;background:radial-gradient({score_color}20,transparent);
                    display:flex;align-items:center;justify-content:center;flex-direction:column;">
            <div style="font-size:2.5rem;font-weight:900;color:{score_color};line-height:1;">{score}</div>
            <div style="font-size:0.65rem;color:#6b7280;">out of 100</div>
        </div>
        <div style="font-weight:700;color:{score_color};font-size:1rem;">{score_label}</div>
    </div>
    """, unsafe_allow_html=True)

    # Score Breakdown
    st.markdown(f"""
    <div class="cl-card" style="padding:18px 20px;">
        <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;font-weight:700;letter-spacing:0.08em;margin-bottom:14px;">📊 Score Breakdown</div>
    """, unsafe_allow_html=True)

    breakdown_items = [
        ("Severity Weight", breakdown.get("severity_weight", 0), "#ef4444", 40),
        ("Duplicate Bonus", breakdown.get("duplicate_bonus", 0), "#f59e0b", 20),
        ("Category Risk", breakdown.get("category_risk", 0), "#a78bfa", 15),
        ("Safety Risk", breakdown.get("safety_risk", 0), "#60a5fa", 15),
        ("Location Importance", breakdown.get("location_importance", 0), "#34d399", 10),
    ]
    for name, pts, color, max_pts in breakdown_items:
        pct = (pts / max_pts * 100) if max_pts > 0 else 0
        st.markdown(f"""
        <div style="margin:8px 0;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:0.78rem;color:#9ca3af;">{name}</span>
                <span style="font-size:0.78rem;color:{color};font-weight:700;">{pts}/{max_pts}</span>
            </div>
            <div style="background:rgba(255,255,255,0.04);border-radius:4px;height:7px;">
                <div style="background:{color};width:{pct}%;height:7px;border-radius:4px;transition:width 0.5s;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="border-top:1px solid rgba(255,255,255,0.06);margin-top:12px;padding-top:12px;display:flex;justify-content:space-between;align-items:center;">
            <span style="font-weight:700;color:#e8eaf6;font-size:0.9rem;">Total Score</span>
            <span style="font-weight:800;color:{score_color};font-size:1.1rem;">{score}/100</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Report Details
    detail_rows = [
        ("Report ID", f"#{report['id']}"),
        ("Category", category),
        ("Severity", severity),
        ("Confidence", f"{report.get('confidence', 0)*100:.0f}%"),
        ("Duplicates", str(report.get("duplicate_count", 0))),
        ("Status", report["status"]),
        ("Latitude", str(report.get("latitude", "N/A"))),
        ("Longitude", str(report.get("longitude", "N/A"))),
        ("Submitted", report.get("created_at", "")[:16]),
        ("Last Updated", report.get("updated_at", "")[:16]),
    ]

    st.markdown('<div class="cl-card" style="padding:16px 20px;margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;font-weight:700;letter-spacing:0.08em;margin-bottom:12px;">📋 Report Info</div>', unsafe_allow_html=True)
    for label, value in detail_rows:
        st.markdown(f"""
        <div class="detail-row">
            <span class="detail-label">{label}</span>
            <span class="detail-value">{value}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Status Update ────────────────────────────────────────────────────────────

st.markdown("<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);margin:20px 0;'>", unsafe_allow_html=True)

st.markdown("### ⚙️ Update Report Status")
upd1, upd2, upd3 = st.columns([1.5, 1, 2])
with upd1:
    new_status = st.selectbox(
        "New Status",
        ["Open", "In Progress", "Resolved"],
        index=["Open", "In Progress", "Resolved"].index(report["status"]) if report["status"] in ["Open", "In Progress", "Resolved"] else 0,
        label_visibility="collapsed"
    )
with upd2:
    if st.button("✅ Update Status", use_container_width=True, type="primary"):
        update_report_status(report_id, new_status)
        st.success(f"Status updated to **{new_status}**")
        st.rerun()

# ─── PDF Export ───────────────────────────────────────────────────────────────

st.markdown("### 📄 Export Report")
pdf_col, csv_col, _ = st.columns([1, 1, 2])

def generate_pdf_report(report: dict, breakdown: dict) -> bytes:
    """Generate a PDF report using ReportLab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor, white, black
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.enums import TA_LEFT, TA_CENTER

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # Colors
        PRIMARY = HexColor("#6366f1")
        DARK    = HexColor("#0d1321")
        LIGHT   = HexColor("#e8eaf6")
        GRAY    = HexColor("#6b7280")
        sev_colors = {"HIGH": HexColor("#ef4444"), "MEDIUM": HexColor("#f59e0b"), "LOW": HexColor("#22c55e")}
        sev_color = sev_colors.get(report["severity"], PRIMARY)

        # Title
        story.append(Paragraph(
            "🏙️ CivicLens AI — Civic Problem Report",
            ParagraphStyle("title", parent=styles["Heading1"], fontSize=18, textColor=PRIMARY, alignment=TA_CENTER)
        ))
        story.append(Spacer(1, 0.3*cm))
        story.append(HRFlowable(color=PRIMARY, thickness=2))
        story.append(Spacer(1, 0.5*cm))

        # Report Header
        story.append(Paragraph(
            f"Report #{report['id']} — {report['category']}",
            ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14, textColor=DARK)
        ))
        story.append(Spacer(1, 0.3*cm))

        # Main table
        details_data = [
            ["Field", "Value"],
            ["Category", report["category"]],
            ["Severity", report["severity"]],
            ["Priority Score", f"{report['priority_score']} / 100"],
            ["Location", report.get("location_name", "N/A")],
            ["Latitude / Longitude", f"{report.get('latitude', 0):.4f}, {report.get('longitude', 0):.4f}"],
            ["Duplicate Reports", str(report.get("duplicate_count", 0))],
            ["Status", report["status"]],
            ["AI Confidence", f"{report.get('confidence', 0)*100:.0f}%"],
            ["Submitted", report.get("created_at", "")[:16]],
            ["Last Updated", report.get("updated_at", "")[:16]],
        ]

        table = Table(details_data, colWidths=[6*cm, 11*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), PRIMARY),
            ("TEXTCOLOR", (0,0), (-1,0), white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 11),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [HexColor("#f8f9ff"), white]),
            ("GRID", (0,0), (-1,-1), 0.5, HexColor("#d1d5db")),
            ("FONTSIZE", (0,1), (-1,-1), 10),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("PADDING", (0,0), (-1,-1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.5*cm))

        # Score Breakdown
        story.append(Paragraph("🎯 Priority Score Breakdown", ParagraphStyle("h3", parent=styles["Heading3"], fontSize=12, textColor=PRIMARY)))
        story.append(Paragraph(get_score_breakdown_text(breakdown), ParagraphStyle("code", parent=styles["Normal"], fontName="Courier", fontSize=9)))
        story.append(Spacer(1, 0.3*cm))

        # Description
        story.append(Paragraph("✏️ Description", ParagraphStyle("h3", parent=styles["Heading3"], fontSize=12, textColor=PRIMARY)))
        story.append(Paragraph(report.get("description", "No description."), styles["Normal"]))
        story.append(Spacer(1, 0.3*cm))

        # Recommended Action
        story.append(Paragraph("⚡ Recommended Action", ParagraphStyle("h3", parent=styles["Heading3"], fontSize=12, textColor=PRIMARY)))
        story.append(Paragraph(report.get("recommended_action", "N/A"), styles["Normal"]))
        story.append(Spacer(1, 0.5*cm))

        # Footer
        story.append(HRFlowable(color=GRAY, thickness=0.5))
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            f"Generated by CivicLens AI · {datetime.now().strftime('%d %b %Y %I:%M %p')} · Hackathon Demo v1.0",
            ParagraphStyle("footer", parent=styles["Normal"], fontSize=8, textColor=GRAY, alignment=TA_CENTER)
        ))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    except ImportError:
        return None


with pdf_col:
    pdf_bytes = generate_pdf_report(report, breakdown)
    if pdf_bytes:
        st.download_button(
            "📄 Download PDF Report",
            data=pdf_bytes,
            file_name=f"civiclens_report_{report['id']}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("Install `reportlab` to enable PDF export: `pip install reportlab`")

with csv_col:
    import csv
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Field", "Value"])
    for key, val in report.items():
        writer.writerow([key, val])
    st.download_button(
        "📊 Download CSV",
        data=csv_buffer.getvalue().encode("utf-8"),
        file_name=f"civiclens_report_{report['id']}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ─── Navigation ───────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
nb1, nb2, nb3 = st.columns(3)
with nb1:
    if st.button("◀ Back to Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
with nb2:
    if st.button("📸 Submit New Report", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Report_Problem.py")
with nb3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

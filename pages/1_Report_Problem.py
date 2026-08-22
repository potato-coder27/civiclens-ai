"""
CivicLens AI - Report Problem Page
Users upload or capture an image of a civic problem.
AI analyzes it and generates a structured report.
"""

import streamlit as st
import sys
import os
import io
import json
import uuid
from datetime import datetime
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import insert_report
from ai_analyzer import analyze_image, CATEGORIES
from priority_engine import calculate_priority_score, get_score_label, get_score_breakdown_text
from duplicate_detector import find_duplicates

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Report a Problem — CivicLens AI",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Shared CSS (imported via app.py session, or re-inject a minimal set) ────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1321 50%, #0a0e1a 100%); color: #e8eaf6; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1321 0%, #111827 100%); border-right: 1px solid rgba(99,102,241,0.2); }
.cl-card { background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); border: 1px solid rgba(99,102,241,0.2); border-radius: 16px; padding: 24px; margin: 8px 0; }
.result-card { border-radius: 16px; padding: 20px 24px; margin: 8px 0; border: 1px solid; }
.cl-divider { border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent); margin: 20px 0; }
.badge-high   { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3);  border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.badge-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.badge-low    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3);  border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: 700; }
.stButton > button { border-radius: 10px !important; font-weight: 600 !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important; color: #e8eaf6 !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1321; }
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
    st.markdown("""
    <div style="font-size:0.78rem;color:#6b7280;line-height:1.6;">
    📸 Upload or capture a photo of a civic problem.<br><br>
    Our AI will analyze it and generate a structured report with priority score.
    </div>""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="padding:20px 0 8px;">
    <div style="font-size:2rem;font-weight:900;background:linear-gradient(135deg,#fff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        📸 Report a Civic Problem
    </div>
    <div style="color:#6b7280;font-size:0.95rem;margin-top:4px;">
        Upload a photo → AI analyzes → Structured report generated instantly
    </div>
</div>
<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);margin:12px 0 24px;">
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "submitted_report_id" not in st.session_state:
    st.session_state.submitted_report_id = None
if "form_image_bytes" not in st.session_state:
    st.session_state.form_image_bytes = None

# ─── Form ─────────────────────────────────────────────────────────────────────

if st.session_state.analysis_result is None:
    col_form, col_tip = st.columns([1.6, 1])

    with col_form:
        st.markdown("""
        <div class="cl-card">
            <h3 style="margin:0 0 20px;color:#e8eaf6;font-weight:700;">📋 Submit Report</h3>
        """, unsafe_allow_html=True)

        # Image Upload
        st.markdown("**🖼️ Upload Problem Image**")
        tab_upload, tab_camera = st.tabs(["📂 Upload File", "📷 Camera"])

        uploaded_file = None
        camera_image = None

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Drag & drop or browse",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                help="Supported formats: JPG, PNG, WEBP, BMP. Max 10MB.",
                label_visibility="collapsed"
            )

        with tab_camera:
            camera_image = st.camera_input(
                "Take a photo",
                help="Allow camera access to capture a live photo.",
                label_visibility="collapsed"
            )

        image_source = uploaded_file or camera_image
        image_bytes = None
        filename = ""

        if image_source:
            image_bytes = image_source.read()
            filename = getattr(image_source, "name", "captured_image.jpg")
            img = Image.open(io.BytesIO(image_bytes))
            st.image(img, caption="📷 Uploaded Image", use_container_width=True)
            st.markdown(f"<div style='font-size:0.75rem;color:#6b7280;'>File: {filename} · {len(image_bytes)//1024}KB · {img.width}×{img.height}px</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Location
        st.markdown("**📍 Location Details**")
        col_loc, col_coord = st.columns([1.5, 1])
        with col_loc:
            location_name = st.text_input(
                "Location Name",
                placeholder="e.g. Near College Campus, MG Road",
                help="Enter the nearest landmark or address",
                label_visibility="collapsed"
            )
        with col_coord:
            lat_input = st.text_input("Latitude (optional)", placeholder="28.6139", label_visibility="visible")
            lng_input = st.text_input("Longitude (optional)", placeholder="77.2090", label_visibility="visible")

        # Description
        st.markdown("**✏️ Problem Description**")
        description = st.text_area(
            "Describe the problem",
            placeholder="Describe the civic problem in detail. Include severity, duration, and any immediate safety concerns...",
            height=120,
            label_visibility="collapsed"
        )

        # Category override
        st.markdown("**🏷️ Category Hint** *(optional — helps AI accuracy)*")
        category_hint = st.selectbox(
            "Category",
            ["Let AI decide"] + list(CATEGORIES.keys()),
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit
        submit_col, _ = st.columns([1, 1])
        with submit_col:
            submit_btn = st.button(
                "🚀  Analyze & Submit Report",
                use_container_width=True,
                type="primary",
                disabled=(image_source is None)
            )

        if image_source is None:
            st.markdown("<div style='font-size:0.8rem;color:#6b7280;'>⬆️ Please upload or capture an image to proceed.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_tip:
        st.markdown("""
        <div class="cl-card" style="margin-top:0;">
            <h4 style="color:#a78bfa;font-weight:700;margin-bottom:16px;">💡 Tips for Better Results</h4>
            <div style="font-size:0.85rem;color:#9ca3af;line-height:1.8;">
                📸 <strong style="color:#e8eaf6;">Clear Photo</strong><br>
                Capture the problem clearly, avoid blur<br><br>
                💡 <strong style="color:#e8eaf6;">Good Lighting</strong><br>
                Daylight photos give better AI accuracy<br><br>
                📍 <strong style="color:#e8eaf6;">Exact Location</strong><br>
                Include nearest landmark in location<br><br>
                ✏️ <strong style="color:#e8eaf6;">Detailed Description</strong><br>
                Mention urgency, duration, hazards<br><br>
                🏷️ <strong style="color:#e8eaf6;">Category Hint</strong><br>
                Select category if you already know it
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="cl-card" style="margin-top:8px;">
            <h4 style="color:#a78bfa;font-weight:700;margin-bottom:12px;">⚡ AI Pipeline</h4>
            <div style="font-size:0.8rem;color:#6b7280;line-height:2;">
                1. 🖼️ Image uploaded<br>
                2. 🧠 Vision AI analyzes<br>
                3. 🏷️ Category detected<br>
                4. ⚠️ Severity estimated<br>
                5. 📍 Location attached<br>
                6. 🔍 Duplicates checked<br>
                7. 🎯 Priority calculated<br>
                8. 💾 Report stored<br>
                9. 📊 Dashboard updated
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ─── Analysis Logic ───────────────────────────────────────────────────────

    if submit_btn and image_source:
        # Validate
        if not location_name.strip():
            st.warning("⚠️ Please enter a location name for the report.")
            st.stop()

        # Parse coordinates
        try:
            lat = float(lat_input.strip()) if lat_input.strip() else 28.6139 + (hash(location_name) % 100) * 0.001
            lng = float(lng_input.strip()) if lng_input.strip() else 77.2090 + (hash(location_name) % 100) * 0.001
        except ValueError:
            st.error("❌ Invalid latitude/longitude format.")
            st.stop()

        # AI Analysis
        with st.spinner(""):
            progress_placeholder = st.empty()
            progress_placeholder.markdown("""
            <div style="text-align:center;padding:40px;background:rgba(99,102,241,0.05);border-radius:16px;border:1px solid rgba(99,102,241,0.2);">
                <div style="font-size:2rem;margin-bottom:12px;">🧠</div>
                <div style="font-size:1.1rem;font-weight:700;color:#a78bfa;">AI Analyzing Image...</div>
                <div style="font-size:0.85rem;color:#6b7280;margin-top:8px;">
                    Running vision pipeline · Detecting problem · Estimating severity
                </div>
            </div>
            """, unsafe_allow_html=True)

            ai_result = analyze_image(image_bytes, description, filename)

            # Override category if user hinted
            if category_hint != "Let AI decide":
                ai_result["category"] = category_hint

            # Duplicate detection
            dup_result = find_duplicates(ai_result["category"], lat, lng)

            # Priority score
            score, breakdown = calculate_priority_score(
                severity=ai_result["severity"],
                category=ai_result["category"],
                duplicate_count=dup_result["duplicate_count"],
                location_name=location_name,
                latitude=lat,
                longitude=lng
            )

            # Save image
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
            os.makedirs(images_dir, exist_ok=True)
            img_filename = f"{uuid.uuid4().hex[:8]}_{filename.replace(' ', '_')}"
            img_path = os.path.join(images_dir, img_filename)
            with open(img_path, "wb") as f:
                f.write(image_bytes)

            # Store in DB
            report_data = {
                "image_path": img_path,
                "category": ai_result["category"],
                "severity": ai_result["severity"],
                "description": description,
                "location_name": location_name,
                "latitude": lat,
                "longitude": lng,
                "priority_score": score,
                "priority_breakdown": breakdown,
                "duplicate_count": dup_result["duplicate_count"],
                "status": "Open",
                "confidence": ai_result["confidence"],
                "tags": ai_result["tags"],
                "recommended_action": ai_result["recommended_action"]
            }
            report_id = insert_report(report_data)

            progress_placeholder.empty()

            # Store result in session
            st.session_state.analysis_result = {
                "report_id": report_id,
                "ai": ai_result,
                "dup": dup_result,
                "score": score,
                "breakdown": breakdown,
                "location_name": location_name,
                "description": description,
                "image_bytes": image_bytes
            }
            st.rerun()

# ─── Analysis Result ──────────────────────────────────────────────────────────

else:
    result = st.session_state.analysis_result
    ai = result["ai"]
    dup = result["dup"]
    score = result["score"]
    breakdown = result["breakdown"]
    category = ai["category"]
    severity = ai["severity"]
    cat_meta = CATEGORIES.get(category, {})
    score_label, score_color = get_score_label(score)
    report_id = result["report_id"]

    # Success banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(34,197,94,0.15),rgba(16,185,129,0.08));
                border:1px solid rgba(34,197,94,0.3);border-radius:16px;padding:20px 24px;margin-bottom:20px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.6rem;">✅</span>
            <div>
                <div style="font-weight:700;color:#4ade80;font-size:1.1rem;">Report Submitted Successfully!</div>
                <div style="color:#6b7280;font-size:0.85rem;">Report ID: <strong style="color:#a78bfa;">#{report_id}</strong> · {datetime.now().strftime('%d %b %Y, %I:%M %p')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_score = st.columns([2, 1])

    with col_main:
        # AI Result Card
        severity_badge = {
            "HIGH": '<span class="badge-high">⬆ HIGH</span>',
            "MEDIUM": '<span class="badge-medium">➡ MEDIUM</span>',
            "LOW": '<span class="badge-low">⬇ LOW</span>'
        }.get(severity, severity)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{cat_meta.get('color','#6366f1')}20,{cat_meta.get('color','#6366f1')}08);
                    border:1px solid {cat_meta.get('color','#6366f1')}40;border-radius:16px;padding:24px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <span style="font-size:2.4rem;">{cat_meta.get('icon','🏗️')}</span>
                <div>
                    <div style="font-size:1.4rem;font-weight:800;color:#e8eaf6;">{category}</div>
                    <div style="margin-top:4px;">{severity_badge}
                        &nbsp;<span style="font-size:0.78rem;color:#6b7280;">Confidence: {ai['confidence']*100:.0f}%</span>
                    </div>
                </div>
            </div>
            <hr style="border:none;height:1px;background:rgba(255,255,255,0.05);margin:16px 0;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div>
                    <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">📍 Location</div>
                    <div style="font-weight:600;color:#e8eaf6;font-size:0.9rem;margin-top:2px;">{result['location_name']}</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">🔍 Possible Duplicates</div>
                    <div style="font-weight:600;color:{'#f87171' if dup['duplicate_count']>0 else '#4ade80'};font-size:0.9rem;margin-top:2px;">
                        {dup['duplicate_count']} related report{'s' if dup['duplicate_count']!=1 else ''}
                    </div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">🏷️ Tags</div>
                    <div style="font-size:0.8rem;color:#a78bfa;margin-top:2px;">{ai['tags']}</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">📅 Submitted</div>
                    <div style="font-weight:600;color:#e8eaf6;font-size:0.85rem;margin-top:2px;">{datetime.now().strftime('%d %b %Y, %I:%M %p')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recommended Action
        st.markdown(f"""
        <div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:12px;padding:16px 20px;margin-top:12px;">
            <div style="font-size:0.72rem;color:#fbbf24;text-transform:uppercase;font-weight:700;letter-spacing:0.08em;margin-bottom:8px;">⚡ Recommended Action</div>
            <div style="font-size:0.9rem;color:#e8eaf6;line-height:1.6;">{ai['recommended_action']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Duplicate notice
        if dup["is_duplicate"]:
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:12px;padding:14px 18px;margin-top:10px;">
                <div style="font-size:0.88rem;color:#f87171;">{dup['message']}</div>
                <div style="font-size:0.78rem;color:#6b7280;margin-top:4px;">Related Report IDs: {', '.join(['#'+str(i) for i in dup['related_ids'][:5]])}</div>
            </div>
            """, unsafe_allow_html=True)

        # Display image
        if result.get("image_bytes"):
            st.markdown("<br>", unsafe_allow_html=True)
            img = Image.open(io.BytesIO(result["image_bytes"]))
            st.image(img, caption="📷 Submitted Image", use_container_width=True)

    with col_score:
        # Priority Score Ring
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{score_color}20,{score_color}08);border:1px solid {score_color}40;
                    border-radius:16px;padding:24px;text-align:center;margin-bottom:12px;">
            <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">🎯 Civic Priority Score</div>
            <div style="width:120px;height:120px;border-radius:50%;border:5px solid {score_color};display:flex;
                        align-items:center;justify-content:center;margin:0 auto 16px;
                        background:radial-gradient({score_color}20,transparent);">
                <div>
                    <div style="font-size:2.2rem;font-weight:900;color:{score_color};">{score}</div>
                    <div style="font-size:0.65rem;color:#6b7280;">/ 100</div>
                </div>
            </div>
            <div style="font-weight:700;color:{score_color};font-size:0.9rem;">{score_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Score Breakdown
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:16px;">
            <div style="font-size:0.72rem;color:#6b7280;text-transform:uppercase;font-weight:700;letter-spacing:0.08em;margin-bottom:12px;">📊 Score Breakdown</div>
        """, unsafe_allow_html=True)

        breakdown_items = [
            ("Severity Weight", breakdown.get("severity_weight", 0), "#ef4444", 40),
            ("Duplicate Bonus", breakdown.get("duplicate_bonus", 0), "#f59e0b", 20),
            ("Category Risk", breakdown.get("category_risk", 0), "#a78bfa", 15),
            ("Safety Risk", breakdown.get("safety_risk", 0), "#60a5fa", 15),
            ("Location", breakdown.get("location_importance", 0), "#34d399", 10),
        ]
        for name, pts, color, max_pts in breakdown_items:
            pct = (pts / max_pts) * 100 if max_pts > 0 else 0
            st.markdown(f"""
            <div style="margin:8px 0;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="font-size:0.75rem;color:#9ca3af;">{name}</span>
                    <span style="font-size:0.75rem;color:{color};font-weight:600;">{pts}/{max_pts}</span>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:3px;height:5px;">
                    <div style="background:{color};width:{pct}%;height:5px;border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="border-top:1px solid rgba(255,255,255,0.05);margin-top:10px;padding-top:10px;display:flex;justify-content:space-between;">
                <span style="font-size:0.8rem;font-weight:700;color:#e8eaf6;">Total</span>
                <span style="font-size:0.8rem;font-weight:800;color:{score_color};">{score}/100</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI Info
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(99,102,241,0.1);border-radius:10px;padding:12px;margin-top:10px;">
            <div style="font-size:0.7rem;color:#4b5563;">🤖 {ai.get('analysis_method','CivicLens AI')}</div>
            <div style="font-size:0.7rem;color:#4b5563;margin-top:2px;">Confidence: {ai['confidence']*100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── Action Buttons ───────────────────────────────────────────────────────

    st.markdown("<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);margin:20px 0;'>", unsafe_allow_html=True)

    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
    with btn2:
        if st.button("🔍 View Full Report", use_container_width=True):
            st.session_state["selected_report_id"] = report_id
            st.switch_page("pages/3_Report_Details.py")
    with btn3:
        if st.button("📸 Submit Another Report", use_container_width=True, type="primary"):
            st.session_state.analysis_result = None
            st.session_state.form_image_bytes = None
            st.rerun()

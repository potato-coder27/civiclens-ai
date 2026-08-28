# 🏙️ CivicLens AI

> **AI-Powered Civic Problem Detection & Reporting Platform**
> Built for Hackathon 2026 · Python · Streamlit · SQLite · Plotly

---

## 🚀 What is CivicLens AI?

CivicLens AI transforms citizen-uploaded photos of civic problems — potholes, garbage, broken streetlights, water leakage — into **structured, prioritized government reports** using AI-powered computer vision and an intelligent scoring system.

### Key Features
- 📸 **Photo Upload & Camera Capture** — Upload or take live photos
- 🧠 **AI Vision Analysis** — Detects problem category, severity, and generates tags
- 🎯 **Transparent Priority Score** — 0–100 score with full breakdown (no black box)
- 🔍 **Duplicate Detection** — Haversine GPS-based proximity matching
- 📊 **Interactive Dashboard** — Charts, maps, filters, and real-time stats
- 📄 **PDF/CSV Export** — Download full reports
- ⚡ **Demo Mode** — 7 pre-seeded sample reports for instant demonstration

---

## 📁 Project Structure

```
civiclens-ai/
│
├── app.py                      # Home page (entry point)
├── database.py                 # SQLite CRUD + demo data seeder
├── ai_analyzer.py              # Mock AI vision pipeline
├── priority_engine.py          # Priority Score calculator
├── duplicate_detector.py       # Haversine duplicate detection
├── requirements.txt
├── README.md
│
├── data/
│   └── civiclens.db            # Auto-created SQLite database
│   └── uploads/                # User-uploaded images
│
├── assets/
│   └── sample_images/          # Demo sample images
│
└── pages/
    ├── 1_Report_Problem.py     # Report submission + AI result
    ├── 2_Dashboard.py          # Admin analytics dashboard
    └── 3_Report_Details.py     # Full report view + PDF export
```

---

## ⚡ Quick Start

### 1. Clone / Download

```bash
git clone https://github.com/your-username/civiclens-ai.git
cd civiclens-ai
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and select **Create app**.
3. Choose the repository and branch, then set **Main file path** to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.

This project does not require API keys. Its SQLite database and uploaded images use the app filesystem, so user-created data is temporary and can be reset when the app is redeployed or restarted. The seven demo reports are seeded automatically on a fresh instance.

### Open on another device on the same Wi-Fi

1. Start the app on the host computer with `streamlit run app.py`.
2. Find the host computer's Wi-Fi IPv4 address with `ipconfig`.
3. On the other device, open `http://<HOST-IP>:8501`.

For example, if the host IP is `192.168.30.240`, open **http://192.168.30.240:8501**. Both devices must be connected to the same Wi-Fi network. If Windows Firewall blocks the connection, allow inbound TCP port `8501` for Private networks:

```powershell
New-NetFirewallRule -DisplayName "CivicLens Streamlit 8501" -Direction Inbound -Protocol TCP -LocalPort 8501 -Action Allow -Profile Private
```

---

## 🔑 API Keys

**None required!** CivicLens AI runs completely offline with the mock AI pipeline.

| Feature | Status |
|---------|--------|
| AI Analysis | ✅ Mock AI (no key needed) |
| Database | ✅ SQLite (local) |
| Charts | ✅ Plotly (local) |
| Maps | ✅ Plotly Mapbox (free tile) |
| PDF Export | ✅ ReportLab (local) |

### Optional: Enable Real AI (Future)

To plug in Google Cloud Vision:
1. Get API key from [Google Cloud Console](https://console.cloud.google.com)
2. Set environment variable: `export GOOGLE_APPLICATION_CREDENTIALS=key.json`
3. Uncomment `_google_vision_classify()` in `ai_analyzer.py`

---

## 🎯 Priority Score Formula

```
Score = Severity Weight (max 40)
      + Duplicate Bonus  (max 20)  ← 5 pts per duplicate
      + Category Risk    (max 15)
      + Safety Risk      (max 15)
      + Location Importance (max 10)
      ─────────────────────────────
      TOTAL              (max 100)
```

Every point is explained — no random numbers!

---

## 🗄️ Database Schema

**`reports` table:**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment report ID |
| image_path | TEXT | Path to uploaded image |
| category | TEXT | Detected problem category |
| severity | TEXT | HIGH / MEDIUM / LOW |
| description | TEXT | User-provided description |
| location_name | TEXT | Landmark / address |
| latitude | REAL | GPS latitude |
| longitude | REAL | GPS longitude |
| priority_score | INTEGER | 0–100 score |
| priority_breakdown | TEXT | JSON breakdown |
| duplicate_count | INTEGER | Number of similar reports |
| status | TEXT | Open / In Progress / Resolved |
| confidence | REAL | AI confidence (0–1) |
| tags | TEXT | Comma-separated tags |
| recommended_action | TEXT | AI action recommendation |
| is_demo | INTEGER | 1 if demo data |
| created_at | TEXT | Timestamp |
| updated_at | TEXT | Last update timestamp |

---

## 📊 Demo Data

7 pre-seeded reports are loaded automatically on first run:

| Problem | Severity | Score | Status |
|---------|----------|-------|--------|
| Road Damage | HIGH | 92/100 | Open |
| Garbage Overflow | MEDIUM | 58/100 | In Progress |
| Broken Streetlight | MEDIUM | 61/100 | Open |
| Water Leakage | HIGH | 84/100 | Resolved |
| Damaged Pavement | LOW | 27/100 | Open |
| Open Drain | HIGH | 78/100 | In Progress |
| Broken Infrastructure | MEDIUM | 55/100 | Open |

---

## 🎤 Hackathon Demo Steps

1. **Open Home page** → Show hero, live stats, feature cards
2. **Click "Report a Problem"** → Upload a pothole photo, type location
3. **Show AI Analysis loading** → Result cards appear with score breakdown
4. **Open Dashboard** → Show charts, map, filter by HIGH severity
5. **Click "View" on a report** → Show full details, update status to Resolved
6. **Export PDF** → Download and show the formatted report

---

## 🎤 2–3 Minute Presentation Script

> "Imagine a city with hundreds of potholes, overflowing garbage bins, and broken streetlights — and no efficient way to report them.
>
> CivicLens AI solves this. A citizen takes one photo. Our AI instantly identifies the problem, classifies it, estimates severity, checks for duplicates, and calculates a transparent priority score from 0 to 100 — every single point is explained, no black box.
>
> [Demo: Upload photo → Show result]
>
> The score tells city authorities exactly what to fix first. All reports flow into a live admin dashboard with charts, location maps, and filters.
>
> [Demo: Show dashboard, filter HIGH severity]
>
> Officials can update status, download PDF reports, and track resolution rates — all in one platform.
>
> CivicLens AI bridges the gap between citizens and government. It's fast, transparent, and built to scale. Thank you."

---

## ❓ Possible Judge Questions & Answers

**Q: How does the AI work without an external API?**
> A: We use a smart mock AI pipeline with keyword analysis, description parsing, and image metadata. The architecture is designed to plug in Google Cloud Vision or HuggingFace models with minimal code changes — we just uncomment the stub functions.

**Q: How accurate is the duplicate detection?**
> A: We use the Haversine formula to calculate GPS distance. Reports within 500 meters with the same category are flagged as potential duplicates. This is a standard approach used in location-based apps.

**Q: Why is the priority score transparent?**
> A: We believe government decisions should be explainable. Every point in the score is justified — severity, safety risk, duplicate count, and location importance — so officials can trust and audit the ranking.

**Q: How would you scale this for a real city?**
> A: Replace SQLite with PostgreSQL, deploy on a cloud VM or Kubernetes, integrate with real government APIs, add authentication, and connect to Google Vision for production-grade AI.

**Q: How would you prevent fake reports?**
> A: Add user authentication, GPS verification (compare submitted location with device GPS), image metadata analysis (EXIF data for time/location), and a community moderation flag system.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web UI framework |
| SQLite | Local database |
| Pillow | Image processing |
| Plotly | Interactive charts |
| Pandas | Data manipulation |
| ReportLab | PDF generation |
| Haversine | GPS distance calculation |

---

## 📤 GitHub Upload

```bash
git init
git add .
git commit -m "Initial commit: CivicLens AI hackathon project"
git branch -M main
git remote add origin https://github.com/your-username/civiclens-ai.git
git push -u origin main
```

---

## 📝 License

MIT License — Free to use, modify, and distribute for educational and hackathon purposes.

---

*Built with ❤️ for Hackathon 2026 · CivicLens AI v1.0*

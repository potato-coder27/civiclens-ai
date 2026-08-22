# 🚀 CivicLens AI — FastAPI Backend Documentation

## Overview

CivicLens AI now includes a **complete REST API** built with FastAPI. This allows:
- ✅ Mobile apps (iOS/Android) to submit reports
- ✅ Web frontends to consume data
- ✅ Third-party integrations
- ✅ Real-time data access
- ✅ Auto-generated API documentation

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API
```bash
python api.py
```

API will be live at: `http://localhost:8000`

### 3. Access Documentation
- **Interactive Docs (Swagger UI):** `http://localhost:8000/docs`
- **Alternative Docs (ReDoc):** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## Core Endpoints

### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "CivicLens AI API",
  "version": "1.0.0"
}
```

---

### Submit a Report
```http
POST /api/reports/submit
Content-Type: multipart/form-data

file: <image_file>
description: "Large pothole on Main Street"
location_name: "Main Street, Downtown"
latitude: 40.7128
longitude: -74.0060
```

**Response:**
```json
{
  "success": true,
  "report_id": 42,
  "analysis": {
    "category": "Road Damage",
    "severity": "HIGH",
    "confidence": 0.94,
    "tags": "road-damage, pothole, asphalt",
    "recommended_action": "URGENT: Deploy road maintenance team within 24 hours..."
  },
  "duplicates": {
    "duplicate_count": 3,
    "related_ids": [35, 38, 41],
    "is_duplicate": true
  },
  "priority_score": 92,
  "score_label": "CRITICAL"
}
```

---

### Get All Reports
```http
GET /api/reports?category=Road%20Damage&severity=HIGH&status=Open&priority_min=80&priority_max=100
```

**Query Parameters:**
- `category` (optional): Problem category
- `severity` (optional): HIGH, MEDIUM, LOW
- `status` (optional): Open, In Progress, Resolved
- `priority_min` (optional): Min priority score (0-100)
- `priority_max` (optional): Max priority score (0-100)

**Response:**
```json
{
  "count": 5,
  "reports": [
    {
      "id": 42,
      "category": "Road Damage",
      "severity": "HIGH",
      "priority_score": 92,
      "location_name": "Main Street",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "status": "Open",
      "created_at": "2026-08-22T10:30:00",
      "duplicate_count": 3
    }
  ]
}
```

---

### Get Single Report
```http
GET /api/reports/42
```

**Response:** Full report details with priority breakdown

---

### Update Report Status
```http
PUT /api/reports/42/status
Content-Type: application/json

{
  "status": "In Progress"
}
```

**Valid Statuses:**
- `Open`
- `In Progress`
- `Resolved`

---

## Dashboard Endpoints

### Get Statistics
```http
GET /api/dashboard/stats
```
Returns: Total reports, HIGH/MEDIUM/LOW count, average priority score

### Get Category Distribution
```http
GET /api/dashboard/category-distribution
```
Returns: Report counts by problem category

### Get Severity Distribution
```http
GET /api/dashboard/severity-distribution
```
Returns: Report counts by severity level

### Get Reports Over Time
```http
GET /api/dashboard/reports-over-time
```
Returns: Daily report submission counts

### Get Location Data
```http
GET /api/dashboard/location-data
```
Returns: Lat/long and report count for mapping

### Get Priority Distribution
```http
GET /api/dashboard/priority-distribution
```
Returns: Critical/High/Medium/Low counts

---

## Duplicate Detection Endpoints

### Check for Duplicates
```http
GET /api/duplicates/check?category=Road%20Damage&latitude=40.7128&longitude=-74.0060
```

**Response:**
```json
{
  "duplicate_count": 3,
  "related_ids": [35, 38, 41],
  "is_duplicate": true,
  "message": "⚠️ Possible duplicate detected! 3 similar 'Road Damage' reports found nearby."
}
```

---

## Priority Scoring Endpoints

### Calculate Priority Score
```http
POST /api/priority/calculate
Content-Type: application/json

{
  "severity": "HIGH",
  "category": "Road Damage",
  "duplicate_count": 3,
  "location_name": "Main Street",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response:**
```json
{
  "score": 92,
  "label": "CRITICAL",
  "color": "#FF2D2D",
  "breakdown": {
    "severity_weight": 40,
    "duplicate_bonus": 15,
    "category_risk": 15,
    "safety_risk": 12,
    "location_importance": 10,
    "total": 92
  }
}
```

---

## Metadata Endpoints

### Get Categories
```http
GET /api/categories
```

**Response:**
```json
{
  "categories": [
    {
      "name": "Road Damage",
      "icon": "🚧",
      "color": "#FF4B4B",
      "default_severity": "HIGH"
    },
    ...
  ]
}
```

### Get Severities
```http
GET /api/severities
```

### Get Statuses
```http
GET /api/statuses
```

---

## CORS & Access

✅ **CORS Enabled** — API accessible from any origin
✅ **No Authentication** — Open access for public submissions
✅ **File Upload** — Supports up to 200MB images

---

## Example: Complete Mobile App Flow

```python
import requests

BASE_URL = "http://192.168.30.240:8000"

# 1. Submit a report with image
with open("pothole.jpg", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/reports/submit",
        files={"file": f},
        data={
            "description": "Large pothole blocking traffic",
            "location_name": "Main Street, Downtown",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    )
    report = response.json()
    print(f"✅ Report submitted: ID {report['report_id']}")
    print(f"🎯 Priority Score: {report['priority_score']}/100")

# 2. Get all HIGH priority reports
response = requests.get(
    f"{BASE_URL}/api/reports",
    params={"severity": "HIGH"}
)
reports = response.json()
print(f"📊 Found {reports['count']} HIGH priority reports")

# 3. Update a report status
response = requests.put(
    f"{BASE_URL}/api/reports/{report['report_id']}/status",
    json={"status": "In Progress"}
)
print(f"✅ Status updated: {response.json()}")

# 4. Get dashboard stats
response = requests.get(f"{BASE_URL}/api/dashboard/stats")
stats = response.json()
print(f"📈 Total Reports: {stats['total']}")
```

---

## Deployment Options

### Local Network
```bash
python api.py
# Accessible at: http://YOUR-IP:8000
```

### Production (Heroku, Railway, AWS)
```bash
# Using Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

### Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Error Handling

All errors return JSON with status code:

```json
{
  "detail": "Report not found"
}
```

**Common Errors:**
- `400` — Bad request (invalid data)
- `404` — Not found (invalid report ID)
- `422` — Validation error (missing fields)

---

## Rate Limiting

Currently: **No rate limiting** (open for hackathon/demo)

For production, add rate limiting with `slowapi`:
```bash
pip install slowapi
```

---

**🎉 Your API is ready for mobile apps, integrations, and deployments!**

"""
CivicLens AI - FastAPI Backend
Complete REST API for mobile apps, web frontends, and integrations.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
import json
from typing import List, Optional
from io import BytesIO

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from database import (
    init_db, seed_demo_data, insert_report, get_all_reports,
    get_report_by_id, update_report_status, get_stats,
    get_category_distribution, get_severity_distribution,
    get_reports_over_time, get_location_data, get_priority_distribution
)
from ai_analyzer import analyze_image
from duplicate_detector import find_duplicates, haversine_distance
from priority_engine import calculate_priority_score, get_score_label, get_score_breakdown_text

# ─── Initialize FastAPI ────────────────────────────────────────────────────────

app = FastAPI(
    title="CivicLens AI API",
    description="AI-powered civic problem detection and reporting platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ─── CORS Configuration ────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Initialize Database ──────────────────────────────────────────────────────

init_db()
seed_demo_data()

# ─── Health Check ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "CivicLens AI API",
        "version": "1.0.0"
    }

# ─── Report Endpoints ─────────────────────────────────────────────────────────

@app.post("/api/reports/submit")
async def submit_report(
    file: UploadFile = File(...),
    description: str = Form(...),
    location_name: str = Form(""),
    latitude: float = Form(0.0),
    longitude: float = Form(0.0)
):
    """
    Submit a new civic problem report with image analysis.
    
    - **file**: Image file (JPG, PNG)
    - **description**: Problem description
    - **location_name**: Landmark or address
    - **latitude**: GPS latitude
    - **longitude**: GPS longitude
    
    Returns: Report ID and AI analysis results
    """
    try:
        # Read image bytes
        contents = await file.read()
        
        # Analyze with AI
        analysis = analyze_image(contents, description, file.filename)
        
        # Check for duplicates
        dup_info = find_duplicates(
            category=analysis["category"],
            latitude=latitude,
            longitude=longitude
        )
        
        # Calculate priority score
        priority_score, breakdown = calculate_priority_score(
            severity=analysis["severity"],
            category=analysis["category"],
            duplicate_count=dup_info["duplicate_count"],
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )
        
        # Save image
        os.makedirs("data/uploads", exist_ok=True)
        image_path = f"data/uploads/{file.filename}"
        with open(image_path, "wb") as f:
            f.write(contents)
        
        # Insert report
        report_data = {
            "image_path": image_path,
            "category": analysis["category"],
            "severity": analysis["severity"],
            "description": description,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "priority_score": priority_score,
            "priority_breakdown": json.dumps(breakdown),
            "duplicate_count": dup_info["duplicate_count"],
            "confidence": analysis["confidence"],
            "tags": analysis["tags"],
            "recommended_action": analysis["recommended_action"],
            "is_demo": 0
        }
        
        report_id = insert_report(report_data)
        
        return {
            "success": True,
            "report_id": report_id,
            "analysis": analysis,
            "duplicates": dup_info,
            "priority_score": priority_score,
            "priority_breakdown": breakdown,
            "score_label": get_score_label(priority_score)[0]
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/reports")
async def get_reports(
    category: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority_min: Optional[int] = Query(0),
    priority_max: Optional[int] = Query(100)
):
    """
    Get all civic reports with optional filters.
    
    Query parameters:
    - **category**: Filter by problem category
    - **severity**: Filter by severity (HIGH, MEDIUM, LOW)
    - **status**: Filter by status (Open, In Progress, Resolved)
    - **priority_min**: Minimum priority score (0-100)
    - **priority_max**: Maximum priority score (0-100)
    """
    filters = {}
    if category:
        filters["category"] = category
    if severity:
        filters["severity"] = severity
    if status:
        filters["status"] = status
    if priority_min or priority_max:
        filters["priority_score"] = (priority_min, priority_max)
    
    reports = get_all_reports(filters if filters else None)
    
    # Add score labels
    for report in reports:
        report["score_label"] = get_score_label(report["priority_score"])[0]
    
    return {
        "count": len(reports),
        "reports": reports
    }

@app.get("/api/reports/{report_id}")
async def get_report(report_id: int):
    """Get a single report by ID."""
    report = get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report["score_label"] = get_score_label(report["priority_score"])[0]
    if report["priority_breakdown"]:
        report["priority_breakdown"] = json.loads(report["priority_breakdown"])
    
    return report

@app.put("/api/reports/{report_id}/status")
async def update_status(report_id: int, status: str):
    """
    Update report status.
    
    Valid statuses: Open, In Progress, Resolved
    """
    if status not in ["Open", "In Progress", "Resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    try:
        update_report_status(report_id, status)
        return {
            "success": True,
            "report_id": report_id,
            "status": status
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Dashboard & Analytics Endpoints ──────────────────────────────────────────

@app.get("/api/dashboard/stats")
async def dashboard_stats():
    """Get dashboard statistics and summary metrics."""
    stats = get_stats()
    return stats

@app.get("/api/dashboard/category-distribution")
async def category_distribution():
    """Get distribution of reports by category."""
    data = get_category_distribution()
    return {
        "categories": [row["category"] for row in data],
        "counts": [row["count"] for row in data]
    }

@app.get("/api/dashboard/severity-distribution")
async def severity_distribution():
    """Get distribution of reports by severity."""
    data = get_severity_distribution()
    return {
        "severities": [row["severity"] for row in data],
        "counts": [row["count"] for row in data]
    }

@app.get("/api/dashboard/reports-over-time")
async def reports_over_time():
    """Get report submissions over time."""
    data = get_reports_over_time()
    return {
        "dates": [row["date"] for row in data],
        "counts": [row["count"] for row in data]
    }

@app.get("/api/dashboard/location-data")
async def location_data():
    """Get location-based data for mapping."""
    data = get_location_data()
    return {
        "locations": [
            {
                "name": row["location_name"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "reports": row["report_count"]
            }
            for row in data
        ]
    }

@app.get("/api/dashboard/priority-distribution")
async def priority_distribution():
    """Get distribution of reports by priority score range."""
    data = get_priority_distribution()
    return {
        "critical": data[0]["count"] if len(data) > 0 else 0,
        "high": data[1]["count"] if len(data) > 1 else 0,
        "medium": data[2]["count"] if len(data) > 2 else 0,
        "low": data[3]["count"] if len(data) > 3 else 0
    }

# ─── Duplicate Detection Endpoint ─────────────────────────────────────────────

@app.get("/api/duplicates/check")
async def check_duplicates(
    category: str,
    latitude: float = 0.0,
    longitude: float = 0.0
):
    """
    Check for duplicate/similar reports.
    
    Uses Haversine distance calculation for GPS-based proximity matching.
    """
    result = find_duplicates(category, latitude, longitude)
    return result

# ─── Priority Scoring Endpoint ──────────────────────────────────────────────

@app.post("/api/priority/calculate")
async def calculate_priority(
    severity: str = Query(...),
    category: str = Query(...),
    duplicate_count: int = Query(0),
    location_name: str = Query(""),
    latitude: float = Query(0.0),
    longitude: float = Query(0.0)
):
    """
    Calculate transparent priority score.
    
    Returns score (0-100) and detailed breakdown of all factors.
    """
    try:
        score, breakdown = calculate_priority_score(
            severity=severity,
            category=category,
            duplicate_count=duplicate_count,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )
        
        label, color = get_score_label(score)
        
        return {
            "score": score,
            "label": label,
            "color": color,
            "breakdown": breakdown
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Metadata Endpoints ────────────────────────────────────────────────────

@app.get("/api/categories")
async def get_categories():
    """Get all supported problem categories."""
    from ai_analyzer import CATEGORIES
    return {
        "categories": [
            {
                "name": cat,
                "icon": meta["icon"],
                "color": meta["color"],
                "default_severity": meta["default_severity"]
            }
            for cat, meta in CATEGORIES.items()
        ]
    }

@app.get("/api/severities")
async def get_severities():
    """Get all supported severity levels."""
    return {
        "severities": ["LOW", "MEDIUM", "HIGH"]
    }

@app.get("/api/statuses")
async def get_statuses():
    """Get all report statuses."""
    return {
        "statuses": ["Open", "In Progress", "Resolved"]
    }

# ─── Root Endpoint ────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """API root endpoint with documentation links."""
    return {
        "service": "CivicLens AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "endpoints": {
            "health": "GET /health",
            "submit_report": "POST /api/reports/submit",
            "get_reports": "GET /api/reports",
            "get_report": "GET /api/reports/{id}",
            "update_status": "PUT /api/reports/{id}/status",
            "dashboard_stats": "GET /api/dashboard/stats",
            "categories": "GET /api/categories"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

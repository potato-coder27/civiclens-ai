"""
CivicLens AI - Database Module
Handles SQLite database operations for civic reports.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "civiclens.db")


def get_connection():
    """Get a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            location_name TEXT,
            latitude REAL DEFAULT 0.0,
            longitude REAL DEFAULT 0.0,
            priority_score INTEGER DEFAULT 0,
            priority_breakdown TEXT,
            duplicate_count INTEGER DEFAULT 0,
            duplicate_group_id INTEGER,
            status TEXT DEFAULT 'Open',
            confidence REAL DEFAULT 0.0,
            tags TEXT,
            recommended_action TEXT,
            is_demo INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Duplicate groups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS duplicate_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            report_ids TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Locations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            report_count INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def seed_demo_data():
    """Seed database with demo reports if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE is_demo = 1")
    count = cursor.fetchone()["cnt"]

    if count > 0:
        conn.close()
        return

    demo_reports = [
        {
            "category": "Road Damage",
            "severity": "HIGH",
            "description": "Large pothole on main road near college campus causing vehicle damage. Multiple vehicles affected daily.",
            "location_name": "Near College Campus, MG Road",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "priority_score": 92,
            "priority_breakdown": json.dumps({
                "severity_weight": 40,
                "duplicate_bonus": 20,
                "category_risk": 15,
                "safety_risk": 12,
                "location_importance": 5,
                "total": 92
            }),
            "duplicate_count": 7,
            "status": "Open",
            "confidence": 0.94,
            "tags": "pothole,road damage,vehicle hazard",
            "recommended_action": "URGENT: Immediate repair required. Deploy road maintenance team within 24 hours.",
            "days_ago": 2
        },
        {
            "category": "Garbage Overflow",
            "severity": "MEDIUM",
            "description": "Overflowing garbage bin near bus stop. Garbage spilling onto sidewalk creating unhygienic conditions.",
            "location_name": "Central Bus Stop, Nehru Nagar",
            "latitude": 28.6200,
            "longitude": 77.2150,
            "priority_score": 58,
            "priority_breakdown": json.dumps({
                "severity_weight": 25,
                "duplicate_bonus": 10,
                "category_risk": 10,
                "safety_risk": 8,
                "location_importance": 5,
                "total": 58
            }),
            "duplicate_count": 3,
            "status": "In Progress",
            "confidence": 0.89,
            "tags": "garbage,overflow,hygiene,public health",
            "recommended_action": "Schedule garbage collection within 48 hours. Increase collection frequency.",
            "days_ago": 5
        },
        {
            "category": "Broken Streetlight",
            "severity": "MEDIUM",
            "description": "Streetlight not functioning for past 2 weeks. Area becomes completely dark at night causing safety concerns.",
            "location_name": "Residential Colony, Sector 12",
            "latitude": 28.6080,
            "longitude": 77.2020,
            "priority_score": 61,
            "priority_breakdown": json.dumps({
                "severity_weight": 25,
                "duplicate_bonus": 5,
                "category_risk": 12,
                "safety_risk": 14,
                "location_importance": 5,
                "total": 61
            }),
            "duplicate_count": 2,
            "status": "Open",
            "confidence": 0.91,
            "tags": "streetlight,darkness,safety,night",
            "recommended_action": "Replace faulty bulb/fuse. Inspect electrical connections within 72 hours.",
            "days_ago": 10
        },
        {
            "category": "Water Leakage",
            "severity": "HIGH",
            "description": "Major water pipe burst on main street. Water flooding the road and nearby shops. Heavy water wastage.",
            "location_name": "Market Area, Gandhi Chowk",
            "latitude": 28.6300,
            "longitude": 77.2200,
            "priority_score": 84,
            "priority_breakdown": json.dumps({
                "severity_weight": 40,
                "duplicate_bonus": 15,
                "category_risk": 13,
                "safety_risk": 11,
                "location_importance": 5,
                "total": 84
            }),
            "duplicate_count": 4,
            "status": "Resolved",
            "confidence": 0.96,
            "tags": "water leakage,pipe burst,flooding,water wastage",
            "recommended_action": "URGENT: Emergency plumbing required. Shut water supply to affected area immediately.",
            "days_ago": 14
        },
        {
            "category": "Damaged Pavement",
            "severity": "LOW",
            "description": "Minor cracks and uneven tiles on pedestrian walkway. Poses tripping hazard for elderly pedestrians.",
            "location_name": "Park Street, Laxmi Nagar",
            "latitude": 28.6050,
            "longitude": 77.1980,
            "priority_score": 27,
            "priority_breakdown": json.dumps({
                "severity_weight": 10,
                "duplicate_bonus": 0,
                "category_risk": 8,
                "safety_risk": 5,
                "location_importance": 4,
                "total": 27
            }),
            "duplicate_count": 0,
            "status": "Open",
            "confidence": 0.82,
            "tags": "pavement,cracks,tiles,pedestrian hazard",
            "recommended_action": "Schedule repair during next maintenance cycle within 2 weeks.",
            "days_ago": 3
        },
        {
            "category": "Open Drain",
            "severity": "HIGH",
            "description": "Open drain without cover near school entrance. Extremely dangerous for children. Foul smell spreading.",
            "location_name": "Government School Gate, Ashok Nagar",
            "latitude": 28.6170,
            "longitude": 77.2100,
            "priority_score": 78,
            "priority_breakdown": json.dumps({
                "severity_weight": 40,
                "duplicate_bonus": 10,
                "category_risk": 13,
                "safety_risk": 10,
                "location_importance": 5,
                "total": 78
            }),
            "duplicate_count": 3,
            "status": "In Progress",
            "confidence": 0.93,
            "tags": "open drain,safety hazard,children,school",
            "recommended_action": "URGENT: Install drain cover immediately. Health department inspection required.",
            "days_ago": 7
        },
        {
            "category": "Broken Infrastructure",
            "severity": "MEDIUM",
            "description": "Public bench in city park completely broken. Metal parts exposed creating injury risk for park visitors.",
            "location_name": "Central City Park, Ring Road",
            "latitude": 28.6120,
            "longitude": 77.2060,
            "priority_score": 55,
            "priority_breakdown": json.dumps({
                "severity_weight": 25,
                "duplicate_bonus": 5,
                "category_risk": 10,
                "safety_risk": 10,
                "location_importance": 5,
                "total": 55
            }),
            "duplicate_count": 1,
            "status": "Open",
            "confidence": 0.87,
            "tags": "broken bench,park,infrastructure,injury risk",
            "recommended_action": "Remove or repair broken bench within 5 days. Conduct park infrastructure audit.",
            "days_ago": 1
        },
    ]

    now = datetime.now()
    for i, report in enumerate(demo_reports):
        created_at = (now - timedelta(days=report["days_ago"])).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO reports (
                image_path, category, severity, description, location_name,
                latitude, longitude, priority_score, priority_breakdown,
                duplicate_count, status, confidence, tags, recommended_action,
                is_demo, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            f"assets/sample_images/demo_{i+1}.jpg",
            report["category"],
            report["severity"],
            report["description"],
            report["location_name"],
            report["latitude"],
            report["longitude"],
            report["priority_score"],
            report["priority_breakdown"],
            report["duplicate_count"],
            report["status"],
            report["confidence"],
            report["tags"],
            report["recommended_action"],
            created_at,
            created_at
        ))

    conn.commit()
    conn.close()


def insert_report(data: dict) -> int:
    """Insert a new report and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO reports (
            image_path, category, severity, description, location_name,
            latitude, longitude, priority_score, priority_breakdown,
            duplicate_count, status, confidence, tags, recommended_action,
            is_demo, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
    """, (
        data.get("image_path", ""),
        data.get("category", "Unknown"),
        data.get("severity", "LOW"),
        data.get("description", ""),
        data.get("location_name", "Unknown Location"),
        data.get("latitude", 0.0),
        data.get("longitude", 0.0),
        data.get("priority_score", 0),
        json.dumps(data.get("priority_breakdown", {})),
        data.get("duplicate_count", 0),
        data.get("status", "Open"),
        data.get("confidence", 0.0),
        data.get("tags", ""),
        data.get("recommended_action", ""),
        now,
        now
    ))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id


def get_all_reports(filters: dict = None) -> list:
    """Fetch all reports with optional filters."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM reports WHERE 1=1"
    params = []

    if filters:
        if filters.get("severity") and filters["severity"] != "All":
            query += " AND severity = ?"
            params.append(filters["severity"])
        if filters.get("category") and filters["category"] != "All":
            query += " AND category = ?"
            params.append(filters["category"])
        if filters.get("status") and filters["status"] != "All":
            query += " AND status = ?"
            params.append(filters["status"])
        if filters.get("search"):
            query += " AND (description LIKE ? OR location_name LIKE ? OR category LIKE ?)"
            s = f"%{filters['search']}%"
            params.extend([s, s, s])

    sort = filters.get("sort", "created_at") if filters else "created_at"
    order = filters.get("order", "DESC") if filters else "DESC"
    valid_sorts = ["created_at", "priority_score", "severity", "duplicate_count"]
    if sort not in valid_sorts:
        sort = "created_at"
    query += f" ORDER BY {sort} {order}"

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_report_by_id(report_id: int) -> dict:
    """Fetch a single report by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_report_status(report_id: int, status: str):
    """Update the status of a report."""
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
        (status, now, report_id)
    )
    conn.commit()
    conn.close()


def get_stats() -> dict:
    """Get aggregate statistics for dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM reports")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE severity = 'HIGH'")
    high = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE severity = 'MEDIUM'")
    medium = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE severity = 'LOW'")
    low = cursor.fetchone()["cnt"]

    cursor.execute("SELECT AVG(priority_score) as avg FROM reports")
    avg_score = cursor.fetchone()["avg"] or 0

    cursor.execute("""
        SELECT category, COUNT(*) as cnt FROM reports
        GROUP BY category ORDER BY cnt DESC LIMIT 1
    """)
    row = cursor.fetchone()
    most_common = row["category"] if row else "N/A"

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE status = 'Open'")
    open_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE status = 'Resolved'")
    resolved_count = cursor.fetchone()["cnt"]

    conn.close()

    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "avg_score": round(avg_score, 1),
        "most_common": most_common,
        "open": open_count,
        "resolved": resolved_count
    }


def get_category_distribution() -> list:
    """Get count per category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as cnt FROM reports GROUP BY category ORDER BY cnt DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_severity_distribution() -> list:
    """Get count per severity."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT severity, COUNT(*) as cnt FROM reports GROUP BY severity")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_reports_over_time() -> list:
    """Get report counts grouped by date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as cnt
        FROM reports
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_location_data() -> list:
    """Get all report locations for heatmap."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, latitude, longitude, category, severity, priority_score, location_name
        FROM reports WHERE latitude != 0 OR longitude != 0
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_priority_distribution() -> list:
    """Get priority score buckets."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT priority_score FROM reports")
    scores = [r["priority_score"] for r in cursor.fetchall()]
    conn.close()
    return scores

"""
CivicLens AI - Priority Engine
Transparent Civic Priority Score calculator (0-100).
Every point is explained and traceable.
"""

from __future__ import annotations
from typing import Tuple
from ai_analyzer import CATEGORIES


# ─── Scoring Weights ──────────────────────────────────────────────────────────

SEVERITY_WEIGHTS = {
    "HIGH":   40,
    "MEDIUM": 25,
    "LOW":    10
}

MAX_DUPLICATE_BONUS = 20   # max 20 pts from duplicates
DUPLICATE_PER_REPORT = 5   # 5 pts per duplicate report

MAX_SAFETY_RISK   = 15     # from category definition
MAX_CATEGORY_RISK = 15     # from category definition
MAX_LOCATION_IMP  = 10     # location importance


def calculate_priority_score(
    severity: str,
    category: str,
    duplicate_count: int,
    location_name: str = "",
    latitude: float = 0.0,
    longitude: float = 0.0
) -> Tuple[int, dict]:
    """
    Calculate Civic Priority Score (0–100) with a full breakdown.

    Formula:
        Score = severity_weight
              + min(duplicate_count × 5, 20)
              + category_risk  (from CATEGORIES definition, max 15)
              + safety_risk    (from CATEGORIES definition, max 15)
              + location_importance (0–10)

    Returns:
        (score: int, breakdown: dict)
    """
    breakdown = {}

    # 1. Severity weight (10 / 25 / 40 pts)
    sev_pts = SEVERITY_WEIGHTS.get(severity.upper(), 10)
    breakdown["severity_weight"] = sev_pts

    # 2. Duplicate bonus (5 pts per duplicate, max 20)
    dup_pts = min(duplicate_count * DUPLICATE_PER_REPORT, MAX_DUPLICATE_BONUS)
    breakdown["duplicate_bonus"] = dup_pts

    # 3. Category risk (8–15 pts from definition)
    cat_meta = CATEGORIES.get(category, {})
    cat_pts = cat_meta.get("category_risk", 10)
    breakdown["category_risk"] = cat_pts

    # 4. Safety risk (5–14 pts from definition)
    safety_pts = cat_meta.get("safety_risk", 8)
    breakdown["safety_risk"] = safety_pts

    # 5. Location importance (0–10 pts)
    loc_pts = _location_importance(location_name, latitude, longitude)
    breakdown["location_importance"] = loc_pts

    # Total
    total = sev_pts + dup_pts + cat_pts + safety_pts + loc_pts
    total = max(0, min(100, total))  # clamp to [0, 100]
    breakdown["total"] = total

    return total, breakdown


def _location_importance(location_name: str, lat: float, lng: float) -> int:
    """
    Score location importance (0–10).
    High-importance zones: hospitals, schools, markets, main roads.
    """
    high_importance = ["hospital", "school", "college", "market", "main road", "mg road",
                       "national highway", "bus stop", "railway", "airport", "junction"]
    medium_importance = ["park", "sector", "colony", "nagar", "chowk", "plaza", "complex"]

    loc_lower = location_name.lower() if location_name else ""

    if any(kw in loc_lower for kw in high_importance):
        return 10
    elif any(kw in loc_lower for kw in medium_importance):
        return 6
    elif lat != 0.0 or lng != 0.0:
        return 4  # GPS-tagged but unrecognized zone
    else:
        return 2  # No location info


def get_score_label(score: int) -> tuple[str, str]:
    """Return human-readable label and color for a priority score."""
    if score >= 80:
        return "CRITICAL", "#FF2D2D"
    elif score >= 60:
        return "HIGH PRIORITY", "#FF6B35"
    elif score >= 40:
        return "MEDIUM PRIORITY", "#FFB703"
    else:
        return "LOW PRIORITY", "#4CAF50"


def get_score_breakdown_text(breakdown: dict) -> str:
    """Format breakdown as a readable string."""
    lines = [
        f"  • Severity Weight     : {breakdown.get('severity_weight', 0):>3} pts",
        f"  • Duplicate Bonus     : {breakdown.get('duplicate_bonus', 0):>3} pts",
        f"  • Category Risk       : {breakdown.get('category_risk', 0):>3} pts",
        f"  • Safety Risk         : {breakdown.get('safety_risk', 0):>3} pts",
        f"  • Location Importance : {breakdown.get('location_importance', 0):>3} pts",
        f"  {'─'*32}",
        f"  • TOTAL SCORE         : {breakdown.get('total', 0):>3} / 100",
    ]
    return "\n".join(lines)

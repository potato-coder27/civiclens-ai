"""
CivicLens AI - Duplicate Detector
Detects duplicate civic reports using:
  1. Same problem category
  2. Location proximity (Haversine distance < 500m)
Returns duplicate count and list of related report IDs.
"""

import math
from database import get_all_reports

PROXIMITY_RADIUS_METERS = 500  # Reports within 500m are considered nearby


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance (in meters) between two GPS coordinates.
    Uses the Haversine formula.
    """
    R = 6_371_000  # Earth's radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_duplicates(
    category: str,
    latitude: float,
    longitude: float,
    exclude_id: int = None
) -> dict:
    """
    Find existing reports that are potential duplicates of the new report.

    Matching criteria:
      - Same category (exact match)
      - AND location within PROXIMITY_RADIUS_METERS meters

    If either lat/lng is 0, falls back to category-only matching.

    Returns:
        {
            "duplicate_count": int,
            "related_ids": [int, ...],
            "is_duplicate": bool,
            "message": str
        }
    """
    all_reports = get_all_reports()
    related_ids = []
    use_location = (latitude != 0.0 or longitude != 0.0)

    for report in all_reports:
        if exclude_id and report["id"] == exclude_id:
            continue

        if report["category"] != category:
            continue

        if use_location:
            r_lat = report.get("latitude", 0.0) or 0.0
            r_lng = report.get("longitude", 0.0) or 0.0

            if r_lat == 0.0 and r_lng == 0.0:
                # Other report has no GPS → match by category only
                related_ids.append(report["id"])
                continue

            dist = haversine_distance(latitude, longitude, r_lat, r_lng)
            if dist <= PROXIMITY_RADIUS_METERS:
                related_ids.append(report["id"])
        else:
            # No GPS on new report — category match is sufficient
            related_ids.append(report["id"])

    count = len(related_ids)
    is_dup = count > 0

    if is_dup:
        message = (
            f"⚠️ Possible duplicate detected! {count} similar "
            f"'{category}' report{'s' if count > 1 else ''} found nearby."
        )
    else:
        message = "✅ No duplicates detected. This appears to be a new report."

    return {
        "duplicate_count": count,
        "related_ids": related_ids,
        "is_duplicate": is_dup,
        "message": message
    }


def get_proximity_label(distance_m: float) -> str:
    """Return a human-readable proximity label."""
    if distance_m < 100:
        return "Same location"
    elif distance_m < 500:
        return f"{int(distance_m)}m away"
    elif distance_m < 1000:
        return f"{distance_m/1000:.1f}km away"
    else:
        return f"{distance_m/1000:.1f}km away"

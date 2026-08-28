"""
CivicLens AI - AI Analyzer Module
Mock AI vision pipeline for civic problem detection.
Provides realistic, deterministic analysis without external API dependencies.
Stub hooks are included for Google Cloud Vision / HuggingFace integration.
"""

import random
import time
import hashlib
from PIL import Image
import io
import os

# ─── Category Definitions ─────────────────────────────────────────────────────

CATEGORIES = {
    "Road Damage": {
        "keywords": ["road", "pothole", "crack", "asphalt", "highway", "street", "damage", "tar"],
        "default_severity": "HIGH",
        "safety_risk": 12,
        "category_risk": 15,
        "icon": "🚧",
        "color": "#FF4B4B"
    },
    "Garbage Overflow": {
        "keywords": ["garbage", "trash", "waste", "bin", "litter", "dump", "rubbish", "overflow"],
        "default_severity": "MEDIUM",
        "safety_risk": 8,
        "category_risk": 10,
        "icon": "🗑️",
        "color": "#FFA500"
    },
    "Broken Streetlight": {
        "keywords": ["light", "streetlight", "lamp", "dark", "bulb", "pole", "electric", "night"],
        "default_severity": "MEDIUM",
        "safety_risk": 14,
        "category_risk": 12,
        "icon": "💡",
        "color": "#FFD700"
    },
    "Water Leakage": {
        "keywords": ["water", "leak", "pipe", "flood", "drain", "wet", "burst", "puddle", "flow"],
        "default_severity": "HIGH",
        "safety_risk": 11,
        "category_risk": 13,
        "icon": "💧",
        "color": "#00B4D8"
    },
    "Damaged Pavement": {
        "keywords": ["pavement", "sidewalk", "footpath", "tile", "walk", "pedestrian", "broken"],
        "default_severity": "LOW",
        "safety_risk": 5,
        "category_risk": 8,
        "icon": "🧱",
        "color": "#8B8B8B"
    },
    "Open Drain": {
        "keywords": ["drain", "sewer", "manhole", "open", "cover", "gutter", "sewage", "smell"],
        "default_severity": "HIGH",
        "safety_risk": 10,
        "category_risk": 13,
        "icon": "🕳️",
        "color": "#8B4513"
    },
    "Broken Infrastructure": {
        "keywords": ["bench", "fence", "wall", "building", "structure", "broken", "collapsed", "railing"],
        "default_severity": "MEDIUM",
        "safety_risk": 10,
        "category_risk": 10,
        "icon": "🏗️",
        "color": "#6C757D"
    }
}

SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH"]

RECOMMENDED_ACTIONS = {
    "Road Damage": {
        "HIGH": "URGENT: Immediate repair required. Deploy road maintenance team within 24 hours. Place warning signs.",
        "MEDIUM": "Schedule road repair within 3–5 days. Place warning markers at site.",
        "LOW": "Add to maintenance queue. Repair within 2 weeks during scheduled maintenance."
    },
    "Garbage Overflow": {
        "HIGH": "URGENT: Emergency garbage collection needed. Health department notification required.",
        "MEDIUM": "Schedule garbage collection within 48 hours. Increase collection frequency.",
        "LOW": "Add to next collection route. Monitor bin capacity."
    },
    "Broken Streetlight": {
        "HIGH": "URGENT: Night safety at risk. Repair electrical fault within 24 hours.",
        "MEDIUM": "Replace faulty bulb/fuse. Inspect electrical connections within 72 hours.",
        "LOW": "Add to routine maintenance. Replace within 1 week."
    },
    "Water Leakage": {
        "HIGH": "URGENT: Emergency plumbing required. Shut water supply to affected area immediately.",
        "MEDIUM": "Dispatch plumbing team within 24 hours. Monitor water loss.",
        "LOW": "Schedule plumbing inspection within 3 days."
    },
    "Damaged Pavement": {
        "HIGH": "URGENT: Immediate repair to prevent injury. Place barriers around damaged area.",
        "MEDIUM": "Schedule repair within 5 days. Place temporary warning signs.",
        "LOW": "Schedule repair during next maintenance cycle within 2 weeks."
    },
    "Open Drain": {
        "HIGH": "URGENT: Install drain cover immediately. Health department inspection required.",
        "MEDIUM": "Install temporary barrier. Permanent cover within 72 hours.",
        "LOW": "Schedule drain cover installation within 1 week."
    },
    "Broken Infrastructure": {
        "HIGH": "URGENT: Remove or secure broken structure immediately to prevent injury.",
        "MEDIUM": "Repair or remove within 5 days. Conduct infrastructure audit.",
        "LOW": "Schedule repair in next maintenance cycle."
    }
}


# ─── Main Analyzer ────────────────────────────────────────────────────────────

def analyze_image(image_bytes: bytes, description: str = "", filename: str = "") -> dict:
    """
    Analyze an uploaded image and return structured civic problem report data.

    This is a mock AI pipeline that:
    1. Computes a deterministic hash-based seed from the image bytes
    2. Uses description keywords to detect the most likely category
    3. Falls back to image-hash-based classification
    4. Returns realistic confidence scores and tags

    To integrate a real AI model, replace the `_mock_classify()` call with
    `_google_vision_classify()` or `_huggingface_classify()`.
    """
    # Simulate AI processing time
    time.sleep(1.5)

    # Deterministic seed from image content for consistent demo results
    img_hash = hashlib.md5(image_bytes[:4096]).hexdigest()
    seed = int(img_hash[:8], 16)
    rng = random.Random(seed)

    # Classify using description + filename hints
    category, confidence = _mock_classify(description, filename, rng)

    severity = _estimate_severity(category, description, rng)
    tags = _generate_tags(category, severity, description)
    recommended_action = RECOMMENDED_ACTIONS.get(category, {}).get(severity, "Assess and schedule repair.")

    # Image analysis metadata
    image_info = _analyze_image_metadata(image_bytes)

    return {
        "category": category,
        "severity": severity,
        "confidence": round(confidence, 2),
        "tags": ", ".join(tags),
        "recommended_action": recommended_action,
        "icon": CATEGORIES[category]["icon"],
        "color": CATEGORIES[category]["color"],
        "safety_risk": CATEGORIES[category]["safety_risk"],
        "category_risk": CATEGORIES[category]["category_risk"],
        "image_info": image_info,
        "analysis_method": "CivicLens Mock AI v1.0 (Demo Mode)"
    }


def _mock_classify(description: str, filename: str, rng: random.Random):
    """
    Classify civic problem from description keywords and filename.
    Returns (category, confidence).
    """
    text = (description + " " + filename).lower()

    best_category = None
    best_score = 0

    for cat, meta in CATEGORIES.items():
        score = sum(1 for kw in meta["keywords"] if kw in text)
        if score > best_score:
            best_score = score
            best_category = cat

    if best_category and best_score > 0:
        confidence = min(0.75 + best_score * 0.04 + rng.uniform(0, 0.08), 0.99)
        return best_category, confidence

    # Fallback: hash-based random selection (still deterministic)
    categories = list(CATEGORIES.keys())
    category = rng.choice(categories)
    confidence = rng.uniform(0.72, 0.88)
    return category, confidence


def _estimate_severity(category: str, description: str, rng: random.Random) -> str:
    """Estimate severity based on category default and description signals."""
    high_signals = ["urgent", "dangerous", "emergency", "severe", "critical", "major", "broken", "burst", "flood", "collapse", "blocked"]
    low_signals = ["minor", "small", "slight", "little", "crack", "scratch", "cosmetic"]

    text = description.lower()
    high_count = sum(1 for s in high_signals if s in text)
    low_count = sum(1 for s in low_signals if s in text)

    default = CATEGORIES[category]["default_severity"]

    if high_count > low_count and high_count > 0:
        return "HIGH"
    elif low_count > high_count and low_count > 0:
        return "LOW"
    else:
        # Near default with some randomness
        idx = SEVERITY_LEVELS.index(default)
        drift = rng.choice([-1, 0, 0, 1])
        new_idx = max(0, min(2, idx + drift))
        return SEVERITY_LEVELS[new_idx]


def _generate_tags(category: str, severity: str, description: str) -> list:
    """Generate relevant tags for the report."""
    base_tags = CATEGORIES[category]["keywords"][:3]
    tags = [category.lower().replace(" ", "-"), severity.lower()]
    tags.extend(base_tags[:2])
    if "school" in description.lower() or "college" in description.lower():
        tags.append("near-educational-institution")
    if "market" in description.lower() or "shop" in description.lower():
        tags.append("commercial-area")
    if "hospital" in description.lower():
        tags.append("near-hospital")
    return list(set(tags))[:6]


def _analyze_image_metadata(image_bytes: bytes) -> dict:
    """Extract basic image metadata."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format or "JPEG",
            "mode": img.mode,
            "size_kb": round(len(image_bytes) / 1024, 1)
        }
    except Exception:
        return {"width": 0, "height": 0, "format": "Unknown", "mode": "RGB", "size_kb": 0}


# ─── Stub: Real AI Integration ────────────────────────────────────────────────

def _google_vision_classify(image_bytes: bytes):
    """
    STUB: Google Cloud Vision API integration.
    Uncomment and configure when API key is available.

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.label_detection(image=image)
    labels = [label.description.lower() for label in response.label_annotations]
    # Map labels to categories using CATEGORIES keyword matching
    """
    raise NotImplementedError("Configure Google Cloud Vision API key to enable.")


def _huggingface_classify(image_bytes: bytes):
    """
    STUB: HuggingFace Vision Transformer integration.
    Uncomment and configure when model is available.

    from transformers import pipeline
    classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
    # Map ViT labels to civic categories
    """
    raise NotImplementedError("Configure HuggingFace model to enable.")

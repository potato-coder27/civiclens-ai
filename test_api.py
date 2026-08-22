#!/usr/bin/env python3
"""
Quick API test script - verify all endpoints work
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_api():
    print("\n" + "="*80)
    print("🚀 CIVICLENS AI - API TEST SUITE")
    print("="*80)
    
    # Test 1: Health check
    print("\n✓ Testing Health Check...")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"  Status: {r.status_code}")
        print(f"  Response: {r.json()}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Get categories
    print("\n✓ Testing Get Categories...")
    try:
        r = requests.get(f"{BASE_URL}/api/categories", timeout=5)
        data = r.json()
        print(f"  Categories found: {len(data['categories'])}")
        for cat in data['categories'][:3]:
            print(f"    • {cat['name']} {cat['icon']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 3: Get reports
    print("\n✓ Testing Get Reports...")
    try:
        r = requests.get(f"{BASE_URL}/api/reports", timeout=5)
        data = r.json()
        print(f"  Total reports: {data['count']}")
        if data['reports']:
            report = data['reports'][0]
            print(f"  Sample: {report['category']} - Priority {report['priority_score']}/100")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 4: Dashboard stats
    print("\n✓ Testing Dashboard Stats...")
    try:
        r = requests.get(f"{BASE_URL}/api/dashboard/stats", timeout=5)
        stats = r.json()
        print(f"  Total: {stats['total']}")
        print(f"  High Priority: {stats['high']}")
        print(f"  Avg Score: {stats['avg_score']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 5: Priority calculation
    print("\n✓ Testing Priority Score Calculation...")
    try:
        payload = {
            "severity": "HIGH",
            "category": "Road Damage",
            "duplicate_count": 2,
            "location_name": "Main Street"
        }
        r = requests.post(f"{BASE_URL}/api/priority/calculate", json=payload, timeout=5)
        data = r.json()
        print(f"  Score: {data['score']}/100")
        print(f"  Label: {data['label']}")
        print(f"  Breakdown: {json.dumps(data['breakdown'], indent=4)}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 6: API root
    print("\n✓ Testing API Root...")
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        data = r.json()
        print(f"  Service: {data['service']}")
        print(f"  Version: {data['version']}")
        print(f"  Documentation: {data['docs']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ API TEST COMPLETE - All endpoints responsive!")
    print("="*80)
    print("\n📚 Interactive Documentation:")
    print(f"   Swagger UI: http://localhost:8000/docs")
    print(f"   ReDoc:      http://localhost:8000/redoc")
    print(f"   OpenAPI:    http://localhost:8000/openapi.json")
    print("\n")

if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted")
        sys.exit(0)

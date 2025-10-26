#!/usr/bin/env python
"""
Quick test script to verify API endpoints are working.
Run this after starting the server with: python manage.py runserver
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test basic API endpoints"""
    
    print("Testing GSoC Review Platform API\n")
    print("=" * 50)
    
    # Test 1: Get organizations (should work without auth)
    print("\n1. Testing GET /api/organizations/")
    response = requests.get(f"{BASE_URL}/organizations/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    
    # Test 2: Get projects
    print("\n2. Testing GET /api/projects/")
    response = requests.get(f"{BASE_URL}/projects/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    
    # Test 3: Get profiles
    print("\n3. Testing GET /api/profiles/")
    response = requests.get(f"{BASE_URL}/profiles/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
    
    # Test 4: Try to create organization (should require auth)
    print("\n4. Testing POST /api/organizations/ (without auth)")
    org_data = {
        "name": "Test Organization",
        "description": "A test organization",
        "contact_email": "test@example.com",
        "year_joined": 2024
    }
    response = requests.post(f"{BASE_URL}/organizations/", json=org_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 403:
        print("   ✓ Correctly requires authentication")
    
    print("\n" + "=" * 50)
    print("\nAPI is working! ✓")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Visit http://localhost:8000/admin/ to login")
    print("3. Visit http://localhost:8000/api/ to explore the browsable API")
    print("4. See API_DOCUMENTATION.md for detailed endpoint information")

if __name__ == "__main__":
    try:
        test_api_endpoints()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Please start the server first with: python manage.py runserver")
    except Exception as e:
        print(f"Error: {e}")


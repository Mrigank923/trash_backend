#!/usr/bin/env python3
"""
Test script for admin endpoints and device registration
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def get_admin_token():
    """Login as admin and get token"""
    print("🔑 Getting admin token...")
    
    login_data = {
        "email": "admin@wastemanagement.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Admin logged in successfully")
            return token
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error logging in: {e}")
        return None

def test_get_user_by_id(token, user_id=2):
    """Test getting user by ID with correct URL"""
    print(f"\n🧪 Testing GET /admin/user/{user_id}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/user/{user_id}", headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ User retrieved successfully!")
        else:
            print("❌ Failed to get user")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_register_device(token):
    """Register a test device"""
    print(f"\n🧪 Testing device registration...")
    
    device_data = {
        "device_id": "DEVICE001",
        "api_key": "DEV_TEST123456"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/admin/device/register", json=device_data, headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Device registered successfully!")
        elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
            print("ℹ️  Device already exists")
        else:
            print("❌ Failed to register device")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_get_all_users(token):
    """Test getting all users"""
    print(f"\n🧪 Testing GET /admin/users...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Found {len(users)} users:")
            for user in users:
                print(f"  - ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, QR: {user.get('qr_code', 'None')}")
        else:
            print(f"❌ Failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Get admin token
    token = get_admin_token()
    if not token:
        print("❌ Cannot proceed without admin token")
        exit(1)
    
    # Test admin endpoints
    test_get_all_users(token)
    test_get_user_by_id(token, 2)
    test_register_device(token)
    
    print("\n📝 Summary:")
    print("✅ Correct URL format: /admin/user/{user_id}")
    print("❌ Incorrect URL format: /admin/user?{user_id}")
    print("\n🔗 Try these URLs in your browser/Postman:")
    print("   - GET http://localhost:8000/admin/user/2")
    print("   - GET http://localhost:8000/admin/users")
    print("   - GET http://localhost:8000/admin/devices")

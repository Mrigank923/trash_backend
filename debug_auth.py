#!/usr/bin/env python3
"""
Debug authentication issues
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_login_and_token():
    """Test login and token validation"""
    print("🔍 Debugging authentication issues...\n")
    
    # Check environment variables
    print("📋 Environment Check:")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    print(f"   SECRET_KEY: {'✅ Set' if secret_key else '❌ Missing'}")
    print(f"   ALGORITHM: {algorithm}")
    print(f"   SECRET_KEY length: {len(secret_key) if secret_key else 0}")
    
    # Test admin login
    print("\n🔑 Testing admin login...")
    login_data = {
        "email": "admin@wastemanagement.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login successful")
            print(f"   Token length: {len(access_token)}")
            print(f"   Token starts with: {access_token[:20]}...")
            
            # Test token validation
            print("\n🛡️  Testing token validation...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test /auth/me endpoint
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            print(f"   /auth/me Status: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"   ✅ Token validation successful")
                user_data = me_response.json()
                print(f"   User: {user_data.get('name')} ({user_data.get('email')})")
            else:
                print(f"   ❌ Token validation failed: {me_response.json()}")
            
            # Test admin endpoint
            print(f"\n🔧 Testing admin endpoint...")
            admin_response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
            print(f"   /admin/users Status: {admin_response.status_code}")
            if admin_response.status_code == 200:
                print(f"   ✅ Admin access successful")
                users = admin_response.json()
                print(f"   Found {len(users)} users")
            else:
                print(f"   ❌ Admin access failed: {admin_response.json()}")
                
            return access_token
            
        else:
            print(f"   ❌ Login failed: {response.json()}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running?")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_user_login():
    """Test normal user login"""
    print("\n👤 Testing normal user login...")
    
    # Try to login with the registered user
    login_data = {
        "email": "mrigankraj23@gmail.com",
        "password": "qwerty12345"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ User login successful")
            return response.json()["access_token"]
        elif response.status_code == 403:
            print("   ⚠️  Email verification required")
            print("   Use /auth/send-otp and /auth/verify-otp first")
        else:
            print(f"   ❌ Login failed: {response.json()}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
    return None

def debug_common_issues():
    """Debug common authentication issues"""
    print("\n🔧 Common Authentication Issues:")
    print("   1. Missing Authorization header")
    print("   2. Wrong token format (should be 'Bearer <token>')")
    print("   3. Expired token")
    print("   4. Invalid SECRET_KEY in environment")
    print("   5. Email not verified for normal users")
    
    print("\n✅ Correct Authorization header format:")
    print("   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    
    print("\n📝 Steps to test manually:")
    print("   1. POST /auth/login with admin credentials")
    print("   2. Copy the access_token from response")
    print("   3. Add header: Authorization: Bearer <access_token>")
    print("   4. Test protected endpoints")

if __name__ == "__main__":
    admin_token = test_login_and_token()
    test_user_login()
    debug_common_issues()
    
    if admin_token:
        print(f"\n🎯 Use this token for testing:")
        print(f"Authorization: Bearer {admin_token}")

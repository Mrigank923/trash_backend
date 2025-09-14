#!/usr/bin/env python3
"""
Quick test script to verify registration API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration with the new schema"""
    
    # Test data
    user_data = {
        "name": "Mrigank",
        "email": "mrigankraj23@gmail.com",
        "phone_no": "7376777953",
        "password": "qwerty12345",
        "role": "normal_user"
    }
    
    print("🧪 Testing user registration...")
    print(f"📤 Request data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            user_response = response.json()
            if user_response.get("qr_code"):
                print(f"🎫 QR Code generated: {user_response['qr_code']}")
            else:
                print("⚠️  No QR code in response")
        else:
            print("❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_waste_upload():
    """Test the new waste upload schema"""
    
    waste_data = {
        "device_id": "DEVICE001",
        "user_qr": "USER_A1B2C3D4",  # Example QR code
        "organic": 2.5,
        "recyclable": 1.8,
        "hazardous": 0.3
    }
    
    print("\n🧪 Testing waste upload schema...")
    print(f"📤 Request data: {json.dumps(waste_data, indent=2)}")
    print("📋 New schema uses 'user_qr' instead of 'user_id' and no 'api_key'")

if __name__ == "__main__":
    test_registration()
    test_waste_upload()

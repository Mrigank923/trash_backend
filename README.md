# 🚀 Smart Waste Management System - Quick Start Guide

## Project Structure

This project follows a clean MVC (Model-View-Controller) architecture:

```
backend/
├── config/           # Configuration files
│   ├── database.py   # Database connection setup
│   └── settings.py   # Application settings
├── models/           # Data models and schemas
│   ├── database.py   # SQLAlchemy database models
│   └── schemas.py    # Pydantic request/response schemas
├── controllers/      # Business logic
│   ├── auth.py       # Authentication logic
│   ├── user.py       # User operations
│   ├── buyer.py      # Buyer operations
│   ├── admin.py      # Admin operations
│   └── waste.py      # Waste data operations
├── middlewares/      # Middleware functions
│   ├── auth.py       # Authentication middleware
│   └── cors.py       # CORS middleware
├── helpers/          # Utility functions
│   ├── auth.py       # Authentication helpers
│   └── utils.py      # General utilities
├── routes/           # API route definitions
│   ├── auth.py       # Authentication routes
│   ├── user.py       # User routes
│   ├── buyer.py      # Buyer routes
│   ├── admin.py      # Admin routes
│   └── waste.py      # Waste routes
├── main.py           # FastAPI application entry point
├── .env              # Environment variables
└── requirements.txt  # Python dependencies
```

## How to Run the Project

### 1. Prerequisites
Make sure you have the following installed:
- **Python 3.8+**
- **PostgreSQL** (running on localhost:5432)
- **pip** (Python package manager)

### 2. Setup Database
First, create a PostgreSQL database:
```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE waste_management;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE waste_management TO username;
\q
```

### 3. Configure Environment
The `.env` file already contains the necessary configuration:
```env
DATABASE_URL=postgresql://trash_uqbi_user:L5mknKzqSwmis0zlHc2VZBkl16mEqRqI@dpg-d33bp8ndiees739e5tlg-a.oregon-postgres.render.com/trash_uqbi
SECRET_KEY=SvBYXkQ5ZQyRDbS16cg8Y-t7vwYf5CO6YbYSDR2WcZM
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300

# Email Configuration (Update these for email verification)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM_NAME=Smart Waste Management System
```

**For Email Verification to work, update these settings:**
- `EMAIL_USERNAME`: Your Gmail address
- `EMAIL_PASSWORD`: Your Gmail App Password (not regular password)
- To get Gmail App Password: Go to Google Account → Security → 2-Step Verification → App passwords

### 4. Install Dependencies
```bash
cd /home/zoro/sih/backend
pip install -r requirements.txt
```

### 5. Start the API Server
```bash
python main.py
```

The server will start on `http://localhost:8000`

## 📖 API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **API Root**: `http://localhost:8000/`

## 🧪 Testing the APIs

### Method 1: Automated Test Script
Run the comprehensive test script that tests all endpoints:
```bash
# Make sure the server is running first
python test_api.py
```

This script will:
- Test all authentication endpoints
- Register users and buyers
- Test device registration
- Upload waste data
- Test all user/buyer/admin endpoints
- Provide detailed results

### Method 2: Manual Testing with curl

#### Authentication Tests
```bash
# Register a normal user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "normal_user"
  }'

# Login as admin
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@wastemanagement.com&password=admin123"
```

#### Device and Waste Tests
```bash
# Register a device (admin token required)
curl -X POST "http://localhost:8000/admin/device/register" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "SCANNER_001",
    "api_key": "SECRET_KEY_001"
  }'

# Upload waste data
curl -X POST "http://localhost:8000/waste/upload" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "SCANNER_001",
    "api_key": "SECRET_KEY_001", 
    "user_id": "USER_QR_CODE_HERE",
    "organic": 2.5,
    "recyclable": 1.8,
    "hazardous": 0.3
  }'
```

### Method 3: Using Swagger UI
1. Go to `http://localhost:8000/docs`
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## 🔑 Default Credentials

### Admin User
- **Email**: `admin@wastemanagement.com`
- **Password**: `admin123`

### Test Users (created during testing)
- **Normal User**: `john@example.com` / `password123`
- **Buyer**: `jane@recycling.com` / `buyer123`

## 📋 API Endpoints Overview

### Authentication (`/auth/`)
- `POST /auth/register` - Register normal user or buyer
- `POST /auth/send-otp` - Send 4-digit OTP to email for verification
- `POST /auth/verify-otp` - Verify OTP and activate email
- `POST /auth/resend-otp` - Resend OTP if needed
- `POST /auth/login` - Login (returns JWT token, requires verified email)
- `GET /auth/me` - Get current user info

### User Routes (`/user/`)
- `GET /user/waste` - Get waste history
- `GET /user/rewards` - Get total rewards
- `GET /user/qrcode` - Get QR code
- `GET /user/stats` - Get user statistics

### Buyer Routes (`/buyer/`)
- `GET /buyer/recyclables` - Get available recyclable waste
- `GET /buyer/stats` - Get recyclable waste statistics

### Admin Routes (`/admin/`)
- `GET /admin/overview` - Get waste statistics
- `GET /admin/users` - List all users
- `GET /admin/devices` - List all devices
- `POST /admin/device/register` - Register new device
- `PUT /admin/device/{device_id}/deactivate` - Deactivate device
- `GET /admin/user/{user_id}` - Get user by ID
- `DELETE /admin/user/{user_id}` - Delete user

### Waste Routes (`/waste/`)
- `POST /waste/upload` - Upload waste data from devices
- `GET /waste/{waste_id}` - Get waste data by ID

## 🔐 Email Verification Process

1. **User Registration**: User registers with email and phone number
2. **Send OTP**: POST to `/auth/send-otp` with email to receive 4-digit code
3. **Verify Email**: POST to `/auth/verify-otp` with email and OTP code
4. **Login**: Only verified users can login (admins are exempt)

### Email Verification Flow Example:
```bash
# 1. Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_no": "+1234567890",
    "password": "password123",
    "role": "normal_user"
  }'

# 2. Send OTP
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'

# 3. Verify OTP (check your email for 4-digit code)
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp_code": "1234"
  }'

# 4. Now you can login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=password123"
```

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Make sure PostgreSQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Port Already in Use**
   ```bash
   # Kill process on port 8000
   sudo lsof -t -i tcp:8000 | xargs kill -9
   ```

3. **Module Import Errors**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

4. **Permission Denied**
   ```bash
   chmod +x setup.sh
   chmod +x test_api.py
   ```

### Database Reset
If you need to reset the database:
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Drop and recreate database
DROP DATABASE waste_management;
CREATE DATABASE waste_management;
\q

# Restart the API server
python main.py
```

## 📊 Expected Test Results

When running `python test_api.py`, you should see:
```
🧪 Starting API Tests for Smart Waste Management System
============================================================
✅ PASS Health Check - Status: 200
✅ PASS Root Endpoint - Status: 200
✅ PASS Admin Login - Status: 200
✅ PASS User Registration - Status: 201
✅ PASS Buyer Registration - Status: 201
✅ PASS User Login - Status: 200
✅ PASS Buyer Login - Status: 200
✅ PASS Device Registration - Status: 201
✅ PASS Waste Upload - Status: 201
✅ PASS User Waste History - Status: 200
✅ PASS User Rewards - Status: 200
✅ PASS User QR Code - Status: 200
✅ PASS Buyer Recyclables - Status: 200
✅ PASS Admin Overview - Status: 200
✅ PASS Admin Users List - Status: 200
✅ PASS Admin Devices List - Status: 200
============================================================
🏁 Tests completed: 16/16 passed
🎉 All tests passed! API is working correctly.
```

## 🚀 Next Steps

1. **Frontend Integration**: Use the API endpoints in your frontend app
2. **Hardware Integration**: Configure your scanner devices to use the `/waste/upload` endpoint
3. **Production Setup**: Update environment variables for production
4. **Monitoring**: Add logging and monitoring for production use

For more details, check the Swagger documentation at `http://localhost:8000/docs`!

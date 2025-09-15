"""
Database models and utilities for PostgreSQL
"""
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime

class UserRole(str, Enum):
    normal_user = "normal_user"
    buyer = "buyer"
    admin = "admin"

class DatabaseQueries:
    """Collection of SQL queries for database operations."""
    
    # User queries
    """
Simple database operations
"""
from config.database import execute_query

class User:
    @staticmethod
    def create(name, email, phone_no, password, role='normal_user', qr_code=None, is_email_verified=False):
        """Create a new user."""
        # Admin users should have email verified by default
        if role == 'admin':
            is_email_verified = True
            
        query = """
        INSERT INTO users (name, email, phone_no, password, role, qr_code, is_email_verified)
        VALUES (%(name)s, %(email)s, %(phone_no)s, %(password)s, %(role)s, %(qr_code)s, %(is_email_verified)s)
        RETURNING *
        """
        params = {
            'name': name,
            'email': email,
            'phone_no': phone_no,
            'password': password,
            'role': role,
            'qr_code': qr_code,
            'is_email_verified': is_email_verified
        }
        return execute_query(query, params, fetch='one')
    
    @staticmethod
    def get_by_email(email):
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = %(email)s"
        return execute_query(query, {'email': email}, fetch='one')
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        query = "SELECT * FROM users WHERE id = %(id)s"
        return execute_query(query, {'id': user_id}, fetch='one')
    
    @staticmethod
    def verify_email(user_id):
        """Mark user email as verified."""
        query = "UPDATE users SET is_email_verified = TRUE WHERE id = %(id)s"
        return execute_query(query, {'id': user_id})
    
    @staticmethod
    def get_all():
        """Get all users."""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        return execute_query(query, fetch='all')

class OTP:
    @staticmethod
    def create(user_id, email, otp_code, expires_at):
        """Create OTP record."""
        query = """
        INSERT INTO otp_verifications (user_id, email, otp_code, expires_at)
        VALUES (%(user_id)s, %(email)s, %(otp_code)s, %(expires_at)s)
        """
        params = {
            'user_id': user_id,
            'email': email,
            'otp_code': otp_code,
            'expires_at': expires_at
        }
        return execute_query(query, params)
    
    @staticmethod
    def verify(email, otp_code):
        """Verify OTP."""
        query = """
        SELECT * FROM otp_verifications 
        WHERE email = %(email)s AND otp_code = %(otp_code)s 
        AND is_used = FALSE AND expires_at > NOW()
        """
        return execute_query(query, {'email': email, 'otp_code': otp_code}, fetch='one')
    
    @staticmethod
    def mark_used(otp_id):
        """Mark OTP as used."""
        query = "UPDATE otp_verifications SET is_used = TRUE WHERE id = %(id)s"
        return execute_query(query, {'id': otp_id})

class WasteData:
    @staticmethod
    def create(user_id, device_id, organic_weight, recyclable_weight, hazardous_weight):
        """Create waste data record."""
        query = """
        INSERT INTO waste_data (user_id, device_id, organic_weight, recyclable_weight, hazardous_weight)
        VALUES (%(user_id)s, %(device_id)s, %(organic_weight)s, %(recyclable_weight)s, %(hazardous_weight)s)
        RETURNING *
        """
        params = {
            'user_id': user_id,
            'device_id': device_id,
            'organic_weight': organic_weight,
            'recyclable_weight': recyclable_weight,
            'hazardous_weight': hazardous_weight
        }
        return execute_query(query, params, fetch='one')
    
    @staticmethod
    def get_by_user(user_id):
        """Get waste data by user."""
        query = "SELECT * FROM waste_data WHERE user_id = %(user_id)s ORDER BY timestamp DESC"
        return execute_query(query, {'user_id': user_id}, fetch='all')

class Device:
    @staticmethod
    def get_by_device_id(device_id):
        """Get device by device_id."""
        query = "SELECT * FROM devices WHERE device_id = %(device_id)s"
        return execute_query(query, {'device_id': device_id}, fetch='one')
    
    @staticmethod
    def verify_api_key(device_id, api_key):
        """Verify device API key."""
        query = "SELECT * FROM devices WHERE device_id = %(device_id)s AND api_key = %(api_key)s"
        return execute_query(query, {'device_id': device_id, 'api_key': api_key}, fetch='one')
    
    GET_USER_BY_EMAIL = """
        SELECT id, name, email, phone_no, password, role, qr_code, rewards, is_email_verified, created_at
        FROM users WHERE email = %(email)s
    """
    
    GET_USER_BY_ID = """
        SELECT id, name, email, phone_no, role, qr_code, rewards, is_email_verified, created_at
        FROM users WHERE id = %(user_id)s
    """
    
    GET_USER_BY_QR = """
        SELECT id, name, email, phone_no, role, qr_code, rewards, is_email_verified, created_at
        FROM users WHERE qr_code = %(qr_code)s
    """
    
    GET_USER_BY_PHONE = """
        SELECT id FROM users WHERE phone_no = %(phone_no)s
    """
    
    UPDATE_USER_QR_CODE = """
        UPDATE users SET qr_code = %(qr_code)s WHERE id = %(user_id)s
    """
    
    UPDATE_USER_EMAIL_VERIFIED = """
        UPDATE users SET is_email_verified = TRUE WHERE email = %(email)s
    """
    
    UPDATE_USER_REWARDS = """
        UPDATE users SET rewards = rewards + %(points)s WHERE id = %(user_id)s
    """
    
    GET_ALL_USERS = """
        SELECT id, name, email, phone_no, role, qr_code, rewards, is_email_verified, created_at
        FROM users ORDER BY created_at DESC
    """
    
    DELETE_USER = """
        DELETE FROM users WHERE id = %(user_id)s
    """
    
    # OTP queries
    CREATE_OTP = """
        INSERT INTO otp_verifications (user_id, email, otp_code, expires_at)
        VALUES (%(user_id)s, %(email)s, %(otp_code)s, %(expires_at)s)
        RETURNING id
    """
    
    GET_VALID_OTP = """
        SELECT id, user_id, email FROM otp_verifications 
        WHERE email = %(email)s AND otp_code = %(otp_code)s 
        AND is_used = FALSE AND expires_at > NOW()
        ORDER BY created_at DESC LIMIT 1
    """
    
    MARK_OTP_USED = """
        UPDATE otp_verifications SET is_used = TRUE WHERE id = %(otp_id)s
    """
    
    DELETE_USER_OTPS = """
        DELETE FROM otp_verifications WHERE user_id = %(user_id)s
    """
    
    # Device queries
    CREATE_DEVICE = """
        INSERT INTO devices (device_id, api_key, is_active)
        VALUES (%(device_id)s, %(api_key)s, %(is_active)s)
        RETURNING id, device_id, is_active, created_at
    """
    
    GET_DEVICE_BY_ID = """
        SELECT id, device_id, is_active, created_at FROM devices WHERE device_id = %(device_id)s
    """
    
    GET_ALL_DEVICES = """
        SELECT id, device_id, is_active, created_at FROM devices ORDER BY created_at DESC
    """
    
    DEACTIVATE_DEVICE = """
        UPDATE devices SET is_active = FALSE WHERE device_id = %(device_id)s
        RETURNING id, device_id, is_active, created_at
    """
    
    # Waste data queries
    CREATE_WASTE_DATA = """
        INSERT INTO waste_data (user_id, device_id, organic_weight, recyclable_weight, hazardous_weight)
        VALUES (%(user_id)s, %(device_id)s, %(organic)s, %(recyclable)s, %(hazardous)s)
        RETURNING id, user_id, device_id, organic_weight, recyclable_weight, hazardous_weight, timestamp
    """
    
    GET_WASTE_DATA_BY_ID = """
        SELECT id, user_id, device_id, organic_weight, recyclable_weight, hazardous_weight, timestamp
        FROM waste_data WHERE id = %(waste_id)s
    """
    
    GET_USER_WASTE_DATA = """
        SELECT id, organic_weight, recyclable_weight, hazardous_weight, timestamp, device_id
        FROM waste_data WHERE user_id = %(user_id)s ORDER BY timestamp DESC
    """
    
    DELETE_USER_WASTE_DATA = """
        DELETE FROM waste_data WHERE user_id = %(user_id)s
    """
    
    # Rewards queries
    CREATE_REWARD = """
        INSERT INTO rewards (user_id, points, waste_type, weight)
        VALUES (%(user_id)s, %(points)s, %(waste_type)s, %(weight)s)
        RETURNING id, points, waste_type, weight, created_at
    """
    
    GET_USER_REWARDS = """
        SELECT SUM(points) as total_points FROM rewards WHERE user_id = %(user_id)s
    """
    
    GET_USER_REWARD_BREAKDOWN = """
        SELECT waste_type, SUM(points) as total_points, SUM(weight) as total_weight
        FROM rewards WHERE user_id = %(user_id)s GROUP BY waste_type
    """
    
    DELETE_USER_REWARDS = """
        DELETE FROM rewards WHERE user_id = %(user_id)s
    """
    
    # Statistics queries
    GET_WASTE_OVERVIEW = """
        SELECT 
            COALESCE(SUM(organic_weight), 0) as total_organic,
            COALESCE(SUM(recyclable_weight), 0) as total_recyclable,
            COALESCE(SUM(hazardous_weight), 0) as total_hazardous,
            COUNT(*) as total_entries
        FROM waste_data
    """
    
    GET_USER_COUNT = """
        SELECT COUNT(*) as count FROM users WHERE role = %(role)s
    """
    
    GET_DEVICE_COUNT = """
        SELECT COUNT(*) as count FROM devices
    """
    
    GET_RECYCLABLE_STATS = """
        SELECT 
            COALESCE(SUM(recyclable_weight), 0) as total_recyclable,
            COUNT(*) as total_entries
        FROM waste_data WHERE recyclable_weight > 0
    """

def row_to_dict(cursor, row) -> Dict[str, Any]:
    """Convert database row to dictionary."""
    if row is None:
        return None
    
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

def rows_to_dict_list(cursor, rows) -> list:
    """Convert database rows to list of dictionaries."""
    if not rows:
        return []
    
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in rows]

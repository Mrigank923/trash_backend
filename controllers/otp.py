"""
OTP controller for email verification operations
"""
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.database import User, OTPVerification
from models.schemas import OTPRequest, OTPVerify, OTPResponse, EmailVerificationResponse
from helpers.email_service import email_service

class OTPController:
    
    @staticmethod
    def send_verification_otp(otp_request: OTPRequest, db: Session) -> OTPResponse:
        """Send OTP for email verification."""
        # Check if user exists with this email
        user = db.query(User).filter(User.email == otp_request.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found"
            )
        
        # Check if email is already verified
        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )
        
        # Generate OTP
        otp_code = email_service.generate_otp()
        expires_at = email_service.get_otp_expiry_time()
        
        # Invalidate any existing OTPs for this user
        db.query(OTPVerification).filter(
            OTPVerification.user_id == user.id,
            OTPVerification.is_used == False
        ).update({"is_used": True})
        
        # Create new OTP record
        otp_verification = OTPVerification(
            user_id=user.id,
            email=otp_request.email,
            otp_code=otp_code,
            expires_at=expires_at,
            is_used=False
        )
        
        db.add(otp_verification)
        db.commit()
        
        # Send email
        email_sent = email_service.send_otp_email(
            to_email=otp_request.email,
            name=user.name,
            otp_code=otp_code
        )
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email. Please try again."
            )
        
        return OTPResponse(
            message="OTP sent successfully to your email",
            expires_in_minutes=10
        )
    
    @staticmethod
    def verify_otp(otp_verify: OTPVerify, db: Session) -> EmailVerificationResponse:
        """Verify OTP and mark email as verified."""
        # Find user
        user = db.query(User).filter(User.email == otp_verify.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found"
            )
        
        # Check if email is already verified
        if user.is_email_verified:
            return EmailVerificationResponse(
                message="Email is already verified",
                is_verified=True
            )
        
        # Find valid OTP
        otp_record = db.query(OTPVerification).filter(
            OTPVerification.user_id == user.id,
            OTPVerification.email == otp_verify.email,
            OTPVerification.otp_code == otp_verify.otp_code,
            OTPVerification.is_used == False,
            OTPVerification.expires_at > datetime.utcnow()
        ).first()
        
        if not otp_record:
            # Check if OTP exists but is expired or used
            expired_otp = db.query(OTPVerification).filter(
                OTPVerification.user_id == user.id,
                OTPVerification.email == otp_verify.email,
                OTPVerification.otp_code == otp_verify.otp_code
            ).first()
            
            if expired_otp:
                if expired_otp.is_used:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="OTP has already been used"
                    )
                elif expired_otp.expires_at <= datetime.utcnow():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="OTP has expired. Please request a new one."
                    )
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code"
            )
        
        # Mark OTP as used
        otp_record.is_used = True
        
        # Mark user email as verified
        user.is_email_verified = True
        
        db.commit()
        
        return EmailVerificationResponse(
            message="Email verified successfully",
            is_verified=True
        )
    
    @staticmethod
    def resend_otp(otp_request: OTPRequest, db: Session) -> OTPResponse:
        """Resend OTP for email verification."""
        return OTPController.send_verification_otp(otp_request, db)

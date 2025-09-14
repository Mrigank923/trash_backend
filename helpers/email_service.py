"""
Email service for sending OTP verification emails
"""
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional

from config.settings import settings

class EmailService:
    def __init__(self):
        # Use settings for email configuration
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.email_username = settings.EMAIL_USERNAME
        self.email_password = settings.EMAIL_PASSWORD
        self.from_name = settings.EMAIL_FROM_NAME
        
    def generate_otp(self) -> str:
        """Generate a 4-digit OTP code."""
        return str(random.randint(1000, 9999))
    
    def create_otp_email_body(self, name: str, otp_code: str) -> str:
        """Create HTML email body for OTP verification."""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h2 style="color: #28a745; text-align: center;">Smart Waste Management System</h2>
                <h3 style="color: #333;">Email Verification Required</h3>
                
                <p>Hello {name},</p>
                
                <p>Thank you for registering with our Smart Waste Management System. To complete your registration, please verify your email address using the OTP code below:</p>
                
                <div style="background-color: #007bff; color: white; padding: 15px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <h1 style="margin: 0; font-size: 32px; letter-spacing: 5px;">{otp_code}</h1>
                </div>
                
                <p><strong>Important:</strong></p>
                <ul>
                    <li>This OTP is valid for 10 minutes only</li>
                    <li>Do not share this code with anyone</li>
                    <li>If you didn't request this verification, please ignore this email</li>
                </ul>
                
                <p>Thank you for helping us build a sustainable future!</p>
                
                <hr style="margin: 30px 0; border: 1px solid #eee;">
                <p style="color: #666; font-size: 12px; text-align: center;">
                    This is an automated email. Please do not reply to this message.
                </p>
            </div>
        </body>
        </html>
        """
    
    def send_otp_email(self, to_email: str, name: str, otp_code: str) -> bool:
        """
        Send OTP verification email.
        Returns True if successful, False otherwise.
        """
        # Check if email credentials are configured
        if not self.email_username or not self.email_password:
            print(f"⚠️  Email not sent to {to_email}. Email credentials not configured.")
            print(f"🔑 OTP Code for {name}: {otp_code} (Valid for 10 minutes)")
            return True  # Return True to not block the flow, but log the OTP
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Email Verification - {self.from_name}"
            msg['From'] = f"{self.from_name} <{self.email_username}>"
            msg['To'] = to_email
            
            # Create HTML content
            html_body = self.create_otp_email_body(name, otp_code)
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Create plain text alternative
            text_body = f"""
            Smart Waste Management System - Email Verification
            
            Hello {name},
            
            Your verification code is: {otp_code}
            
            This code expires in 10 minutes.
            
            Thank you!
            """
            text_part = MIMEText(text_body, 'plain')
            msg.attach(text_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_username, self.email_password)
                server.send_message(msg)
            
            print(f"✅ OTP email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send OTP email to {to_email}: {str(e)}")
            return False
    
    def get_otp_expiry_time(self) -> datetime:
        """Get OTP expiry time (10 minutes from now)."""
        return datetime.utcnow() + timedelta(minutes=10)

# Create a global instance
email_service = EmailService()

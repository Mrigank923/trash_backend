"""
Email sending utilities
"""
import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str):
    """Send email to user. For now, just print to console."""
    print(f"""
📧 EMAIL SENT:
To: {to_email}
Subject: {subject}
Body: {body}
""")
    logger.info(f"Email sent to {to_email}")
    return True

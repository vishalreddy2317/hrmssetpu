"""
✅ Email utilities
"""
from typing import List, Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(
        self, 
        smtp_server: str = None, 
        port: int = None, 
        username: str = None, 
        password: str = None
    ):
        """
        Initialize email service
        Falls back to settings if params not provided
        """
        self.smtp_server = smtp_server or settings.EMAIL_SERVER
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_FROM
        self.password = password or settings.EMAIL_PASSWORD
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        body: str, 
        is_html: bool = False
    ) -> bool:
        """Send an email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_notification(self, to_email: str, title: str, message: str) -> bool:
        """Send a notification email"""
        subject = f"Notification: {title}"
        body = f"""
        Hello,
        
        {message}
        
        Best regards,
        Hospital Management System
        """
        return self.send_email(to_email, subject, body)
    
    def send_appointment_reminder(
        self, 
        to_email: str, 
        patient_name: str, 
        appointment_date: str, 
        doctor_name: str
    ) -> bool:
        """Send appointment reminder email"""
        subject = "Appointment Reminder"
        body = f"""
        Dear {patient_name},
        
        This is a reminder for your appointment with Dr. {doctor_name} 
        scheduled for {appointment_date}.
        
        Please arrive 15 minutes before your scheduled time.
        
        Best regards,
        Hospital Management System
        """
        return self.send_email(to_email, subject, body)


# ✅ Global email service instance
email_service = EmailService()
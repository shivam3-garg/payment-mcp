import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional
from utils.base_service import BaseService

logger = logging.getLogger(__name__)

class EmailServiceError(Exception):
    """Base exception for EmailService"""
    pass

class EmailService(BaseService):
    def __init__(self):
        super().__init__()
        self._load_config()
        self._validate_config()

    def _load_config(self):
        """Load email configuration from environment"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_app_password = os.getenv('SMTP_APP_PASSWORD')

    def _validate_config(self):
        """Validate email configuration"""
        if not all([self.smtp_username, self.smtp_app_password]):
            logger.error("Email configuration is missing")
            raise EmailServiceError(
                "Email configuration is missing. Please set SMTP_USERNAME and SMTP_APP_PASSWORD environment variables."
            )

    def send_email(
        self, 
        subject: str, 
        from_email: str, 
        to_email: str, 
        message: str,
        html_message: Optional[str] = None
    ) -> str:
        """
        Send email using SMTP with app password
        
        Args:
            subject: Email subject
            from_email: Sender email address
            to_email: Recipient email address
            message: Plain text message
            html_message: Optional HTML message
        """
        try:
            msg = MIMEMultipart('alternative')
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email

            # Add plain text part
            msg.attach(MIMEText(message, 'plain'))

            # Add HTML part if provided
            if html_message:
                msg.attach(MIMEText(html_message, 'html'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_app_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return f"Email sent successfully from {from_email} to {to_email}"

        except smtplib.SMTPException as e:
            error_msg = f"SMTP error while sending email: {str(e)}"
            logger.error(error_msg)
            raise EmailServiceError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error while sending email: {str(e)}"
            logger.error(error_msg)
            raise EmailServiceError(error_msg) from e 
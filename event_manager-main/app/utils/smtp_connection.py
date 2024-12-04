# smtp_client.py
from builtins import Exception, int, str
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings
import logging
from contextlib import contextmanager

class SMTPClient:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    @contextmanager
    def _get_server(self):
        """Context manager for SMTP server connection."""
        server = smtplib.SMTP(self.server, self.port)
        try:
            server.starttls()
            server.login(self.username, self.password)
            yield server
        finally:
            server.quit()

    def send_email(self, subject: str, html_content: str, recipient: str):
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = recipient
            message.attach(MIMEText(html_content, 'html'))

            with self._get_server() as server:
                server.sendmail(self.username, recipient, message.as_string())
            logging.info(f"Email sent to {recipient}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            raise

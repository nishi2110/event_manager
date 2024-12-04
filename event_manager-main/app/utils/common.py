import logging.config
import os
from app.dependencies import get_settings
from datetime import datetime
import re
import random
import string
from html import escape
from urllib.parse import urlparse

settings = get_settings()
def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    This ensures standardized logging across the entire application.
    """
    # Construct the path to 'logging.conf', assuming it's in the project's root.
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    # Normalize the path to handle any '..' correctly.
    normalized_path = os.path.normpath(logging_config_path)
    # Apply the logging configuration.
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)

def format_datetime(dt: datetime) -> str:
    """Format a datetime object to string."""
    if not isinstance(dt, datetime):
        raise ValueError("Input must be a datetime object")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_url(url: str) -> bool:
    """Validate if a given string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def sanitize_input(text: str) -> str:
    """Sanitize input text by removing HTML tags and escaping special characters."""
    if text is None:
        return ""
        
    # First remove HTML tags
    clean_text = re.sub(r'<[^>]*>', '', text)
    # Then escape special characters
    return clean_text

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length."""
    if not isinstance(length, int) or length < 1:
        raise ValueError("Length must be a positive integer")
    
    # Use a combination of letters and numbers
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
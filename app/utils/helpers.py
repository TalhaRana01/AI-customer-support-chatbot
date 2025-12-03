from datetime import datetime
from typing import Optional
import re


def validate_email(email: str) -> bool:
    """
    Email validation
    
    Args:
        email: Email address
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_filename(filename: str) -> str:
    """
    Filename ko sanitize karta hai (special characters remove)
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove special characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Datetime ko formatted string mein convert karta hai
    
    Args:
        dt: Datetime object
        format: Format string
    
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format)


def calculate_duration(start: datetime, end: Optional[datetime] = None) -> float:
    """
    Duration calculate karta hai (minutes mein)
    
    Args:
        start: Start datetime
        end: End datetime (default: current time)
    
    Returns:
        Duration in minutes
    """
    if end is None:
        end = datetime.utcnow()
    
    duration = end - start
    return duration.total_seconds() / 60


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Text ko truncate karta hai
    
    Args:
        text: Original text
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."
"""
✅ General helper functions
"""
import logging
from typing import Any, Dict, List
from datetime import datetime, date
from decimal import Decimal


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Set up a logger with consistent formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def format_date(value: date) -> str:
    """Format date to ISO string"""
    return value.isoformat() if value else None


def parse_date(value: str) -> date:
    """Parse ISO string to date"""
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def format_currency(amount: Decimal | float, symbol: str = "$") -> str:
    """Format currency amount"""
    return f"{symbol}{amount:,.2f}"


def paginate_data(data: List[Any], page: int, size: int) -> Dict[str, Any]:
    """
    Paginate a list of data
    
    Args:
        data: List of items to paginate
        page: Page number (1-indexed)
        size: Items per page
    
    Returns:
        Dict with items, total, page, size, pages
    """
    total = len(data)
    pages = (total + size - 1) // size  # Ceiling division
    
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_items = data[start_idx:end_idx]
    
    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
"""Utility functions for password validation."""
import re
from config import settings


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
    
    if settings.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if settings.REQUIRE_DIGITS and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if settings.REQUIRE_SPECIAL_CHARS and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)"
    
    return True, ""


def sanitize_update_data(data: dict) -> dict:
    """
    Sanitize update data to prevent NoSQL injection.
    
    Args:
        data: Data dictionary to sanitize
        
    Returns:
        Sanitized data dictionary
    """
    # Remove sensitive fields that shouldn't be updated directly
    forbidden_fields = {'_id', 'password', 'created_at'}
    return {k: v for k, v in data.items() if k not in forbidden_fields}

"""User data model and helper functions."""
from datetime import datetime
from typing import Dict, Any


def user_helper(user: Dict[str, Any]) -> Dict[str, Any]:
    """Transform MongoDB user document to response format (excludes password)."""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "is_active": user.get("is_active", True),
        "mobile": user.get("mobile"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
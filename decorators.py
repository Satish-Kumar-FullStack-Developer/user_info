"""Decorators for route handling."""
import functools
import logging
from typing import Callable, Any
from fastapi import HTTPException
from exceptions import UserNotFoundError, InvalidUserIDError, DuplicateUserError, InvalidUserDataError

logger = logging.getLogger(__name__)


def handle_exceptions(func: Callable) -> Callable:
    """
    Decorator to handle service exceptions and convert to HTTP exceptions.
    
    Args:
        func: Async route handler function
        
    Returns:
        Wrapped function with exception handling
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except InvalidUserIDError as e:
            logger.warning(f"Invalid user ID: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except InvalidUserDataError as e:
            logger.warning(f"Invalid user data: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except UserNotFoundError as e:
            logger.warning(f"User not found: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except DuplicateUserError as e:
            logger.warning(f"Duplicate user: {str(e)}")
            raise HTTPException(status_code=409, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")
    
    return wrapper

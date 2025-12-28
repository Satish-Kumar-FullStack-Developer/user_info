"""User service for business logic."""
from repositories.user_repository import UserRepository
from models.user_model import user_helper
from schemas.user_schema import UserCreateSchema, UserResponseSchema
from exceptions import UserNotFoundError, InvalidUserIDError, DuplicateUserError, InvalidUserDataError
from utils import validate_password_strength, sanitize_update_data
from datetime import datetime
from typing import Dict, Any, Optional
import bcrypt
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserService:
    """Service class for user business logic."""

    def __init__(self):
        """Initialize with repository."""
        self.repo = UserRepository()

    async def add_user(self, user: UserCreateSchema) -> Dict[str, Any]:
        """
        Add a new user to the database.
        
        Args:
            user: UserCreateSchema instance
            
        Returns:
            User response dictionary
            
        Raises:
            InvalidUserDataError: If password validation fails
            DuplicateUserError: If username or email already exists
        """
        # Validate password strength
        is_valid, error_msg = validate_password_strength(user.password)
        if not is_valid:
            logger.warning(f"Password validation failed: {error_msg}")
            raise InvalidUserDataError(error_msg)
        
        user_data = {
            "username": user.username.strip().lower(),
            "email": user.email.strip().lower(),
            "password": hash_password(user.password),
            "full_name": user.full_name.strip() if user.full_name else None,
            "mobile": user.mobile,
            "is_active": user.is_active,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.repo.create(user_data)
        logger.info(f"User created: {user_data['username']}")
        return user_helper(result)

    async def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID as string
            
        Returns:
            User response dictionary
            
        Raises:
            InvalidUserIDError: If user ID format is invalid
            UserNotFoundError: If user not found
        """
        if not ObjectId.is_valid(user_id):
            raise InvalidUserIDError("Invalid user ID format")
        
        user = await self.repo.get_by_id(user_id)
        
        if not user:
            raise UserNotFoundError("User not found")
        
        return user_helper(user)

    async def get_user_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get user by username.
        
        Args:
            username: Username string
            
        Returns:
            User response dictionary
            
        Raises:
            UserNotFoundError: If user not found
        """
        user = await self.repo.get_by_username(username)
        
        if not user:
            raise UserNotFoundError("User not found")
        
        return user_helper(user)

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user information.
        
        Args:
            user_id: User ID as string
            update_data: Dictionary of fields to update
            
        Returns:
            Updated user response dictionary
            
        Raises:
            InvalidUserIDError: If user ID format is invalid
            UserNotFoundError: If user not found
        """
        if not ObjectId.is_valid(user_id):
            raise InvalidUserIDError("Invalid user ID format")
        
        # Sanitize update data to prevent injection attacks
        update_data = sanitize_update_data(update_data)
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        user = await self.repo.update(user_id, update_data)
        
        if not user:
            raise UserNotFoundError("User not found")
        
        logger.info(f"User updated: {user_id}")
        return user_helper(user)

    async def delete_user(self, user_id: str) -> Dict[str, str]:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID as string
            
        Returns:
            Success message
            
        Raises:
            InvalidUserIDError: If user ID format is invalid
            UserNotFoundError: If user not found
        """
        if not ObjectId.is_valid(user_id):
            raise InvalidUserIDError("Invalid user ID format")
        
        deleted = await self.repo.delete(user_id)
        
        if not deleted:
            raise UserNotFoundError("User not found")
        
        return {"message": "User deleted successfully"}
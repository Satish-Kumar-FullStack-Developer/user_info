"""User repository for database operations."""
from bson import ObjectId
from services.db import get_user_collection
from typing import Optional, Dict, Any
from exceptions import DuplicateUserError


class UserRepository:
    """Repository class for user database operations."""

    def __init__(self):
        """Initialize with user collection."""
        self.collection = get_user_collection()

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user after checking for duplicates.
        
        Args:
            data: User data dictionary
            
        Returns:
            Created user document
            
        Raises:
            DuplicateUserError: If user with same email/username exists
        """
        # Check for duplicate username or email
        existing_user = await self.collection.find_one({
            "$or": [
                {"email": data["email"]},
                {"username": data["username"]}
            ]
        })

        if existing_user:
            raise DuplicateUserError("User with this email or username already exists")

        result = await self.collection.insert_one(data)
        user = await self.collection.find_one({"_id": result.inserted_id})
        return user

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID as string
            
        Returns:
            User document or None if not found
        """
        if not ObjectId.is_valid(user_id):
            return None

        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user by username.
        
        Args:
            username: Username string
            
        Returns:
            User document or None if not found
        """
        return await self.collection.find_one({"username": username})

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: Email string
            
        Returns:
            User document or None if not found
        """
        return await self.collection.find_one({"email": email})

    async def update(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user by ID.
        
        Args:
            user_id: User ID as string
            data: Data to update
            
        Returns:
            Updated user document or None if not found
        """
        if not ObjectId.is_valid(user_id):
            return None

        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": data},
            return_document=True
        )
        return result

    async def delete(self, user_id: str) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID as string
            
        Returns:
            True if deleted, False otherwise
        """
        if not ObjectId.is_valid(user_id):
            return False

        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
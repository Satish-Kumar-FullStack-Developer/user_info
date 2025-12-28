"""User routes for API endpoints."""
from fastapi import APIRouter, status
from schemas.user_schema import (
    UserCreateSchema, 
    UserResponseSchema, 
    UserApiResponse,
    UserUpdateSchema
)
from services.user_service import UserService
from decorators import handle_exceptions
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])
user_service = UserService()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserApiResponse,
    summary="Create a new user",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User already exists"}
    }
)
@handle_exceptions
async def create_user(user: UserCreateSchema):
    """
    Create a new user.
    
    - **username**: Unique username (3-50 chars)
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, uppercase, digit, special char)
    - **full_name**: Optional full name
    - **mobile**: Optional 10-digit phone number
    """
    new_user = await user_service.add_user(user)
    logger.info(f"New user created: {user.username}")
    return {
        "status": "success",
        "message": "User created successfully",
        "data": new_user
    }


@router.get(
    "/{user_id}", 
    response_model=UserApiResponse,
    summary="Get user by ID",
    responses={
        200: {"description": "User found"},
        400: {"description": "Invalid user ID format"},
        404: {"description": "User not found"}
    }
)
@handle_exceptions
async def get_user(user_id: str):
    """
    Get user by MongoDB ObjectId.
    
    - **user_id**: MongoDB ObjectId as string (24 hex characters)
    """
    logger.info(f"Fetching user: {user_id}")
    user = await user_service.get_user_by_id(user_id)
    return {
        "status": "success",
        "data": user
    }


@router.get(
    "/username/{username}", 
    response_model=UserApiResponse,
    summary="Get user by username",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
@handle_exceptions
async def get_user_by_username(username: str):
    """
    Get user by username.
    
    - **username**: Username string
    """
    logger.info(f"Fetching user by username: {username}")
    user = await user_service.get_user_by_username(username)
    return {
        "status": "success",
        "data": user
    }


@router.put(
    "/{user_id}", 
    response_model=UserApiResponse,
    summary="Update user information",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Invalid user ID format"},
        404: {"description": "User not found"}
    }
)
@handle_exceptions
async def update_user(user_id: str, update_data: UserUpdateSchema):
    """
    Update user information.
    
    - **user_id**: MongoDB ObjectId as string
    - **update_data**: Fields to update (full_name, mobile, is_active)
    """
    logger.info(f"Updating user: {user_id}")
    updated_user = await user_service.update_user(user_id, update_data.model_dump(exclude_unset=True))
    return {
        "status": "success",
        "message": "User updated successfully",
        "data": updated_user
    }


@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by ID",
    responses={
        204: {"description": "User deleted successfully"},
        400: {"description": "Invalid user ID format"},
        404: {"description": "User not found"}
    }
)
@handle_exceptions
async def delete_user(user_id: str):
    """
    Delete user by MongoDB ObjectId.
    
    - **user_id**: MongoDB ObjectId as string
    """
    logger.info(f"Deleting user: {user_id}")
    result = await user_service.delete_user(user_id)
    return result
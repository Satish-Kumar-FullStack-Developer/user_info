"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class UserCreateSchema(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 chars)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 chars)")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    mobile: Optional[str] = Field(None, pattern=r"^\d{10}$", description="10-digit phone number")
    is_active: Optional[bool] = Field(True, description="User active status")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "user@example.com",
                "password": "SecurePass123!",
                "full_name": "user name",
                "mobile": "1234567890",
                "is_active": True
            }
        }


class UserResponseSchema(BaseModel):
    """Schema for user response (excludes password)."""
    id: str = Field(..., description="User ID (MongoDB ObjectId as string)")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full name")
    is_active: bool = Field(True, description="User active status")
    mobile: Optional[str] = Field(None, description="Phone number")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    status: str = Field(..., description="Response status: success or error")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[T] = Field(None, description="Response data")


class UserApiResponse(BaseModel):
    """API response for single user."""
    status: str = Field(..., description="Response status")
    message: Optional[str] = Field(None, description="Optional message")
    data: UserResponseSchema = Field(..., description="User data")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "User fetched successfully",
                "data": {
                    "id": "507f1f77bcf86cd799439011",
                    "username": "username",
                    "email": "user@example.com",
                    "full_name": "user name",
                    "is_active": True,
                    "mobile": "1234567890",
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            }
        }


class UserUpdateSchema(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    mobile: Optional[str] = Field(None, pattern=r"^\d{10}$", description="10-digit phone number")
    is_active: Optional[bool] = Field(None, description="User active status")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "user Updated",
                "mobile": "9876543210",
                "is_active": True
            }
        }
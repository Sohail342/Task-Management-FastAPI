from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for user registration"""
    name: str
    email: EmailStr
    phone_number: str
    password: str
    role: Optional[UserRole] = UserRole.EMPLOYEE


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    name: str
    email: str
    phone_number: str
    role: UserRole
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
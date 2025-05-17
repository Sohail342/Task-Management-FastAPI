from pydantic import BaseModel, EmailStr, model_validator, field_validator, Field
from typing import Optional
import re

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for user registration"""

    name: str = Field(..., min_length=5, max_length=50, examples=["John doe"])
    email: EmailStr = Field(..., max_length=100)
    phone_number: Optional[str] = Field(
        default="",
        max_length=15,
        description="Phone number must be a 10-digit number",
        examples=["03429123456"],
    )
    password: str = Field(..., min_length=8, max_length=20, examples=[""])
    confirm_password: str = Field(..., min_length=8, max_length=20, examples=[""])
    role: Optional[UserRole] = Field(
        default=UserRole.EMPLOYEE,
        description="Select the user role"
    )

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        """Ensure that password and confirm_password match"""
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("Passwords do not match")
        
        if not password:
            raise ValueError("Password cannot be empty")

        # Check if password contains at least one digit, one uppercase letter, and one lowercase letter
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        return values
    

    @field_validator("phone_number")
    def validate_pakistani_phone(cls, v):
        # Remove spaces
        v_clean = v.replace(" ", "")

        # Match +923XXXXXXXXX, 03XXXXXXXXX
        if not re.match(r"^(?:\+92|0)3[0-4][0-9]{8}$", v_clean):
            raise ValueError("Invalid Pakistani phone number format")
        return v_clean


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
        
        

class EmployeeResponse(BaseModel):
    """Schema for employee response"""

    id: int
    name: str
    email: str
    phone_number: str
    role: UserRole = UserRole.EMPLOYEE
    is_active: bool

    class Config:
        from_attributes = True

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse, EmployeeResponse
from app.core.dependencies import get_current_user, role_required
from app.services.auth_service import (
    create_new_user_by_email,
    authenticate_user,
    recreate_access_token,
    get_all_users,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    return await create_new_user_by_email(user_data=user_data, db=db)


@router.post("/signin", response_model=TokenResponse)
async def signin(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await authenticate_user(user_data=user_data, db=db)


refresh_scheme = HTTPBearer(auto_error=False)


@router.post("/refresh")
async def refresh(credentials: HTTPAuthorizationCredentials = Depends(refresh_scheme)):
    return await recreate_access_token(credentials=credentials)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout a user by revoking their JWT token"""
    return {"message": "Successfully logged out"}


@router.get("/employees", response_model=list[EmployeeResponse])
async def get_employees(
    current_user: User = Depends(role_required(["Admin", "Supervisor"])),
    db: AsyncSession = Depends(get_db)
):
    """Get all employees"""
    return await get_all_users(db=db)
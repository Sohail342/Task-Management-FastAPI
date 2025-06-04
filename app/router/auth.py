from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    TokenResponse,
    UserResponse,
    EmployeeResponse,
    UserCreateByAdmin,
)
from app.core.dependencies import get_current_user, role_required
from app.services.auth_service import (
    create_new_user_by_email,
    authenticate_user,
    recreate_access_token,
    get_all_users,
    create_new_user_by_admin,
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


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile"""
    return current_user


@router.get("/employees", response_model=list[EmployeeResponse])
async def get_employees(
    current_user: User = Depends(role_required(["Admin", "Supervisor"])),
    db: AsyncSession = Depends(get_db),
):
    """Get all employees or all users if Admin"""
    return await get_all_users(db=db, current_user=current_user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(role_required(["Admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Get a user by ID"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: dict,
    current_user: User = Depends(role_required(["Admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Update a user"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    # Update user fields
    for key, value in user_data.items():
        if hasattr(user, key) and key != "id":
            if key == "password" and value:
                user.set_password(value)
            else:
                setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(role_required(["Admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Delete a user"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    # Instead of hard delete, set is_active to False
    user.is_active = False
    await db.commit()
    
    return None

@router.post("/users/create", response_model=UserResponse)
async def create_user_by_admin(
    user_data: UserCreateByAdmin,
    current_user: User = Depends(role_required(["Admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Create a new user by Admin"""
    return await create_new_user_by_admin(user_data=user_data, db=db)

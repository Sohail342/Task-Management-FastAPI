from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from jose import JWTError
from fastapi.security import HTTPAuthorizationCredentials

from app.models.user import User, UserRole
from app.schemas.auth import UserCreate, UserLogin
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import TokenResponse


async def create_new_user_by_email(
    user_data: UserCreate, db: AsyncSession
) -> User | None:
    # Check if user with the same email already exists
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    user_dict = user_data.model_dump(exclude={"confirm_password"})
    user = User(**user_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    user_data: UserLogin, db: AsyncSession
) -> TokenResponse | None:
    """Authenticate a user and return JWT tokens"""
    # Find user by email
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Verify password
    try:
        user.verify_password(user_data.password)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Create access token and refresh token
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


async def recreate_access_token(
    credentials: HTTPAuthorizationCredentials,
) -> dict | None:
    """Recreate refresh token"""
    token = credentials.credentials if credentials else None
    if token is None:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = decode_token(token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token(data={"sub": user_id})
        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


async def get_all_users(
    db: AsyncSession,
):
    """Get all users"""
    query = select(User).where(
        User.is_active.is_(True), User.role == UserRole.EMPLOYEE.value
    )
    result = await db.execute(query)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )

    return users

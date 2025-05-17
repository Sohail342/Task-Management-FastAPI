from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.user import User
from app.utils.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """
    Get the current authenticated user from the JWT token.

    Args:
        token: The JWT token from the Authorization header.
        db: The database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    payload = decode_token(token)
    try:
        user_id = int(payload.get("sub"))

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get the current active user.

    Args:
        current_user: The current authenticated user.

    Returns:
        User: The current active user.
    """
    return current_user


def role_required(role: list[str]):
    """
    Dependency to check if the user has the required role.

    Args:
        role: The required role.

    Returns:
        Callable: A function that checks the user's role.
    """

    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return current_user

    return role_checker


admin_or_supervisor = role_required(["Admin", "Supervisor"])
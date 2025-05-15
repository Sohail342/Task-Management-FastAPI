from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.core.config import get_settings

settings = get_settings()


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a new JWT access token.

    Args:
        data: The data to encode in the token.
        expires_delta: Optional expiration time delta. If not provided, default expiration time is used.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=settings.AUTHJWT_ACCESS_TOKEN_EXPIRES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTHJWT_SECRET_KEY, algorithm=settings.AUTHJWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a new JWT refresh token.

    Args:
        data: The data to encode in the token.
        expires_delta: Optional expiration time delta. If not provided, default expiration time is used.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            seconds=settings.AUTHJWT_REFRESH_TOKEN_EXPIRES
        )

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTHJWT_SECRET_KEY, algorithm=settings.AUTHJWT_ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token.

    Args:
        token: The token to decode.

    Returns:
        Dict[str, Any]: The decoded token payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token, settings.AUTHJWT_SECRET_KEY, algorithms=[settings.AUTHJWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

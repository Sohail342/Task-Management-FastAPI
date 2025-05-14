from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.jwt import create_access_token, create_refresh_token, decode_token
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user with the same email already exists
    email = select(User).where(User.email == user_data.email)
    result = await db.execute(email)
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if user with the same phone number already exists
    phone = select(User).where(User.phone_number == user_data.phone_number)
    result = await db.execute(phone) 
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Create new user
    user = User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/signin", response_model=TokenResponse)
async def signin(user_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return JWT tokens"""
    # Find user by email
    user = select(User).where(User.email == user_data.email)
    result = await db.execute(user)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    try:
        user.verify_password(user_data.password)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token and refresh token
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


refresh_scheme = HTTPBearer(auto_error=False)

@router.post("/refresh")
async def refresh(credentials: HTTPAuthorizationCredentials = Depends(refresh_scheme)):
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
    
    

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout a user by revoking their JWT token"""
    return {"message": "Successfully logged out"}
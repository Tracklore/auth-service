# Authentication service logic (signup, login, refresh, logout)
from datetime import timedelta, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_username, get_user_by_email, create_user
from app.utils.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.settings import settings
from app.schemas.user import UserResponse, Token
from fastapi import HTTPException, status
from app.crud.token import add_token_to_blacklist, is_token_blacklisted
from app.services.message_queue import message_queue_client

async def signup(db: AsyncSession, username: str, email: str, password: str):
    """User signup service."""
    # Check if user already exists
    existing_user = await get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email is already used
    existing_email = await get_user_by_email(db, email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = await create_user(db, username, email, password)
    
    # Prepare user data for the event
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    
    # Publish UserCreated event to message queue
    await message_queue_client.publish_user_created_event(user_data)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )

async def login(db: AsyncSession, username: str, password: str):
    """User login service."""
    # Get user by username
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}, 
        expires_delta=refresh_token_expires
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

async def refresh_access_token(db: AsyncSession, refresh_token: str):
    """Refresh access token using refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode refresh token
    payload = decode_token(refresh_token)
    token_type = payload.get("type")
    if token_type != "refresh":
        raise credentials_exception

    jti = payload.get("jti")
    if not jti:
        raise credentials_exception

    if await is_token_blacklisted(db, jti):
        raise credentials_exception

    username = payload.get("sub")
    user_id = payload.get("user_id")

    if not username or not user_id:
        raise credentials_exception

    # Blacklist the old refresh token
    exp = payload.get("exp")
    if exp:
        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        await add_token_to_blacklist(db, jti, expires_at)

    # Create new tokens
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)

    new_access_token = create_access_token(
        data={"sub": username, "user_id": user_id},
        expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        data={"sub": username, "user_id": user_id},
        expires_delta=refresh_token_expires
    )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

# Note: Logout is typically handled on the client side by removing the tokens
# For server-side logout, we would need to maintain a token blacklist
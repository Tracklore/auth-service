# Password hashing, JWT creation & validation helpers
from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from shared_libs import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    oauth2_scheme
)
from shared_libs.settings import SharedSettings
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud.token import is_token_blacklisted

# Load settings
settings = SharedSettings()

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> dict:
    """Get the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, settings.SECRET_KEY, settings.ALGORITHM)
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
        jti = payload.get("jti")
        if jti is None:
            raise credentials_exception
        if await is_token_blacklisted(db, jti):
            raise credentials_exception
        return payload
    except Exception as e:
        raise credentials_exception from e

def create_access_token_wrapper(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new access token using shared utility."""
    return create_access_token(
        data,
        settings.SECRET_KEY,
        settings.ALGORITHM,
        expires_delta,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

def create_refresh_token_wrapper(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new refresh token using shared utility."""
    return create_refresh_token(
        data,
        settings.SECRET_KEY,
        settings.ALGORITHM,
        expires_delta,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

def decode_token_wrapper(token: str) -> dict:
    """Decode a JWT token using shared utility."""
    return decode_token(token, settings.SECRET_KEY, settings.ALGORITHM)
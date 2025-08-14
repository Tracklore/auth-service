# API routes for login, signup, logout, refresh token, and user info
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.auth import signup, login, refresh_access_token
from app.utils.security import get_current_user, decode_token, oauth2_scheme
from app.schemas.user import UserCreate, UserLogin, TokenRefresh, Token, UserResponse
from app.crud.user import get_user_by_id
from app.crud.token import add_token_to_blacklist

router = APIRouter()

# Routes
@router.post("/signup", response_model=UserResponse)
async def signup_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """User signup endpoint."""
    return await signup(db, user.username, user.email, user.password)

@router.post("/login", response_model=Token)
async def login_route(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """User login endpoint."""
    return await login(db, user.username, user.password)

@router.post("/refresh", response_model=Token)
async def refresh_token_route(token_data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    """Refresh access token endpoint."""
    return await refresh_access_token(db, token_data.refresh_token)

@router.post("/logout")
async def logout_route(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """User logout endpoint."""
    payload = decode_token(token)
    jti = payload.get("jti")
    exp = payload.get("exp")
    if jti and exp:
        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        await add_token_to_blacklist(db, jti, expires_at)
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_route(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get current user endpoint."""
    user_id = current_user.get("user_id")
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
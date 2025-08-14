# API routes for login, signup, logout, refresh token, and user info
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.auth import signup, login, refresh_access_token
from app.utils.security import get_current_user
from app.schemas.user import UserCreate, UserLogin, TokenRefresh, Token, UserResponse

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
async def refresh_token_route(token_data: TokenRefresh):
    """Refresh access token endpoint."""
    return await refresh_access_token(token_data.refresh_token)

@router.post("/logout")
async def logout_route():
    """User logout endpoint."""
    # As noted in the service, logout is typically handled client-side
    # For server-side logout, we would need to maintain a token blacklist
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_route(current_user: dict = Depends(get_current_user)):
    """Get current user endpoint."""
    # This would need to fetch the user from the database using the token data
    # For now, we'll return a placeholder
    return {"id": current_user.get("user_id"), "username": current_user.get("sub"), "email": "user@example.com", "is_active": True}

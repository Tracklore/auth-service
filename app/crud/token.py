# app/crud/token.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.token import TokenBlacklist
import datetime

async def add_token_to_blacklist(db: AsyncSession, jti: str, expires_at: datetime.datetime):
    """Add a token to the blacklist."""
    blacklist_entry = TokenBlacklist(jti=jti, expires_at=expires_at)
    db.add(blacklist_entry)
    await db.commit()
    await db.refresh(blacklist_entry)
    return blacklist_entry

async def is_token_blacklisted(db: AsyncSession, jti: str) -> bool:
    """Check if a token is blacklisted."""
    result = await db.execute(select(TokenBlacklist).where(TokenBlacklist.jti == jti))
    return result.scalar_one_or_none() is not None

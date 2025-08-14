# app/models/token.py
from sqlalchemy import Column, String, DateTime
from app.db.database import Base
import datetime

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    jti = Column(String, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False)

# Test database connectivity
import asyncio
import sys
from pathlib import Path
import pytest

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.database import engine, Base
from app.core.settings import settings

@pytest.mark.asyncio
async def test_connection():
    """Test the database connection."""
    try:
        async with engine.connect() as conn:
            print("Database connection successful!")
            # Try to create tables
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
    finally:
        await engine.dispose()
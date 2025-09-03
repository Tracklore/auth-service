from fastapi import FastAPI
from app.api.routes import router as auth_router
from app.services.message_queue import message_queue_client
from app.core.config import get_settings

# Get settings instance
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Include the authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    """Initialize the message queue connection on startup."""
    await message_queue_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close the message queue connection on shutdown."""
    await message_queue_client.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}
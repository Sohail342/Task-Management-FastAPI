from fastapi import FastAPI
from app.core.config import get_settings
from app.router.auth import router as auth_router


app = FastAPI(title="Task Management API", description="API for managing tasks")


# Include routers
app.include_router(auth_router)
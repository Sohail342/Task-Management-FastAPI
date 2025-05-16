from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import (
    auth,
    task,
)


app = FastAPI(title="Task Management API", description="API for managing tasks", version="1.0.0")


# Include routers
app.include_router(auth.router)
app.include_router(task.router)

# Allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

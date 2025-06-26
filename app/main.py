from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import (
    auth,
    task,
)


app = FastAPI(root_path="/api", title="Task Management API", description="API for managing tasks", version="1.0.0")


# Include routers
app.include_router(auth.router)
app.include_router(task.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://94.136.188.243:3000", "http://localhost:3000/", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

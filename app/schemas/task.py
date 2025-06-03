from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task"""

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: Optional[int] = None
    start_date: Optional[datetime] = datetime.now(timezone.utc)
    due_date: Optional[datetime] = None


class CreateTaskDependant(BaseModel):
    """Schema for creating a new task dependant by employee"""

    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True


class TaskGet(BaseModel):
    """Schema for getting a task"""

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: Optional[int] = None
    assigned_by_id: Optional[int] = None
    start_date: Optional[datetime] = datetime.now(timezone.utc)
    due_date: Optional[datetime] = None
    escalation_flagged: Optional[bool] = False

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Schema for updating a task"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: Optional[int] = None
    assigned_by_id: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    escalation_flagged: Optional[bool] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr

from app.models.task import TaskStatus



class TaskCreate(BaseModel):
    """Schema for creating a new task"""

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: Optional[list[int]] = None
    assigned_by_id: Optional[int] = None
    start_date: Optional[datetime] = datetime.now(timezone.utc)
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    assigned_to_id: Optional[int]
    assigned_by_id: Optional[int]
    start_date: Optional[datetime]
    due_date: Optional[datetime]

    class Config:
        from_attributes = True

class MultipleUserTaskResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class CreateTaskDependant(BaseModel):
    """Schema for creating a new task dependant by employee"""

    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
        

class GetTaskDependant(BaseModel):
    """Schema for getting a task dependant"""

    id: int
    title: str
    description: Optional[str] = None
    dependant_to_id: int
    created_in: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


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

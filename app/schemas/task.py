from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task"""

    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[int] = None
    start_date: Optional[datetime] = datetime.now(timezone.utc)
    due_date: Optional[datetime] = None
    dependency_task_id: Optional[int] = None
    escalation_flagged: Optional[bool] = False
    
    
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
    dependency_task_id: Optional[int] = None
    escalation_flagged: Optional[bool] = False

    class Config:
        orm_mode = True
        
        
class TaskUpdate(BaseModel):
    """Schema for updating a task"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_id: Optional[int] = None
    assigned_by_id: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    dependency_task_id: Optional[int] = None
    escalation_flagged: Optional[bool] = None

    class Config:
        orm_mode = True

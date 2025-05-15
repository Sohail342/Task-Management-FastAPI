from pydantic import BaseModel
from typing import Optional
from app.models.task import TaskStatus
from datetime import datetime, timezone


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

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate


async def create_task_service(
    task_data: TaskCreate,
    current_user: int,
    db: AsyncSession,
) -> Task:
    """Create a new task"""
    task = Task(**task_data.model_dump(), assigned_by_id=current_user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task

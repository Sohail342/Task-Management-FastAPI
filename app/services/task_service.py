from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status

from app.models.task import Task
from app.models.user import UserRole
from app.schemas.task import TaskCreate, TaskUpdate


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


async def get_task_service(
    task_id: int,
    current_user: int,
    db: AsyncSession,
) -> Task | None:
    """Get a task by ID"""
    task = await db.get(Task, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
        
    # If user is Employee, check if assigned_to matches current_user.id
    if current_user.role == UserRole.EMPLOYEE and task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task",
        )
    return task


async def update_task_service(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession,
) -> Task | None:
    """Update a task by ID"""
    task = await db.get(Task, task_id)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    for key, value in task_data.model_dump().items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)

    return task



async def delete_task_service(
    task_id: int,
    db: AsyncSession,
) -> Task | None:
    """Delete a task by ID"""
    task = await db.get(Task, task_id)
    if not task:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await db.delete(task)
    await db.commit()

    return task

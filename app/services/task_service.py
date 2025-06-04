from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.future import select

from app.models.task import Task, DependantTask
from app.models.user import UserRole
from app.schemas.task import TaskCreate, TaskUpdate, CreateTaskDependant


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
    if (
        current_user.role == UserRole.EMPLOYEE
        and task.assigned_to_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task",
        )
    return task


async def get_all_tasks_service(
    current_user: int,
    db: AsyncSession,
) -> list[Task]:
    """Get all tasks"""

    tasks = await db.execute(select(Task))

    return tasks.scalars().all()


async def update_task_service(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession,
) -> Task | None:
    """Update a task by ID"""
    task = await db.get(Task, task_id)
    if not task:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

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
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    await db.delete(task)
    await db.commit()

    return task


async def get_assigned_tasks_service(
    current_user: int,
    db: AsyncSession,
) -> list[Task]:
    """Get all tasks assigned to the current user"""
    tasks = await db.execute(select(Task).where(Task.assigned_to_id == current_user.id))
    return tasks.scalars().all()


async def create_dependant_task_service(
    task_id: int,
    current_user: int,
    dependant_task_data: CreateTaskDependant,
    db: AsyncSession,
) -> DependantTask:
    """Create a new dependant task"""
    dependant_task = DependantTask(
        **dependant_task_data.model_dump(),
        dependant_to_id=task_id,
        created_by_id=current_user.id,
    )
    db.add(dependant_task)
    await db.commit()
    await db.refresh(dependant_task)

    return dependant_task


async def get_dependant_task_service(
    dependant_task_id: int,
    current_user: int,
    db: AsyncSession,
) -> DependantTask | None:
    """Get a dependant task by ID"""
    result = await db.execute(
        select(DependantTask).where(
            DependantTask.id == dependant_task_id,
            DependantTask.created_by_id == current_user.id,
        )
    )
    
    dependant_task = result.scalar_one_or_none()

    if not dependant_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dependant task not found",
        )

    return dependant_task


async def get_task_dependants_service(
    task_id: int,
    current_user: int,
    db: AsyncSession,
) -> list[DependantTask]:
    """Get all dependant tasks for a specific task"""
    # First check if the user has access to the parent task
    task = await get_task_service(task_id=task_id, current_user=current_user, db=db)
    
    # If we get here, the user has access to the task
    result = await db.execute(
        select(DependantTask).where(DependantTask.dependant_to_id == task_id)
    )
    
    return result.scalars().all()
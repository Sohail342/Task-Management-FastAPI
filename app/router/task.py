from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from typing import Annotated

from app.core.dependencies import role_required
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskGet, TaskUpdate, CreateTaskDependant, GetTaskDependant, TaskResponse
from app.services.task_service import (
    create_task_service,
    get_task_service,
    update_task_service,
    delete_task_service,
    create_dependant_task_service,
    get_assigned_tasks_service,
    get_all_tasks_service,
    get_task_dependants_service,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Admin"])),
):
    """Create a new task"""

    return await create_task_service(
        task_data=task_data, current_user=current_user, db=db
    )


@router.get("/assigned", response_model=list[TaskGet], status_code=status.HTTP_200_OK)
async def get_assigned_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Employee"])),
):
    """Get all tasks assigned to the current user"""
    return await get_assigned_tasks_service(current_user=current_user, db=db)


@router.get("/", response_model=list[TaskGet], status_code=status.HTTP_200_OK)
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Admin", "Supervisor", "Compliance"])),
):
    """Get all tasks"""
    return await get_all_tasks_service(current_user=current_user, db=db)


@router.get("/{task_id}", response_model=TaskUpdate, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(
        role_required(["Admin", "Supervisor", "Compliance", "Employee"])
    ),
):
    """Get a task by ID"""

    return await get_task_service(task_id=task_id, current_user=current_user, db=db)


@router.put("/{task_id}", response_model=TaskGet, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Admin"])),
):
    """Update a task by ID"""

    return await update_task_service(task_id=task_id, task_data=task_data, db=db)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Admin"])),
):
    """Delete a task by ID"""

    task = await delete_task_service(task_id=task_id, db=db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.post(
    "/dependant/{task_id}",
    response_model=CreateTaskDependant,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_dependant(
    task_data: CreateTaskDependant,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Employee"])),
):
    """Create a new task dependant by employee"""

    return await create_dependant_task_service(
        task_id=task_id, current_user=current_user, dependant_task_data=task_data, db=db
    )



@router.get(
    "/dependants/{task_id}",
    response_model=list[GetTaskDependant],
    status_code=status.HTTP_200_OK,
)
async def get_task_dependants(
    task_id: int,
    current_user: Annotated[int, Depends(role_required(["Admin", "Supervisor", "Compliance", "Employee"]))],
    db: Annotated[AsyncSession, Depends(get_db)],

):
    """Get all dependant tasks for a specific task"""

    return await get_task_dependants_service(
        task_id=task_id, current_user=current_user, db=db
    )




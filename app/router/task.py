from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import role_required
from app.db.session import get_db
from app.schemas.task import TaskCreate
from app.services.task_service import create_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(role_required(["Admin"])),
):
    """Create a new task"""

    return await create_task_service(
        task_data=task_data, current_user=current_user, db=db
    )

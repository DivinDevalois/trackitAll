from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


def get_project_repository(session: Session = Depends(get_session)) -> ProjectRepository:
    return ProjectRepository(session)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    repo: TaskRepository = Depends(get_task_repository),
    project_repo: ProjectRepository = Depends(get_project_repository),
):
    if payload.project_id is not None and project_repo.get(payload.project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {payload.project_id} not found",
        )
    return repo.create(**payload.model_dump())


@router.get("", response_model=list[TaskRead])
def list_tasks(
    project_id: int | None = Query(default=None),
    repo: TaskRepository = Depends(get_task_repository),
):
    return repo.list(project_id=project_id)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, repo: TaskRepository = Depends(get_task_repository)):
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=TaskRead)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    repo: TaskRepository = Depends(get_task_repository),
):
    task = repo.update_status(task_id, payload.status)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

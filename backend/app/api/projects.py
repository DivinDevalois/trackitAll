from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_repository(session: Session = Depends(get_session)) -> ProjectRepository:
    return ProjectRepository(session)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, repo: ProjectRepository = Depends(get_project_repository)):
    return repo.create(**payload.model_dump())


@router.get("", response_model=list[ProjectRead])
def list_projects(repo: ProjectRepository = Depends(get_project_repository)):
    return repo.list()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, repo: ProjectRepository = Depends(get_project_repository)):
    project = repo.get(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    repo: ProjectRepository = Depends(get_project_repository),
):
    project = repo.update(project_id, **payload.model_dump(exclude_unset=True))
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, repo: ProjectRepository = Depends(get_project_repository)):
    deleted = repo.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

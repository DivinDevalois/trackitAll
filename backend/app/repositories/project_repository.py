from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, name: str, description: str | None = None) -> Project:
        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get(self, project_id: int) -> Project | None:
        return self.session.get(Project, project_id)

    def list(self) -> list[Project]:
        return list(self.session.scalars(select(Project).order_by(Project.id)))

    def update(
        self,
        project_id: int,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Project | None:
        project = self.session.get(Project, project_id)
        if project is None:
            return None
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        project = self.session.get(Project, project_id)
        if project is None:
            return False
        self.session.delete(project)
        self.session.commit()
        return True

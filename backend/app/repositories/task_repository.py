from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        title: str,
        description: str | None = None,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: date | None = None,
        project_id: int | None = None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            project_id=project_id,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def list(self, *, project_id: int | None = None) -> list[Task]:
        stmt = select(Task).order_by(Task.id)
        if project_id is not None:
            stmt = stmt.where(Task.project_id == project_id)
        return list(self.session.scalars(stmt))

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        task.status = status
        task.completed_at = func.now() if status == TaskStatus.DONE else None
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(
        self,
        task_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: date | None = None,
        project_id: int | None = None,
    ) -> Task | None:
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date
        if project_id is not None:
            task.project_id = project_id
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.session.get(Task, task_id)
        if task is None:
            return False
        self.session.delete(task)
        self.session.commit()
        return True

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
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def list(self) -> list[Task]:
        return list(self.session.scalars(select(Task).order_by(Task.id)))

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        task = self.session.get(Task, task_id)
        if task is None:
            return None
        task.status = status
        task.completed_at = func.now() if status == TaskStatus.DONE else None
        self.session.commit()
        self.session.refresh(task)
        return task

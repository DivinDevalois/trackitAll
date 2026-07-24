from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.analytics.habit_metrics import get_daily_habit_metrics
from app.analytics.task_metrics import get_daily_task_metrics
from app.db.session import get_session
from app.schemas.analytics import HabitDailyMetric, TaskDailyMetric

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/tasks", response_model=list[TaskDailyMetric])
def read_task_metrics(session: Session = Depends(get_session)):
    return get_daily_task_metrics(session)


@router.get("/habits", response_model=list[HabitDailyMetric])
def read_habit_metrics(
    habit_id: int | None = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_daily_habit_metrics(session, habit_id=habit_id)

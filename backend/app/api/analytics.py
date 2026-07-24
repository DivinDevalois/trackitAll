from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.analytics.correlation import get_habit_task_correlation
from app.analytics.finance_metrics import get_daily_finance_metrics
from app.analytics.habit_metrics import get_daily_habit_metrics
from app.analytics.task_metrics import get_daily_task_metrics
from app.db.session import get_session
from app.schemas.analytics import (
    FinanceDailyMetric,
    HabitDailyMetric,
    HabitTaskCorrelationSummary,
    TaskDailyMetric,
)

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


@router.get("/finances", response_model=list[FinanceDailyMetric])
def read_finance_metrics(
    category: str | None = Query(default=None),
    session: Session = Depends(get_session),
):
    return get_daily_finance_metrics(session, category=category)


@router.get("/correlation", response_model=HabitTaskCorrelationSummary)
def read_habit_task_correlation(
    window_days: int = Query(default=30, ge=1, le=365),
    session: Session = Depends(get_session),
):
    days = get_habit_task_correlation(session, window_days=window_days)
    rated_days = [d for d in days if d["habit_completion_rate"] is not None]
    good_days = [d["tasks_completed"] for d in rated_days if d["habit_completion_rate"] >= 0.5]
    bad_days = [d["tasks_completed"] for d in rated_days if d["habit_completion_rate"] < 0.5]
    return {
        "days": days,
        "avg_tasks_completed_on_good_habit_days": sum(good_days) / len(good_days) if good_days else None,
        "avg_tasks_completed_on_bad_habit_days": sum(bad_days) / len(bad_days) if bad_days else None,
    }

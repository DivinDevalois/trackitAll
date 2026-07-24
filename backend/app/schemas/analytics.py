from datetime import date

from pydantic import BaseModel, ConfigDict


class TaskDailyMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day: date
    tasks_created: int
    tasks_completed: int


class HabitDailyMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    habit_id: int
    habit_name: str
    day: date
    completed: bool


class HabitTaskCorrelationDay(BaseModel):
    day: date
    tasks_completed: int
    habit_completion_rate: float | None


class HabitTaskCorrelationSummary(BaseModel):
    days: list[HabitTaskCorrelationDay]
    avg_tasks_completed_on_good_habit_days: float | None
    avg_tasks_completed_on_bad_habit_days: float | None

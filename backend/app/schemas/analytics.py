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

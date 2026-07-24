from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    target_frequency_per_week: int = Field(default=7, ge=1, le=7)


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    target_frequency_per_week: int
    created_at: datetime
    updated_at: datetime


class HabitCheckIn(BaseModel):
    date: date_type | None = None
    completed: bool = True


class HabitLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    date: date_type
    completed: bool

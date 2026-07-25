from datetime import date as date_type
from datetime import datetime
from datetime import time as time_type

from pydantic import BaseModel, ConfigDict, Field

from app.models.habit import HabitType


class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    type: HabitType = HabitType.BUILD
    target_frequency_per_week: int = Field(default=7, ge=1, le=7)
    target_time: time_type | None = None
    is_active: bool = True


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    type: HabitType | None = None
    target_frequency_per_week: int | None = Field(default=None, ge=1, le=7)
    target_time: time_type | None = None
    is_active: bool | None = None


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    type: HabitType
    target_frequency_per_week: int
    target_time: time_type | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class HabitCheckIn(BaseModel):
    date: date_type | None = None
    completed: bool = True
    duration_minutes: int | None = Field(default=None, gt=0)


class HabitLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    date: date_type
    completed: bool
    duration_minutes: int | None

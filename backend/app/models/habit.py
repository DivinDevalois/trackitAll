import datetime as dt
import enum

from sqlalchemy import DateTime, Enum, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HabitType(str, enum.Enum):
    BUILD = "build"
    BREAK = "break"


class Habit(Base):
    __tablename__ = "habit"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[HabitType] = mapped_column(
        Enum(
            HabitType,
            name="habit_type",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        default=HabitType.BUILD,
    )
    target_frequency_per_week: Mapped[int] = mapped_column(Integer, default=7)
    target_time: Mapped[dt.time | None] = mapped_column(Time)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

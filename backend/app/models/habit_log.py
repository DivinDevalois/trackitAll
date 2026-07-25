import datetime as dt

from sqlalchemy import Boolean, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HabitLog(Base):
    __tablename__ = "habit_log"
    __table_args__ = (UniqueConstraint("habit_id", "date", name="uq_habit_log_habit_id_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habit.id"))
    date: Mapped[dt.date] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(Boolean, default=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)

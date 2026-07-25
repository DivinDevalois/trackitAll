import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit import Habit, HabitType


class HabitRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        type: HabitType = HabitType.BUILD,
        target_frequency_per_week: int = 7,
        target_time: dt.time | None = None,
        is_active: bool = True,
    ) -> Habit:
        habit = Habit(
            name=name,
            description=description,
            type=type,
            target_frequency_per_week=target_frequency_per_week,
            target_time=target_time,
            is_active=is_active,
        )
        self.session.add(habit)
        self.session.commit()
        self.session.refresh(habit)
        return habit

    def get(self, habit_id: int) -> Habit | None:
        return self.session.get(Habit, habit_id)

    def list(self, *, active_only: bool = False) -> list[Habit]:
        stmt = select(Habit).order_by(Habit.id)
        if active_only:
            stmt = stmt.where(Habit.is_active.is_(True))
        return list(self.session.scalars(stmt))

    def update(
        self,
        habit_id: int,
        *,
        name: str | None = None,
        description: str | None = None,
        type: HabitType | None = None,
        target_frequency_per_week: int | None = None,
        target_time: dt.time | None = None,
        is_active: bool | None = None,
    ) -> Habit | None:
        habit = self.session.get(Habit, habit_id)
        if habit is None:
            return None
        if name is not None:
            habit.name = name
        if description is not None:
            habit.description = description
        if type is not None:
            habit.type = type
        if target_frequency_per_week is not None:
            habit.target_frequency_per_week = target_frequency_per_week
        if target_time is not None:
            habit.target_time = target_time
        if is_active is not None:
            habit.is_active = is_active
        self.session.commit()
        self.session.refresh(habit)
        return habit

    def delete(self, habit_id: int) -> bool:
        habit = self.session.get(Habit, habit_id)
        if habit is None:
            return False
        self.session.delete(habit)
        self.session.commit()
        return True

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit import Habit


class HabitRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, name: str, target_frequency_per_week: int = 7) -> Habit:
        habit = Habit(name=name, target_frequency_per_week=target_frequency_per_week)
        self.session.add(habit)
        self.session.commit()
        self.session.refresh(habit)
        return habit

    def get(self, habit_id: int) -> Habit | None:
        return self.session.get(Habit, habit_id)

    def list(self) -> list[Habit]:
        return list(self.session.scalars(select(Habit).order_by(Habit.id)))

    def update(
        self,
        habit_id: int,
        *,
        name: str | None = None,
        target_frequency_per_week: int | None = None,
    ) -> Habit | None:
        habit = self.session.get(Habit, habit_id)
        if habit is None:
            return None
        if name is not None:
            habit.name = name
        if target_frequency_per_week is not None:
            habit.target_frequency_per_week = target_frequency_per_week
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

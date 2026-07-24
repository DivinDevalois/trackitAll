from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog


class HabitLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def check_in(self, habit_id: int, log_date: date, *, completed: bool = True) -> HabitLog:
        # Relies on the uq_habit_log_habit_id_date constraint: a second check-in
        # for the same day updates the existing row instead of erroring, atomically.
        stmt = (
            pg_insert(HabitLog)
            .values(habit_id=habit_id, date=log_date, completed=completed)
            .on_conflict_do_update(
                index_elements=[HabitLog.habit_id, HabitLog.date],
                set_={"completed": completed},
            )
            .returning(HabitLog.id)
        )
        log_id = self.session.execute(stmt).scalar_one()
        self.session.commit()
        return self.session.get(HabitLog, log_id)

    def list_for_habit(self, habit_id: int) -> list[HabitLog]:
        return list(
            self.session.scalars(
                select(HabitLog).where(HabitLog.habit_id == habit_id).order_by(HabitLog.date)
            )
        )

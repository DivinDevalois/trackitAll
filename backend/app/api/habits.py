from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository
from app.schemas.habit import HabitCheckIn, HabitCreate, HabitLogRead, HabitRead, HabitUpdate

router = APIRouter(prefix="/habits", tags=["habits"])


def get_habit_repository(session: Session = Depends(get_session)) -> HabitRepository:
    return HabitRepository(session)


def get_habit_log_repository(session: Session = Depends(get_session)) -> HabitLogRepository:
    return HabitLogRepository(session)


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, repo: HabitRepository = Depends(get_habit_repository)):
    return repo.create(**payload.model_dump())


@router.get("", response_model=list[HabitRead])
def list_habits(repo: HabitRepository = Depends(get_habit_repository)):
    return repo.list()


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, repo: HabitRepository = Depends(get_habit_repository)):
    habit = repo.get(habit_id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return habit


@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(
    habit_id: int,
    payload: HabitUpdate,
    repo: HabitRepository = Depends(get_habit_repository),
):
    habit = repo.update(habit_id, **payload.model_dump(exclude_unset=True))
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, repo: HabitRepository = Depends(get_habit_repository)):
    deleted = repo.delete(habit_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")


@router.post("/{habit_id}/check-in", response_model=HabitLogRead)
def check_in_habit(
    habit_id: int,
    payload: HabitCheckIn,
    habit_repo: HabitRepository = Depends(get_habit_repository),
    log_repo: HabitLogRepository = Depends(get_habit_log_repository),
):
    if habit_repo.get(habit_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found")
    return log_repo.check_in(
        habit_id,
        payload.date or date.today(),
        completed=payload.completed,
        duration_minutes=payload.duration_minutes,
    )

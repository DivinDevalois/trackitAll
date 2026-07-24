from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transaction_repository(session: Session = Depends(get_session)) -> TransactionRepository:
    return TransactionRepository(session)


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    repo: TransactionRepository = Depends(get_transaction_repository),
):
    return repo.create(**payload.model_dump())


@router.get("", response_model=list[TransactionRead])
def list_transactions(repo: TransactionRepository = Depends(get_transaction_repository)):
    return repo.list()


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: int,
    repo: TransactionRepository = Depends(get_transaction_repository),
):
    transaction = repo.get(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    repo: TransactionRepository = Depends(get_transaction_repository),
):
    transaction = repo.update(transaction_id, **payload.model_dump(exclude_unset=True))
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    repo: TransactionRepository = Depends(get_transaction_repository),
):
    deleted = repo.delete(transaction_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

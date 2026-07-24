from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        date: date,
        amount: Decimal,
        type: TransactionType,
        category: str,
        description: str | None = None,
    ) -> Transaction:
        transaction = Transaction(
            date=date,
            amount=amount,
            type=type,
            category=category,
            description=description,
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get(self, transaction_id: int) -> Transaction | None:
        return self.session.get(Transaction, transaction_id)

    def list(self) -> list[Transaction]:
        return list(
            self.session.scalars(select(Transaction).order_by(Transaction.date, Transaction.id))
        )

    def update(
        self,
        transaction_id: int,
        *,
        date: date | None = None,
        amount: Decimal | None = None,
        type: TransactionType | None = None,
        category: str | None = None,
        description: str | None = None,
    ) -> Transaction | None:
        transaction = self.session.get(Transaction, transaction_id)
        if transaction is None:
            return None
        if date is not None:
            transaction.date = date
        if amount is not None:
            transaction.amount = amount
        if type is not None:
            transaction.type = type
        if category is not None:
            transaction.category = category
        if description is not None:
            transaction.description = description
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(self, transaction_id: int) -> bool:
        transaction = self.session.get(Transaction, transaction_id)
        if transaction is None:
            return False
        self.session.delete(transaction)
        self.session.commit()
        return True

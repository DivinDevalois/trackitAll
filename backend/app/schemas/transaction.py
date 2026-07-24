from datetime import date as date_type
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    date: date_type
    amount: Decimal = Field(gt=0)
    type: TransactionType
    category: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TransactionUpdate(BaseModel):
    date: date_type | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    type: TransactionType | None = None
    category: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date_type
    amount: Decimal
    type: TransactionType
    category: str
    description: str | None
    created_at: datetime
    updated_at: datetime

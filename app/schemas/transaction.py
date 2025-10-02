from pydantic import BaseModel
from decimal import Decimal

class TransactionBase(BaseModel):
    sender_account: str
    receiver_account: str
    amount: Decimal
    type_transaction: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    currency: str
    class Config:
        from_attributes = True

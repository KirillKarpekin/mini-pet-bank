from pydantic import BaseModel
from decimal import Decimal

class AccountBase(BaseModel):
    balance: Decimal
    currency_id: int
    is_active: bool

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    acc_number: str
    user_id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from decimal import Decimal

class CreditBase(BaseModel):
    user_id: int
    amount: Decimal
    interest_rate: float
    term_months: int

class CreditCreate(CreditBase):
    pass

class Credit(CreditBase):
    id: int
    monthly_payment: Decimal
    amount_debt: Decimal
    status: str

    class Config:
        orm_mode = True
from pydantic import BaseModel
from decimal import Decimal

class CurrencyBase(BaseModel):
    name: str
    code: str
    rate_to_base: Decimal

class CurrencyCreate(CurrencyBase):
    pass 

class Currency(CurrencyBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from decimal import Decimal
from typing import List
from .account import Account 

class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    accounts: List[Account] = []
    class Config:
        from_attributes = True

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from app.database import SessionLocal
from app.schemas.credit import CreditCreate, Credit as CreditSchema
from app.crud.credit import (
    take_credit,
    replenish_debt,
    get_credit_by_id,      
    get_credits_by_user_id,
    get_all_credits,
    delete_credit
)


router = APIRouter(prefix="/credits", tags=["Credits"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CreditSchema)
def create_credit(credit_data: CreditCreate, db: Session = Depends(get_db)):
    return take_credit(
        db=db,
        user_id=credit_data.user_id,
        amount=credit_data.amount,
        interest_rate=credit_data.interest_rate,
        term_months=credit_data.term_months
    )


@router.get("/{credit_id}", response_model=CreditSchema)
def read_credit(credit_id: int, db: Session = Depends(get_db)):
    return get_credit_by_id(db, credit_id)


@router.get("/user/{user_id}", response_model=list[CreditSchema])
def read_credits_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_credits_by_user_id(db, user_id)


@router.get("/", response_model=list[CreditSchema])
def read_all_credits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_credits(db, skip=skip, limit=limit)


@router.put("/pay")
def pay_credit(user_id: int, account_number: str, amount: Decimal, db: Session = Depends(get_db)):
    return replenish_debt(db, user_id=user_id, amount=amount, account_number=account_number)


@router.delete("/{credit_id}")
def delete_credit_endpoint(credit_id: int, db: Session = Depends(get_db)):
    return delete_credit(db, credit_id)

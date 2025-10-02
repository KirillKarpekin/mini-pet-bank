from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.account import Account, AccountCreate
from app.crud.account import (
    get_account_by_id,
    get_user_accounts,
    get_accounts,
    create_account,
    update_account,
    delete_account,
)
from app.crud.user import get_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Account)
def create_account_endpoint(account: AccountCreate, user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return create_account(db=db, account=account, user_id=user_id)


@router.get("/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    account = get_account_by_id(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")
    return account


@router.get("/user/{user_id}", response_model=list[Account])
def read_account_by_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return get_user_accounts(db, user_id)


@router.get("/", response_model=list[Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_accounts(db, skip, limit)


@router.put("/{account_id}", response_model=Account)
def update_account_endpoint(account_id: int, account_data: AccountCreate, db: Session = Depends(get_db)):
    update_acc = update_account(db, account_id, account_data.dict())
    if not update_acc:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")
    return update_acc


@router.delete("/{account_id}", response_model=Account)
def delete_account_endpoint(account_id: int, db: Session = Depends(get_db)):
    return delete_account(db, account_id)

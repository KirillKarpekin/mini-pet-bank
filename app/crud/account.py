from sqlalchemy.orm import Session
from schwifty import IBAN
import random

from app.models.account import Account as AccountModel
from app.schemas.account import AccountCreate


def create_account(db: Session, account: AccountCreate, user_id: int):
    db_account = AccountModel(
        acc_number = IBAN.generate('BY', bank_code='1001', account_code=str(random.randint(10000, 99999))),
        balance = account.balance,
        currency_id = account.currency_id,
        is_active = account.is_active,
        user_id = user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account_by_id(db: Session, account_id: int):
    return db.query(AccountModel).filter(AccountModel.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AccountModel).offset(skip).limit(limit).all()

def get_user_accounts(db: Session, user_id: int):
    accounts = db.query(AccountModel).filter(AccountModel.user_id == user_id).all()
    return accounts 

def update_account(db: Session, account_id: int, update_data: dict):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        return None
    for key, value in update_data.items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account

def delete_account(db: Session, account_id: int):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        return None
    db.delete(account)
    db.commit()
    return account
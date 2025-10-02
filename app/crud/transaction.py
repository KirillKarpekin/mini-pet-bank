from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.exc import IntegrityError

from app.models.transaction import Transaction as TransactionModel
from app.schemas.transaction import TransactionCreate
from app.models.account import Account as AccountModel
from app.schemas.account import AccountCreate
from app.models.currency import Currency as CurrencyModel
from app.schemas.currency import CurrencyCreate

def get_all_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TransactionModel).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()

def create_transaction(db: Session, sender_account: str, receiver_account: str, amount: Decimal, type_transactions: str):
    sender = db.query(AccountModel).filter(AccountModel.acc_number == sender_account).first()
    receiver = db.query(AccountModel).filter(AccountModel.acc_number == receiver_account).first()

    if not sender or not receiver:
        raise HTTPException(status_code=400, detail="Аккаунт не найден")
    
    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Недостаточно средств")
    
    sender_currency = db.query(CurrencyModel).filter(CurrencyModel.id == sender.currency_id).first()
    receiver_currency = db.query(CurrencyModel).filter(CurrencyModel.id == receiver.currency_id).first()

    convert_amount = amount * sender_currency.rate_to_base / receiver_currency.rate_to_base

    sender.balance -= amount
    receiver.balance += convert_amount

    transaction = TransactionModel(
        sender_account = sender.acc_number,
        receiver_account = receiver.acc_number,
        amount = amount,
        currency = sender_currency.code,
        type_transaction = type_transactions
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
    
def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=400, detail="транзакция не найдена")
    db.delete(transaction)
    db.commit()
    return transaction
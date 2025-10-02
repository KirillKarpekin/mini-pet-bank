from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.transaction import Transaction, TransactionCreate
from app.crud.transaction import (
    create_transaction,
    get_all_transactions,
    get_transaction,
    delete_transaction,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Transaction)
def create_transaction_endpoint(transaction: TransactionCreate, db: Session = Depends(get_db)):
    if transaction.sender_account == transaction.receiver_account:
        raise HTTPException(
            status_code=400,
            detail="Нельзя отправлять деньги между своими счетами"
        )
    return create_transaction(
        db,
        transaction.sender_account,
        transaction.receiver_account,
        transaction.amount,
        transaction.type_transaction,
    )


@router.get("/", response_model=list[Transaction])
def read_all_transactions_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_transactions(db, skip, limit)


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction


@router.delete("/{transaction_id}", response_model=Transaction)
def delete_transaction_endpoint(transaction_id: int, db: Session = Depends(get_db)):
    return delete_transaction(db, transaction_id)

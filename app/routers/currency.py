from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.currency import Currency, CurrencyCreate
from app.crud.currency import (
    get_currency_by_code,
    get_currencies,
    get_currency,
    create_currency,
    update_currency,
    delete_currency,
)

router = APIRouter(prefix="/currencies", tags=["Currencies"])

# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Currency)
def create_currency_endpoint(currency: CurrencyCreate, db: Session = Depends(get_db)):
    existing = get_currency_by_code(db, cur_code=currency.code)
    if existing:
        raise HTTPException(status_code=400, detail="Валюта уже зарегистрирована")
    return create_currency(db, currency)


@router.get("/", response_model=list[Currency])
def read_currencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_currencies(db, skip, limit)


@router.get("/{currency_id}", response_model=Currency)
def read_currency_by_id(currency_id: int, db: Session = Depends(get_db)):
    currency = get_currency(db, currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Валюта не найдена")
    return currency


@router.put("/{currency_id}", response_model=Currency)
def update_currency_endpoint(currency_id: int, data: CurrencyCreate, db: Session = Depends(get_db)):
    currency_update = update_currency(db, data.dict(), currency_id)
    if not currency_update:
        raise HTTPException(status_code=404, detail="Валюта не найдена")
    return currency_update


@router.delete("/{currency_id}", response_model=Currency)
def delete_currency_endpoint(currency_id: int, db: Session = Depends(get_db)):
    deleted_currency = delete_currency(db, currency_id)
    if not deleted_currency:
        raise HTTPException(status_code=404, detail="Валюта не найдена")
    return deleted_currency

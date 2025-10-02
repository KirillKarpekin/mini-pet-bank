from sqlalchemy.orm import Session
from app.models.currency import Currency as CurrencyModel
from app.schemas.currency import CurrencyCreate
def create_currency(db: Session, currency: CurrencyCreate):
    db_curency = CurrencyModel(
        name = currency.name,
        code = currency.code,
        rate_to_base = currency.rate_to_base
    )
    db.add(db_curency)
    db.commit()
    db.refresh(db_curency)
    return db_curency

def get_currency(db: Session, currency_id: int):
    return db.query(CurrencyModel).filter(CurrencyModel.id == currency_id).first()

def get_currencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CurrencyModel).offset(skip).limit(limit).all()

def get_currency_by_code(db: Session, cur_code: str):
    return db.query(CurrencyModel).filter(CurrencyModel.code == cur_code).first()

def update_currency(db: Session, currency_data: dict, currency_id: int):
    currency = db.query(CurrencyModel).filter(CurrencyModel.id == currency_id).first()
    if not currency:
        return None
    for key, value in currency_data.items():
        setattr(currency, key, value)
    db.commit()
    db.refresh(currency)
    return currency

def delete_currency(db: Session, currency_id: int):
    currency = db.query(CurrencyModel).filter(CurrencyModel.id == currency_id).first()
    if not currency:
        return None
    
    db.delete(currency)
    db.commit()
    return currency
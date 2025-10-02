from sqlalchemy.orm import Session
from decimal import Decimal, ROUND_HALF_UP
from fastapi import HTTPException
from app.models.credit import Credit as CreditModel
from app.models.user import User as UserModel
from app.models.account import Account as AccountModel
from app.models.transaction import Transaction as TransactionModel


def take_credit(db: Session, user_id: int, amount: Decimal, interest_rate: float, term_months: int):
    if term_months <= 0:
        raise HTTPException(status_code=400, detail="Срок кредита должен быть больше 0 месяцев")

    credit_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not credit_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    month_payment = calculate_annuity_payment(amount, interest_rate, term_months)

    credit = CreditModel(
        user_id=user_id,
        amount=amount,
        interest_rate=interest_rate,
        term_months=term_months,
        monthly_payment=month_payment,
        amount_debt=amount,
        status="active"
    )
    
    main_account = db.query(AccountModel).filter(AccountModel.user_id == user_id).first()
    if not main_account:
        raise HTTPException(status_code=400, detail="Аккаунт не найден")
    main_account.balance += amount

    db.add(credit)
    db.commit()
    db.refresh(credit)
    db.refresh(main_account)
    
    return credit


def get_credit_by_id(db: Session, credit_id: int) -> CreditModel:
    credit = db.query(CreditModel).filter(CreditModel.id == credit_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="Кредит не найден")
    return credit


def get_credits_by_user_id(db: Session, user_id: int):
    credits = db.query(CreditModel).filter(CreditModel.user_id == user_id).all()
    if not credits:
        raise HTTPException(status_code=404, detail="Кредиты не найдены")
    return credits


def get_all_credits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CreditModel).offset(skip).limit(limit).all()


def replenish_debt(db: Session, user_id: int, amount: Decimal, account_number: str):
    user_acc = db.query(AccountModel).filter(
        AccountModel.acc_number == account_number,
        AccountModel.user_id == user_id
    ).first()

    if not user_acc:
        raise HTTPException(status_code=400, detail="Аккаунт не найден")

    if user_acc.balance < amount:
        raise HTTPException(status_code=400, detail="Недостаточно средств на счете")

    credit = db.query(CreditModel).filter(
        CreditModel.user_id == user_id,
        CreditModel.status == "active"
    ).first()
    if not credit:
        raise HTTPException(status_code=400, detail="Активный кредит не найден")

    user_acc.balance -= amount
    credit.amount_debt -= amount
    if credit.amount_debt < 0:
        credit.amount_debt = 0

    transaction = TransactionModel(
        sender_account=user_acc.acc_number,
        receiver_account="BANK_CREDIT_ACCOUNT",
        amount=amount,
        currency=user_acc.currency.code,
        type_transaction="credit_payment"
    )
    db.add(transaction)

    db.commit()
    db.refresh(user_acc)
    db.refresh(credit)
    db.refresh(transaction)

    return {
        "message": "Долг успешно погашен",
        "остаток кредита": credit.amount_debt,
        "баланс": user_acc.balance,
        "transaction_id": transaction.id
    }


def delete_credit(db: Session, credit_id: int):
    credit = db.query(CreditModel).filter(CreditModel.id == credit_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="Кредит не найден")
    db.delete(credit)
    db.commit()
    return {"message": "Кредит удалён"}


def calculate_annuity_payment(amount: Decimal, interest_rate: float, term_months: int) -> Decimal:
    monthly_rate = Decimal((interest_rate / 100) / 12)
    payment = amount * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
    return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import User, UserCreate
from app.crud.user import (
    get_user_by_email,
    get_user_by_phone,
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user_email = get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    db_user_phone = get_user_by_phone(db, phone=user.phone)
    if db_user_phone:
        raise HTTPException(status_code=400, detail="Номер телефона уже зарегистрирован")

    return create_user(db, user)


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user_data.dict())
    if not updated_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user


@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return deleted_user
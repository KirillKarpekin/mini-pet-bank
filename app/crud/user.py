from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(UserModel).filter(UserModel.phone == phone).first()

def update_user(db: Session, user_id: int, new_data: dict):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return None
    for key, value in new_data.items():
        setattr(user,key,value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return None
    
    db.delete(user)
    db.commit()
    return user
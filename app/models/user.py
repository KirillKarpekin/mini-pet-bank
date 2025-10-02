from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    password = Column(String(255))

    accounts = relationship("Account", back_populates="user")
    credits = relationship("Credit", back_populates="user")  
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    acc_number = Column(String(50), unique=True, index=True, nullable=False)
    balance = Column(Numeric(12,2), default=0.00)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    is_active = Column(Boolean, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="accounts")
    currency = relationship("Currency")
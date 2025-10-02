from sqlalchemy import Integer, String, Column, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship
from ..database import Base

class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(12,2), default=0.00) #сумма кредитп
    interest_rate = Column(Float, nullable=False) # процентная ставка
    term_months = Column(Integer, nullable=False) # срок кредита (в месяцах)
    monthly_payment = Column(Numeric(12,2), nullable=False) # в месяц плата
    amount_debt = Column(Numeric(12,2), default=0.00)
    status = Column(String, default="active")

    user = relationship("User", back_populates="credits")

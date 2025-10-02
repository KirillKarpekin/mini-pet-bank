from sqlalchemy import Integer, String, Column, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_account = Column(String, nullable=False)
    receiver_account = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), default=0.00)
    currency = Column(String, nullable=False, index=True)
    type_transaction = Column(String(25), nullable=False, index=True)
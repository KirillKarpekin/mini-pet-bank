from sqlalchemy import Integer, String, Column, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    rate_to_base = Column(Numeric(12, 2), default=1.00)

    accounts = relationship("Account", back_populates="currency")
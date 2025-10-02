from .user import Base as UserBase
from .account import Base as AccountBase
from .credit import Base as CreditBase
from .transaction import Base as TransactionBase
from .currency import Base as CurrencyBase

# Объединяем все Base в один
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Импортируем все модели для create_all
from .user import *
from .account import *
from .credit import *
from .transaction import *
from .currency import *
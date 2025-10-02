from fastapi import FastAPI
from .routers import users, accounts, currency, transactions, credits
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

app.include_router(accounts.router)

app.include_router(currency.router)

app.include_router(transactions.router)

app.include_router(credits.router)
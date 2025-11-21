import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.core.database import Base, engine
from app.models.income_model import Income
from app.routers import income_router


app = FastAPI(title="Income Service")

raw_origins = os.getenv("BACKEND_CORS_ORIGINS")
allowed_origins = (
    [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if raw_origins
    else [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    retries = 5
    while retries:
        try:
            Base.metadata.create_all(bind=engine, tables=[Income.__table__])
            break
        except OperationalError:
            retries -= 1
            time.sleep(2)
    else:
        raise RuntimeError("Database unavailable, could not create incomes tables.")


app.include_router(income_router.router)


@app.get("/")
def root():
    return {"message": "Income Service is running"}

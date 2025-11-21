from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.income_schema import IncomeCreate, IncomeResponse, IncomeUpdate
from app.services import income_service

router = APIRouter(prefix="/incomes", tags=["Incomes"])


@router.post("/", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(income_in: IncomeCreate, db: Session = Depends(get_db)):
    return income_service.create_income(db, income_in)


@router.get("/", response_model=list[IncomeResponse])
def list_income(
    user_id: int = Query(...),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    return income_service.list_income(
        db,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{income_id}", response_model=IncomeResponse)
def get_income(income_id: int, user_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    income = income_service.get_income(db, income_id, user_id)
    return IncomeResponse.from_orm(income)


@router.patch("/{income_id}", response_model=IncomeResponse)
def update_income(
    income_id: int,
    payload: IncomeUpdate,
    user_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    return income_service.update_income(db, income_id, payload, user_id)


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(income_id: int, user_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    income_service.delete_income(db, income_id, user_id)

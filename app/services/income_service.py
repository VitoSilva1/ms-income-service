from datetime import date, datetime
from typing import Iterable, Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income_model import Income
from app.schemas.income_schema import IncomeCreate, IncomeResponse, IncomeSummary, IncomeUpdate, IncomeBase


def create_income(db: Session, payload: IncomeCreate) -> IncomeResponse:
    income = Income(**payload.dict())
    db.add(income)
    db.commit()
    db.refresh(income)
    return IncomeResponse.from_orm(income)


def get_income(db: Session, income_id: int, user_id: Optional[int] = None) -> Income:
    query = db.query(Income).filter(Income.id == income_id)
    if user_id is not None:
        query = query.filter(Income.user_id == user_id)
    income = query.first()
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return income


def list_income(
    db: Session,
    *,
    user_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> Iterable[IncomeResponse]:
    query = db.query(Income).filter(Income.user_id == user_id)
    if date_from:
        query = query.filter(Income.income_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Income.income_date <= datetime.combine(date_to, datetime.max.time()))
    incomes = query.order_by(Income.income_date.desc()).all()
    return [IncomeResponse.from_orm(income) for income in incomes]


def update_income(db: Session, income_id: int, payload: IncomeUpdate, user_id: Optional[int] = None) -> IncomeResponse:
    income = get_income(db, income_id, user_id)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(income, field, value)
    db.commit()
    db.refresh(income)
    return IncomeResponse.from_orm(income)


def delete_income(db: Session, income_id: int, user_id: Optional[int] = None) -> None:
    income = get_income(db, income_id, user_id)
    db.delete(income)
    db.commit()


def summarize_income(
    db: Session,
    *,
    user_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> IncomeSummary:
    query = db.query(
        func.coalesce(func.sum(Income.salary), 0).label("salary"),
        func.coalesce(func.sum(Income.bonus), 0).label("bonus"),
        func.coalesce(func.sum(Income.other_income), 0).label("other_income"),
        func.coalesce(func.sum(Income.total_income), 0).label("total_income"),
    ).filter(Income.user_id == user_id)

    if date_from:
        query = query.filter(Income.income_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Income.income_date <= datetime.combine(date_to, datetime.max.time()))

    row = query.one()
    return IncomeSummary(
        salary=row.salary,
        bonus=row.bonus,
        other_income=row.other_income,
        total_income=row.total_income,
    )

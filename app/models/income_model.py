from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, Numeric

from app.core.database import Base


class IncomeStatus(str, Enum):
    PLANNED = "planned"
    POSTED = "posted"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    salary = Column(Numeric(12, 2), nullable=False)
    bonus = Column(Numeric(12, 2), nullable=True, default=0)
    other_income = Column(Numeric(12, 2), nullable=True, default=0)
    total_income = Column(Numeric(12, 2), nullable=False)
    status = Column(SqlEnum(IncomeStatus), nullable=False, default=IncomeStatus.POSTED)
    income_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Income id={self.id} user_id={self.user_id} total_income={self.total_income}>"

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.income_model import IncomeStatus


class IncomeBase(BaseModel):
    user_id: int = Field(..., description="Identificador del usuario dueño del ingreso")
    salary: Decimal = Field(..., gt=0, description="Monto del salario")
    bonus: Optional[Decimal] = Field(0, ge=0, description="Monto del bono")
    other_income: Optional[Decimal] = Field(0, ge=0, description="Monto de otros ingresos")
    total_income: Decimal = Field(..., gt=0, description="Monto total de ingresos")
    income_date: datetime = Field(default_factory=datetime.utcnow, description="Fecha del ingreso")


class IncomeCreate(IncomeBase):
    status: IncomeStatus = IncomeStatus.POSTED


class IncomeUpdate(BaseModel):
    salary: Optional[Decimal] = Field(None, gt=0, description="Monto del salario")
    bonus: Optional[Decimal] = Field(None, ge=0, description="Monto del bono")
    other_income: Optional[Decimal] = Field(None, ge=0, description="Monto de otros ingresos")
    total_income: Optional[Decimal] = Field(None, gt=0, description="Monto total de ingresos")
    income_date: Optional[datetime] = Field(None, description="Fecha del ingreso")
    status: Optional[IncomeStatus] = None


class IncomeResponse(IncomeBase):
    id: int
    status: IncomeStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class IncomeSummary(BaseModel):
    salary: Decimal
    bonus: Decimal
    other_income: Decimal
    total_income: Decimal

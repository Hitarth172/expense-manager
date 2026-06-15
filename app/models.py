from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class CategoryCreate(BaseModel):
    name: str
    color: str = "#0078D4"


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    amount: float
    description: str
    date: date
    category_id: int

    @field_validator("amount")
    def validate_amount(cls, value):

        if value <= 0:
            raise ValueError(
                "Amount must be positive"
            )

        return round(value, 2)


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    category_id: Optional[int] = None


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str
    date: date
    category_id: int

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category_id: int
    month_limit: float


class InsightRequest(BaseModel):
    month: int
    year: int
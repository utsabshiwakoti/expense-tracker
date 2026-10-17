from decimal import Decimal

from pydantic import BaseModel


class Summary(BaseModel):
    total: Decimal
    count: int
    average: Decimal


class CategoryTotal(BaseModel):
    category_id: int | None
    category: str
    total: Decimal
    percent: float


class MonthTotal(BaseModel):
    month: str  # "2026-10"
    total: Decimal

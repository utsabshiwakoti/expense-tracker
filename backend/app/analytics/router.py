from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.analytics import service
from app.analytics.schemas import CategoryTotal, MonthTotal, Summary
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=Summary)
def summary(
    start: date | None = None,
    end: date | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.summary(db, user.id, start, end)


@router.get("/by-category", response_model=list[CategoryTotal])
def by_category(
    start: date | None = None,
    end: date | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.by_category(db, user.id, start, end)


@router.get("/monthly", response_model=list[MonthTotal])
def monthly(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.monthly_trend(db, user.id, months)

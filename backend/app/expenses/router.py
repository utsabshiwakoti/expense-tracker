from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.categories.service import get_owned_category
from app.core.database import get_db
from app.expenses import service
from app.expenses.models import Expense
from app.expenses.schemas import (
    ExpenseCreate,
    ExpenseOut,
    ExpensePage,
    ExpenseUpdate,
)

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _check_category(db: Session, user: User, category_id: int | None) -> None:
    """Reject a category that doesn't exist or belongs to another user."""
    if category_id is not None and get_owned_category(db, user.id, category_id) is None:
        raise HTTPException(status_code=400, detail="Invalid category")


@router.post("", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    _check_category(db, user, data.category_id)
    expense = Expense(**data.model_dump(), user_id=user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=ExpensePage)
def list_expenses(
    start: date | None = None,
    end: date | None = None,
    category_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items, total = service.list_expenses(
        db,
        user.id,
        start=start,
        end=end,
        category_id=category_id,
        page=page,
        page_size=page_size,
    )
    return ExpensePage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = service.get_owned_expense(db, user.id, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = service.get_owned_expense(db, user.id, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    _check_category(db, user, data.category_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    expense = service.get_owned_expense(db, user.id, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

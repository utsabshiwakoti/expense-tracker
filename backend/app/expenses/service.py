from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.expenses.models import Expense


def list_expenses(
    db: Session,
    user_id: int,
    *,
    start: date | None,
    end: date | None,
    category_id: int | None,
    page: int,
    page_size: int,
):
    query = select(Expense).where(Expense.user_id == user_id)
    if start:
        query = query.where(Expense.spent_on >= start)
    if end:
        query = query.where(Expense.spent_on <= end)
    if category_id:
        query = query.where(Expense.category_id == category_id)

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(Expense.spent_on.desc(), Expense.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return items, total


def get_owned_expense(db: Session, user_id: int, expense_id: int) -> Expense | None:
    expense = db.get(Expense, expense_id)
    if expense is None or expense.user_id != user_id:
        return None
    return expense

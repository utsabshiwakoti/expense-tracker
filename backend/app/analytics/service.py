from datetime import date
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.categories.models import Category
from app.expenses.models import Expense

ZERO = Decimal("0.00")


def _money(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))


def _conditions(user_id: int, start: date | None, end: date | None) -> list:
    conds = [Expense.user_id == user_id]
    if start:
        conds.append(Expense.spent_on >= start)
    if end:
        conds.append(Expense.spent_on <= end)
    return conds


def summary(db: Session, user_id: int, start: date | None, end: date | None):
    total, count = db.execute(
        select(func.sum(Expense.amount), func.count(Expense.id)).where(
            *_conditions(user_id, start, end)
        )
    ).one()
    total = _money(total)
    average = (total / count).quantize(Decimal("0.01")) if count else ZERO
    return {"total": total, "count": count, "average": average}


def by_category(db: Session, user_id: int, start: date | None, end: date | None):
    rows = db.execute(
        select(Expense.category_id, func.sum(Expense.amount))
        .where(*_conditions(user_id, start, end))
        .group_by(Expense.category_id)
    ).all()

    names = {
        c.id: c.name
        for c in db.scalars(select(Category).where(Category.user_id == user_id))
    }
    grand_total = sum((_money(total) for _, total in rows), ZERO)

    result = [
        {
            "category_id": cat_id,
            "category": names.get(cat_id, "Uncategorized"),
            "total": _money(total),
            "percent": round(float(_money(total) / grand_total * 100), 1)
            if grand_total
            else 0.0,
        }
        for cat_id, total in rows
    ]
    return sorted(result, key=lambda r: r["total"], reverse=True)


def monthly_trend(db: Session, user_id: int, months: int):
    today = date.today()
    first_index = today.year * 12 + (today.month - 1) - (months - 1)
    start = date(first_index // 12, first_index % 12 + 1, 1)

    year = extract("year", Expense.spent_on).label("y")
    month = extract("month", Expense.spent_on).label("m")
    rows = db.execute(
        select(year, month, func.sum(Expense.amount))
        .where(Expense.user_id == user_id, Expense.spent_on >= start)
        .group_by(year, month)
    ).all()
    totals = {f"{int(y):04d}-{int(m):02d}": _money(t) for y, m, t in rows}

    # Fill months with no spending so the chart has no gaps
    result = []
    for i in range(months):
        idx = first_index + i
        key = f"{idx // 12:04d}-{idx % 12 + 1:02d}"
        result.append({"month": key, "total": totals.get(key, ZERO)})
    return result

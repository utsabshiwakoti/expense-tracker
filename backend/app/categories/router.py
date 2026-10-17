from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.categories import service
from app.categories.models import Category
from app.categories.schemas import CategoryCreate, CategoryOut, CategoryUpdate
from app.core.database import get_db
from app.expenses.models import Expense

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return db.scalars(
        select(Category).where(Category.user_id == user.id).order_by(Category.name)
    ).all()


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if service.get_by_name(db, user.id, data.name):
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(name=data.name, user_id=user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoryOut)
def rename_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    category = service.get_owned_category(db, user.id, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    existing = service.get_by_name(db, user.id, data.name)
    if existing and existing.id != category.id:
        raise HTTPException(status_code=400, detail="Category already exists")
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    category = service.get_owned_category(db, user.id, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    in_use = db.scalar(
        select(func.count()).select_from(Expense).where(Expense.category_id == category.id)
    )
    if in_use:
        raise HTTPException(
            status_code=400,
            detail=f"Category is used by {in_use} expense(s). Reassign them first.",
        )
    db.delete(category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

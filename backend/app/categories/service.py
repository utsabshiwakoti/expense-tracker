from sqlalchemy import select
from sqlalchemy.orm import Session

from app.categories.models import Category

DEFAULT_CATEGORIES = [
    "Food",
    "Transport",
    "Housing",
    "Entertainment",
    "Health",
    "Shopping",
    "Other",
]


def create_default_categories(db: Session, user_id: int) -> None:
    """Called once when a user registers."""
    db.add_all([Category(name=n, user_id=user_id) for n in DEFAULT_CATEGORIES])


def get_owned_category(db: Session, user_id: int, category_id: int) -> Category | None:
    category = db.get(Category, category_id)
    if category is None or category.user_id != user_id:
        return None
    return category


def get_by_name(db: Session, user_id: int, name: str) -> Category | None:
    return db.scalar(
        select(Category).where(Category.user_id == user_id, Category.name == name)
    )

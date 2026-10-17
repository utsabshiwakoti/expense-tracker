from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models BEFORE create_all so every table gets created
from app.auth import models as auth_models  # noqa: F401
from app.categories import models as category_models  # noqa: F401
from app.expenses import models as expense_models  # noqa: F401

from app.auth.router import router as auth_router
from app.categories.router import router as categories_router
from app.core.config import settings
from app.core.database import Base, engine
from app.expenses.router import router as expenses_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(expenses_router)


@app.get("/health")
def health():
    return {"status": "ok"}

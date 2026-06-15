from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session
from datetime import date

from app import crud
from app import models
from app import llm

from app.database import (
    engine,
    Base,
    get_db
)

import app.db_models as db_models

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Monthly Expense Manager",
    version="1.0.0"
)


# ==========================
# HEALTH
# ==========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.0.0"
    }


# ==========================
# CATEGORIES
# ==========================

@app.post(
    "/categories",
    response_model=models.CategoryResponse,
    status_code=201
)
def create_category(
    data: models.CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(
        db,
        data
    )


@app.get(
    "/categories",
    response_model=list[models.CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return crud.get_categories(db)


# ==========================
# EXPENSES
# ==========================

@app.post(
    "/expenses",
    response_model=models.ExpenseResponse,
    status_code=201
)
def create_expense(
    data: models.ExpenseCreate,
    db: Session = Depends(get_db)
):

    category = db.query(
        db_models.Category
    ).filter(
        db_models.Category.id == data.category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Invalid category_id"
        )

    return crud.create_expense(
        db,
        data
    )


@app.get(
    "/expenses",
    response_model=list[models.ExpenseResponse]
)
def get_expenses(
    month: int = Query(None),
    year: int = Query(None),
    category_id: int = Query(None),
    db: Session = Depends(get_db)
):

    return crud.get_expenses(
        db,
        month,
        year,
        category_id
    )


@app.get(
    "/expenses/{expense_id}",
    response_model=models.ExpenseResponse
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    expense = crud.get_expense(
        db,
        expense_id
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


@app.put(
    "/expenses/{expense_id}",
    response_model=models.ExpenseResponse
)
def update_expense(
    expense_id: int,
    data: models.ExpenseUpdate,
    db: Session = Depends(get_db)
):

    expense = crud.update_expense(
        db,
        expense_id,
        data
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


@app.delete(
    "/expenses/{expense_id}",
    status_code=204
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    crud.delete_expense(
        db,
        expense_id
    )

    return None


# ==========================
# SUMMARY
# ==========================

@app.get("/summary/monthly")
def monthly_summary(
    db: Session = Depends(get_db)
):

    rows = crud.get_monthly_summary(db)

    return [
        {
            "year": int(row.year),
            "month": int(row.month),
            "total": round(row.total, 2)
        }
        for row in rows
    ]


@app.get("/summary/categories")
def category_summary(
    db: Session = Depends(get_db)
):

    rows = crud.get_category_totals(db)

    return [
        {
            "category": row.name,
            "total": round(row.total, 2)
        }
        for row in rows
    ]


# ==========================
# BUDGETS
# ==========================

@app.post(
    "/budget",
    status_code=201
)
def set_budget(
    data: models.BudgetCreate,
    db: Session = Depends(get_db)
):

    return crud.set_budget(
        db,
        data
    )


@app.get("/budget/alerts")
def budget_alerts(
    month: int = Query(date.today().month),
    year: int = Query(date.today().year),
    db: Session = Depends(get_db)
):

    return crud.get_budget_alerts(
        db,
        month,
        year
    )


# ==========================
# AI INSIGHTS (GROQ)
# ==========================

@app.post("/insights")
def get_insights(
    data: models.InsightRequest,
    db: Session = Depends(get_db)
):

    expenses = crud.get_expenses(
        db,
        month=data.month,
        year=data.year
    )

    cat_totals = crud.get_category_totals(db)

    alerts = crud.get_budget_alerts(
        db,
        data.month,
        data.year
    )

    insight = llm.analyse_spending(
        expenses,
        cat_totals,
        alerts,
        data.month,
        data.year
    )

    return {
        "month": data.month,
        "year": data.year,
        "insight": insight
    }
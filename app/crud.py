from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.db_models import Expense, Category, Budget
from app.models import (
    ExpenseCreate,
    ExpenseUpdate,
    CategoryCreate,
    BudgetCreate
)

# ==========================
# CATEGORY FUNCTIONS
# ==========================

def create_category(db: Session, data: CategoryCreate):
    category = Category(
        name=data.name,
        color=data.color
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session):
    return db.query(Category).all()


# ==========================
# EXPENSE FUNCTIONS
# ==========================

def create_expense(db: Session, data: ExpenseCreate):

    expense = Expense(
        amount=data.amount,
        description=data.description,
        date=data.date,
        category_id=data.category_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expenses(
    db: Session,
    month: int = None,
    year: int = None,
    category_id: int = None
):

    query = db.query(Expense)

    if month:
        query = query.filter(
            extract("month", Expense.date) == month
        )

    if year:
        query = query.filter(
            extract("year", Expense.date) == year
        )

    if category_id:
        query = query.filter(
            Expense.category_id == category_id
        )

    return query.order_by(
        Expense.date.desc()
    ).all()


def get_expense(
    db: Session,
    expense_id: int
):

    return db.query(Expense).filter(
        Expense.id == expense_id
    ).first()


def update_expense(
    db: Session,
    expense_id: int,
    data: ExpenseUpdate
):

    expense = get_expense(
        db,
        expense_id
    )

    if not expense:
        return None

    updates = data.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():
        setattr(
            expense,
            key,
            value
        )

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(
    db: Session,
    expense_id: int
):

    expense = get_expense(
        db,
        expense_id
    )

    if expense:
        db.delete(expense)
        db.commit()

    return True


# ==========================
# MONTHLY SUMMARY
# ==========================

def get_monthly_summary(db: Session):

    return db.query(
        extract(
            "year",
            Expense.date
        ).label("year"),

        extract(
            "month",
            Expense.date
        ).label("month"),

        func.sum(
            Expense.amount
        ).label("total")

    ).group_by(
        "year",
        "month"
    ).order_by(
        "year",
        "month"
    ).all()


# ==========================
# CATEGORY TOTALS
# ==========================

def get_category_totals(db: Session):

    return db.query(
        Category.name,

        func.sum(
            Expense.amount
        ).label("total")

    ).join(
        Expense
    ).group_by(
        Category.name
    ).all()


# ==========================
# BUDGET FUNCTIONS
# ==========================

def set_budget(
    db: Session,
    data: BudgetCreate
):

    existing = db.query(
        Budget
    ).filter(
        Budget.category_id == data.category_id
    ).first()

    if existing:
        existing.month_limit = data.month_limit

        db.commit()
        db.refresh(existing)

        return existing

    budget = Budget(
        category_id=data.category_id,
        month_limit=data.month_limit
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget


def get_budget_alerts(
    db: Session,
    month: int,
    year: int
):

    spending = db.query(
        Expense.category_id,

        func.sum(
            Expense.amount
        ).label("spent")

    ).filter(
        extract(
            "month",
            Expense.date
        ) == month,

        extract(
            "year",
            Expense.date
        ) == year

    ).group_by(
        Expense.category_id
    ).all()

    alerts = []

    for row in spending:

        budget = db.query(
            Budget
        ).filter(
            Budget.category_id == row.category_id
        ).first()

        if budget and row.spent > budget.month_limit:

            category = db.query(
                Category
            ).filter(
                Category.id == row.category_id
            ).first()

            alerts.append({
                "category": category.name,
                "spent": round(row.spent, 2),
                "limit": budget.month_limit,
                "over_by": round(
                    row.spent - budget.month_limit,
                    2
                )
            })

    return alerts
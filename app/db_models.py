from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base

from datetime import date


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(20), default="#0078D4")

    expenses = relationship(
        "Expense",
        back_populates="category"
    )


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)

    description = Column(String(255), nullable=False)

    date = Column(
        Date,
        default=date.today,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="expenses"
    )


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    month_limit = Column(
        Float,
        nullable=False
    )
    
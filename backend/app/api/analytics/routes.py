from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date, timedelta

from app.db.session import get_db
from app.models.expense import Expense
from app.api.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/monthly-total")
async def monthly_total(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    today = date.today()

    result = await db.execute(
        select(func.coalesce(func.sum(Expense.amount), 0))
        .where(Expense.user_id == user.id)
        .where(func.date_part("month", Expense.created_at) == today.month)
        .where(func.date_part("year", Expense.created_at) == today.year)
    )

    total = result.scalar()

    return {
        "month": today.strftime("%B"),
        "year": today.year,
        "total_spent": total
    }

@router.get("/by-category")
async def expenses_by_category(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .where(Expense.user_id == user.id)
        .group_by(Expense.category)
    )

    rows = result.all()

    return [
        {
            "category": row.category,
            "total": row.total
        }
        for row in rows
    ]

@router.get("/last-7-days")
async def last_7_days_trend(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    start_date = date.today() - timedelta(days=6)

    result = await db.execute(
        select(
            func.date(Expense.created_at).label("day"),
            func.sum(Expense.amount).label("total")
        )
        .where(Expense.user_id == user.id)
        .where(Expense.created_at >= start_date)
        .group_by(func.date(Expense.created_at))
        .order_by(func.date(Expense.created_at))
    )

    rows = result.all()

    return [
        {
            "date": row.day,
            "total": row.total
        }
        for row in rows
    ]

@router.get("/last-30-days")
async def last_30_days_trend(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    start_date = date.today() - timedelta(days=29)

    result = await db.execute(
        select(
            func.date(Expense.created_at).label("day"),
            func.sum(Expense.amount).label("total")
        )
        .where(Expense.user_id == user.id)
        .where(Expense.created_at >= start_date)
        .group_by(func.date(Expense.created_at))
        .order_by(func.date(Expense.created_at))
    )

    rows = result.all()

    return [
        {
            "date": row.day,
            "total": row.total
        }
        for row in rows
    ]
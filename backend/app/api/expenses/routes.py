from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.api.auth.dependencies import get_current_user
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy import func

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    new_expense = Expense(
        id=uuid.uuid4(),
        user_id=user.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        created_at=datetime.utcnow()
    )

    db.add(new_expense)
    await db.commit()   
    await db.refresh(new_expense)  

    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
async def list_expenses(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Expense).where(Expense.user_id == user.id)
    )
    expenses = result.scalars().all()
    return expenses

@router.get("/by-category/{category}", response_model=list[ExpenseResponse])
async def expenses_by_category(
    category: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Expense).where(
            Expense.user_id == user.id,
            Expense.category == category
        )
    )
    return result.scalars().all()

@router.get("/by-date", response_model=list[ExpenseResponse])
async def expenses_by_date(
    start: datetime,
    end: datetime,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(Expense).where(
            Expense.user_id == user.id,
            Expense.created_at.between(start, end)
        )
    )
    return result.scalars().all()

@router.get("/summary/monthly")
async def monthly_summary(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    result = await db.execute(
        select(
            func.sum(Expense.amount).label("total"),
            Expense.category
        )
        .where(Expense.user_id == user.id)
        .group_by(Expense.category)
    )

    rows = result.all()

    return {
        "total": sum(r.total for r in rows),
        "by_category": [
            {"category": r.category, "amount": r.total}
            for r in rows
        ]
    }
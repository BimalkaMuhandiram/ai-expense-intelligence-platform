from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.api.auth.dependencies import get_current_user
import uuid
from datetime import datetime

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
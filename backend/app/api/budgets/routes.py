from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.api.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/", response_model=BudgetResponse)
async def set_budget(
    budget: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    new_budget = Budget(
        user_id=user.id,
        monthly_limit=budget.monthly_limit
    )

    db.add(new_budget)
    await db.commit()
    await db.refresh(new_budget)

    return new_budget
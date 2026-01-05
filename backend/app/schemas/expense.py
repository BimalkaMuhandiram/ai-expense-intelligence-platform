from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str | None = None

class ExpenseResponse(BaseModel):
    id: UUID
    amount: float
    category: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True
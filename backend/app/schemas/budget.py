from pydantic import BaseModel

class BudgetCreate(BaseModel):
    monthly_limit: float

class BudgetResponse(BaseModel):
    monthly_limit: float
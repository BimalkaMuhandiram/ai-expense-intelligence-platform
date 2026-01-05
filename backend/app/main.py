from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models import user
from app.api.auth.routes import router as auth_router
from app.core.dependencies import get_current_user
from app.core.dependencies import require_admin
from app.api.expenses.routes import router as expense_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(expense_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
    
@app.get("/protected")
def protected(user_id: str = Depends(get_current_user)):
    return {"message": f"Hello user {user_id}"}

@app.get("/admin")
def admin_dashboard(user=Depends(require_admin)):
    return {"message": "Welcome Admin"}
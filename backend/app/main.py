from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models import user
from app.api.auth.routes import router as auth_router
from app.core.dependencies import get_current_user
from app.core.dependencies import require_admin
from app.api.expenses.routes import router as expense_router
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.api.admin.routes import router as admin_router
from app.api.analytics.routes import router as analytics_router
from app.api.budgets.routes import router as budget_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(budget_router)

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

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )
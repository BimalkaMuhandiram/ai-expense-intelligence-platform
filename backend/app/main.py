from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.models import user
from app.api.auth.routes import router as auth_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
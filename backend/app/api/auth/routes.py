from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.schemas.auth import LoginRequest
from app.core.exceptions import AppException
from app.db.session import get_db
from app.core.security import hash_password
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer"
        )

    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully"
    }

@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(f"Login failed | email={form_data.username}")
        raise AppException("Invalid email or password", status_code=401)

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })
    logger.info(f"User login success | user_id={user.id}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
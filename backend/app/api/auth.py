from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..schemas.user import UserCreate, UserLogin, TokenResponse
from ..services import auth as auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, data)


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_service.login(db, data.email, data.password)

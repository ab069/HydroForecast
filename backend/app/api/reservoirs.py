from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.reservoir import ReservoirCreate, ReservoirUpdate, ReservoirResponse
from ..services.reservoir_service import (
    create_reservoir,
    get_reservoirs,
    get_reservoir,
    update_reservoir,
    delete_reservoir,
    get_stats,
)

router = APIRouter(prefix="/api/reservoirs", tags=["reservoirs"])


@router.get("/stats")
async def reservoir_stats(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_stats(db, current_user.id)


@router.get("")
async def list_reservoirs(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_reservoirs(db, current_user.id)


@router.post("")
async def new_reservoir(data: ReservoirCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_reservoir(db, current_user.id, data)


@router.get("/{reservoir_id}")
async def get_reservoir_endpoint(reservoir_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_reservoir(db, current_user.id, reservoir_id)


@router.put("/{reservoir_id}")
async def update_reservoir_endpoint(reservoir_id: str, data: ReservoirUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_reservoir(db, current_user.id, reservoir_id, data)


@router.delete("/{reservoir_id}")
async def delete_reservoir_endpoint(reservoir_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_reservoir(db, current_user.id, reservoir_id)
    return {"message": "Reservoir deleted"}

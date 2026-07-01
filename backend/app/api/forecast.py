from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.production import ProductionCreate
from ..services.forecast_service import (
    create_forecast,
    get_forecasts,
    get_forecast,
    delete_forecast,
    get_forecast_stats,
)

router = APIRouter(prefix="/api/forecasts", tags=["forecasts"])


@router.get("/stats")
async def forecast_stats(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_forecast_stats(db, current_user.id)


@router.get("")
async def list_forecasts(
    reservoir_id: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_forecasts(db, current_user.id, reservoir_id)


@router.post("")
async def new_forecast(data: ProductionCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_forecast(db, current_user.id, data)


@router.get("/{forecast_id}")
async def get_forecast_endpoint(forecast_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_forecast(db, current_user.id, forecast_id)


@router.delete("/{forecast_id}")
async def delete_forecast_endpoint(forecast_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_forecast(db, current_user.id, forecast_id)
    return {"message": "Forecast deleted"}

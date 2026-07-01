from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from ..models.production import ProductionForecast
from ..schemas.production import ProductionCreate


async def create_forecast(db: AsyncSession, user_id: str, data: ProductionCreate) -> ProductionForecast:
    forecast = ProductionForecast(
        user_id=user_id,
        reservoir_id=data.reservoir_id,
        oil_rate_bpd=data.oil_rate_bpd,
        gas_rate_mmscfd=data.gas_rate_mmscfd,
        water_rate_bpd=data.water_rate_bpd,
        cumulative_oil_mmboe=data.cumulative_oil_mmboe,
        cumulative_gas_bcf=data.cumulative_gas_bcf,
        water_cut_pct=data.water_cut_pct,
        gor=data.gor,
        days_on_production=data.days_on_production,
    )
    db.add(forecast)
    await db.commit()
    await db.refresh(forecast)
    return forecast


async def get_forecasts(db: AsyncSession, user_id: str, reservoir_id: str | None = None) -> list[ProductionForecast]:
    query = select(ProductionForecast).where(ProductionForecast.user_id == user_id)
    if reservoir_id:
        query = query.where(ProductionForecast.reservoir_id == reservoir_id)
    query = query.order_by(ProductionForecast.forecast_date.asc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_forecast(db: AsyncSession, user_id: str, forecast_id: str) -> ProductionForecast:
    result = await db.execute(select(ProductionForecast).where(ProductionForecast.id == forecast_id, ProductionForecast.user_id == user_id))
    forecast = result.scalar_one_or_none()
    if not forecast:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forecast not found")
    return forecast


async def delete_forecast(db: AsyncSession, user_id: str, forecast_id: str) -> None:
    forecast = await get_forecast(db, user_id, forecast_id)
    await db.delete(forecast)
    await db.commit()


async def get_forecast_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(ProductionForecast).where(ProductionForecast.user_id == user_id))
    forecasts = list(result.scalars().all())
    total_entries = len(forecasts)
    avg_oil_rate = sum(f.oil_rate_bpd for f in forecasts) / total_entries if total_entries else 0
    avg_water_cut = sum(f.water_cut_pct for f in forecasts) / total_entries if total_entries else 0
    return {
        "total_entries": total_entries,
        "avg_oil_rate_bpd": round(avg_oil_rate, 2),
        "avg_water_cut_pct": round(avg_water_cut, 2),
    }

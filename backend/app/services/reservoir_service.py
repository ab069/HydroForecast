from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from ..models.reservoir import Reservoir
from ..schemas.reservoir import ReservoirCreate, ReservoirUpdate


async def create_reservoir(db: AsyncSession, user_id: str, data: ReservoirCreate) -> Reservoir:
    reservoir = Reservoir(
        user_id=user_id,
        reservoir_name=data.reservoir_name,
        field_name=data.field_name,
        reservoir_type=data.reservoir_type,
        depth_m=data.depth_m,
        porosity_pct=data.porosity_pct,
        permeability_md=data.permeability_md,
        pressure_initial=data.pressure_initial,
        pressure_current=data.pressure_current or data.pressure_initial,
        temperature_c=data.temperature_c,
        oil_in_place_mmboe=data.oil_in_place_mmboe,
        gas_in_place_bcf=data.gas_in_place_bcf,
        recovery_factor_pct=data.recovery_factor_pct,
    )
    db.add(reservoir)
    await db.commit()
    await db.refresh(reservoir)
    return reservoir


async def get_reservoirs(db: AsyncSession, user_id: str) -> list[Reservoir]:
    result = await db.execute(select(Reservoir).where(Reservoir.user_id == user_id).order_by(Reservoir.created_at.desc()))
    return list(result.scalars().all())


async def get_reservoir(db: AsyncSession, user_id: str, reservoir_id: str) -> Reservoir:
    result = await db.execute(select(Reservoir).where(Reservoir.id == reservoir_id, Reservoir.user_id == user_id))
    reservoir = result.scalar_one_or_none()
    if not reservoir:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservoir not found")
    return reservoir


async def update_reservoir(db: AsyncSession, user_id: str, reservoir_id: str, data: ReservoirUpdate) -> Reservoir:
    reservoir = await get_reservoir(db, user_id, reservoir_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reservoir, key, value)
    await db.commit()
    await db.refresh(reservoir)
    return reservoir


async def delete_reservoir(db: AsyncSession, user_id: str, reservoir_id: str) -> None:
    reservoir = await get_reservoir(db, user_id, reservoir_id)
    await db.delete(reservoir)
    await db.commit()


async def get_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(Reservoir).where(Reservoir.user_id == user_id))
    reservoirs = list(result.scalars().all())
    total_reservoirs = len(reservoirs)
    total_ooip = sum(r.oil_in_place_mmboe for r in reservoirs)
    avg_recovery = sum(r.recovery_factor_pct for r in reservoirs) / total_reservoirs if total_reservoirs else 0
    active_fields = len(set(r.field_name for r in reservoirs))
    return {
        "total_reservoirs": total_reservoirs,
        "total_ooip_mmboe": round(total_ooip, 2),
        "avg_recovery_factor_pct": round(avg_recovery, 2),
        "active_fields": active_fields,
    }

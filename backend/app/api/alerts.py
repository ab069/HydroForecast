from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.alert import AlertUpdate
from ..services.alert_service import get_alerts, update_alert_status, get_alert_stats

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/stats")
async def alert_stats(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_alert_stats(db, current_user.id)


@router.get("")
async def list_alerts(
    status: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_alerts(db, current_user.id, status)


@router.put("/{alert_id}")
async def update_alert(alert_id: str, data: AlertUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_alert_status(db, current_user.id, alert_id, data)

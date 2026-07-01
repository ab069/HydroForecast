from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
from ..models.alert import Alert
from ..schemas.alert import AlertUpdate


async def get_alerts(db: AsyncSession, user_id: str, status_filter: str | None = None) -> list[Alert]:
    query = select(Alert).where(Alert.user_id == user_id)
    if status_filter:
        query = query.where(Alert.status == status_filter)
    query = query.order_by(Alert.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_alert_status(db: AsyncSession, user_id: str, alert_id: str, data: AlertUpdate) -> Alert:
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.user_id == user_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    alert.status = data.status
    await db.commit()
    await db.refresh(alert)
    return alert


async def get_alert_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(Alert).where(Alert.user_id == user_id))
    alerts = list(result.scalars().all())
    active = sum(1 for a in alerts if a.status == "active")
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for a in alerts:
        if a.severity in by_severity:
            by_severity[a.severity] += 1
    return {
        "total": len(alerts),
        "active": active,
        "by_severity": by_severity,
    }

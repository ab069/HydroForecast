from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db, async_session
from ..core.security import decode_token
from ..models.production import ProductionForecast
from ..models.reservoir import Reservoir
from ..agents.forecast_engine import (
    analyze_decline,
    calculate_recovery,
    detect_water_breakthrough,
    calculate_forecast_confidence,
    generate_forecast_report,
)
from sqlalchemy import select
from ..models.alert import Alert
import json

router = APIRouter()


@router.websocket("/ws/forecast/{reservoir_id}")
async def forecast_websocket(websocket: WebSocket, reservoir_id: str):
    await websocket.accept()
    token = None
    try:
        token_data = await websocket.receive_text()
        token_data = json.loads(token_data)
        token = token_data.get("token")
        if not token:
            await websocket.send_json({"error": "No token provided"})
            await websocket.close()
            return
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception:
        await websocket.send_json({"error": "Authentication failed"})
        await websocket.close()
        return

    try:
        async with async_session() as db:
            result = await db.execute(select(Reservoir).where(Reservoir.id == reservoir_id, Reservoir.user_id == user_id))
            reservoir = result.scalar_one_or_none()
            if not reservoir:
                await websocket.send_json({"error": "Reservoir not found"})
                await websocket.close()
                return

            result = await db.execute(
                select(ProductionForecast)
                .where(ProductionForecast.reservoir_id == reservoir_id, ProductionForecast.user_id == user_id)
                .order_by(ProductionForecast.forecast_date.asc())
            )
            forecasts = list(result.scalars().all())

            if not forecasts:
                await websocket.send_json({"error": "No production data found"})
                await websocket.close()
                return

            oil_rates = [f.oil_rate_bpd for f in forecasts]
            days = [f.days_on_production for f in forecasts]
            latest = forecasts[-1]

            decline = analyze_decline(oil_rates, days)
            recovery = calculate_recovery(latest.cumulative_oil_mmboe, reservoir.oil_in_place_mmboe)
            wb = detect_water_breakthrough(latest.water_cut_pct, latest.water_rate_bpd)
            confidence = calculate_forecast_confidence(len(forecasts), reservoir.pressure_current > 0.8 * reservoir.pressure_initial)

            findings = {
                "decline_analysis": decline,
                "recovery_analysis": recovery,
                "water_breakthrough": wb,
                "confidence": confidence,
            }
            report = generate_forecast_report(reservoir.reservoir_name, findings)

            await websocket.send_json({"type": "analysis", "data": findings, "report": report})

            while True:
                data = await websocket.receive_text()
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except Exception:
            pass

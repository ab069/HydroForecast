from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductionCreate(BaseModel):
    reservoir_id: str
    oil_rate_bpd: float
    gas_rate_mmscfd: float
    water_rate_bpd: float
    cumulative_oil_mmboe: float
    cumulative_gas_bcf: float
    water_cut_pct: float
    gor: float
    days_on_production: int


class ProductionResponse(BaseModel):
    id: str
    user_id: str
    reservoir_id: str
    forecast_date: datetime
    oil_rate_bpd: float
    gas_rate_mmscfd: float
    water_rate_bpd: float
    cumulative_oil_mmboe: float
    cumulative_gas_bcf: float
    water_cut_pct: float
    gor: float
    days_on_production: int
    created_at: datetime

    model_config = {"from_attributes": True}

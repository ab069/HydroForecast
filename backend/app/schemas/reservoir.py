from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReservoirCreate(BaseModel):
    reservoir_name: str
    field_name: str
    reservoir_type: str
    depth_m: float
    porosity_pct: float
    permeability_md: float
    pressure_initial: float
    pressure_current: Optional[float] = None
    temperature_c: float = 25.0
    oil_in_place_mmboe: float
    gas_in_place_bcf: float
    recovery_factor_pct: float


class ReservoirUpdate(BaseModel):
    reservoir_name: Optional[str] = None
    field_name: Optional[str] = None
    pressure_current: Optional[float] = None
    recovery_factor_pct: Optional[float] = None


class ReservoirResponse(BaseModel):
    id: str
    user_id: str
    reservoir_name: str
    field_name: str
    reservoir_type: str
    depth_m: float
    porosity_pct: float
    permeability_md: float
    pressure_initial: float
    pressure_current: float
    temperature_c: float
    oil_in_place_mmboe: float
    gas_in_place_bcf: float
    recovery_factor_pct: float
    created_at: datetime

    model_config = {"from_attributes": True}

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertResponse(BaseModel):
    id: str
    user_id: str
    reservoir_id: str
    title: str
    alert_type: str
    severity: str
    status: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertUpdate(BaseModel):
    status: str

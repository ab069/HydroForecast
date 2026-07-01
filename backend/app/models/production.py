import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base


class ProductionForecast(Base):
    __tablename__ = "production_forecasts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    reservoir_id: Mapped[str] = mapped_column(String(36), ForeignKey("reservoirs.id"), nullable=False)
    forecast_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    oil_rate_bpd: Mapped[float] = mapped_column(Float, nullable=False)
    gas_rate_mmscfd: Mapped[float] = mapped_column(Float, nullable=False)
    water_rate_bpd: Mapped[float] = mapped_column(Float, nullable=False)
    cumulative_oil_mmboe: Mapped[float] = mapped_column(Float, nullable=False)
    cumulative_gas_bcf: Mapped[float] = mapped_column(Float, nullable=False)
    water_cut_pct: Mapped[float] = mapped_column(Float, nullable=False)
    gor: Mapped[float] = mapped_column(Float, nullable=False)
    days_on_production: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="forecasts")
    reservoir = relationship("Reservoir", back_populates="forecasts")

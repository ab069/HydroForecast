import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base


class Reservoir(Base):
    __tablename__ = "reservoirs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    reservoir_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    reservoir_type: Mapped[str] = mapped_column(String(50), nullable=False)
    depth_m: Mapped[float] = mapped_column(Float, nullable=False)
    porosity_pct: Mapped[float] = mapped_column(Float, nullable=False)
    permeability_md: Mapped[float] = mapped_column(Float, nullable=False)
    pressure_initial: Mapped[float] = mapped_column(Float, nullable=False)
    pressure_current: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)
    oil_in_place_mmboe: Mapped[float] = mapped_column(Float, nullable=False)
    gas_in_place_bcf: Mapped[float] = mapped_column(Float, nullable=False)
    recovery_factor_pct: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="reservoirs")
    forecasts = relationship("ProductionForecast", back_populates="reservoir", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="reservoir", cascade="all, delete-orphan")

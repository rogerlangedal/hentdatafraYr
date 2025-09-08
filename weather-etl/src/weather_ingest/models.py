from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    altitude_m: Mapped[int | None] = mapped_column(Integer, nullable=True)

class ForecastRaw(Base):
    __tablename__ = "forecast_raw"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column()
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_modified: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload_json = mapped_column(JSON)

class ForecastPoint(Base):
    __tablename__ = "forecast_point"
    # Composite primary key to allow upsert via session.merge()
    location_id: Mapped[int] = mapped_column(primary_key=True)
    forecast_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    temp_c: Mapped[float | None]
    wind_mps: Mapped[float | None]
    wind_from_deg: Mapped[float | None]
    precip_mm_1h: Mapped[float | None]
    precip_mm_6h: Mapped[float | None]
    cloud_area_frac: Mapped[float | None]
    symbol_code: Mapped[str | None] = mapped_column(String(40))

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TelemetryCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accel_x: float
    accel_y: float
    accel_z: float


class TelemetryResponse(TelemetryCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True) 


class TelemetryPage(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TelemetryResponse]

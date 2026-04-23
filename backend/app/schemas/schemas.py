from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TelemetryCreate(BaseModel):
    # TODO додати валідацію даних (ge=-90, le=90)
    latitude: float
    longitude: float
    accel_x: float
    accel_y: float
    accel_z: float


class TelemetryResponse(TelemetryCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


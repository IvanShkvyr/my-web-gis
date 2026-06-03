from typing import Optional, List, Tuple
from datetime import date, datetime, timezone, timedelta

from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryCreate


def create(
        db: Session,
        data: TelemetryCreate,
        user_id: Optional[int] = None,
        ) -> Telemetry:
    """
    Persists a telemetry record to the database.
    """
    record = Telemetry(
        accel_x=data.accel_x,
        accel_y=data.accel_y,
        accel_z=data.accel_z,
        geom=WKTElement(f"POINT({data.longitude} {data.latitude})", srid=4326),
        user_id=user_id,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_list_by_user(
        db: Session,
        *,
        user_ids: List[int],
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 50,
        offset: int = 0,
        ) -> Tuple[List[Telemetry], int]:
    """
    Return paginated telemetry records for a specific user.
    """
    query = db.query(Telemetry).filter(Telemetry.user_id.in_(user_ids))

    if date_from:
        query = query.filter(
            Telemetry.timestamp >= datetime(
                date_from.year, date_from.month, date_from.day,
                tzinfo=timezone.utc,
                )
        )

    if date_to:
        end = datetime(date_to.year, date_to.month, date_to.day,
                        tzinfo=timezone.utc) + timedelta(days=1)
        query = query.filter(Telemetry.timestamp < end)

    total = query.count()
    records = (
        query
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return records, total

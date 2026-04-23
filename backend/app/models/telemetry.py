from sqlalchemy import Column, Integer, Float, DateTime, func
from geoalchemy2 import Geometry

from app.models.base_class import Base


class Telemetry(Base):
    """
    """
    __tablename__ = "phone_telemetry"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    accel_x = Column(Float, nullable=False)
    accel_y = Column(Float, nullable=False)
    accel_z = Column(Float, nullable=False)

    # Геометрія: Точка (Point), SRID 4326 (стандарт для GPS/WGS84)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)


    # from sqlalchemy import Index TODO
    # Index("idx_telemetry_geom", Telemetry.geom, postgresql_using="gist")



from sqlalchemy import Column, Integer, Float, DateTime, func, ForeignKey, Index
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

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
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
        )

    __table_args__ = (
        Index("idx_phone_telemetry_user_timestamp", "user_id", "timestamp"),
        Index("idx_phone_telemetry_geom", "geom", postgresql_using="gist"),
    )

    @property
    def latitude(self) -> float:
        """Extract latitude from PostGIS geometry"""
        return to_shape(self.geom).y
    

    @property
    def longitude(self):
        """Extract longitude from PostGIS geometry"""
        return to_shape(self.geom).x

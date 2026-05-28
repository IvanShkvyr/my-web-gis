import logging
from typing import Dict

from sqlalchemy import text
from sqlalchemy.engine import Engine


logger = logging.getLogger(__name__)


_SHAPES_TABLE = "vil"


def get_geojson_feature_collection(engine: Engine) -> Dict:
    """
    Returns all shapes from the `vil` table as a GeoJSON FeatureCollection.
    """
    query = text(f"""
                SELECT json_build_object(
                    'type', 'FeatureCollection',
                    'features', json_agg(ST_AsGeoJSON(t.*)::json)
                )
                FROM (SELECT * FROM "{_SHAPES_TABLE}") AS t;
            """)
    try:
        with engine.connect() as conn:
            
            result = conn.execute(query).fetchone()

            if result and result[0]:
                return result[0]
            
            return {"type": "FeatureCollection", "features": []}
      
    except Exception:
        logger.exception("Failed to fetch shapes from database")
        raise

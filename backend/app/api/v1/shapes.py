import logging
 
from fastapi import APIRouter, HTTPException
 
from app.crud import shapes as shapes_crud
from app.database import engine
 
logger = logging.getLogger(__name__)
 
router = APIRouter(prefix="/api/v1", tags=["shapes"])
 
 
@router.get("/shapes")
def get_shapes():
    """
    Returns all geographic shapes as a GeoJSON FeatureCollection.
 
    Used by Leaflet on the frontend to render map layers.
    """
    try:
        return shapes_crud.get_geojson_feature_collection(engine)

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to load map data. Please try again later.",
        )

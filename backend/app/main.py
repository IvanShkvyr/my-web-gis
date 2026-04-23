from pathlib import Path
from typing import List


from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models.telemetry import Telemetry
from app.schemas.schemas import TelemetryCreate, TelemetryResponse


BASE_DIR = Path(__file__).resolve().parent.parent

frontend_dir = BASE_DIR.parent / "frontend"


app = FastAPI(title="My Web GIS API")


# --- Static ---


app.mount("/css", StaticFiles(directory=frontend_dir / "css"), name="css")
app.mount("/js", StaticFiles(directory=frontend_dir / "js"), name="js")
app.mount("/media", StaticFiles(directory=frontend_dir / "media"), name="media")


# --- API for Telemetry ---


@app.post("/api/telemetry", response_model=TelemetryResponse)
def create_telemetry(data: TelemetryCreate, db: Session = Depends(get_db)):
    """Receives data from the phone and saves it to the database"""
    try:
        point_wkt = f"POINT({data.longitude} {data.latitude})"

        new_entry = Telemetry(
            accel_x=data.accel_x,
            accel_y=data.accel_y,
            accel_z=data.accel_z,
            geom=point_wkt
        )

        db.add(new_entry)
        db.commit()
        # db.refresh(new_entry)

        return {"status": "success", "message": "Дані збережено в Supabase"}

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Write error: {e}")


@app.get("/api/telemetry", response_model=List[TelemetryResponse])
def get_telemetry(db: Session = Depends(get_db)):    
    """Return a list of all collected telemetry"""
    return db.query(Telemetry).all()


# --- API  ---


@app.get("/api/shapes")
def get_shapes():
    try:
        with engine.connect() as conn:
            
            table_name = "vil" 
            
            
            query = text(f"""
                SELECT json_build_object(
                    'type', 'FeatureCollection',
                    'features', json_agg(ST_AsGeoJSON(t.*)::json)
                )
                FROM (SELECT * FROM "{table_name}") AS t;
            """)
            
            result = conn.execute(query).fetchone()
            
            # Перевіряємо, чи є дані
            if result and result[0]:
                return result[0]
            
            return {"type": "FeatureCollection", "features": []}
      
    except Exception as e:
        print(f"ПОМИЛКА БАЗИ ДАНИХ: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    return FileResponse(frontend_dir / "index.html")


@app.get("/{page_name}.html")
async def get_page(page_name: str):
    if not page_name.endswith(".html"):
        page_name += ".html"

    file_path = frontend_dir / page_name
    print(file_path)
    if file_path.exists():
        return FileResponse(file_path)
    
    return {"detail": f"Сторінку {page_name} не знайдено в {frontend_dir}"}


@app.get("/test-db")
def test_connection():
    try:
        with engine.connect() as conn:
            return {"status": "success", "message": "З'єднання з Supabase встановлено!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}




# uvicorn app.main:app --reload

# python -m uvicorn app.main:app --reload

# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# http://10.0.0.2:8000


# alembic revision --autogenerate -m "Create telemetry table"
# alembic upgrade head

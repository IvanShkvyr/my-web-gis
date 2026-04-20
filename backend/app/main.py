import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
frontend_dir = BASE_DIR.parent / "frontend"
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


safe_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
safe_user = quote_plus(DB_USER) if DB_USER else ""

DATABASE_URL = (
    f"postgresql://{safe_user}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
               )
engine = create_engine(DATABASE_URL)


app = FastAPI(title="My Web GIS API")


app.mount("/css", StaticFiles(directory=frontend_dir / "css"), name="css")
app.mount("/js", StaticFiles(directory=frontend_dir / "js"), name="js")
app.mount("/media", StaticFiles(directory=frontend_dir / "media"), name="media")

@app.get("/api/shapes")
def get_shapes():
    try:
        with engine.connect() as conn:
            # УВАГА: Заміни 'spatial_data' на назву своєї таблиці з QGIS
            table_name = "vil" 
            
            # Цей запит формує GeoJSON прямо всередині PostgreSQL
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




# uvicorn backend.app.main:app --reload

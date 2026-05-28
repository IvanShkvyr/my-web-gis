import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings, FRONTEND_DIR  


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: database warm-up, cache loading
    logger.info(
        "Startup | env=%s | frontend=%s", settings.APP_ENV, FRONTEND_DIR
    )
    yield
    logger.info("Shutdown complete")


# --- App ---
app = FastAPI(
    title="My Web GIS API",
    lifespan=lifespan,
    )

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# --- API Router ---
app.include_router(api_router)

# --- Static ---
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

logger.info("Application startup complete. Frontend dir: %s", FRONTEND_DIR)

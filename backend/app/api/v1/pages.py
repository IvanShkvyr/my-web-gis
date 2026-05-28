from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import FRONTEND_DIR


router = APIRouter(tags=["pages"])


@router.get("/", response_class=FileResponse)
async def root():
    """Serves the main page."""
    return FileResponse(FRONTEND_DIR / "index.html")


@router.get("/{page_name}.html", response_class=FileResponse)
async def get_page(page_name: str):
    """
    Serves a frontend HTML page by name.
    """
    if ".." in page_name or "/" in page_name or "\\" in page_name:
        raise HTTPException(status_code=400, detail="Invalid page name")

    file_path = (FRONTEND_DIR / f"{page_name}.html").resolve()

    if not file_path.is_relative_to(FRONTEND_DIR):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists():
        raise HTTPException(
                        status_code=404,
                        detail=f"Page {page_name} not found in {FRONTEND_DIR}"
                        )

    return FileResponse(file_path)

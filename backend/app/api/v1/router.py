from fastapi import APIRouter

from app.api.v1 import users, telemetry, shapes, pages


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(telemetry.router)
api_router.include_router(shapes.router)
api_router.include_router(pages.router)

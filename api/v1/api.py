from fastapi import APIRouter

from api.v1.routers import health


def get_api():
    api_router = APIRouter()
    api_router.include_router(health.router)
    return api_router

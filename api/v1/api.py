from fastapi import APIRouter

from api.v1.routers import health, schools


def get_api():
    api_router = APIRouter()
    api_router.include_router(health.router)
    api_router.include_router(schools.router, prefix="/schools")
    return api_router

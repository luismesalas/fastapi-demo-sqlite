from fastapi import APIRouter

from api.v1.routers import health, schools, positions, assignments


def get_api():
    api_router = APIRouter()
    api_router.include_router(health.router)
    api_router.include_router(schools.router, prefix="/schools")
    api_router.include_router(positions.router, prefix="/positions")
    api_router.include_router(assignments.router, prefix="/assignments")
    return api_router

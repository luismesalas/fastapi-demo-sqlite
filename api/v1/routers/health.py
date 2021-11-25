from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"message": "API is alive"}

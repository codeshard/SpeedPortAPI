from fastapi import APIRouter, status

from app.health.models import HealthCheckModel

router = APIRouter()


@router.get(
    "/health",
    tags=["health-check"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckModel,
)
def get_health() -> HealthCheckModel:
    return HealthCheckModel(status="OK")

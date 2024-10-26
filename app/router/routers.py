from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.core.settings import get_settings
from app.core.utils import get_field, http_get_encrypted_json
from app.router.models import Router

router = APIRouter()
settings = get_settings()


@router.get(
    "/info",
    tags=["router"],
    summary="Get Router Info",
    status_code=status.HTTP_200_OK,
    response_model=Router,
)
async def get_router() -> Router:
    host = settings.speedport_host
    key = settings.default_key
    request, err = await http_get_encrypted_json(key, f"http://{host}/data/Router.json")
    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status from {host}",
        )
    info_fields = [
        "device_name",
        "factorydefault",
        "rebooting",
        "router_state",
        "dsl_link_status",
        "ap_mode",
        "onlinestatus",
        "days_online",
        "time_online",
        "inet_uptime",
        "domain_name",
    ]
    return {field: get_field(request, field) for field in info_fields}

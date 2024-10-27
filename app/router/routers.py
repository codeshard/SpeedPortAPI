from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.core.settings import get_settings
from app.core.utils import get_encrypted_json, get_field
from app.router.models import InfoModel, RouterModel, StatusModel

router = APIRouter()
settings = get_settings()


@router.get(
    "/status",
    tags=["router"],
    summary="Get Router Status",
    status_code=status.HTTP_200_OK,
    response_model=StatusModel,
)
async def get_status(human_readable: bool = False) -> StatusModel:
    request, err = await get_encrypted_json(path="data/Status.json")
    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status from {settings.speedport_host}",
        )
    router_fields = [
        "device_name",
        "factorydefault",
        "router_state",
    ]
    status_fields = [
        "firmware_version",
        "serial_number",
        "modem_id",
        "dsl_downstream",
        "dsl_upstream",
        "inet_download",
        "inet_upload",
        "use_wlan",
        "use_wps",
        "wlan_ssid",
        "wlan_5ghz_ssid",
    ]
    router_data = {field: get_field(request, field) for field in router_fields}
    status_data = {
        field: get_field(request, field, human_readable) for field in status_fields
    }
    return StatusModel(router=RouterModel(**router_data), **status_data)


@router.get(
    "/info",
    tags=["router"],
    summary="Get Router Info",
    status_code=status.HTTP_200_OK,
    response_model=InfoModel,
)
async def get_router(human_readable: bool = False) -> InfoModel:
    request, err = await get_encrypted_json(path="data/Router.json")
    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status from {settings.speedport_host}",
        )
    router_fields = [
        "device_name",
        "factorydefault",
        "router_state",
    ]
    info_fields = [
        "rebooting",
        "dsl_link_status",
        "ap_mode",
        "onlinestatus",
        "days_online",
        "time_online",
        "inet_uptime",
        "domain_name",
    ]
    router_data = {field: get_field(request, field) for field in router_fields}
    info_data = {
        field: get_field(request, field, human_readable) for field in info_fields
    }
    return InfoModel(router=RouterModel(**router_data), **info_data)

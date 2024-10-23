from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.core.settings import get_settings
from app.core.utils import get_field, http_get_encrypted_json
from app.status.models import DSLStatus, Information, InternetConnection, Link

router = APIRouter()
settings = get_settings()


@router.get(
    "",
    tags=["status"],
    summary="Get Router Status",
    status_code=status.HTTP_200_OK,
    response_model=DSLStatus,
)
async def get_status(human_readable: bool = False) -> DSLStatus:
    host = settings.speedport_host
    key = settings.default_key
    request, err = await http_get_encrypted_json(key, f"http://{host}/data/Status.json")
    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status from {host}",
        )
    info_data = {}
    dsl_data = {}
    link_data = {}
    internet_data = {}
    info_fields = ["device_name", "firmware_version", "serial_number", "modem_id"]
    dsl_fields = ["router_state", "days_online"]
    link_fields = ["dsl_link_status", "dsl_downstream", "dsl_upstream"]
    internet_fields = ["inet_download", "inet_upload", "dsl_pop"]

    info_data = {field: get_field(request, field) for field in info_fields}
    dsl_data = {field: get_field(request, field) for field in dsl_fields}
    link_data = {
        field: get_field(request, field, human_readable) for field in link_fields
    }
    internet_data = {
        field: get_field(request, field, human_readable) for field in internet_fields
    }

    return DSLStatus(
        **dsl_data,
        info=Information(**info_data),
        link=Link(**link_data),
        internet=InternetConnection(**internet_data),
    )

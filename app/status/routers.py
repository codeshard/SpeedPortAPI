from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.core.settings import get_settings
from app.core.utils import get_field, http_get_encrypted_json
from app.status.models import WLAN, DSLLink, DSLStatus, Information, InternetConnection

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
    internet_data = {}
    wlan_data = {}
    info_fields = [
        "device_name",
        "factorydefault",
        "router_state",
        "firmware_version",
        "serial_number",
        "modem_id",
    ]
    dsl_fields = [
        "dsl_link_status",
        "ap_mode",
        "onlinestatus",
        "days_online",
        "time_online",
        "inet_uptime",
        "dsl_downstream",
        "dsl_upstream",
    ]
    internet_fields = ["inet_download", "inet_upload", "dsl_pop"]
    wlan_fields = [
        "use_wlan",
        "use_wps",
        "wlan_ssid",
        "wlan_5ghz_ssid",
    ]

    info_data = {field: get_field(request, field) for field in info_fields}
    dsl_data = {
        field: get_field(request, field, human_readable) for field in dsl_fields
    }
    internet_data = {
        field: get_field(request, field, human_readable) for field in internet_fields
    }
    wlan_data = {field: get_field(request, field) for field in wlan_fields}

    return DSLStatus(
        **dsl_data,
        information=Information(**info_data),
        dsl_link=DSLLink(**dsl_data),
        internet_connection=InternetConnection(**internet_data),
        wlan=WLAN(**wlan_data),
    )

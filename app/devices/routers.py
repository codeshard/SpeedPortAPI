from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.core.settings import get_settings
from app.core.utils import get_field, http_get_encrypted_json
from app.devices.models import Device

router = APIRouter()
settings = get_settings()


@router.get(
    "",
    tags=["devices"],
    summary="Get Device List",
    status_code=status.HTTP_200_OK,
    response_model=list[Device],
)
async def get_device_list(
    connected: bool = True, human_readable: bool = False
) -> list[Device]:
    host = settings.speedport_host
    key = settings.default_key
    request, err = await http_get_encrypted_json(
        key, f"http://{host}/data/DeviceList.json"
    )
    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status from {host}",
        )
    device_list = [
        device["varvalue"] for device in request if device["varid"] == "addmdevice"
    ]
    device_fields = [
        "id",
        "mdevice_name",
        "mdevice_mac",
        "mdevice_use_dhcp",
        "mdevice_rssi",
        "mdevice_wifi",
        "mdevice_downspeed",
        "mdevice_upspeed",
        "mdevice_connected",
        "mdevice_ipv4",
        "mdevice_gua_ipv6",
    ]
    devices = [
        {field: get_field(device, field, human_readable) for field in device_fields}
        for device in device_list
    ]
    if connected:
        devices = [device for device in devices if device["mdevice_connected"] == "1"]
    return sorted(devices, key=lambda d: d["id"])

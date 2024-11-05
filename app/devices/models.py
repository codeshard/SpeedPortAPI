from pydantic import BaseModel, Field
from pydantic.networks import IPvAnyAddress
from pydantic_extra_types.mac_address import MacAddress


class Device(BaseModel):
    id: int = Field(..., validation_alias="id")
    name: str = Field(..., validation_alias="mdevice_name")
    mac: MacAddress = Field(..., validation_alias="mdevice_mac")
    dhcp: bool = Field(..., validation_alias="mdevice_use_dhcp")
    rssi: int = Field(..., validation_alias="mdevice_rssi")
    wifi: int | None = Field(..., validation_alias="mdevice_wifi")
    downspeed: int | float = Field(..., validation_alias="mdevice_downspeed")
    upspeed: int | float = Field(..., validation_alias="mdevice_upspeed")
    connected: bool = Field(..., validation_alias="mdevice_connected")
    ipv4: IPvAnyAddress | str = Field(..., validation_alias="mdevice_ipv4")
    ipv6: IPvAnyAddress | str = Field(..., validation_alias="mdevice_gua_ipv6")

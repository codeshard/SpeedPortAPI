from datetime import datetime

from pydantic import BaseModel, Field


class RouterModel(BaseModel):
    name: str = Field(..., validation_alias="device_name")
    factory_default: bool = Field(..., validation_alias="factorydefault")
    state: str = Field(..., validation_alias="router_state")


class StatusModel(BaseModel):
    router: RouterModel
    firmware_version: str = Field(..., validation_alias="firmware_version")
    serial_number: str = Field(..., validation_alias="serial_number")
    modem_id: str = Field(..., validation_alias="modem_id")
    downstream: int | float = Field(..., validation_alias="dsl_downstream")
    upstream: int | float = Field(..., validation_alias="dsl_upstream")
    download: int | float = Field(..., validation_alias="inet_download")
    upload: int | float = Field(..., validation_alias="inet_upload")
    active: bool = Field(..., validation_alias="use_wlan")
    wps: bool = Field(..., validation_alias="use_wps")
    ssid: str = Field(..., validation_alias="wlan_ssid")
    ssid_5ghz: str = Field(..., validation_alias="wlan_5ghz_ssid")


class InfoModel(BaseModel):
    router: RouterModel
    rebooting: bool
    link_status: str = Field(..., validation_alias="dsl_link_status")
    ap_mode: bool = Field(..., validation_alias="ap_mode")
    online_status: str = Field(..., validation_alias="onlinestatus")
    days_online: int = Field(..., validation_alias="days_online")
    time_online: str = Field(..., validation_alias="time_online")
    uptime: datetime = Field(..., validation_alias="inet_uptime")
    domain: str = Field(..., validation_alias="domain_name")

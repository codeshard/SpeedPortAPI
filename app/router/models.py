from datetime import datetime

from pydantic import BaseModel, Field


class Router(BaseModel):
    name: str = Field(..., validation_alias="device_name")
    factory_default: bool = Field(..., validation_alias="factorydefault")
    rebooting: bool
    state: str = Field(..., validation_alias="router_state")
    status: str = Field(..., validation_alias="dsl_link_status")
    ap_mode: bool = Field(..., validation_alias="ap_mode")
    online_status: str = Field(..., validation_alias="onlinestatus")
    days_online: int = Field(..., validation_alias="days_online")
    time_online: str = Field(..., validation_alias="time_online")
    uptime: datetime = Field(..., validation_alias="inet_uptime")
    domain: str = Field(..., validation_alias="domain_name")

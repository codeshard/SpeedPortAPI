from pydantic import BaseModel, Field


class Information(BaseModel):
    name: str = Field(..., validation_alias="device_name")
    firmware_version: str = Field(..., validation_alias="firmware_version")
    serial_number: str = Field(..., validation_alias="serial_number")
    modem_id: str = Field(..., validation_alias="modem_id")


class Link(BaseModel):
    status: str = Field(..., validation_alias="dsl_link_status")
    downstream: int | float = Field(..., validation_alias="dsl_downstream")
    upstream: int | float = Field(..., validation_alias="dsl_upstream")


class InternetConnection(BaseModel):
    download: int | float = Field(..., validation_alias="inet_download")
    upload: int | float = Field(..., validation_alias="inet_upload")
    pppoe: str = Field(..., validation_alias="dsl_pop")


class DSLStatus(BaseModel):
    state: str = Field(..., validation_alias="router_state")
    days_online: int = Field(..., validation_alias="days_online")
    info: Information
    link: Link
    internet: InternetConnection

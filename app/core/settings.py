from functools import lru_cache

from pydantic.networks import IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    debug: bool = True
    title: str = "SpeedPort API"
    version: str = "0.1.0"
    debug_level: str = "INFO"

    speedport_host: IPvAnyAddress = "192.168.2.1"
    speedport_port: int = 80
    speedport_password: str | None = None

    default_key: str = (
        "cdc0cac1280b516e674f0057e4929bca84447cca8425007e33a88a5cf598a190"
    )


@lru_cache
def get_settings():
    return Settings()

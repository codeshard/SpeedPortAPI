from functools import lru_cache
from typing import Any, Optional

from pydantic import computed_field
from pydantic.networks import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    debug: bool = True
    version: str = "0.1.0"
    log_level: str = "INFO"

    speedport_host: AnyUrl = "http://192.168.1.1"
    speedport_password: Optional[str] = None

    http_timeout: int = 5
    http_max_retries: int = 3
    http_retry_wait: int = 3

    hex_key: str = "cdc0cac1280b516e674f0057e4929bca84447cca8425007e33a88a5cf598a190"

    @computed_field
    @property
    def logging_config(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(asctime)s [%(name)s] %(levelprefix)s %(message)s",
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - %(request_line)s %(status_code)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn.error": {
                    "level": self.log_level,
                    "handlers": ["default"],
                    "propagate": False,
                },
                "uvicorn.access": {
                    "level": self.log_level,
                    "handlers": ["access"],
                    "propagate": False,
                },
                "hishel.controller": {
                    "level": self.log_level,
                    "handlers": ["access"],
                    "propagate": False,
                },
                "httpx": {
                    "level": self.log_level,
                    "handlers": ["default"],
                    "propagate": False,
                },
                "httpcore": {
                    "level": self.log_level,
                    "handlers": ["default"],
                    "propagate": False,
                },
            },
        }


@lru_cache(maxsize=1)
def get_settings():
    return Settings()

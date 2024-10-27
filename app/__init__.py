import logging

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from app.core.settings import get_settings
from app.devices.routers import router as devices_router
from app.health.routers import router as health_router
from app.router.routers import router as router_router

settings = get_settings()


logging.config.dictConfig(settings.logging_config)

# logger = logging.getLogger(__name__)

app = FastAPI(
    debug=settings.debug,
    title="SpeedPort API",
    version=settings.version,
    dependencies=[Depends(get_settings)],
    default_response_class=ORJSONResponse,
)

app.include_router(health_router)
app.include_router(router_router, prefix="/router")
app.include_router(devices_router, prefix="/router")

import logging
import sys

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from app.core.settings import get_settings
from app.devices.routers import router as devices_router
from app.health.routers import router as health_router
from app.router.routers import router as router_router
from app.status.routers import router as status_router

settings = get_settings()

logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG if settings.debug else logging.INFO
)
logging.getLogger("hishel.controller").setLevel(settings.debug_level)

app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    version=settings.version,
    dependencies=[Depends(get_settings)],
    default_response_class=ORJSONResponse,
)

app.include_router(health_router)
app.include_router(status_router, prefix="/status")
app.include_router(devices_router, prefix="/devices")
app.include_router(router_router, prefix="/router")

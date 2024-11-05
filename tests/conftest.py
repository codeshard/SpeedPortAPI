import pytest
import respx
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from respx.fixtures import session_event_loop as event_loop  # noqa: F401

from app import app


@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def mocked_api():
    with respx.mock(
        base_url="http://speed.port", assert_all_called=False
    ) as respx_mock:
        health_route = respx_mock.get("/health", name="health_endpoint")
        health_route.return_value = Response(
            status.HTTP_200_OK, json=[{"status": "OK"}]
        )
        status_route = respx_mock.get("/router/status", name="status_endpoint")
        status_route.return_value = Response(
            status_code=status.HTTP_200_OK,
            json=[
                {
                    "router": {
                        "name": "string",
                        "factory_default": True,
                        "state": "string",
                    },
                    "firmware_version": "string",
                    "serial_number": "string",
                    "modem_id": "string",
                    "downstream": 0,
                    "upstream": 0,
                    "download": 0,
                    "upload": 0,
                    "active": True,
                    "wps": True,
                    "ssid": "string",
                    "ssid_5ghz": "string",
                }
            ],
        )
        info_route = respx_mock.get("/router/info", name="info_endpoint")
        info_route.return_value = Response(
            status_code=status.HTTP_200_OK,
            json=[
                {
                    "router": {
                        "name": "string",
                        "factory_default": True,
                        "state": "string",
                    },
                    "rebooting": True,
                    "link_status": "string",
                    "ap_mode": True,
                    "online_status": "string",
                    "days_online": 0,
                    "time_online": "string",
                    "uptime": "2024-11-05T21:23:33.248Z",
                    "domain": "string",
                }
            ],
        )
        devices_route = respx_mock.get("/router/devices", name="devices_endpoint")
        devices_route.return_value = Response(
            status_code=status.HTTP_200_OK,
            json=[
                {
                    "id": 0,
                    "name": "string",
                    "mac": "string",
                    "dhcp": True,
                    "rssi": 0,
                    "wifi": 0,
                    "downspeed": 0,
                    "upspeed": 0,
                    "connected": True,
                    "ipv4": "string",
                    "ipv6": "string",
                }
            ],
        )
        yield respx_mock

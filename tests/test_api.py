import httpx
from fastapi import status


def test_health(mocked_api):
    response = httpx.get("http://speed.port/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"status": "OK"}]
    assert mocked_api["health_endpoint"].called


def test_router_status(mocked_api):
    response = httpx.get("http://speed.port/router/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
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
    ]
    assert mocked_api["status_endpoint"].called


def test_router_info(mocked_api):
    response = httpx.get("http://speed.port/router/info")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
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
    ]
    assert mocked_api["info_endpoint"].called


def test_router_devices(mocked_api):
    response = httpx.get("http://speed.port/router/devices")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
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
    ]
    assert mocked_api["devices_endpoint"].called

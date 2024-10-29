def test_router_status(test_app):
    response = test_app.get("/router/status")
    assert response.status_code == 200


def test_router_info(test_app):
    response = test_app.get("/router/info")
    assert response.status_code == 200


def test_router_devices(test_app):
    response = test_app.get("/router/devices")
    assert response.status_code == 200

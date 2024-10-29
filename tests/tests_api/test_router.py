def test_router_status(test_app):
    response = test_app.get("/router/status")
    assert response.status_code == 200

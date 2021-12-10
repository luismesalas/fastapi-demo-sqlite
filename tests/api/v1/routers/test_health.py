from fastapi.testclient import TestClient

import main

client = TestClient(main.get_app())
health_path_v1 = "/api/v1/health"


def test_get_health_on_api_v1_gets_200():
    # Given none

    # When
    response = client.get(health_path_v1)

    # Then
    assert response.status_code == 200
    assert response.json() == {"message": "API is alive"}

from unittest.mock import call

from api.v1 import api


def test_get_api(mocker):
    # Given
    api_router_mock = mocker.patch('api.v1.api.APIRouter')
    health_mock = mocker.patch('api.v1.api.health')
    schools_mock = mocker.patch('api.v1.api.schools')
    positions_mock = mocker.patch('api.v1.api.positions')
    assignments_mock = mocker.patch('api.v1.api.assignments')

    # When
    result = api.get_api()

    # Then
    api_router_mock.assert_called_once()
    api_router_mock.return_value.include_router.assert_has_calls(
        [call(health_mock.router), call(schools_mock.router, prefix="/schools"),
         call(positions_mock.router, prefix="/positions"), call(assignments_mock.router, prefix="/assignments")])
    assert result == api_router_mock.return_value

import main


def test_get_app(mocker):
    # Given
    fast_api_mock = mocker.patch('main.FastAPI')
    api_v1_mock = mocker.patch('main.api_router_v1')

    # When
    result = main.get_app()

    # Then
    fast_api_mock.assert_called_once()
    api_v1_mock.get_api.assert_called_once()
    fast_api_mock.return_value.include_router.assert_called_once_with(api_v1_mock.get_api.return_value,
                                                                      prefix="/api/v1")

    assert result == fast_api_mock.return_value

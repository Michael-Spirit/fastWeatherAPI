import pytest


@pytest.mark.asyncio
async def test_weather_api_endpoint(client):
    response = await client.get(client.app.url_path_for('get_weather_by_zipcode', zipcode='12345'))

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_weather_api_endpoint_caching_zipcode(client, request_weather_data_mock):
    await client.get(client.app.url_path_for('get_weather_by_zipcode', zipcode='12345'))

    request_weather_data_mock.assert_called_once()

    await client.get(client.app.url_path_for('get_weather_by_zipcode', zipcode='12345'))

    request_weather_data_mock.assert_called_once()


@pytest.mark.asyncio
async def test_weather_api_endpoint_hard_refresh(client, request_weather_data_mock):
    await client.get(client.app.url_path_for('get_weather_by_zipcode', zipcode='12345'))

    request_weather_data_mock.assert_called_once()

    await client.get(client.app.url_path_for('get_weather_by_zipcode', zipcode='12345'), params={'force_update': True})

    assert request_weather_data_mock.call_count == 2

import pytest

from apps.weather.models.weather import ObservationLocation
from apps.weather.models.weather import ObservationResponse
from apps.weather.models.weather import ObservationWeather
from apps.weather.services.weather_request_data import RequestWeatherDataClient


@pytest.fixture(scope='function')
def request_weather_data_mock(mocker):
    mock = mocker.Mock(called=False)

    async def _request_observation_mock(instance, zipcode, *args, **kwargs):
        mock(instance, zipcode, *args, **kwargs)
        return ObservationResponse(
            reception_time=121242432,
            location=ObservationLocation(name='Mocked Location', coordinates={}, ID=1, country='US'),
            weather=ObservationWeather(
                reference_time=121242432,
                sunset_time=121242432,
                sunrise_time=121242432,
                clouds=1,
                rain={},
                snow={},
                wind={'speed': 200},
                humidity=90,
                pressure={},
                temperature={'temp': 300},
                status='mock status',
                detailed_status='mocked detailed_status',
                weather_code=1,
                weather_icon_name='mock weather_icon_name',
                visibility_distance=1,
                utc_offset=1,
            ),
        )

    mocker.patch.object(
        RequestWeatherDataClient,
        '_request_observation',
        _request_observation_mock,
    )

    return mock

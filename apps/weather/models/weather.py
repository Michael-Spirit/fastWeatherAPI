from typing import Optional

from pydantic import BaseModel


class WeatherData(BaseModel):
    reception_time: int
    location_name: str
    main_description: str
    temperature: int
    precipitation: Optional[int]
    humidity: int
    wind: int


class ObservationLocation(BaseModel):
    name: str
    coordinates: dict
    ID: int
    country: str


class ObservationWeather(BaseModel):
    reference_time: int
    sunset_time: int
    sunrise_time: int
    clouds: int
    rain: dict
    snow: dict
    wind: dict
    humidity: int
    pressure: dict
    temperature: dict
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    visibility_distance: int
    dewpoint: Optional[str] = None
    humidex: Optional[str] = None
    heat_index: Optional[str] = None
    utc_offset: int
    uvi: Optional[str] = None
    precipitation_probability: Optional[str] = None


class ObservationResponse(BaseModel):
    reception_time: int
    location: ObservationLocation
    weather: ObservationWeather

    def to_weather_data(self) -> WeatherData:
        return WeatherData(
            reception_time=self.reception_time,
            main_description=self.weather.detailed_status.capitalize(),
            temperature=self.weather.temperature['temp'],
            precipitation=self.weather.precipitation_probability if self.weather.precipitation_probability else 0,
            humidity=self.weather.humidity,
            wind=self.weather.wind['speed'],
            location_name=self.location.name,
        )

from fastapi import APIRouter

from config.constants import TAG_WEATHER_API

router = APIRouter(tags=[TAG_WEATHER_API])

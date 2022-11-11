from fastapi import APIRouter

from config.constants import TAG_METRICS

router = APIRouter(tags=[TAG_METRICS])

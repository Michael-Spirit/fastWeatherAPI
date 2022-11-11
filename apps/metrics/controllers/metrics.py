from fastapi.responses import Response
from prometheus_client import REGISTRY
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST
from prometheus_client.openmetrics.exposition import generate_latest

from apps.metrics.router import router


@router.get('/metrics/')
async def metrics() -> Response:
    return Response(generate_latest(REGISTRY), headers={'Content-Type': CONTENT_TYPE_LATEST})

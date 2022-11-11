from kafka.errors import KafkaError

from apps.healthcheck.enums import StatusEnum
from apps.healthcheck.serializers.healthcheck_result import HealthcheckServiceResult
from apps.healthcheck.services.checkers.base import BaseHealthchecker


class KafkaHealthchecker(BaseHealthchecker):
    def __init__(self, kafka_app):
        self.__kafka_app = kafka_app

    async def check(self) -> HealthcheckServiceResult:
        try:
            future = await self.__kafka_app.send('healthcheck')
            await future

            return HealthcheckServiceResult(status=StatusEnum.success, service='kafka')
        except KafkaError as e:
            return HealthcheckServiceResult(status=StatusEnum.error, service='kafka', message=str(e))

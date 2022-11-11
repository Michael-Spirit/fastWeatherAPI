import asyncio
import json
import os
from json import JSONDecodeError
from typing import Any

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from botocore.session import Session


class AwsSecretsManagerLoader:
    def __init__(self, secret_name: str, aws_region_name: str):
        self.secret_name = secret_name
        self.aws_region_name = aws_region_name
        os.environ.update(self.load())

    def load(self) -> dict[str, Any]:
        try:
            loop = asyncio.get_running_loop()
            data = self.load_sync()

        except RuntimeError:
            loop = asyncio.new_event_loop()

            data = loop.run_until_complete(self.load_async())
            loop.close()

        return data

    def load_sync(self) -> dict[str, Any]:
        session = Session()
        client = session.create_client('secretsmanager', region_name=self.aws_region_name)

        try:
            secret_value_response = client.get_secret_value(
                SecretId=self.secret_name,
            )
        except ClientError as err:
            raise Exception(f'Cannot load values from AWS Secrets Manager "{self.secret_name}": {err}') from err

        try:
            return json.loads(secret_value_response['SecretString'])
        except (JSONDecodeError, TypeError) as err:
            raise Exception(f'Cannot parse JSON values from AWS Secrets Manager "{self.secret_name}": {err}') from err

    async def load_async(self) -> dict[str, Any]:
        session = get_session()

        async with session.create_client('secretsmanager', region_name=self.aws_region_name) as client:
            try:
                secret_value_response = await client.get_secret_value(SecretId=self.secret_name)
            except ClientError as err:
                raise Exception(f'Cannot load values from AWS Secrets Manager "{self.secret_name}": {err}') from err

            try:
                return json.loads(secret_value_response['SecretString'])
            except (JSONDecodeError, TypeError) as err:
                raise Exception(
                    f'Cannot parse JSON values from AWS Secrets Manager "{self.secret_name}": {err}'
                ) from err

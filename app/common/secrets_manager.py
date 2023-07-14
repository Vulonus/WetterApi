import json
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SecretsManager:
    SECRETS_SERVICE_NAME = "secretsmanager"
    SECRETS_REGION_NAME = "eu-central-1"

    def __init__(self, secret_id: str):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name=self.SECRETS_SERVICE_NAME,
            region_name=self.SECRETS_REGION_NAME
        )
        self.secret_id = secret_id

    def get_value(self, name: str):
        if name is None:
            raise ValueError

        try:
            kwargs = {"SecretId": self.secret_id}
            get_secret_value_response = self.client.get_secret_value(**kwargs)

            if "SecretString" not in get_secret_value_response:
                logger.exception(f"Couldn't get value for secret {name}.")
                raise ValueError
            secret = json.loads(get_secret_value_response["SecretString"])
            return secret[name]

        except ClientError as error:
            logger.exception(f'An error occurred on the server side\n{error.response["Error"]}')
            raise

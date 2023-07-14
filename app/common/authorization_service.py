import json
import logging
from typing import Union

from jwt import PyJWTError, decode
from fastapi import Request

from app.common.enums import DataContext
from app.common.secrets_manager import SecretsManager
from app.common.util import api_clients

logger = logging.getLogger(__name__)


def is_request_allowed(request: Request, data_context: DataContext, leadquelle: str, secrets_manager: SecretsManager) \
        -> bool:
    client_name = api_clients.get(determine_api_client_id(request))
    allowed_leadquellen = json.loads(secrets_manager.get_value("allowed_leadquellen"))
    logger.info(f"Caller: {client_name}")
    if client_name and data_context == DataContext.PROD and leadquelle in allowed_leadquellen[DataContext.PROD.value]:
        return any([DataContext.PROD.value in client_name, client_name == "DRKLEINRK"])
    if client_name and data_context == DataContext.TEST and leadquelle in allowed_leadquellen[DataContext.TEST.value]:
        return any([DataContext.TEST.value in client_name, client_name == "DRKLEINRK"])
    return False


def determine_api_client_id(request: Request) -> Union[str, None]:
    token: str = request.headers.get("authorization", None)
    if token:
        try:
            payload = decode(jwt=token.replace("Bearer ", ""), options={"verify_signature": False})
            return payload["client_id"]
        except JWTError:
            return None
    return None

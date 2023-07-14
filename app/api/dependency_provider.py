import logging
import os
from functools import lru_cache
from http import HTTPStatus

from fastapi import Header, HTTPException

from app import config
# from app.common.authentication_service import AuthenticationService
# from app.common.exceptions.authentication_exception import AuthenticationException
# from app.common.secrets_manager import SecretsManager

logger = logging.getLogger(__name__)


# @lru_cache
# def get_secrets_manager():
#     return SecretsManager(config.SECRETS_ID)
#
#
# @lru_cache
# def get_authentication_provider():
#     return AuthenticationService(get_secrets_manager())


@lru_cache
def get_config_by_stage():
    return config.get_config_by_stage(os.getenv("STAGE"))


# def is_valid_token(allowed_scope):
#     def _is_valid_token(authorization=Header(None)):
#         try:
#             return get_authentication_provider().is_valid_token(access_token=authorization, allowed_scope=allowed_scope)
#         except AuthenticationException as error:
#             logger.error(error)
#             raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden") from error
#
#     return _is_valid_token

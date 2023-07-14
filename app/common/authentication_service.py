import json
import logging

import jwt
import requests
from jwt.algorithms import RSAAlgorithm

from app.common.secrets_manager import SecretsManager
from app.common.exceptions.authentication_exception import AuthenticationException

logger = logging.getLogger(__name__)


class AuthenticationService:
    def __init__(self, secrets_manager: SecretsManager) -> None:
        user_pool_region = secrets_manager.get_value("cognito_pool_region")
        user_pool_id = secrets_manager.get_value("cognito_pool_id")

        self.user_pool_client_ids = secrets_manager.get_value("cognito_pool_client_ids")
        self.jwk_url = f"https://cognito-idp.{user_pool_region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

    def is_valid_token(self, access_token: str, allowed_scope: str) -> bool:
        try:
            public_keys = self.get_well_known_jwk()
            if not access_token:
                raise AuthenticationException("Token missing")
            encoded_token = access_token.replace("Bearer ", "")
            kid = jwt.get_unverified_header(encoded_token)["kid"]
            token = jwt.decode(encoded_token, key=public_keys[kid], algorithms=["RS256"])
            if token["client_id"] not in json.loads(self.user_pool_client_ids):
                raise AuthenticationException("Wrong client id")
            if token["scope"] != allowed_scope:
                raise AuthenticationException("Wrong scope")
            return True
        except KeyError as error:
            raise AuthenticationException(error) from error
        except jwt.exceptions.InvalidSignatureError as error:
            raise AuthenticationException(error) from error
        except jwt.exceptions.ExpiredSignatureError as error:
            raise AuthenticationException(error) from error
        except jwt.exceptions.DecodeError as error:
            raise AuthenticationException(error) from error

    def get_well_known_jwk(self) -> dict:
        jwks = requests.get(self.jwk_url).json()
        public_keys = {}
        for jwk in jwks["keys"]:
            kid = jwk["kid"]
            public_keys[kid] = RSAAlgorithm.from_jwk(json.dumps(jwk))
        return public_keys

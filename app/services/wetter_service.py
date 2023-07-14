import json
import logging

import httpx

from app.common.enums import DataContext
from app.common.httpx_client import HttpxClient
from app.common.errors.internal_error import InternalError, InternalDataError
from app.common.exceptions.api_exception import ApiException
from app.common.exceptions.internal_exception import InternalException
from app.models.config import ConfigWetterCom

logger = logging.getLogger(__name__)


class WetterService:
    client: HttpxClient
    config: ConfigWetterCom
    api_key = "0d24db2f08msh8a993462034b32cp11fd70jsnd8d1bc2d83ba"

    def __init__(self, config: ConfigWetterCom) -> None:
        super().__init__()

        self.config = config
        self.client = HttpxClient({"Content-Type": "application/json;charset=UTF-8"})

    async def get_index(self) -> dict:
        try:
            url = f"{self.config.host}/"
            headers = {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': "forecast9.p.rapidapi.com"
            }

            response = await self.client.get(url=url, headers=headers)

            if response.status_code == 200:
                return json.loads(response.content)
            if response.status_code == 500:
                logger.error("INTERNAL_ERROR")
                logger.error(response.content)

                raise InternalException(InternalError(errors=[InternalDataError()]))
            raise ApiException(json.loads(response.content)["detail"])

        except httpx.RequestError as request_error:
            logger.error(request_error.request.url)
            raise InternalException(InternalError(errors=[InternalDataError()])) from request_error

    async def get_status(self) -> dict:
        try:
            url = f"{self.config.host}/status"
            headers = {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': "forecast9.p.rapidapi.com"
            }

            response = await self.client.get(url=url, headers=headers)

            if response.status_code == 200:
                return json.loads(response.content)
            if response.status_code == 500:
                logger.error("INTERNAL_ERROR")
                logger.error(response.content)

                raise InternalException(InternalError(errors=[InternalDataError()]))
            raise ApiException(json.loads(response.content)["detail"])

        except httpx.RequestError as request_error:
            logger.error(request_error.request.url)
            raise InternalException(InternalError(errors=[InternalDataError()])) from request_error

    async def get_forecast_summary_by_location(self, location_name: str) -> dict:
        try:
            url = f"{self.config.host}/rapidapi/forecast/{location_name}/summary"
            headers = {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': "forecast9.p.rapidapi.com"
            }

            response = await self.client.get(url=url, headers=headers)

            if response.status_code == 200:
                return json.loads(response.content)
            if response.status_code == 500:
                logger.error("INTERNAL_ERROR")
                logger.error(response.content)

                raise InternalException(InternalError(errors=[InternalDataError()]))
            raise ApiException(response.content)

        except httpx.RequestError as request_error:
            logger.error(request_error.request.url)
            raise InternalException(InternalError(errors=[InternalDataError()])) from request_error

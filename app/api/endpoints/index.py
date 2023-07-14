import json
import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api import dependency_provider
from app.api.endpoints.openapi import OpenApi
from app.common.data_context_service import DataContextService
from app.common.errors.internal_error import InternalError, InternalDataError
from app.common.exceptions.api_exception import ApiException
from app.common.exceptions.internal_exception import InternalException
from app.common.httpx_client import HttpxClient
from app.common.logging_helper import log_request
from app.models.response.index_response import IndexResponse
from app.services.wetter_service import WetterService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    path="/index",
    status_code=200,
    summary="Wetter.com Index",
    response_model=IndexResponse,
    responses=OpenApi.http_responses(IndexResponse.Config.schema_extra),
    tags=["Index"]
)
async def index(request: Request,
                config=Depends(dependency_provider.get_config_by_stage),
                data_context=Depends(DataContextService.determine_from_query)):

    # data_context: DataContext = DataContextService.determine(request)
    log_request(logger=logger, data_context=data_context, request=request)

    try:
        service = WetterService(config=config)
        response = await service.get_index()

        logger.info(f"Response: {response}")
        return response
    except ApiException as error:
        logger.error(error)
        return JSONResponse(status_code=HTTPStatus.BAD_REQUEST,
                            content=error.message)
    except InternalException as error:
        logger.error(error)
        return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            content=json.loads(InternalError(errors=[InternalDataError()]).json()))

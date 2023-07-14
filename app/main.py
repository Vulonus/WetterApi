import logging
from http import HTTPStatus

import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# noinspection PyPackageRequirements
from starlette.exceptions import HTTPException

from app.api.endpoints import index, status, forecast_by_location
from app.api.endpoints.openapi import OpenApi
from app.common.logging_helper import init_logging
from app.common.util import map_validation_error


init_logging()
logger = logging.getLogger(__name__)
app = FastAPI(docs_url=None, redoc_url="/api-documentation", openapi_url="/api-documentation/openapi.json")

app.include_router(index.router)
app.include_router(status.router)
app.include_router(forecast_by_location.router)

app.openapi = OpenApi(app).schema


@app.get("/", include_in_schema=False)
async def health():
    return 200


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):  # pylint: disable=unused-argument
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.info(request.headers)
    return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content=map_validation_error(exc))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

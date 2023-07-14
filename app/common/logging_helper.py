import logging
import os

from starlette.requests import Request

from app.common.enums import DataContext


def logging_default_format():
    return "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/") == -1


def init_logging():
    if os.environ.get("STAGE") in ["DEVELOPMENT", "LOCAL"]:
        logging.basicConfig(format=logging_default_format(), level=logging.DEBUG)
    else:
        logging.basicConfig(format=logging_default_format(), level=logging.INFO)

    if os.environ.get("STAGE") == "PROD":
        logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


def log_request(logger: logging.Logger, data_context: DataContext, request: Request, request_json=None):
    logger.debug(request.headers)
    logger.debug(request.query_params.get("leadquelle"))
    logger.info(f"INCOMING REQUEST {request.url.path}:\n"
                f"DataContext: {data_context}\n"
                f"requestId: {request.headers.get('requestId')}\n"
                f"Request: {request_json}")

from fastapi.openapi.utils import get_openapi

from app.common.errors.forbidden_error import ForbiddenError
from app.common.errors.unauthorized_error import UnauthorizedError
from app.common.errors.field_value_error import FieldValueError
from app.common.errors.internal_error import InternalError


class OpenApi:

    def __init__(self, app, hidden_endpoints: list = None) -> None:
        self.app = app
        self.hidden_endpoints = hidden_endpoints if hidden_endpoints else []

    def schema(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="Dr. Klein RK GmbH Privatkredit Marktplatz API",
            version="1.0",
            routes=[route for route in self.app.routes if route.path not in self.hidden_endpoints],
        )
        openapi_schema["info"] = {
            "title": "Dr. Klein RK GmbH Privatkredit Marktplatz API",
            "version": "1.0",
            "description": "Mithilfe der API lassen sich Konditionen für "
                           "Ratenkredite ermitteln und Angebote annehmen.",
            "contact": {
                "name": "Wir helfen dir bei der Anbindung der Privatkredit Marktplatz API",
                "url": "https://developer.drkleinservice.de",
                "email": "dev@drklein.de"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "x-logo": {
                "url": "https://www.drklein-rk.de/content/uploads/2019/11/drklein-logo-xs.png"
            }
        }

        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                if openapi_schema["paths"][path][method]["responses"].get("422"):
                    openapi_schema["paths"][path][method]["responses"]["422"] = {
                        "description": "Unprocessable Entity",
                        "content": {
                            "application/json": {"schema": {"$ref": f"#/components/schemas/{FieldValueError.__name__}"}}
                        }
                    }

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema

    @staticmethod
    def http_responses(schema):
        return {
            200: {
                "description": "Success",
                "content": {
                    "application/json": schema
                },
            },
            400: {
                "description": "Bad Request",
                "model": FieldValueError
            },
            401: {
                "description": "Unauthorized",
                "model": UnauthorizedError,
            },
            403: {
                "description": "Forbidden",
                "model": ForbiddenError,
            },
            500: {
                "description": "Internal Server Error",
                "model": InternalError
            }
        }

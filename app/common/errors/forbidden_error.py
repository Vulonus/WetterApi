from typing import List

from pydantic import BaseModel


class DataError(BaseModel):
    status: str


class ForbiddenError(BaseModel):
    errors: List[DataError]

    class Config:
        schema_extra = {
            "example": {
                "errors": [
                    {
                        "status": "Forbidden"
                    }
                ]
            }
        }

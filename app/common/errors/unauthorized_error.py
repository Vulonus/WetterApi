from typing import List

from pydantic import BaseModel


class DataError(BaseModel):
    status: str


class UnauthorizedError(BaseModel):
    errors: List[DataError]

    class Config:
        schema_extra = {
            "example": {
                "errors": [
                    {
                        "status": "Unauthorized"
                    }
                ]
            }
        }

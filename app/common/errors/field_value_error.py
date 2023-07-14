from typing import List

from pydantic import BaseModel


class DataError(BaseModel):
    field: str
    message: str


class FieldValueError(BaseModel):
    errors: List[DataError]

    class Config:
        schema_extra = {
            "example": {
                "errors": [
                    {
                        "field": "leadquelle",
                        "message": "none is not an allowed value"
                    }
                ]
            }
        }

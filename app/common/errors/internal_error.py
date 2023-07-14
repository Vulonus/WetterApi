from typing import List

from pydantic import BaseModel


class InternalDataError(BaseModel):
    status: str = "INTERNAL_ERROR"
    message: str = "Es ist ein Fehler aufgetreten."


class InternalError(BaseModel):
    errors: List[InternalDataError]

    class Config:
        schema_extra = {
            "example": {
                "errors": [
                    {
                        "status": "INTERNAL_ERROR",
                        "message": "Es ist ein Fehler aufgetreten."
                    }
                ]
            }
        }

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str
    date: str

    class Config:
        schema_extra = {
            "example": {
                "status": "All services are operational.",
                "date": "2017-06-19T11:31:23Z"
            }
        }

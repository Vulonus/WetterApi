from pydantic import BaseModel


class IndexResponse(BaseModel):
    title: str
    version: str
    documentation: str

    class Config:
        schema_extra = {
            "example": {
                "title": "wetter.com REST API",
                "version": "1.0.0",
                "documentation": "https://api.wetter.com/"
            }
        }

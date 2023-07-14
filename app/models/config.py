from pydantic import BaseModel


class ConfigWetterCom(BaseModel):
    host: str


from pydantic import BaseModel


class ForecastSummaryByLocation(BaseModel):
    location_name: str

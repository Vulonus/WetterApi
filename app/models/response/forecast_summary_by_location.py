from typing import List

from pydantic import BaseModel, Field


class Weather(BaseModel):
    state: int
    text: str
    icon: str


class Prec(BaseModel):
    sum: float
    sumAsRain: float
    probability: float
    _class: int = Field(alias="class")


class Temperature(BaseModel):
    min: float
    max: float
    avg: float


class Gusts(BaseModel):
    test: str
    value: float


class Wind(BaseModel):
    avg: float
    direction: str
    gusts: Gusts
    _min: float = Field(alias="min")
    _max: float = Field(alias="max")
    significationWind: bool
    text: str
    unit: str


class Windchill(BaseModel):
    avg: float
    _min: float = Field(alias="min")
    _max: float = Field(alias="max")


class SnowLine(BaseModel):
    avg: float
    _min: float = Field(alias="min")
    _max: float = Field(alias="max")
    unit: str


class Astronomy(BaseModel):
    dawn: str
    sunrise: str
    suntransit: str
    sunset: str
    dusk: str
    moonrise: str
    moontransit: str
    moonset: str
    moonphase: int
    moonzodiac: int


class ForecastItem(BaseModel):
    date: str
    dateWithTimezone: str
    freshSnow: float
    snowHeight: float
    weather: Weather
    prec: Prec
    sunHours: float
    rainHours: float
    temperature: Temperature
    wind: Wind
    windchill: Windchill
    snowLine: SnowLine
    astronomy: Astronomy


class Forecast(BaseModel):
    items: List
    forecastDate: str
    nextUpdate: str
    source: str
    point: str


class Location(BaseModel):
    code: str
    timezone: str
    name: str


class ForecastSummaryByLocation(BaseModel):
    location: Location
    forecast: str

    class Config:
        schema_extra = {
            "example": {
                "location": {
                    "code": "DE0004130",
                    "timezone": "Europe/Berlin",
                    "name": "Hamburg",
                    "coordinates": {
                        "latitude": 0,
                        "longitude": 0
                    }
                },
                "forecast": {
                    "items": [
                        {
                            "date": "2019-01-25",
                            "dateWithTimezone": "2020-11-02T14:59:00Z",
                            "freshSnow": 1.1,
                            "snowHeight": 1.1,
                            "weather": {
                                "state": 0,
                                "text": "",
                                "icon": ""
                            },
                            "prec": {
                                "sum": 0,
                                "sumAsRain": 0,
                                "probability": 0,
                                "class": 0
                            },
                            "sunHours": 5.17,
                            "rainHours": 1.2,
                            "temperature": {
                                "min": 0,
                                "max": 0,
                                "avg": 0
                            },
                            "wind": {
                                "unit": "km/h",
                                "direction": "SW",
                                "avg": 5,
                                "min": 1,
                                "max": 8,
                                "text": "Südwestwind",
                                "significationWind": True,
                                "gusts": {
                                    "value": 100,
                                    "text": "Sturm mit Orkanböen"
                                }
                            },
                            "windchill": {
                                "avg": 0,
                                "min": 0,
                                "max": 0
                            },
                            "snowLine": {
                                "avg": 0,
                                "min": 0,
                                "max": 0,
                                "unit": ""
                            },
                            "astronomy": {
                                "dawn": "",
                                "sunrise": "",
                                "suntransit": "",
                                "sunset": "",
                                "dusk": "",
                                "moonrise": "",
                                "moontransit": "",
                                "moonset": "",
                                "moonphase": 0,
                                "moonzodiac": 0
                            }
                        }
                    ],
                    "forecastDate": "2019-02-07T10:00:00",
                    "nextUpdate": "2019-02-07T10:00:00",
                    "source": "w3Data",
                    "point": "global"
                }
            }
        }

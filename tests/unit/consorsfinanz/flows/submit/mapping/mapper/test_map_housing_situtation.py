import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_housing_situation import map_housing_situation
from app.consorsfinanz.flows.submit.models.request_loan_submit_model import HousingSituationEnum
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Stammdaten, WohnartEnum, Immobilie, Darlehen


@pytest.mark.parametrize("data", [
    {"key": Stammdaten(wohnartAs1=WohnartEnum.ZUR_MIETE), "value": "RENTER"},
    {"key": Stammdaten(wohnartAs1=WohnartEnum.ZUR_UNTERMIETE), "value": "RENTER"},
    {"key": Stammdaten(wohnartAs1=WohnartEnum.BEI_DEN_ELTERN), "value": "BY_FAMILY"},
    {"key": Stammdaten(wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS), "value": "OWNER_WITH_MORTGAGE"},
])
def test_map_housing_situation(data):
    # WHEN
    response = map_housing_situation(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_housing_situation_without_baufinanzierungsrate():
    # WHEN
    response = map_housing_situation(Stammdaten(
        wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
        immobilien=[Immobilie(
            darlehen=[Darlehen(
                rateMonatlich=0
            )]
        )]
    ))

    # THEN
    assert_that(response, equal_to(HousingSituationEnum.OWNER_WITHOUT_MORTGAGE))


def test_map_housing_situation_with_baufinanzierungsrate():
    # WHEN
    response = map_housing_situation(Stammdaten(
        wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
        immobilien=[Immobilie(
            darlehen=[Darlehen(
                rateMonatlich=100
            )]
        )]
    ))

    # THEN
    assert_that(response, equal_to(HousingSituationEnum.OWNER_WITH_MORTGAGE))


def test_map_housing_situation_none():
    # WHEN
    response = map_housing_situation(None)

    # THEN
    assert_that(response, equal_to(None))

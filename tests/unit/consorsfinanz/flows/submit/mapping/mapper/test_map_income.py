import pytest
from hamcrest import assert_that, equal_to, calling, raises

from app.consorsfinanz.flows.submit.mapping.mapper.map_income import map_income
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import BeschaeftigungsartEnum


@pytest.mark.parametrize("data", [
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.BEAMTER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.ARBEITER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.RENTNER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.ARBEITSLOSER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.HAUSFRAU,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 2500},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.SELBSTSTAENDIGER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 3000},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.FREIBERUFLER,
     "einkommenMonatlichAs1": 2500, "nettoeinkommenJaehrlichAs1": 36000, "netIncome": 3000},
])
def test_map_income_net_income__provide_valid_data__return_income(vorgang, data):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = data["beschaeftigungsartAs1"]
    vorgang.stammdaten.einkommenMonatlichAs1 = data["einkommenMonatlichAs1"]
    vorgang.stammdaten.nettoeinkommenJaehrlichAs1 = data["nettoeinkommenJaehrlichAs1"]
    # WHEN
    response = map_income(vorgang.stammdaten)

    # THEN
    assert_that(response.netIncome, equal_to(data["netIncome"]))


def test_map_income_net_income__all_none(vorgang):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = None
    vorgang.stammdaten.einkommenMonatlichAs1 = None
    vorgang.stammdaten.nettoeinkommenJaehrlichAs1 = None
    # WHEN
    response = map_income(vorgang.stammdaten)

    # THEN
    assert_that(response, equal_to(None))


def test_map_income_net_income__income_none(vorgang):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = BeschaeftigungsartEnum.ANGESTELLTER
    vorgang.stammdaten.einkommenMonatlichAs1 = None

    # WHEN
    response = map_income(vorgang.stammdaten)

    # THEN
    assert_that(response, equal_to(None))


def test_map_income_net_income__income_zero(vorgang):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = BeschaeftigungsartEnum.ANGESTELLTER
    vorgang.stammdaten.einkommenMonatlichAs1 = 0

    # WHEN
    response = map_income(vorgang.stammdaten)

    # THEN
    assert_that(response.netIncome, equal_to(0))


def test_map_income_net_income__selbststaendiger__income_none(vorgang):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = BeschaeftigungsartEnum.SELBSTSTAENDIGER
    vorgang.stammdaten.einkommenMonatlichAs1 = None
    vorgang.stammdaten.nettoeinkommenJaehrlichAs1 = None

    # WHEN
    response = map_income(vorgang.stammdaten)

    # THEN
    assert_that(response, equal_to(None))

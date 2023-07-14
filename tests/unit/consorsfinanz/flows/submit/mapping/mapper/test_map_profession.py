import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_profession import map_profession


@pytest.mark.parametrize("data", [
    {"key": "ANGESTELLTER", "value": "REGULAR_EMPLOYED"},
    {"key": "ARBEITER", "value": "WORKER"},
    {"key": "ARBEITSLOSER", "value": "UNEMPLOYED"},
    {"key": "RENTNER", "value": "PENSIONER"},
    {"key": "FREIBERUFLER", "value": "SELF_EMPLOYED"},
    {"key": "SELBSTSTAENDIGER", "value": "SELF_EMPLOYED"},
    {"key": "HAUSFRAU", "value": "HOUSE_WIFE"},
    {"key": "BEAMTER", "value": "PUBLIC_SERVANT"},
])
def test_map_profession(data):
    # WHEN
    response = map_profession(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_profession_none():
    # WHEN
    response = map_profession(None)

    # THEN
    assert_that(response, equal_to(None))

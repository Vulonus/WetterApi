import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_family_situation import map_family_situation


@pytest.mark.parametrize("data", [
    {"key": "LEDIG", "value": "FREE"},
    {"key": "EHEAEHNLICHE_LEBENSGEMEINSCHAFT", "value": "COHABIT"},
    {"key": "VERHEIRATET", "value": "MARRIED"},
    {"key": "VERWITWET", "value": "WIDOWED"},
    {"key": "EINGETRAGENE_LEBENSPARTNERSCHAFT", "value": "MARRIED"},
    {"key": "GESCHIEDEN", "value": "DIVORCED"},
    {"key": "GETRENNT_LEBEND", "value": "SEPARATED"},
])
def test_map_family_situation(data):
    # WHEN
    response = map_family_situation(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_family_situation_none():
    # WHEN
    response = map_family_situation(None)

    # THEN
    assert_that(response, equal_to(None))

import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_gender import map_gender


@pytest.mark.parametrize("data", [
    {"key": "HERR", "value": "MALE"},
    {"key": "FRAU", "value": "FEMALE"},
])
def test_map_gender(data):
    # WHEN
    response = map_gender(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_gender_none():
    # WHEN
    response = map_gender(None)

    # THEN
    assert_that(response, equal_to(None))

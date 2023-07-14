import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_identification_type import map_identification_type


@pytest.mark.parametrize("data", [
    {"key": "DEUTSCHER_PERSONALAUSWEIS", "value": "GERMAN_ID_CARD"},
    {"key": "AUSLAENDISCHER_PERSONALAUSWEIS", "value": "FOREIGN_PASS_PERMISION"},
    {"key": "DEUTSCHER_REISEPASS", "value": "GERMAN_PASS"},
    {"key": "EU_PERSONALAUSWEIS", "value": "EU_ID_CARD"},
    {"key": "EU_REISEPASS", "value": "EU_PASS"},
    {"key": "KEINE_AUSWEISPAPIERE", "value": "NO_PASS"},
    {"key": "VORLAEUFIGER_DEUTSCHER_REISEPASS", "value": "GERMAN_ID_CARD_TMP"},
])
def test_map_identification_type(data):
    # WHEN
    response = map_identification_type(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_identification_type_none():
    # WHEN
    response = map_identification_type("bar_foo")

    # THEN
    assert_that(response, equal_to(None))

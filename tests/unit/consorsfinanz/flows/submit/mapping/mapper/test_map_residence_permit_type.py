import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_residence_permit_type import map_residence_permit_type
from app.consorsfinanz.flows.submit.models.request_loan_submit_model import ResidencePermitTypeEnum
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Stammdaten, AufenthaltstitelEnum


@pytest.mark.parametrize("data", [
    {"key": AufenthaltstitelEnum.VISUM, "value": ResidencePermitTypeEnum.RESIDENCE_PERMIT_CARD},
    {"key": AufenthaltstitelEnum.AUFENTHALTSERLAUBNIS,
     "value": ResidencePermitTypeEnum.LIMITED_RESIDENCE_PERMIT_PARAGRAPH_OTHERS},
    {"key": AufenthaltstitelEnum.NIEDERLASSUNGSERLAUBNIS, "value": ResidencePermitTypeEnum.UNLIMITED_RESIDENCE_PERMIT},
    {"key": AufenthaltstitelEnum.ERLAUBNIS_ZUM_DAUERAUFENTHALT_EU,
     "value": ResidencePermitTypeEnum.PERMANENT_RESIDENCE_PERMIT},
])
def test_map_residence_permit_type(data):
    # WHEN
    response = map_residence_permit_type(Stammdaten(
        aufenthaltstitelAs1=data["key"])
    )

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_residence_permit_type_none():
    # WHEN
    response = map_residence_permit_type(None)

    # THEN
    assert_that(response, equal_to(None))

import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_employer_address import map_employer_address
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import BeschaeftigungsartEnum, BrancheEnum


@pytest.mark.parametrize("data", [
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.ARBEITSLOSER, "expected_result": None},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.HAUSFRAU, "expected_result": None},
    {"beschaeftigungsartAs1": BeschaeftigungsartEnum.RENTNER, "expected_result": None}
])
def test_map_employer_address__provide_unemployed__return_none(vorgang, data):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = data["beschaeftigungsartAs1"]
    # WHEN
    response = map_employer_address(vorgang)

    # THEN
    assert_that(response, equal_to(None))


def test_map_employer_address__provide_regular_employed__return_correct_data(vorgang):
    # WHEN
    response = map_employer_address(vorgang)

    # THEN
    assert_that(response.employerName, equal_to("Siemens GmbH"))
    assert_that(response.employerStreet, equal_to("Hansastr. 11"))
    assert_that(response.employerZipcode, equal_to("80339"))
    assert_that(response.employerCity, equal_to("Muenchen"))


def test_map_employer_address__provide_self_employed__return_correct_data(vorgang):
    # GIVEN
    vorgang.stammdaten.beschaeftigungsartAs1 = BeschaeftigungsartEnum.SELBSTSTAENDIGER
    vorgang.stammdaten.firmaNameAs1 = "Siemens GmbH"
    vorgang.stammdaten.firmaBrancheAs1 = BrancheEnum.ENERGIE_WASSERVERSORGUNG_BERGBAU
    vorgang.stammdaten.firmaStrasseAs1 = "Hansastr."
    vorgang.stammdaten.firmaHausnummerAs1 = "11"
    vorgang.stammdaten.firmaPlzAs1 = "80339"
    vorgang.stammdaten.firmaOrtAs1 = "Muenchen"
    vorgang.stammdaten.selbststaendigSeitAs1 = "2014-10-20"
    # WHEN
    response = map_employer_address(vorgang)

    # THEN
    assert_that(response.employerName, equal_to("Siemens GmbH"))
    assert_that(response.employerStreet, equal_to("Hansastr. 11"))
    assert_that(response.employerZipcode, equal_to("80339"))
    assert_that(response.employerCity, equal_to("Muenchen"))

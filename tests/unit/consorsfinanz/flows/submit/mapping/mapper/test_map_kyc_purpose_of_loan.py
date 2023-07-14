from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom
from app.consorsfinanz.flows.submit.mapping.mapper.map_kyc_purpose_of_loan import map_kyc_purpose_of_loan


def test_map_kyc_purpose_of_loan():
    # GIVEN
    partner = PartnerCustom(custom=[
        Custom(key="finanzierungszweckBeschreibung", value="AMA"),
    ])

    # WHEN
    response = map_kyc_purpose_of_loan(partner)

    # THEN
    assert_that(response, equal_to("AMA"))


def test_map_kyc_purpose_of_loan_wrong_enum_value():
    # GIVEN
    partner = PartnerCustom(custom=[
        Custom(key="finanzierungszweckBeschreibung", value="FOO"),
    ])

    # WHEN
    response = map_kyc_purpose_of_loan(partner)

    # THEN
    assert_that(response, equal_to(None))


def test_map_kyc_purpose_of_loan_none():
    # WHEN
    response = map_kyc_purpose_of_loan(None)

    # THEN
    assert_that(response, equal_to(None))


def test_map_kyc_purpose_of_loan_custom():
    # GIVEN
    partner = PartnerCustom(custom=[])

    # WHEN
    response = map_kyc_purpose_of_loan(partner)

    # THEN
    assert_that(response, equal_to(None))

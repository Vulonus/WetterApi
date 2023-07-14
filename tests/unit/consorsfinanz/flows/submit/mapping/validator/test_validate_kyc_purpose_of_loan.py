from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import FieldEnum, DataError
from app.consorsfinanz.flows.submit.mapping.validator.validate_kyc_purpose_of_loan import validate_kyc_purpose_of_loan
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import AnredeEnum, PartnerCustom, Custom
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages


def test_validate_kyc_purpose_of_loan():
    partner = PartnerCustom(
        custom=[
            Custom(key="finanzierungszweckBeschreibung", value="AMA"),
        ]
    )

    # WHEN
    response = validate_kyc_purpose_of_loan(partner)

    # THEN
    assert_that(response, equal_to([]))


def test_validate_kyc_purpose_of_loan_error():
    # WHEN
    response = validate_kyc_purpose_of_loan(None)

    # THEN
    assert_that(response, equal_to([DataError(field=FieldEnum.FINANZIERUNGSZWECKBESCHREIBUNG,
                                              message=ErrorMessages.FINANZIERUNGSZWECKBESCHREIBUNG_ERROR)]))

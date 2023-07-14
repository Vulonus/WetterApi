import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom, Stammdaten
from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_bank_account import validate_bank_account


def test_validate_bank_account_missing_zeitpunkt_kontoeroeffnung():
    partner = PartnerCustom(
        custom=[
            Custom(key="zeitpunktKontoeroeffnungAs1Foo", value="2014-01-01"),
        ]
    )

    # WHEN
    response = validate_bank_account(Stammdaten(iban="DE89370400440532013000"), partner)

    # THEN
    assert_that(response, equal_to(
        [DataError(field=FieldEnum.KONTOVERBINDUNG_ZEITPUNKT_EROEFFNUNG,
                   message=ErrorMessages.KONTOVERBINDUNG_ZEITPUNKT_EROEFFNUNG_ERROR)]
    ))


def test_validate_bank_account_missing_iban():
    partner = PartnerCustom(
        custom=[
            Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-01-01"),
        ]
    )

    # WHEN
    response = validate_bank_account(Stammdaten(iban=None), partner)

    # THEN
    assert_that(response, equal_to(
        [DataError(field=FieldEnum.KONTOVERBINDUNG_IBAN, message=ErrorMessages.KONTOVERBINDUNG_IBAN_ERROR)]
    ))

@pytest.mark.parametrize("data", [
    {"iban": "DE.89370400440532013000"},
    {"iban": "DE89370400440532013000)"},
    {"iban": "DE.8937040044053203A000"},
])
def test_validate_bank_account_wrong_pattern(data):
    partner = PartnerCustom(
        custom=[
            Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-01-01"),
        ]
    )

    # WHEN
    response = validate_bank_account(Stammdaten(iban=data["iban"]), partner)

    # THEN
    assert_that(response, equal_to(
        [DataError(field=FieldEnum.KONTOVERBINDUNG_IBAN, message=ErrorMessages.KONTOVERBINDUNG_IBAN_ERROR)]
    ))


@pytest.mark.parametrize("data", [
    {"iban": "DE39 1001 0010 0721 4381 26"},
    {"iban": "DE89370400440532013000"},
])
def test_validate_bank_account_no_errors(data):
    partner = PartnerCustom(
        custom=[
            Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-01-01"),
        ]
    )

    # WHEN
    response = validate_bank_account(Stammdaten(iban=data["iban"]), partner)

    # THEN
    assert_that(response, equal_to([]))

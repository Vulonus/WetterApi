import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_contact_address import validate_contact_address


@pytest.mark.parametrize("data", [
    {
        "emailAs1": "a#b.de",
        "telefonPrivatAs1": "111",
        "telefonGeschaeftlichAs1": "111",
        "strasseAs1": "Barstr##",
        "hausnummerAs1": "ab+#",
        "plzAs1": "10713asd##",
        "ortAs1": "Berli#++",
        "errors": [DataError(field=FieldEnum.EMAIL_AS1, message=ErrorMessages.EMAIL_INVALID_ERROR),
                   DataError(field=FieldEnum.TELEFON_PRIVAT_AS1, message=ErrorMessages.PRIVATE_PHONE_INVALID_ERROR),
                   DataError(field=FieldEnum.TELEFON_GEASCHAEFTLICH_AS1,
                             message=ErrorMessages.BUSINESS_PHONE_INVALID_ERROR),
                   DataError(field=FieldEnum.STRASSE_AS1, message=ErrorMessages.STREET_INVALID_ERROR),
                   DataError(field=FieldEnum.HAUSNUMMER_AS1, message=ErrorMessages.HOUSENUMBER_INVALID_ERROR),
                   DataError(field=FieldEnum.PLZ_AS1, message=ErrorMessages.ZIPCODE_INVALID_ERROR),
                   DataError(field=FieldEnum.ORT_AS1, message=ErrorMessages.CITY_INVALID_ERROR)]
    },
    {
        "emailAs1": "",
        "telefonPrivatAs1": "",
        "telefonGeschaeftlichAs1": "",
        "strasseAs1": "",
        "hausnummerAs1": "",
        "plzAs1": "",
        "ortAs1": "",
        "errors": [DataError(field=FieldEnum.EMAIL_AS1, message=ErrorMessages.EMAIL_ERROR),
                   DataError(field=FieldEnum.TELEFON_PRIVAT_AS1, message=ErrorMessages.PRIVATE_PHONE_ERROR),
                   DataError(field=FieldEnum.STRASSE_AS1, message=ErrorMessages.STREET_ERROR),
                   DataError(field=FieldEnum.HAUSNUMMER_AS1, message=ErrorMessages.HOUSENUMBER_ERROR),
                   DataError(field=FieldEnum.PLZ_AS1, message=ErrorMessages.ZIPCODE_ERROR),
                   DataError(field=FieldEnum.ORT_AS1, message=ErrorMessages.CITY_ERROR)]
    }
])
def test_data_invalid_or_missing(data, vorgang):
    # GIVEN
    vorgang.stammdaten.emailAs1 = data["emailAs1"]
    vorgang.stammdaten.telefonPrivatAs1 = data["telefonPrivatAs1"]
    vorgang.stammdaten.telefonGeschaeftlichAs1 = data["telefonGeschaeftlichAs1"]
    vorgang.stammdaten.strasseAs1 = data["strasseAs1"]
    vorgang.stammdaten.hausnummerAs1 = data["hausnummerAs1"]
    vorgang.stammdaten.plzAs1 = data["plzAs1"]
    vorgang.stammdaten.ortAs1 = data["ortAs1"]

    # WHEN
    errors = validate_contact_address(vorgang)

    # THEN
    assert_that(errors, equal_to(data["errors"]))


@pytest.mark.parametrize("data", [
    {
        "emailAs1": "stephan.malek@drklein.de",
        "strasseAs1": "Barstraße",
        "hausnummerAs1": "11",
        "plzAs1": "10713",
        "ortAs1": "Berlin",
        "telefonPrivatAs1": "0451123456",
        "telefonGeschaeftlichAs1": "+4945043132",
        "errors": []
    }
])
def test_valid_data(data, vorgang):
    # GIVEN
    vorgang.stammdaten.emailAs1 = data["emailAs1"]
    vorgang.stammdaten.telefonPrivatAs1 = data["telefonPrivatAs1"]
    vorgang.stammdaten.telefonGeschaeftlichAs1 = data["telefonGeschaeftlichAs1"]
    vorgang.stammdaten.strasseAs1 = data["strasseAs1"]
    vorgang.stammdaten.hausnummerAs1 = data["hausnummerAs1"]
    vorgang.stammdaten.plzAs1 = data["plzAs1"]
    vorgang.stammdaten.ortAs1 = data["ortAs1"]

    # WHEN
    errors = validate_contact_address(vorgang)

    # THEN
    assert_that(errors, equal_to(data["errors"]))

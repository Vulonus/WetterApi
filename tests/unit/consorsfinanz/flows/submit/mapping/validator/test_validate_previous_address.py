from datetime import datetime
from unittest import mock

import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_previous_address import validate_previous_address


@pytest.mark.parametrize("data", [
    {
        "errorMessage": [
            DataError(field=FieldEnum.VORANSCHRIFT_STRASSE_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_STREET_INVALID_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_HAUSNUMMER_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_HOUSENUMBER_INVALID_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_PLZ_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_ZIPCODE_INVALID_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_ORT_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_CITY_INVALID_ERROR)
        ],
        "voranschriftStrasseAs1": "Barstr##",
        "voranschriftHausnummerAs1": "abc+#",
        "voranschriftPlzAs1": "10713asd##",
        "voranschriftOrtAs1": "Berli#++"
    },
    {
        "errorMessage": [
            DataError(field=FieldEnum.VORANSCHRIFT_STRASSE_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_STREET_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_HAUSNUMMER_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_HOUSENUMBER_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_PLZ_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_ZIPCODE_ERROR),
            DataError(field=FieldEnum.VORANSCHRIFT_ORT_AS1,
                      message=ErrorMessages.PREVIOUS_ADDRESS_CITY_ERROR)
        ],
        "voranschriftStrasseAs1": None,
        "voranschriftHausnummerAs1": None,
        "voranschriftPlzAs1": None,
        "voranschriftOrtAs1": None
    }
])
def test_validate_previous_address__provide_invalid_or_missing_data__return_error(data, vorgang):
    with mock.patch("app.consorsfinanz.flows.submit.mapping.validator.validate_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 1, 1)
        mock_date.fromisoformat.return_value = datetime(2009, 1, 1, 0, 0, 0)

        # GIVEN
        vorgang.stammdaten.voranschriftStrasseAs1 = data["voranschriftStrasseAs1"]
        vorgang.stammdaten.voranschriftHausnummerAs1 = data["voranschriftHausnummerAs1"]
        vorgang.stammdaten.voranschriftPlzAs1 = data["voranschriftPlzAs1"]
        vorgang.stammdaten.voranschriftOrtAs1 = data["voranschriftOrtAs1"]

        # WHEN
        errors = validate_previous_address(vorgang)

        # THEN
        assert_that(data["errorMessage"], equal_to(errors))


def test_validate_previous_address__provide_correct_data__return_no_error(vorgang):
    with mock.patch("app.consorsfinanz.flows.submit.mapping.validator.validate_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 1, 1)
        mock_date.fromisoformat.return_value = datetime(2008, 1, 1, 0, 0, 0)

        # WHEN
        errors = validate_previous_address(vorgang)

        # THEN
        assert_that(errors, equal_to([]))

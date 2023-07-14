from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import FieldEnum, DataError
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import AnredeEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_gender import validate_gender


def test_validate_gender():

    # WHEN
    response = validate_gender(AnredeEnum.HERR)

    # THEN
    assert_that(response, equal_to([]))


def test_validate_gender_error():
    # WHEN
    response = validate_gender(None)

    # THEN
    assert_that(response, equal_to([DataError(field=FieldEnum.ANREDE_AS1, message=ErrorMessages.GENDER_ERROR)]))

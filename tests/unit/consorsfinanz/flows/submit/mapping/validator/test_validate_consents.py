import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_consents import validate_consents
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom, Antragsdaten


@pytest.mark.parametrize("data", [
    {
        "datenweitergabe": False,
        "errorMessages": [DataError(field=FieldEnum.DATENWEITERGABE,
                                    message=ErrorMessages.DATENWEITERGABE_ERROR)],
        "antragsvolumen": 3000,
        "laufzeitInMonaten": 12
    },
    {
        "datenweitergabe": True,
        "errorMessages": [DataError(field=FieldEnum.ANTRAGSDATEN_ANTRAGSVOLUMEN,
                                    message=ErrorMessages.ANTRAGSDATEN_ANTRAGSVOLUMEN_ERROR)],
        "antragsvolumen": None,
        "laufzeitInMonaten": 12
    },
    {
        "datenweitergabe": True,
        "errorMessages": [DataError(field=FieldEnum.ANTRAGSDATEN_LAUFZEIT_IN_MONATEN,
                                    message=ErrorMessages.ANTRAGSDATEN_LAUFZEIT_IN_MONATEN_ERROR)],
        "antragsvolumen": 3000,
        "laufzeitInMonaten": None
    },
    {
        "datenweitergabe": False,
        "errorMessages": [DataError(field=FieldEnum.DATENWEITERGABE,
                                    message=ErrorMessages.DATENWEITERGABE_ERROR),
                          DataError(field=FieldEnum.ANTRAGSDATEN_ANTRAGSVOLUMEN,
                                    message=ErrorMessages.ANTRAGSDATEN_ANTRAGSVOLUMEN_ERROR),
                          DataError(field=FieldEnum.ANTRAGSDATEN_LAUFZEIT_IN_MONATEN,
                                    message=ErrorMessages.ANTRAGSDATEN_LAUFZEIT_IN_MONATEN_ERROR)],
        "antragsvolumen": None,
        "laufzeitInMonaten": None
    },
    {
        "datenweitergabe": True,
        "errorMessages": [],
        "antragsvolumen": 3000,
        "laufzeitInMonaten": 12
    }
])
def test_validate_consents__datenweitergabe(data):
    partner = PartnerCustom(custom=[
        Custom(key="datenweitergabe", value=data["datenweitergabe"]),
        Custom(key="datenweitergabeDirektabschluss", value=False)
    ])
    antragsdaten = Antragsdaten(antragsvolumen=data["antragsvolumen"], laufzeitInMonaten=data["laufzeitInMonaten"])
    # WHEN
    response = validate_consents(partner, antragsdaten)
    # THEN
    assert_that(response, equal_to(data["errorMessages"]))

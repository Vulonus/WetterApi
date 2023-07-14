import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_residence_permit_type import \
    validate_residence_permit_type
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import AufenthaltstitelEnum


@pytest.mark.parametrize("data", [
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.VISUM,
        "aufenthaltBefristetBisAs1": None,
        "errorMessages": [DataError(field=FieldEnum.AUFENTHALT_BEFRISTET_BIS_AS1,
                                    message=ErrorMessages.IDENTITY_RESIDENCE_PERMIT_VALID_TILL_ERROR)],
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.AUFENTHALTSERLAUBNIS,
        "aufenthaltBefristetBisAs1": None,
        "errorMessages": [DataError(field=FieldEnum.AUFENTHALT_BEFRISTET_BIS_AS1,
                                    message=ErrorMessages.IDENTITY_RESIDENCE_PERMIT_VALID_TILL_ERROR)]
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.NIEDERLASSUNGSERLAUBNIS,
        "aufenthaltBefristetBisAs1": "2035-01-01",
        "errorMessages": [DataError(field=FieldEnum.AUFENTHALT_BEFRISTET_BIS_AS1,
                                    message=ErrorMessages.IDENTITY_RESIDENCE_PERMIT_VALID_TILL_INVALID)]
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.ERLAUBNIS_ZUM_DAUERAUFENTHALT_EU,
        "aufenthaltBefristetBisAs1": "2035-01-01",
        "errorMessages": [DataError(field=FieldEnum.AUFENTHALT_BEFRISTET_BIS_AS1,
                                    message=ErrorMessages.IDENTITY_RESIDENCE_PERMIT_VALID_TILL_INVALID)]
    }
])
def test_validate_residence_permit_type__provide_invalid_data__return_error(data, vorgang):
    vorgang.stammdaten.staatsangehoerigkeitAs1 = data["staatsangehoerigkeitAs1"]
    vorgang.stammdaten.aufenthaltstitelAs1 = data["aufenthaltstitelAs1"]
    vorgang.stammdaten.aufenthaltBefristetBisAs1 = data["aufenthaltBefristetBisAs1"]
    # WHEN
    response = validate_residence_permit_type(stammdaten=vorgang.stammdaten)
    # THEN
    assert_that(response, equal_to(data["errorMessages"]))


@pytest.mark.parametrize("data", [
    {
        "staatsangehoerigkeitAs1": "DE",
        "aufenthaltstitelAs1": None,
        "aufenthaltBefristetBisAs1": None,
        "errorMessages": [],
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.VISUM,
        "aufenthaltBefristetBisAs1": "2035-01-01",
        "errorMessages": []
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.AUFENTHALTSERLAUBNIS,
        "aufenthaltBefristetBisAs1": "2035-01-01",
        "errorMessages": []
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.NIEDERLASSUNGSERLAUBNIS,
        "aufenthaltBefristetBisAs1": None,
        "errorMessages": []
    },
    {
        "staatsangehoerigkeitAs1": "CN",
        "aufenthaltstitelAs1": AufenthaltstitelEnum.ERLAUBNIS_ZUM_DAUERAUFENTHALT_EU,
        "aufenthaltBefristetBisAs1": None,
        "errorMessages": []
    },
])
def test_validate_residence_permit_type__provide_valid_data__return_no_error(data, vorgang):
    vorgang.stammdaten.staatsangehoerigkeitAs1 = data["staatsangehoerigkeitAs1"]
    vorgang.stammdaten.aufenthaltstitelAs1 = data["aufenthaltstitelAs1"]
    vorgang.stammdaten.aufenthaltBefristetBisAs1 = data["aufenthaltBefristetBisAs1"]
    # WHEN
    response = validate_residence_permit_type(stammdaten=vorgang.stammdaten)
    # THEN
    assert_that(response, equal_to(data["errorMessages"]))


def test_validate_residence_permit_type__provide_none__return_error(vorgang):
    # GIVEN
    vorgang.stammdaten.staatsangehoerigkeitAs1 = None
    vorgang.stammdaten.aufenthaltstitelAs1 = None
    vorgang.stammdaten.aufenthaltBefristetBisAs1 = None
    # WHEN
    response = validate_residence_permit_type(stammdaten=vorgang.stammdaten)
    # THEN
    assert_that(response, equal_to([DataError(field=FieldEnum.AUFENTHALTSTITEL,
                                              message=ErrorMessages.IDENTITY_RESIDENCE_PERMIT_TYPE_ERROR)]))

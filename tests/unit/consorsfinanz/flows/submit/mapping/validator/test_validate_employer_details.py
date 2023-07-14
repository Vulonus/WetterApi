import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_employer_details import validate_employer_details
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    AnredeEnum, TitleEnum, WohnartEnum, FamilienstandEnum, Kind, BeschaeftigungsartEnum, BrancheEnum


@pytest.mark.parametrize("data", [
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [
            DataError(field=FieldEnum.BESCHAEFTIGUNG_ARBEITSBEGINN_GEBURTSDATUM_AS1,
                      message=ErrorMessages.BESCHAEFTIGUNGSBEGINN_LESS_THEN_18)
        ],
        "geburtsdatumAs1": "1999-12-11",
        "beschaeftigtSeitAs1": "2014-10-20"
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [
            DataError(field=FieldEnum.BESCHAEFTIGT_SEIT_AS1,
                      message=ErrorMessages.BESCHAEFTIGUNGSBEGINN_ERROR),
            DataError(field=FieldEnum.GEBURTSDATUM_AS1,
                      message=ErrorMessages.GEBURTSDATUM_ERROR)
        ],
        "geburtsdatumAs1": None,
        "beschaeftigtSeitAs1": None
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [],
        "geburtsdatumAs1": "1980-12-11",
        "beschaeftigtSeitAs1": "2014-10-20"
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [],
        "geburtsdatumAs1": "1990-01-01",
        "beschaeftigtSeitAs1": "2008-01-01"
    }
])
def test_validate_employer_details_regular_employed(data):
    # GIVEN
    vorgang_martkplatz = VorgangMarktplatzModel(
        stammdaten=Stammdaten(
            anredeAs1=AnredeEnum.HERR,
            titelAs1=[TitleEnum.DOKTOR],
            vornameAs1="Hans",
            nachnameAs1="Dampf",
            emailAs1="jean-marc.nadal@consorsfinanz.de",
            strasseAs1="Fraunbergstr 18",
            plzAs1="81379",
            ortAs1="Bonn",
            wohnhaftSeitAs1="2014-10-20",
            telefonPrivatAs1="089832432432",
            geburtsnameAs1="foo",
            geburtsdatumAs1=data["geburtsdatumAs1"],
            staatsangehoerigkeitAs1="DE",
            geburtslandAs1="DE",
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            familienstandAs1=FamilienstandEnum.VERHEIRATET,
            kinder=[Kind(kindergeldFuer="lisa")],
            iban="DE89370400440532013000",
            einkommenMonatlichAs1=1500,
            beschaeftigungsartAs1=data["beschaeftigungsartAs1"],
            beschaeftigtSeitAs1=data["beschaeftigtSeitAs1"],
            arbeitgeberNameAs1="Siemens GmbH",
            arbeitgeberStrasseAs1="Hansastr. 11",
            arbeitgeberPlzAs1="80339",
            arbeitgeberOrtAs1="Muenchen",
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin"
        )
    )

    errors = validate_employer_details(vorgang_martkplatz)

    # THEN
    assert_that(errors, equal_to(data["errorMessage"]))


@pytest.mark.parametrize("data", [
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.SELBSTSTAENDIGER,
        "errorMessage": [
            DataError(field=FieldEnum.SELBSTSTAENDIG_SEIT_AS1,
                      message=ErrorMessages.SELBSTSTAENDIG_SEIT_LESS_THEN_18)
        ],
        "geburtsdatumAs1": "1999-12-11",
        "selbststaendigSeitAs1": "2014-10-20"
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.FREIBERUFLER,
        "errorMessage": [
            DataError(field=FieldEnum.SELBSTSTAENDIG_SEIT_AS1,
                      message=ErrorMessages.EMPLOYMENT_DETAILS_SELF_EMPLOYED_SINCE_ERROR),
            DataError(field=FieldEnum.GEBURTSDATUM_AS1,
                      message=ErrorMessages.GEBURTSDATUM_ERROR)
        ],
        "geburtsdatumAs1": None,
        "selbststaendigSeitAs1": None
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.SELBSTSTAENDIGER,
        "errorMessage": [],
        "geburtsdatumAs1": "1980-12-11",
        "selbststaendigSeitAs1": "2014-10-20"
    }
])
def test_validate_employer_details_self_employed(data):
    # GIVEN
    vorgang_martkplatz = VorgangMarktplatzModel(
        stammdaten=Stammdaten(
            anredeAs1=AnredeEnum.HERR,
            titelAs1=[TitleEnum.DOKTOR],
            vornameAs1="Hans",
            nachnameAs1="Dampf",
            emailAs1="jean-marc.nadal@consorsfinanz.de",
            strasseAs1="Fraunbergstr 18",
            plzAs1="81379",
            ortAs1="Bonn",
            wohnhaftSeitAs1="2014-10-20",
            telefonPrivatAs1="089832432432",
            geburtsnameAs1="foo",
            geburtsdatumAs1=data["geburtsdatumAs1"],
            staatsangehoerigkeitAs1="DE",
            geburtslandAs1="DE",
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            familienstandAs1=FamilienstandEnum.VERHEIRATET,
            kinder=[Kind(kindergeldFuer="lisa")],
            iban="DE89370400440532013000",
            einkommenMonatlichAs1=1500,
            beschaeftigungsartAs1=data["beschaeftigungsartAs1"],
            selbststaendigSeitAs1=data["selbststaendigSeitAs1"],
            firmaNameAs1="Siemens GmbH",
            firmaStrasseAs1="Hansastr.",
            firmaHausnummerAs1="11",
            firmaPlzAs1="80339",
            firmaOrtAs1="Muenchen",
            firmaBrancheAs1=BrancheEnum.ENERGIE_WASSERVERSORGUNG_BERGBAU,
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin"
        )
    )

    errors = validate_employer_details(vorgang_martkplatz)

    # THEN
    assert_that(errors, equal_to(data["errorMessage"]))

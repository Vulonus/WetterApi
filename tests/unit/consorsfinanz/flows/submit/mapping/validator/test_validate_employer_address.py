import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_employer_address import validate_employer_address
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    FamilienstandEnum, Kind, BeschaeftigungsartEnum, WohnartEnum, AnredeEnum, TitleEnum, BrancheEnum


@pytest.mark.parametrize("data", [
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [
            DataError(field=FieldEnum.ARBEITGEBER_NAME_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_NAME_ERROR),
            DataError(field=FieldEnum.ARBEITGEBER_STRASSE_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_STREET_ERROR),
            DataError(field=FieldEnum.ARBEITGEBER_HAUSNUMMER_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_HOUSE_NUMBER_ERROR),
            DataError(field=FieldEnum.ARBEITGEBER_PLZ_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_ZIPCODE_ERROR),
            DataError(field=FieldEnum.ARBEITGEBER_ORT_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_CITY_ERROR)
        ],
        "arbeitgeberNameAs1": None,
        "arbeitgeberStrasseAs1": None,
        "arbeitgeberHausnummerAs1": None,
        "arbeitgeberPlzAs1": None,
        "arbeitgeberOrtAs1": None
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [
            DataError(field=FieldEnum.ARBEITGEBER_ORT_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_CITY_ERROR)
        ],
        "arbeitgeberNameAs1": "Siemens GmbH",
        "arbeitgeberStrasseAs1": "Hansastr.",
        "arbeitgeberHausnummerAs1": "11",
        "arbeitgeberPlzAs1": "80339",
        "arbeitgeberOrtAs1": None
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.ANGESTELLTER,
        "errorMessage": [],
        "arbeitgeberNameAs1": "Siemens GmbH",
        "arbeitgeberStrasseAs1": "Hansastr.",
        "arbeitgeberHausnummerAs1": "11",
        "arbeitgeberPlzAs1": "80339",
        "arbeitgeberOrtAs1": "Muenchen",
    }
])
def test_validate_employer_address_regular_employed(data):
    # GIVEN
    vorgang_marktplatz = VorgangMarktplatzModel(
        stammdaten=Stammdaten(
            anredeAs1=AnredeEnum.HERR,
            titelAs1=[TitleEnum.DOKTOR],
            vornameAs1="Hans",
            nachnameAs1="Dampf",
            emailAs1="jean-marc.nadal@consorsfinanz.de",
            strasseAs1="Fraunbergstr 18",
            plzAs1="81379",
            ortAs1="Bonn",
            wohnhaftSeitAs1="2014-10-20T13:14:07.712+02:00",
            telefonPrivatAs1="089832432432",
            geburtsnameAs1="foo",
            geburtsdatumAs1="1980-12-11T13:14:07.712+02:00",
            staatsangehoerigkeitAs1="DE",
            geburtslandAs1="DE",
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            familienstandAs1=FamilienstandEnum.VERHEIRATET,
            kinder=[Kind(kindergeldFuer="lisa")],
            iban="DE89370400440532013000",
            einkommenMonatlichAs1=1500,
            beschaeftigungsartAs1=data["beschaeftigungsartAs1"],
            beschaeftigtSeitAs1="2014-10-20T13:14:07.712+02:00",
            arbeitgeberNameAs1=data["arbeitgeberNameAs1"],
            arbeitgeberStrasseAs1=data["arbeitgeberStrasseAs1"],
            arbeitgeberHausnummerAs1=data["arbeitgeberHausnummerAs1"],
            arbeitgeberPlzAs1=data["arbeitgeberPlzAs1"],
            arbeitgeberOrtAs1=data["arbeitgeberOrtAs1"],
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin"
        )
    )

    errors = validate_employer_address(vorgang_marktplatz)

    # THEN
    assert_that(errors, equal_to(data["errorMessage"]))


@pytest.mark.parametrize("data", [
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.SELBSTSTAENDIGER,
        "errorMessage": [
            DataError(field=FieldEnum.FIRMA_NAME_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_NAME_ERROR),
            DataError(field=FieldEnum.FIRMA_BRANCHE_AS1,
                      message=ErrorMessages.EMPLOYMENT_DETAILS_INDUSTRY_ERROR),
            DataError(field=FieldEnum.FIRMA_STRASSE_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_STREET_ERROR),
            DataError(field=FieldEnum.FIRMA_HAUSNUMMER_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_HOUSE_NUMBER_ERROR),
            DataError(field=FieldEnum.FIRMA_PLZ_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_ZIPCODE_ERROR),
            DataError(field=FieldEnum.FIRMA_ORT_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_CITY_ERROR),
            DataError(field=FieldEnum.SELBSTSTAENDIG_SEIT_AS1,
                      message=ErrorMessages.EMPLOYMENT_DETAILS_SELF_EMPLOYED_SINCE_ERROR)
        ],
        "firmaNameAs1": None,
        "firmaStrasseAs1": None,
        "firmaHausnummerAs1": None,
        "firmaPlzAs1": None,
        "firmaOrtAs1": None,
        "firmaBrancheAs1": None,
        "selbststaendigSeitAs1": None
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.FREIBERUFLER,
        "errorMessage": [
            DataError(field=FieldEnum.FIRMA_ORT_AS1,
                      message=ErrorMessages.EMPLOYER_ADDRESS_EMPLOYER_CITY_ERROR)
        ],
        "firmaNameAs1": "Siemens GmbH",
        "firmaStrasseAs1": "Hansastr",
        "firmaHausnummerAs1": "11",
        "firmaPlzAs1": "80339",
        "firmaOrtAs1": None,
        "firmaBrancheAs1": BrancheEnum.ENERGIE_WASSERVERSORGUNG_BERGBAU,
        "selbststaendigSeitAs1": "2014-10-20"
    },
    {
        "beschaeftigungsartAs1": BeschaeftigungsartEnum.SELBSTSTAENDIGER,
        "errorMessage": [],
        "firmaNameAs1": "Siemens GmbH",
        "firmaStrasseAs1": "Hansastr",
        "firmaHausnummerAs1": "11",
        "firmaPlzAs1": "80339",
        "firmaOrtAs1": "Muenchen",
        # "firmaLandAs1": "DE",
        "firmaBrancheAs1": BrancheEnum.ENERGIE_WASSERVERSORGUNG_BERGBAU,
        "selbststaendigSeitAs1": "2014-10-20"
    }
])
def test_validate_employer_address_self_employed(data):
    # GIVEN
    vorgang_marktplatz = VorgangMarktplatzModel(
        stammdaten=Stammdaten(
            anredeAs1=AnredeEnum.HERR,
            titelAs1=[TitleEnum.DOKTOR],
            vornameAs1="Hans",
            nachnameAs1="Dampf",
            emailAs1="jean-marc.nadal@consorsfinanz.de",
            strasseAs1="Fraunbergstr 18",
            plzAs1="81379",
            ortAs1="Bonn",
            wohnhaftSeitAs1="2014-10-20T13:14:07.712+02:00",
            telefonPrivatAs1="089832432432",
            geburtsnameAs1="foo",
            geburtsdatumAs1="1980-12-11T13:14:07.712+02:00",
            staatsangehoerigkeitAs1="DE",
            geburtslandAs1="DE",
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            familienstandAs1=FamilienstandEnum.VERHEIRATET,
            kinder=[Kind(kindergeldFuer="lisa")],
            iban="DE89370400440532013000",
            einkommenMonatlichAs1=1500,
            beschaeftigungsartAs1=data["beschaeftigungsartAs1"],
            firmaNameAs1=data["firmaNameAs1"],
            firmaBrancheAs1=data["firmaBrancheAs1"],
            firmaStrasseAs1=data["firmaStrasseAs1"],
            firmaHausnummerAs1=data["firmaHausnummerAs1"],
            firmaPlzAs1=data["firmaPlzAs1"],
            firmaOrtAs1=data["firmaOrtAs1"],
            selbststaendigSeitAs1=data["selbststaendigSeitAs1"],
            # firmaLandAs1=data["firmaLandAs1"],
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin"
        )
    )

    errors = validate_employer_address(vorgang_marktplatz)

    # THEN
    assert_that(errors, equal_to(data["errorMessage"]))

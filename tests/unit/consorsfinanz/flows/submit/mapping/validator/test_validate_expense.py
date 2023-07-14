import pytest
from hamcrest import equal_to, assert_that

from app.common.errors.field_data_error import DataError, FieldEnum
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from app.consorsfinanz.flows.submit.mapping.validator.validate_expense import validate_expense
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    AnredeEnum, TitleEnum, WohnartEnum, \
    FamilienstandEnum, Kind, Bonitaetsangaben, MietAusgaben, BeschaeftigungsartEnum, Immobilie, Darlehen


@pytest.mark.parametrize("data", [
    {
        "errorMessage": [],
        "bonitaetsangaben": Bonitaetsangaben(),
        "immobilien": [],
        "wohnartAs1": WohnartEnum.BEI_DEN_ELTERN
    },
    {
        "errorMessage": [],
        "bonitaetsangaben": Bonitaetsangaben(mietausgaben=[MietAusgaben(betragMonatlich="200")]),
        "immobilien": [],
        "wohnartAs1": WohnartEnum.ZUR_MIETE
    },
    {
        "errorMessage": [],
        "bonitaetsangaben": Bonitaetsangaben(mietausgaben=[MietAusgaben()]),
        "immobilien": [Immobilie(darlehen=[Darlehen(rateMonatlich=150)])],
        "wohnartAs1": WohnartEnum.IM_EIGENEN_HAUS
    },
    {
        "errorMessage": [DataError(field=FieldEnum.IMMOBILIEN_DARLEHEN_RATE_MONATLICH_AS1,
                                   message=ErrorMessages.WARM_RENT_ERROR)],
        "bonitaetsangaben": Bonitaetsangaben(),
        "immobilien": [],
        "wohnartAs1": WohnartEnum.IM_EIGENEN_HAUS
    }
])
def test_validate_expense(data):
    # GIVEN
    vorgang = VorgangMarktplatzModel(
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
            wohnartAs1=data["wohnartAs1"],
            familienstandAs1=FamilienstandEnum.VERHEIRATET,
            kinder=[Kind(kindergeldFuer="lisa")],
            iban="DE89370400440532013000",
            einkommenMonatlichAs1=1500,
            beschaeftigungsartAs1=BeschaeftigungsartEnum.ANGESTELLTER,
            beschaeftigtSeitAs1="2014-10-20T13:14:07.712+02:00",
            arbeitgeberNameAs1="Siemens GmbH",
            arbeitgeberStrasseAs1="Hansastr. 11",
            arbeitgeberPlzAs1="80339",
            arbeitgeberOrtAs1="Muenchen",
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin",
            immobilien=data["immobilien"]
        ),
        bonitaetsangaben=data["bonitaetsangaben"]
    )

    errors = validate_expense(vorgang)

    # THEN
    assert_that(errors, equal_to(data["errorMessage"]))

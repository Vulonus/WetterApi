import pytest

from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Stammdaten, VorgangMarktplatzModel, \
    AnredeEnum, TitleEnum, WohnartEnum, FamilienstandEnum, Kind, BeschaeftigungsartEnum


@pytest.fixture(name="vorgang")
def vorgang():
    return VorgangMarktplatzModel(
        stammdaten=Stammdaten(
            anredeAs1=AnredeEnum.HERR,
            titelAs1=[TitleEnum.DOKTOR],
            vornameAs1="Hans",
            nachnameAs1="Dampf",
            emailAs1="jean-marc.nadal@consorsfinanz.de",
            strasseAs1="Fraunbergstr 18",
            plzAs1="81379",
            ortAs1="Bonn",
            wohnhaftSeitAs1="2014-10-20T13:14:07.712",
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
            beschaeftigungsartAs1=BeschaeftigungsartEnum.ANGESTELLTER,
            beschaeftigtSeitAs1="2014-10-20T13:14:07.712+02:00",
            arbeitgeberNameAs1="Siemens GmbH",
            arbeitgeberStrasseAs1="Hansastr.",
            arbeitgeberHausnummerAs1="11",
            arbeitgeberPlzAs1="80339",
            arbeitgeberOrtAs1="Muenchen",
            voranschriftStrasseAs1="Barstr",
            voranschriftHausnummerAs1="12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin"
        )
    )

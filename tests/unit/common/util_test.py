from hamcrest import equal_to, assert_that, instance_of

from app.common.util import safe_get, get_custom_value
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    FamilienstandEnum, Kind, BeschaeftigungsartEnum, Bonitaetsangaben, MietAusgaben, WohnartEnum, AnredeEnum, \
    TitleEnum, Unterhaltsverpflichtungen, PartnerCustom, Custom, Immobilie, Darlehen


def test_get_custom_value():
    partner_custom_list = [
        Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-10-20T13:14:07.712+02:00"),
        Custom(key="finanzierungszweckBeschreibung", value="AMA"),
        Custom(key="datenweitergabe", value=None)
    ]

    assert_that(get_custom_value(partner_custom_list, "zeitpunktKontoeroeffnungAs1"),
                equal_to("2014-10-20T13:14:07.712+02:00"))

    assert_that(get_custom_value(partner_custom_list, "finanzierungszweckBeschreibung"), equal_to("AMA"))

    assert_that(get_custom_value(partner_custom_list, "datenweitergabe"), equal_to(None))


def test_get_custom_value_empty_list():
    partner_custom_list = []

    assert_that(get_custom_value(partner_custom_list, "zeitpunktKontoeroeffnungAs1"), equal_to(None))


def test_safe_get():
    # GIVEN
    vorgang = VorgangMarktplatzModel(
        partner=PartnerCustom(custom=[
            Custom(key="finanzierungszweckBeschreibungAs1", value="AMA")
        ]),
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
            beschaeftigungsartAs1=BeschaeftigungsartEnum.ANGESTELLTER,
            beschaeftigtSeitAs1="2014-10-20T13:14:07.712+02:00",
            arbeitgeberNameAs1="Siemens GmbH",
            arbeitgeberStrasseAs1="Hansastr. 11",
            arbeitgeberPlzAs1="80339",
            arbeitgeberOrtAs1="Muenchen",
            voranschriftStrasseAs1="Barstr 12",
            voranschriftPlzAs1="10713",
            voranschriftOrtAs1="Berlin",
            immobilien=[Immobilie(
                darlehen=[Darlehen(
                    rateMonatlich=100
                )]
            )]
        ),
        bonitaetsangaben=Bonitaetsangaben(
            mietausgaben=[MietAusgaben(
                betragMonatlich="1",
                zugehoerigkeit="as1"
            )],
            unterhaltsverpflichtungen=[Unterhaltsverpflichtungen(
                zugehoerigkeit="as1"
            )],
            ehegattenunterhalt=[]
        )
    )

    foo_bar = safe_get(vorgang.dict(), "foo")
    foo_bar_default = safe_get(vorgang.dict(), "foo", "bar", "y", "x", return_default=0)
    bar_bar = safe_get(vorgang.dict(), "foo", "bar")
    mietausgaben_betrag_monatlich = safe_get(vorgang.dict(), "bonitaetsangaben", "mietausgaben", "betragMonatlich")
    mietausgaben = safe_get(vorgang.dict(), "bonitaetsangaben", "mietausgaben")
    ehegattenunterhalt = safe_get(vorgang.dict(), "bonitaetsangaben", "ehegattenunterhalt", "betragMonatlich")
    bonitaetsangaben = safe_get(vorgang.dict(), "bonitaetsangaben")
    voranschrift_ort_as1 = safe_get(vorgang.dict(), "stammdaten", "voranschriftOrtAs1")
    sonstige_ausgaben = safe_get(vorgang.dict(), "bonitaetsangaben", "sonstigeausgaben")
    unterhaltsverpflichtungen_betrag_monatlich = safe_get(
        vorgang.dict(), "bonitaetsangaben", "unterhaltsverpflichtungen", "betragMonatlich")
    unterhaltsverpflichtungen_zugehoerigkeit = safe_get(
        vorgang.dict(), "bonitaetsangaben", "unterhaltsverpflichtungen", "zugehoerigkeit")
    kinder_kindergeld_fuer = safe_get(vorgang.dict(), "stammdaten", "kinder", "kindergeldFuer")
    partner = safe_get(vorgang.partner.dict(), "custom", "value")
    immobilien_darlehen_rate_monatlich = safe_get(vorgang.stammdaten.dict(), "immobilien", "darlehen", "rateMonatlich")

    # THEN
    assert_that(foo_bar, equal_to(None))
    assert_that(foo_bar_default, equal_to(0))
    assert_that(bar_bar, equal_to(None))
    assert_that(mietausgaben_betrag_monatlich, equal_to("1"))
    assert_that(mietausgaben, instance_of(dict))
    assert_that(mietausgaben is None, equal_to(False))
    assert_that(mietausgaben["betragMonatlich"], equal_to("1"))
    assert_that(mietausgaben["zugehoerigkeit"], equal_to("as1"))
    assert_that(bonitaetsangaben, instance_of(dict))
    assert_that(bonitaetsangaben["mietausgaben"][0]["betragMonatlich"], equal_to("1"))
    assert_that(bonitaetsangaben["mietausgaben"][0]["zugehoerigkeit"], equal_to("as1"))
    assert_that(bonitaetsangaben is None, equal_to(False))
    assert_that(voranschrift_ort_as1, equal_to("Berlin"))
    assert_that(sonstige_ausgaben, equal_to(None))
    assert_that(unterhaltsverpflichtungen_betrag_monatlich, equal_to(None))
    assert_that(unterhaltsverpflichtungen_zugehoerigkeit, equal_to("as1"))
    assert_that(kinder_kindergeld_fuer, equal_to("lisa"))
    assert_that(partner, equal_to("AMA"))
    assert_that(ehegattenunterhalt, equal_to(None))
    assert_that(immobilien_darlehen_rate_monatlich, equal_to(100))

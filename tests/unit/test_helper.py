import asyncio

from app.consorsfinanz.flows.product.models.product_identifier_model import ProductDescription
from app.consorsfinanz.flows.submit.models.request_credit_submission_model import RequestCreditSubmissionModel
from app.consorsfinanz.flows.submit.models.response_loan_submit_model import ResponseLoanSubmitModel, \
    FeasibilityStatus, Privatkredit, Ratenschutz
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, AnredeEnum, \
    FamilienstandEnum, WohnartEnum, BrancheEnum, BeschaeftigungsartEnum, Stammdaten, Tippgeber, \
    Antragsdaten


def create_url_with_query(url, **kwargs):
    url_with_query = f"{url}?"
    for (key, value) in kwargs.items():
        url_with_query += f"{key}={value}&"
    return url_with_query[:-1]


def create_async_mock_response(variable) -> asyncio.Future:
    async_response = asyncio.Future()
    async_response.set_result(variable)
    return async_response


def message_with_detail_text(text="Some fancy text"):
    return {"detail": text}


PRODUKTGRENZEN_RESPONSE = {
    "kreditbetrag": {
        "min": 500,
        "max": 5000
    },
    "laufzeit": {
        "min": 6,
        "max": 120
    }
}


def create_mocked_dispatch_offer_request(nettokreditbetrag: int, laufzeit_in_monaten: int, monatliche_rate: float,
                                         effektivzins: float, sollzins: float, gesamtkreditbetrag: float):
    return {
        "loanType": "MCD",
        "loanDescription": ProductDescription.CONSORS_1PS,
        "financialCalculations":
            {
                "insuranceTypes": ["DEATH_DISABILITY_UNEMPLOYMENT"],
                "financialCalculation": [

                    {
                        "index": 0,
                        "creditAmount": nettokreditbetrag,
                        "duration": laufzeit_in_monaten,
                        "monthlyRate": monatliche_rate,
                        "effectiveRate": effektivzins,
                        "nominalRate": sollzins,
                        "totalPayment": gesamtkreditbetrag
                    }

                ]
            }
    }


def create_consors_api_financial_calculations(nettokreditbetrag: int, laufzeit_in_monaten: int, monatliche_rate: float,
                                              effektivzins: float,
                                              sollzins: float, gesamtkreditbetrag: float):
    return {"consorsfinanz": {
        "produktId": "MCD", "produkttyp": "RAHMENKREDIT",
        "produktbeschreibung": "Finanzierung Ihrer Sofortauszahlung (Ratenplan-Verfügung) über den "
                               "Kreditrahmen, den Sie wiederholt in Anspruch nehmen können. "
                               "Nettodarlehensbetrag bonitätsabhängig bis 15.000 €. 9,90 % effektiver "
                               "Jahreszinssatz. Vertragslaufzeit auf unbestimmte Zeit. \nRatenplan-Verfügung: "
                               "Gebundener Sollzinssatz von 11,28 % (jährlich) gilt nur für die ersten "
                               "18 Monate ab Vertragsschluss (Zinsbindungsdauer); Sie müssen monatliche "
                               "Teilzahlungen in der von Ihnen gewählten Höhe leisten. Führen Sie Ihre "
                               "Ratenplan-Verfügung nicht innerhalb der Zinsbindungsdauer zurück, gelten "
                               "die Konditionen für Folgeverfügungen. Folgeverfügungen: Für andere und "
                               "künftige Verfügungen (Folgeverfügungen) beträgt der veränderliche "
                               "Sollzinssatz (jährlich) 9,47 % (falls Sie bereits einen Kreditrahmen "
                               "bei uns haben, kann der tatsächliche veränderliche Sollzinssatz abweichen). "
                               "\nFür Folgeverfügungen müssen Sie monatliche Teilzahlungen in der von Ihnen "
                               "gewählten Höhe, mind. aber 2,5% der jeweils höchsten, auf volle 100 € "
                               "gerundeten Sollsaldos der Folgeverfügungen (mind. 9 €) leisten. Zahlungen "
                               "für Folgeverfügungen werden erst auf verzinste Folgeverfügungen angerechnet, "
                               "bei unterschiedlichen Zinssätzen zuerst auf die höher verzinsten.",
        "produktbezeichnung": "Consors Finanz 1PS",
        "versicherteRisiken": ["TOD", "ARBEITSUNFAEHIGKEIT", "ARBEITSLOSIGKEIT"],
        "nettokreditbetrag": nettokreditbetrag, "laufzeitInMonaten": laufzeit_in_monaten,
        "monatlicheRate": monatliche_rate,
        "effektivzins": effektivzins, "sollzins": sollzins, "gesamtkreditbetrag": gesamtkreditbetrag,
        "pAngV": "2/3 aller angenommenen Kunden erhalten: bei 2.000€ Kreditsumme 2,99% eff. Jahreszins, 2,94% fester "
               "Sollzins p.a., Gesamtbetrag 2061,84 €, mtl. Rate 85,91 €, Kreditgeber ist die BNP Paribas S.A. "
               "Niederlassung Deutschland, Standort München: Schwanthalerstr. 31, 80336 München",
        "kreditDetails": {"produktinformationen": [
            {"key": "PRODUKTINFORMATIONEN_SICHERHEIT",
             "description": "Absicherung des Darlehensnehmers möglich"},
            {"key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
             "description": "Sondertilgungen sind jederzeit möglich (gesetzliche Regelung "
                            "(1% oder Restlaufzeit<1 Jahr dann 0,5%))"},
            {"key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
             "description": "Vorzeitige Ablösung des Kredites ist jederzeit möglich (50% der Restschuld "
                            "kostenfrei, sonst 1% Vorfälligkeitsentschädigung, Laufzeit >1 Jahr 0,5%)"},
            {"key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
             "description": "Ratenpausen sind möglich"},
            {"key": "PRODUKTINFORMATIONEN_KUNDENFREUNDLICHKEIT",
             "description": "Bis 3.000 € Kreditsumme Rahmenkredit der Consors Finanz, mit Möglichkeit "
                            "(bei vorausgesetzter Bonität) jederzeitiger Aufstockung"}],
            "annahmerichtlinien": ["Mindestalter 18 Jahre",
                                   "Kein Höchstalter, Rückzahlung muss aber bis zum 84. Lebensjahr erfolgt sein",
                                   "Probezeit muss beendet sein",
                                   "Maximale Kreditsumme bis 50.000 €",
                                   "Laufzeiten bis 120 Monate möglich"]}}}


def create_request_credit_submission_model(credit_amount: float, duration: int, vorgangsnummer: str,
                                           vorgang: VorgangMarktplatzModel) -> RequestCreditSubmissionModel:
    return RequestCreditSubmissionModel(creditAmount=credit_amount, duration=duration, vorgangsnummer=vorgangsnummer,
                                        vorgang=vorgang)


def create_default_vorgang_marktplatz_model():
    return VorgangMarktplatzModel(
        drkleinrkVorgangsnummer="ABCDEFG",
        europaceVorgangsnummer="ABCDEFGH-1234",
        erstelltAm=20220518,
        aktualisiertAm=20220520,
        endetAm=20220601,
        erstelltAmISODate="2022-04-22T11:36:37.023+02:00",
        dataContext="TEST",
        leadquelle="AWESOME Bank",
        dublette=False,
        stammdaten=create_default_stammdaten(),
        tippgeber=create_default_tippgeber(),
        antragsdaten=create_default_antragsdaten()
    )


def create_default_stammdaten():
    return Stammdaten(
        # personendaten
        anredeAs1=AnredeEnum.HERR,
        vornameAs1="John",
        nachnameAs1="Doe",
        emailAs1="John.Doe@mail.com",
        familienstandAs1=FamilienstandEnum.VERHEIRATET.value,
        geburtsdatumAs1="14.12.1986",
        geburtsortAs1="Husum",
        geburtslandAs1="Deutschland",

        # anschrift
        strasseAs1="Wattwurmstraße",
        hausnummerAs1="42",
        plzAs1="25813",
        ortAs1="Husum",
        wohnhaftSeitAs1="01.01.2020",

        # kontoverbindung
        iban="DE91100000000123456789",
        kreditinstitut="Bundesbank",
        kontoinhaber="John Doe",

        # wohnsituation
        wohnartAs1=WohnartEnum.ZUR_MIETE.value,
        anzahlPersonenImHaushaltAs1="1",
        anzahlPkwAs1=1,

        # arbeitgeber
        arbeitgeberNameAs1="Krabbenfischer Meier",
        arbeitgeberBrancheAs1=BrancheEnum.LANDWIRTSCHAFT_FORSTWIRTSCHAFT_FISCHEREI.value,
        arbeitgeberStrasseAs1="Zum großen Fang",
        arbeitgeberHausnummerAs1="7",
        arbeitgeberPlzAs1="25813",
        arbeitgeberOrtAs1="Husum",
        arbeitgeberLandAs1="Deutschland",

        # beschaeftigung
        beschaeftigungsartAs1=BeschaeftigungsartEnum.ARBEITER.value,
        berufsbezeichnungAs1="Krabbenfischer",
        einkommenMonatlichAs1=3000,
        beschaeftigtSeitAs1="01.01.2000",
        inProbezeitAs1=False
    )


def create_default_tippgeber():
    return Tippgeber(
        externeMitarbeiternummer="NUMER-1234",
        vorname="Jens",
        nachname="Holstein",
        anrede="Herr",
        telefon="04504123456",
        email="Jens.Holstein@mail.com"
    )


def create_default_antragsdaten():
    return Antragsdaten(
        verwendungszweck="Freie Verwendung",
        laufzeitInMonaten=12,
        provisionswunschInProzent=3,
        rateMonatlich=350
    )


def create_response_loan_submit_model():
    return ResponseLoanSubmitModel(
        vorgangsnummer="ABCDEFG",
        verwendungszweck="Freie Verwendung",
        machbarkeit=FeasibilityStatus.ANGENOMMEN.value,
        produktanbieterantragsnummer="ProduktanbieterNr.123",
        qesLink="Https://qes.link",
        privatkredit=create_default_privatkredit(),
        ratenschutz=create_default_ratenschutz(),
        erforderlicheUnterlagen=["Unterlage_1"],
    )


def create_default_privatkredit():
    return Privatkredit(
        nettokreditbetrag=4200,
        laufzeitInMonaten=12,
        monatlicheRate=350,
        effektivzins=12.0,
        sollzins=11.5,
        gesamtkreditbetrag=4704,
    )


def create_default_ratenschutz():
    return Ratenschutz(
        versicherteRisikenAs1=["RISIKO_1", "TOD"],
        praemieMonatlich=42.0,
    )

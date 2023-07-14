import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.offer.mapping.loan_offer_mapper import map_loan_offer, map_product_description, \
    map_price_indication_ordinance, map_credit_details
from app.consorsfinanz.flows.offer.models.loan_offer_model import LoanOfferModel, FinanzierungsvorschlagDetails, \
    Produkttyp
from app.consorsfinanz.flows.product.models.product_identifier_model import ProductDescription
from tests.unit.consorsfinanz.flows.conftest import KREDIT_DETAILS


def test_map_credit_details():
    # WHEN
    result = map_credit_details()

    # THEN
    assert_that(result, equal_to(KREDIT_DETAILS))


@pytest.mark.parametrize("data", [
    {
        "loan_offer": {"loanType": "ICCL"},
        "pangv": "2/3 aller angenommenen Kunden erhalten: bei 20.000€ Kreditsumme 4,99% eff. Jahreszins, 4,88% fester "
                 "Sollzins p.a., Gesamtbetrag 23.110,62€, mtl. Rate 320,98 €, Kreditgeber ist die BNP Paribas S.A. "
                 "Niederlassung Deutschland, Standort München: Schwanthalerstr. 31, 80336 München"
    },
    {
        "loan_offer": {"loanType": "MCD"},
        "pangv": "2/3 aller angenommenen Kunden erhalten: bei 2.000€ Kreditsumme 2,99% eff. Jahreszins, 2,94% fester "
                 "Sollzins p.a., Gesamtbetrag 2061,84 €, mtl. Rate 85,91 €, Kreditgeber ist die BNP Paribas S.A. "
                 "Niederlassung Deutschland, Standort München: Schwanthalerstr. 31, 80336 München"
    }
])
def test_map_price_indication_ordinance(data):
    # WHEN
    result = map_price_indication_ordinance(data["loan_offer"])

    # THEN
    assert_that(result, equal_to(data["pangv"]))


def test_map_product_description():
    # WHEN
    result = map_product_description()

    # THEN
    assert_that(result, equal_to(
        "Finanzierung Ihrer Sofortauszahlung (Ratenplan-Verfügung) über den Kreditrahmen, " \
        "den Sie wiederholt in Anspruch nehmen können. Nettodarlehensbetrag bonitätsabhängig bis 15.000 €. 9,90 % " \
        "effektiver Jahreszinssatz. Vertragslaufzeit auf unbestimmte Zeit. \n" \
        "Ratenplan-Verfügung: Gebundener Sollzinssatz von 11,28 % (jährlich) gilt nur für die ersten " \
        "18 Monate ab Vertragsschluss (Zinsbindungsdauer); Sie müssen monatliche Teilzahlungen in der von Ihnen " \
        "gewählten Höhe leisten. Führen Sie Ihre Ratenplan-Verfügung nicht innerhalb der Zinsbindungsdauer zurück," \
        " gelten die Konditionen für Folgeverfügungen. Folgeverfügungen: Für andere und künftige Verfügungen " \
        "(Folgeverfügungen) beträgt der veränderliche Sollzinssatz (jährlich) 9,47 % (falls Sie bereits einen " \
        "Kreditrahmen bei uns haben, kann der tatsächliche veränderliche Sollzinssatz abweichen). \n" \
        "Für Folgeverfügungen müssen Sie monatliche Teilzahlungen in der von Ihnen gewählten Höhe, mind. aber " \
        "2,5% der jeweils höchsten, auf volle 100 € gerundeten Sollsaldos der Folgeverfügungen (mind. 9 €) leisten" \
        ". Zahlungen für Folgeverfügungen werden erst auf verzinste Folgeverfügungen angerechnet, " \
        "bei unterschiedlichen Zinssätzen zuerst auf die höher verzinsten."
    ))


def test_map_loan_offer():
    # GIVEN
    loan = {
        "loanType": "MCD",
        "loanDescription": ProductDescription.CONSORS_1PS,
        "insuranceTypes": ["DEATH_DISABILITY_UNEMPLOYMENT"],
        "creditAmount": 10000,
        "duration": 84,
        "monthlyRate": 145.27,
        "effectiveRate": 5.99,
        "nominalRate": 5.83,
        "totalPayment": 12202.68
    }

    result: LoanOfferModel = map_loan_offer(loan)

    assert_that(result, equal_to(
        LoanOfferModel(
            consorsfinanz=FinanzierungsvorschlagDetails(
                produktId="MCD",
                produkttyp=Produkttyp.MCD,
                produktbeschreibung=map_product_description(),
                produktbezeichnung="Consors Finanz 1PS",
                versicherteRisiken=["DEATH_DISABILITY_UNEMPLOYMENT"],
                nettokreditbetrag=10000,
                laufzeitInMonaten=84,
                monatlicheRate=145.27,
                effektivzins=5.99,
                sollzins=5.83,
                gesamtkreditbetrag=12202.68,
                pAngV=map_price_indication_ordinance(loan),
                kreditDetails=map_credit_details()
            )
        )))

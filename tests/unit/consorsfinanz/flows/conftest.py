import pytest

from app.consorsfinanz.flows.product.models.product_identifier_model import ProductDescription


@pytest.fixture
def response_loan_offer():
    return {
        "financialCalculations": {
            "defaultIndex": 60,
            "financialCalculation": [
                {
                    "index": 439.0,
                    "creditAmount": 10000.0,
                    "duration": 12,
                    "monthlyRate": 859.89,
                    "effectiveRate": 5.99,
                    "nominalRate": 5.83,
                    "totalInterestAmount": 318.68,
                    "totalPayment": 10318.68
                },
                {
                    "index": 500.0,
                    "creditAmount": 500,
                    "duration": 6,
                    "monthlyRate": 86.1,
                    "effectiveRate": 11.9,
                    "nominalRate": 11.29,
                    "totalInterestAmount": 16.6,
                    "totalPayment": 516.6
                }
            ],
            "insuranceTypes": [
                "DEATH_DISABILITY_UNEMPLOYMENT"
            ],
        },
        "loanType": "ICCL",
        "loanDescription": ProductDescription.CONSORS_1PS
    }


PANGV = "2/3 aller angenommenen Kunden erhalten: bei 20.000€ Kreditsumme 4,99% eff. Jahreszins, 4,88% fester " \
        "Sollzins p.a., Gesamtbetrag 23.110,62€, mtl. Rate 320,98 €, Kreditgeber ist die BNP Paribas S.A. " \
        "Niederlassung Deutschland, Standort München: Schwanthalerstr. 31, 80336 München"

KREDIT_DETAILS = {
    "produktinformationen": [
        {
            "key": "PRODUKTINFORMATIONEN_SICHERHEIT",
            "description": "Absicherung des Darlehensnehmers möglich"
        },
        {
            "key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
            "description": "Sondertilgungen sind jederzeit möglich (gesetzliche Regelung (1% oder "
                           "Restlaufzeit<1 Jahr dann 0,5%))"
        },
        {
            "key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
            "description": "Vorzeitige Ablösung des Kredites ist jederzeit möglich (50% der "
                           "Restschuld kostenfrei, sonst 1% Vorfälligkeitsentschädigung, Laufzeit "
                           ">1 Jahr 0,5%)"
        },
        {
            "key": "PRODUKTINFORMATIONEN_FLEXIBILITAET",
            "description": "Ratenpausen sind möglich"
        },
        {
            "key": "PRODUKTINFORMATIONEN_KUNDENFREUNDLICHKEIT",
            "description": "Bis 3.000 € Kreditsumme Rahmenkredit der Consors Finanz, mit "
                           "Möglichkeit (bei vorausgesetzter Bonität) jederzeitiger Aufstockung"
        }
    ],
    "annahmerichtlinien": [
        "Mindestalter 18 Jahre",
        "Kein Höchstalter, Rückzahlung muss aber bis zum 84. Lebensjahr erfolgt sein",
        "Probezeit muss beendet sein",
        "Maximale Kreditsumme bis 50.000 €",
        "Laufzeiten bis 120 Monate möglich"
    ]
}

import json

import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from hamcrest import assert_that, equal_to
from mockito import when
from starlette.responses import Response

from app.consorsfinanz.consors_api import SecretsManager
from app.main import app as main_app
from tests.integration.conftest import credit_submission_request_body1

client = TestClient(main_app)


# TODO: MOCK ALL CONSORS RESPONSES AND MOVE THIS FILE TO UNITTESTS!


def test_health():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("data", [
    {
        "url": "/productlimits",
        "query": "?leadquelle=TEST&data_context=TEST",
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps([
            {
                "minDuration": 6,
                "maxDuration": 120,
                "minCreditLimit": 500.0,
                "maxCreditLimit": 50000.0
            },
            {
                "minDuration": 6,
                "maxDuration": 36,
                "minCreditLimit": 500.0,
                "maxCreditLimit": 10000.0
            }
        ]), status_code=200)
    },
    {
        "url": "/productlimits",
        "query": "",
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps([
            {
                "minDuration": 6,
                "maxDuration": 120,
                "minCreditLimit": 500.0,
                "maxCreditLimit": 50000.0
            },
            {
                "minDuration": 6,
                "maxDuration": 36,
                "minCreditLimit": 500.0,
                "maxCreditLimit": 10000.0
            }
        ]), status_code=200)
    }
])
def test_get_product_limits(data):
    # GIVEN
    when(SecretsManager).get_value("client_secret").thenReturn("Pqfsr>8760")
    when(SecretsManager).get_value("client_id").thenReturn("direct")
    when(SecretsManager).get_value("x_api_key").thenReturn("1d2265c3-f18f-4f3d-a6da-2af0cbc2a0d1")
    when(SecretsManager).get_value("username").thenReturn("1PSD_DrKlein")

    response = client.get(url=data["url"] + data["query"],
                          headers=data["headers"])

    assert_that(json.loads(response.content), equal_to(json.loads(data["response"].body)))


@pytest.mark.parametrize("data", [
    {
        "url": "/financialcalculations",
        "query": "?credit_amount=10000&duration=12&leadquelle=TEST&data_context=TEST",
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps(
            {
                "consorsfinanz": {
                    "produktId": "ICCL",
                    "produktDescription": "Finanzierung Ihrer Sofortauszahlung (Ratenplan-Verfügung) über den "
                                          "Kreditrahmen, den Sie wiederholt in Anspruch nehmen können. "
                                          "Nettodarlehensbetrag bonitätsabhängig bis 15.000 €. 9,90 % effektiver "
                                          "Jahreszinssatz. Vertragslaufzeit auf unbestimmte Zeit. \n"
                                          "Ratenplan-Verfügung: Gebundener Sollzinssatz von 11,28 % (jährlich) gilt "
                                          "nur für die ersten 18 Monate ab Vertragsschluss (Zinsbindungsdauer); Sie "
                                          "müssen monatliche Teilzahlungen in der von Ihnen gewählten Höhe leisten. "
                                          "Führen Sie Ihre Ratenplan-Verfügung nicht innerhalb der Zinsbindungsdauer "
                                          "zurück, gelten die Konditionen für Folgeverfügungen. Folgeverfügungen: Für "
                                          "andere und künftige Verfügungen (Folgeverfügungen) beträgt der veränderliche"
                                          " Sollzinssatz (jährlich) 9,47 % (falls Sie bereits einen Kreditrahmen bei "
                                          "uns haben, kann der tatsächliche veränderliche Sollzinssatz abweichen). \n"
                                          "Für Folgeverfügungen müssen Sie monatliche Teilzahlungen in der von Ihnen "
                                          "gewählten Höhe, mind. aber 2,5% der jeweils höchsten, auf volle 100 € "
                                          "gerundeten Sollsaldos der Folgeverfügungen (mind. 9 €) leisten. Zahlungen "
                                          "für Folgeverfügungen werden erst auf verzinste Folgeverfügungen angerechnet,"
                                          " bei unterschiedlichen Zinssätzen zuerst auf die höher verzinsten.",
                    "versicherteRisiken": [
                        "TOD",
                        "ARBEITSUNFAEHIGKEIT",
                        "ARBEITSLOSIGKEIT"
                    ],
                    "nettokreditbetrag": 10000,
                    "laufzeitInMonaten": 12,
                    "monatlicheRate": 859.89,
                    "effektivzins": 5.99,
                    "sollzins": 5.83,
                    "gesamtkreditbetrag": 10318.68,
                    "pAngV": "2/3 aller angenommenen Kunden erhalten: Sollzinssatz: 5.83 % p.a. fest (gebunden) für "
                             "die gesamte Laufzeit, effektiver Jahreszins: 5.99 %, Nettokreditbetrag: 10000.0 Euro, "
                             "Vertragslaufzeit: 12 Monate, Gesamtbetrag: 10318.68 Euro, Monatliche Rate: 859.89 Euro. "
                             "Vermittelt durch den Kreditgeber BNP Paribas S.A. Niederlassung Deutschland, "
                             "Schwanthalerstr. 31, 80336 München. Entspricht dem repr. Beispiel nach §6a PAngV."
                }
            }
        ), status_code=200)
    },
    {
        "url": "/financialcalculations",
        "query": "?credit_amount=3000&duration=12&leadquelle=TEST&data_context=TEST",
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps(
            {
                "consorsfinanz": {
                    "produktId": "MCD",
                    "produktDescription": "Finanzierung Ihrer Sofortauszahlung (Ratenplan-Verfügung) über den "
                                          "Kreditrahmen, den Sie wiederholt in Anspruch nehmen können. "
                                          "Nettodarlehensbetrag bonitätsabhängig bis 15.000 €. 9,90 % effektiver "
                                          "Jahreszinssatz. Vertragslaufzeit auf unbestimmte Zeit. \n"
                                          "Ratenplan-Verfügung: Gebundener Sollzinssatz von 11,28 % (jährlich) gilt "
                                          "nur für die ersten 18 Monate ab Vertragsschluss (Zinsbindungsdauer); Sie "
                                          "müssen monatliche Teilzahlungen in der von Ihnen gewählten Höhe leisten. "
                                          "Führen Sie Ihre Ratenplan-Verfügung nicht innerhalb der Zinsbindungsdauer "
                                          "zurück, gelten die Konditionen für Folgeverfügungen. Folgeverfügungen: Für "
                                          "andere und künftige Verfügungen (Folgeverfügungen) beträgt der veränderliche"
                                          " Sollzinssatz (jährlich) 9,47 % (falls Sie bereits einen Kreditrahmen bei "
                                          "uns haben, kann der tatsächliche veränderliche Sollzinssatz abweichen). \n"
                                          "Für Folgeverfügungen müssen Sie monatliche Teilzahlungen in der von Ihnen "
                                          "gewählten Höhe, mind. aber 2,5% der jeweils höchsten, auf volle 100 € "
                                          "gerundeten Sollsaldos der Folgeverfügungen (mind. 9 €) leisten. Zahlungen "
                                          "für Folgeverfügungen werden erst auf verzinste Folgeverfügungen angerechnet,"
                                          " bei unterschiedlichen Zinssätzen zuerst auf die höher verzinsten.",
                    "versicherteRisiken": [
                        "TOD",
                        "ARBEITSUNFAEHIGKEIT",
                        "ARBEITSLOSIGKEIT"
                    ],
                    "nettokreditbetrag": 3000,
                    "laufzeitInMonaten": 12,
                    "monatlicheRate": 265.55,
                    "effektivzins": 11.9,
                    "sollzins": 11.29,
                    "gesamtkreditbetrag": 3186.6,
                    "pAngV": "2/3 aller angenommenen Kunden erhalten: Sollzinssatz: 11.29 % p.a. fest (gebunden) für "
                             "die gesamte Laufzeit, effektiver Jahreszins: 11.9 %, Nettokreditbetrag: 3000 Euro, "
                             "Vertragslaufzeit: 12 Monate, Gesamtbetrag: 3186.6 Euro, Monatliche Rate: 265.55 Euro. "
                             "Vermittelt durch den Kreditgeber BNP Paribas S.A. Niederlassung Deutschland, "
                             "Schwanthalerstr. 31, 80336 München. Entspricht dem repr. Beispiel nach §6a PAngV."
                }
            }
        ), status_code=200)
    },
    {
        "url": "/financialcalculations",
        "query": "?credit_amount=3000&duration=84&leadquelle=TEST&data_context=TEST",
        "headers": {"requestid": "foo"},
        "response": Response(content="{}", status_code=200)
    }
])
def test_get_financial_calculations(data):
    # GIVEN
    when(SecretsManager).get_value("client_secret").thenReturn("Pqfsr>8760")
    when(SecretsManager).get_value("client_id").thenReturn("direct")
    when(SecretsManager).get_value("x_api_key").thenReturn("1d2265c3-f18f-4f3d-a6da-2af0cbc2a0d1")
    when(SecretsManager).get_value("username").thenReturn("1PSD_DrKlein")
    when(SecretsManager).get_value("short_link_mcd").thenReturn("mcd_2595593")
    when(SecretsManager).get_value("short_link_iccl").thenReturn("iccl_2595593")
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    response = client.get(url=data["url"] + data["query"],
                          headers=data["headers"])

    assert_that(json.loads(response.content), equal_to(json.loads(data["response"].body)))


@pytest.mark.parametrize("data", [
    {
        "url": "/financialcalculation",
        "query": "?leadquelle=DRKLEINRK_POSTBANK_ONLINE_DIGITALER_ABSCHLUSS_TEST_API&data_context=TEST",
        "body": credit_submission_request_body1,
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps([
            {
                "consorsfinanz": {
                    "produktId": "ICCL",
                    "versicherteRisiken": [
                        "TOD",
                        "ARBEITSUNFAEHIGKEIT",
                        "ARBEITSLOSIGKEIT"
                    ],
                    "nettokreditbetrag": 10000,
                    "laufzeitInMonaten": 12,
                    "monatlicheRate": 859.89,
                    "effektivzins": 5.99,
                    "sollzins": 5.83,
                    "gesamtkreditbetrag": 10318.68,
                    "pAngV": "2/3 aller angenommenen Kunden erhalten: Sollzinssatz: 5.83 % p.a. fest (gebunden) für "
                             "die gesamte Laufzeit, effektiver Jahreszins: 5.99 %, Nettokreditbetrag: 10000.0 Euro, "
                             "Vertragslaufzeit: 12 Monate, Gesamtbetrag: 10318.68 Euro, Monatliche Rate: 318.68 Euro. "
                             "Vermittelt durch den Kreditgeber BNP Paribas S.A. Niederlassung Deutschland, "
                             "Schwanthalerstr. 31, 80336 München. Entspricht dem repr. Beispiel nach §6a PAngV."
                }
            }
        ]), status_code=200)
    },
    {
        "url": "/financialcalculation",
        "query": "?leadquelle=DRKLEINRK_POSTBANK_ONLINE_DIGITALER_ABSCHLUSS_TEST_API&data_context=TEST",
        "body": credit_submission_request_body1,
        "headers": {"requestid": "foo"},
        "response": Response(content=json.dumps([
            {
                "consorsfinanz": {
                    "produktId": "MCD",
                    "versicherteRisiken": [
                        "TOD",
                        "ARBEITSUNFAEHIGKEIT",
                        "ARBEITSLOSIGKEIT"
                    ],
                    "nettokreditbetrag": 3000,
                    "laufzeitInMonaten": 12,
                    "monatlicheRate": 303.45,
                    "effektivzins": 5.99,
                    "sollzins": 5.83,
                    "gesamtkreditbetrag": 10924.2,
                    "pAngV": "2/3 aller angenommenen Kunden erhalten: Sollzinssatz: 5.83 % p.a. fest (gebunden) für "
                             "die gesamte Laufzeit, effektiver Jahreszins: 5.99 %, Nettokreditbetrag: 10000.0 Euro, "
                             "Vertragslaufzeit: 36 Monate, Gesamtbetrag: 10924.2 Euro, Monatliche Rate: 303.45 Euro. "
                             "Vermittelt durch den Kreditgeber BNP Paribas S.A. Niederlassung Deutschland, "
                             "Schwanthalerstr. 31, 80336 München. Entspricht dem repr. Beispiel nach §6a PAngV."
                }
            }
        ]), status_code=200)
    }
])
def test_credit_submission(data):
    # GIVEN
    when(SecretsManager).get_value("client_secret").thenReturn("Pqfsr>8760")
    when(SecretsManager).get_value("client_id").thenReturn("direct")
    when(SecretsManager).get_value("x_api_key").thenReturn("1d2265c3-f18f-4f3d-a6da-2af0cbc2a0d1")
    when(SecretsManager).get_value("username").thenReturn("1PSD_DrKlein")
    when(SecretsManager).get_value("short_link_mcd").thenReturn("mcd_2595593")
    when(SecretsManager).get_value("short_link_iccl").thenReturn("iccl_2595593")

    response = client.post(url=data["url"] + data["query"], json=data["body"],
                           headers=data["headers"])

    assert_that(json.loads(response.content), equal_to(json.loads(data["response"].body)))

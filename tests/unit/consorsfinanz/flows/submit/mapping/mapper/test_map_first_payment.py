from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Antragsdaten, RatenzahlungsterminEnum
from app.consorsfinanz.flows.submit.mapping.mapper.map_first_payment import map_first_payment


def test_map_first_payment_monatsende():
    # GIVEN
    antragsdaten = Antragsdaten(ratenzahlungstermin=RatenzahlungsterminEnum.MONATSENDE)

    # WHEN
    response = map_first_payment(antragsdaten)

    # THEN
    assert_that(response, equal_to(1))


def test_map_first_payment_monatsmitte():
    # GIVEN
    antragsdaten = Antragsdaten(ratenzahlungstermin=RatenzahlungsterminEnum.MONATSMITTE)

    # WHEN
    response = map_first_payment(antragsdaten)

    # THEN
    assert_that(response, equal_to(15))


def test_map_first_payment_none_ratenzahlungstermin():
    # GIVEN
    antragsdaten = Antragsdaten(ratenzahlungstermin=None)

    # WHEN
    response = map_first_payment(antragsdaten)

    # THEN
    assert_that(response, equal_to(1))


def test_map_first_payment_none_antragsdaten():
    # WHEN
    response = map_first_payment(None)

    # THEN
    assert_that(response, equal_to(1))

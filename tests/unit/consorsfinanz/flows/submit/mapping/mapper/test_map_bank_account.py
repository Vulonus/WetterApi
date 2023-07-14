from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.request_loan_submit_model import BankAccount
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom, Stammdaten
from app.consorsfinanz.flows.submit.mapping.mapper.map_bank_account import map_bank_account


def test_map_bank_account():
    # GIVEN
    partner = PartnerCustom(
        custom=[
            Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-01-01"),
        ]
    )

    result: BankAccount = map_bank_account(Stammdaten(iban="DE 8937 04004 40532013000"), partner)

    # THEN
    assert_that(result.iban, equal_to("DE89370400440532013000"))
    assert_that(result.accountSince, equal_to("2014-01"))


def test_map_bank_account_none():
    result = map_bank_account(None, None)

    # THEN
    assert_that(result, equal_to(None))


def test_map_bank_account_custom():
    # GIVEN
    partner = PartnerCustom(custom=[])

    result = map_bank_account(Stammdaten(), partner)

    # THEN
    assert_that(result, equal_to(None))

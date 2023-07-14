import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.offer.loan_dispatch_offer_flow import filter_and_map_response
from app.consorsfinanz.flows.offer.mapping.loan_offer_mapper import map_product_description
from app.consorsfinanz.flows.offer.models.loan_offer_model import LoanOfferModel, FinanzierungsvorschlagDetails, \
    Produkttyp
from app.consorsfinanz.flows.offer.models.request_loan_offer_model import RequestLoanOfferModel
from tests.unit.consorsfinanz.flows.conftest import PANGV, KREDIT_DETAILS


@pytest.mark.asyncio
@pytest.mark.parametrize("data", [
    {
        "request_loan_offer_model": RequestLoanOfferModel(creditAmount=10000, duration=12),
        "response": LoanOfferModel(
            consorsfinanz=FinanzierungsvorschlagDetails.parse_obj({
                "produktId": "ICCL",
                "produktbeschreibung": map_product_description(),
                "produkttyp": Produkttyp.ICCL,
                "produktbezeichnung": "Consors Finanz 1PS",
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
                "pAngV": PANGV,
                "kreditDetails": KREDIT_DETAILS
            })
        )
    },
    {
        "request_loan_offer_model": RequestLoanOfferModel(creditAmount=500, duration=12),
        "response": {}
    }
])
async def test_filter_and_map_response(data, response_loan_offer):
    # WHEN
    response = await filter_and_map_response(response_loan_offer, data["request_loan_offer_model"])
    # THEN
    assert_that(response, equal_to(data["response"]))

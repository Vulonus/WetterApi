import httpx
import pytest
from hamcrest import assert_that, equal_to
from mockito import mock, when, verify

from app.consorsfinanz.application.secrets import Secrets
from app.consorsfinanz.consors_api_exception import ConsorsApiException
from app.consorsfinanz.flows.offer.api_financial_calculations import get_financial_calculations_for_loan
from app.common.config import Config
from app.main import startup_cache


@pytest.fixture
def loan():
    return {
        "financialCalculations": {
            "defaultIndex": 18,
            "financialCalculation": [{
                "index": 0,
                "creditAmount": 500,
                "duration": 6,
                "monthlyRate": 86.1,
                "effectiveRate": 11.9,
                "nominalRate": 11.29,
                "totalInterestAmount": 16.6,
                "totalPayment": 516.6}],
            "insuranceTypes": ["DEATH_DISABILITY_UNEMPLOYMENT"],
            "durationStepping": [6, 12],
            "amountStepping": [500, 600],
            "_links": [{
                "name": "Insurance Calculation for Financial Option Revolving",
                "href": "/subscription/mcd_2595593/revolving/insurance?version=6.2",
                "method": "POST",
                "rel": "_insurancecalculationsrevolving"}
            ]
        },
        "loanType": "ICCL"
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("data", [
    {"path": "revolving", "type": "MCD"},
    {"path": "ecommerce", "type": "ICCL"}
])
async def test_get_financial_calculations_for_loan_success(data, loan):
    # GIVEN
    client = mock()
    client_response = mock()
    client_response.content = loan
    client_response.status_code = 200

    secrets: Secrets = Secrets(
        x_api_key="asdad_dd"
    )

    async def response():
        return client_response

    when(client).get(any, any).thenReturn(response())
    await startup_cache()

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/ratanet-api/cfg", version="6.4")
    response = await get_financial_calculations_for_loan(
        client=client,
        config=config,
        token={"token": "Bearer eyJhbGciOiX1J"},
        short_link="iccl_123",
        loan_type=data["type"],
        secrets=secrets
    )

    # THEN
    assert_that(response, equal_to(loan))
    verify(client).get(
        f'http://foo/1/ratanet-api/cfg/partner/iccl_123/financialcalculations/{data["path"]}?version=6.4',
        {"x-api-key": "asdad_dd", "Authorization": "Bearer eyJhbGciOiX1J"})


@pytest.mark.asyncio
async def test_get_financial_calculations_for_loan_raises_exception():
    # GIVEN
    client = mock()
    secrets: Secrets = Secrets(
        x_api_key="asdad_dd"
    )

    request = mock()
    request.url = "http://foo/bar"
    error = httpx.RequestError("foo", request=request)

    when(client).get(any, any).thenRaise(error)
    await startup_cache()

    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/ratanet-api/cfg", version="6.4")

    try:
        await get_financial_calculations_for_loan(
            client=client,
            config=config,
            token={"token": "Bearer eyJhbGciOiX1J"},
            short_link="iccl_123",
            loan_type="MCD",
            secrets=secrets
        )
    except ConsorsApiException as error:
        assert error.message == "HTTP Exception for http://foo/bar"

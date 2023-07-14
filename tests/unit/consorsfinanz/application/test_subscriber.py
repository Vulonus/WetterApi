import httpx
import pytest
from hamcrest import equal_to, assert_that
from mockito import mock, when, any, verify

from app.consorsfinanz.application.secrets import Secrets
from app.consorsfinanz.consors_api_exception import ConsorsApiException
from app.consorsfinanz.flows.submit.api_subscriber import start_recognize_subscriber
from app.common.config import Config
from app.consorsfinanz.flows.submit.models.customer_recognition_model import CustomerRecognitionModel, \
    SubscriptionStatusEnum


@pytest.fixture
def customer_recognition_model():
    return CustomerRecognitionModel(
        subscriptionStatus=SubscriptionStatusEnum.INCOMPLETE,
        subscriptionIdentifier="12345678",
        customerWithActiveMasterCard=True,
        customerContactedByPhoneAndEmailForPromotions=True,
        cardLimit=1000,
        bundleCardLimit=1000
    )


@pytest.mark.asyncio
async def test_start_recognize_subscriber_success(customer_recognition_model):
    # GIVEN
    client = mock()
    client_response = mock()

    client_response.content = customer_recognition_model.json()
    client_response.status_code = 200

    async def response():
        return client_response

    when(client).put(url=any, headers=any).thenReturn(response())

    secrets: Secrets = Secrets(
        x_api_key="asdad_dd",
        client_id="1234_11",
        client_secret="_S_",
        username="hans",
    )

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/common-services/cfg", version="6.4")
    response = await start_recognize_subscriber(
        client=client,
        config=config,
        token={"token": "Bearer eyJhbGciOiX1J"},
        short_link="321",
        subscription_identifier="111",
        secrets=secrets
    )

    # THEN
    assert_that(response, equal_to(customer_recognition_model))
    verify(client).put(
        url="http://foo/1/common-services/cfg/subscriber/321/111/recognizesubscriber?version=6.4",
        headers={"x-api-key": "asdad_dd", "Authorization": "Bearer eyJhbGciOiX1J"})


@pytest.mark.asyncio
async def test_start_recognize_subscriber_exception():
    # GIVEN
    client = mock()

    request = mock()
    request.url = "http://foo/bar"

    error = httpx.RequestError("foo", request=request)
    when(client).put(url=any, headers=any).thenRaise(error)

    secrets: Secrets = Secrets(
        x_api_key="asdad_dd",
        client_id="1234_11",
        client_secret="_S_",
        username="hans",
    )

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/common-services/cfg", version="6.4")

    try:
        await start_recognize_subscriber(
            client=client,
            config=config,
            token={"token": "Bearer eyJhbGciOiX1J"},
            short_link="321",
            subscription_identifier="111",
            secrets=secrets
        )
    except ConsorsApiException as error:
        assert error.message == "HTTP Exception for http://foo/bar"

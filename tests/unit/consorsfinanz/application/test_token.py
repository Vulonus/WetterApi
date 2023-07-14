import httpx
import pytest
from hamcrest import equal_to, assert_that
from mockito import mock, when, any, verify

from app.consorsfinanz.application.secrets import Secrets
from app.consorsfinanz.consors_api_exception import ConsorsApiException
from app.consorsfinanz.flows.api_token import get_token
from app.common.config import Config


@pytest.mark.asyncio
async def test_get_token_success():
    # GIVEN
    client = mock()
    client_response = mock()
    when(client_response).json().thenReturn({"token": "Bearer eyJhbGciOiX1J"})
    client_response.status_code = 201

    async def response():
        return client_response

    when(client).post(url=any, data=any, headers=any).thenReturn(response())
    secrets: Secrets = Secrets(
        x_api_key="asdad_dd",
        client_id="1234_11",
        client_secret="_S_",
        username="hans",
    )

    # WHEN
    config = Config(host="http://foo", tokenRootContext="/1/common-services/cfg", loanRootContext="foo", version="6.4")
    response = await get_token(
        client=client,
        config=config,
        secrets=secrets
    )

    # THEN
    assert_that(response, equal_to({"token": "Bearer eyJhbGciOiX1J"}))
    verify(client).post(
        url="http://foo/1/common-services/cfg/token/1234_11",
        data={"username": "hans", "password": "_S_"},
        headers={"x-api-key": "asdad_dd"})


@pytest.mark.asyncio
async def test_get_token_exception():
    # GIVEN
    client = mock()

    request = mock()
    request.url = "http://foo/bar"

    error = httpx.RequestError("foo", request=request)
    when(client).post(url=any, data=any, headers=any).thenRaise(error)

    secrets: Secrets = Secrets(
        x_api_key="asdad_dd",
        client_id="1234_11",
        client_secret="_S_",
        username="hans",
    )
    # WHEN
    config = Config(host="http://foo", tokenRootContext="/1/common-services/cfg", loanRootContext="foo",
                    version="6.4")

    try:
        await get_token(
            client=client,
            config=config,
            secrets=secrets
        )
    except ConsorsApiException as error:
        assert error.message == "Es ist ein technischer Fehler aufgetreten. " \
                                "Bitte kontaktieren Sie dev@drklein.de für Support."

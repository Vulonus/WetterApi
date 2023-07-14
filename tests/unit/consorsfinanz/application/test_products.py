import pytest
from hamcrest import equal_to, assert_that
from mockito import mock, when, any, verify

from app.common.config import Config
from app.consorsfinanz.application.secrets import Secrets
from app.consorsfinanz.flows.product.api_products import get_available_products, get_product_identifier, \
    determine_product_id
from app.consorsfinanz.flows.product.models.product_identifier_model import ProductIdentifierModel, ProductDescription
from app.consorsfinanz.flows.product.models.product_model import ProductModel, FinancialConditionConfigurations, \
    ProductInfoDetails


@pytest.mark.parametrize("data", [
    {"credit_amount": 500, "duration": 12, "result": "MCD"},
    {"credit_amount": 500, "duration": 60, "result": "MCD"},
    {"credit_amount": 3000, "duration": 12, "result": "MCD"},
    {"credit_amount": 3000, "duration": 60, "result": "MCD"},
    {"credit_amount": 3001, "duration": 12, "result": "ICCL"},
    {"credit_amount": 3001, "duration": 120, "result": "ICCL"},
    {"credit_amount": 50000, "duration": 12, "result": "ICCL"},
    {"credit_amount": 50000, "duration": 120, "result": "ICCL"},
    {"credit_amount": 60000, "duration": 12, "result": None}
])
def test_determine_product_id_depends_on_credit_amount_and_duration(data):
    # GIVEN
    # WHEN
    result = determine_product_id(
        credit_amount=data["credit_amount"],
        duration=data["duration"]
    )

    # THEN
    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"product_id": "MCD",
     "expected": ProductIdentifierModel(id="MCD", short_link="321", description=ProductDescription.CONSORS_1PS)},
    {"product_id": "ICCL",
     "expected": ProductIdentifierModel(id="ICCL", short_link="123", description=ProductDescription.CONSORS_1PS)},
    {"product_id": "ABC", "expected": None}
])
def test_get_product_identifier(data):
    # GIVEN
    secrets: Secrets = Secrets(
        short_links={"MCD": "321", "ICCL": "123"}
    )
    # WHEN
    result: ProductIdentifierModel = get_product_identifier(product_id=data["product_id"], secrets=secrets)

    # THEN
    assert_that(result, equal_to(data["expected"]))


@pytest.mark.asyncio
async def test_get_available_products_success():
    # GIVEN
    client = mock()
    client_response = mock()
    secrets: Secrets = Secrets(
        client_id="1234_11",
        x_api_key="asdad_dd"
    )
    product_model = ProductModel(products={
        "1999_810": ProductInfoDetails(
            code="810",
            description="Persönlicher Bedarf",
            insuranceTypes=["DEATH_DISABILITY_UNEMPLOYMENT"],
            insuranceCondition={
                "insuranceAddOn": {
                    "DEATH_DISABILITY_UNEMPLOYMENT": []}
            },
            financialConditionConfigurations=[
                FinancialConditionConfigurations(
                    interestRate=5.99,
                    duration={"minimum": 6,
                              "maximum": 120},
                    creditLimit={
                        "minimum": 500,
                        "maximum": 50000})],
            type="CL",
            subType="CLASSIC"
        )
    })

    client_response.content = product_model.json()

    async def response():
        return client_response

    when(client).get(any, any).thenReturn(response())

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/common-services/cfg", version="6.4")
    response = await get_available_products(
        client=client,
        config=config,
        token={"token": "Bearer eyJhbGciOiX1J"},
        secrets=secrets
    )

    # THEN
    assert_that(response, equal_to(product_model))
    verify(client).get("http://foo/1/common-services/cfg/partner/1234_11/products?version=6.4",
                       {"x-api-key": "asdad_dd", "Authorization": "Bearer eyJhbGciOiX1J"})

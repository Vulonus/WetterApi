import json

import pytest
from hamcrest import equal_to, assert_that
from mockito import mock, when, any, verify

from app.consorsfinanz.application.secrets import Secrets
from app.consorsfinanz.flows.submit.models.request_loan_submit_model import Subscriber, Income, Expense, \
    EmploymentDetails, ContactAddress, Consents, EmployerAddress, BankAccount, RequestLoanSubmitModel, \
    Subscription, ProfessionEnum, KycPurposeOfLoanEnum, GenderEnum, HousingSituationEnum, FamilySituationEnum
from app.consorsfinanz.flows.submit.api_validation import get_validation_rules, validate_subscription_payload
from app.common.config import Config
from app.consorsfinanz.flows.submit.models.validate_subscription_data_model import ValidateSubscriptionPayloadModel
from app.common.util import exclude_optional_json


@pytest.mark.asyncio
async def test_get_validation_rules_success():
    # GIVEN
    client = mock()
    client_response = mock()
    client_response.content = json.dumps({})

    secrets: Secrets = Secrets(x_api_key="asdad_dd")

    async def response():
        return client_response

    when(client).get(any, any).thenReturn(response())

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/common-services/cfg", version="6.4")
    response = await get_validation_rules(
        client=client,
        config=config,
        token={"token": "Bearer eyJhbGciOiX1J"},
        short_link="mcd_12345",
        secrets=secrets
    )

    # THEN
    assert_that(response.content, equal_to("{}"))
    verify(client).get(
        "http://foo/1/common-services/cfg/partner/mcd_12345/validationrules?version=6.4",
        {"x-api-key": "asdad_dd", "Authorization": "Bearer eyJhbGciOiX1J"})


@pytest.mark.asyncio
async def test_validate_subscription_payload_success():
    # GIVEN
    client = mock()
    client_response = mock()
    request_loan_application_model = RequestLoanSubmitModel(
        subscription=Subscription(
            subscribers=[Subscriber(
                rolePlaying="MAIN",
                gender=GenderEnum.MALE,
                firstName="Foo",
                lastName="Bar",
                birthName="Foo Bar",
                dateOfBirth="1980-04-20T13:14:07.712+02:00",
                countryOfBirth="DE",
                nationality="DE",
                housingSituation=HousingSituationEnum.BY_FAMILY,
                familySituation=FamilySituationEnum.MARRIED,
                numberOfChildren=1,
                income=Income(
                    netIncome=1500,
                    rentIncome=0.0,
                    otherIncome=0.0
                ),
                expense=Expense(
                    warmRent=849
                ),
                employmentDetails=EmploymentDetails(
                    profession=ProfessionEnum.SELF_EMPLOYED,
                    professionBeginDate="2014-10-12",
                    employerAddress=EmployerAddress(
                        employerName="Siemens GmbH",
                        employerStreet="Hansastr. 11",
                        employerZipcode="80339",
                        employerCity="Muenchen"
                    )
                ),
                contactAddress=ContactAddress(
                    email="jean-marc.nadal@consorsfinanz.de",
                    street="Fraunbergstr 18",
                    zipcode="81379",
                    city="Bonn",
                    validFrom="2014-10-20T13:14:07.712+02:00",
                    telephoneMobile="089832432432"
                ),
                consents=Consents(
                    isSchufaCallAllowed=True
                ))
            ],
            bankAccount=BankAccount(
                iban="DE89370400440532013000",
                accountSince="2014-10-20T13:14:07.712+02:00"
            ),
            kycPurposeOfLoan=KycPurposeOfLoanEnum.ELK
        ))

    validate_subscription_payload_model = ValidateSubscriptionPayloadModel(
        subscriptionidentifier="foo",
        errors={},
        warning={}
    )

    client_response.content = validate_subscription_payload_model.json()
    client_response.status_code = 201

    secrets: Secrets = Secrets(x_api_key="asdad_dd")

    async def response():
        return client_response

    when(client).post(url=any, json=any, headers=any).thenReturn(response())

    # WHEN
    config = Config(host="http://foo", tokenRootContext="foo", loanRootContext="/1/common-services/cfg", version="6.4")
    response = await validate_subscription_payload(
        client=client,
        config=config,
        token={"token": "Bearer eyJhbGciOiX1J"},
        short_link="mcd_12345",
        model=request_loan_application_model,
        secrets=secrets
    )

    # THEN
    assert_that(response, equal_to(validate_subscription_payload_model))
    verify(client).post(
        url="http://foo/1/common-services/cfg/subscription/mcd_12345?version=6.4",
        json=json.loads(exclude_optional_json(request_loan_application_model.subscription)),
        headers={"x-api-key": "asdad_dd", "Authorization": "Bearer eyJhbGciOiX1J"})

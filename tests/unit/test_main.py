import json
import unittest
from http.client import OK, BAD_REQUEST, UNPROCESSABLE_ENTITY, NOT_FOUND, INTERNAL_SERVER_ERROR

from hamcrest import equal_to, assert_that
from mockito import unstub, when, mock, any, verify
from parameterized import parameterized
from starlette.testclient import TestClient

from app.common.data_context import DataContext
from app.common.errors.business_error import BusinessError, BusinessDataError, BusinessDataEnum
from app.common.errors.field_data_error import FieldDataError, DataError
from app.config import config
from app.consorsfinanz import consors_api
from app.consorsfinanz.consors_api import ConsorsApi
from app.consorsfinanz.consors_api_exception import ConsorsApiException
from app.consorsfinanz.flows.offer.loan_dispatch_offer_flow_exception import LoanDispatchOfferFlowException
from app.consorsfinanz.flows.offer.models.loan_offer_model import LoanOfferModel
from app.consorsfinanz.flows.offer.models.request_loan_offer_model import RequestLoanOfferModel
from app.consorsfinanz.flows.submit.loan_submission_flow_exception import LoanSubmissionFlowException
from app.consorsfinanz.flows.submit.mapping.required_field_missing_error import RequiredFieldMissingError
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages
from tests.unit.test_helper import message_with_detail_text, create_async_mock_response, create_url_with_query, \
    PRODUKTGRENZEN_RESPONSE, create_consors_api_financial_calculations, create_mocked_dispatch_offer_request, \
    create_request_credit_submission_model, create_default_vorgang_marktplatz_model, create_response_loan_submit_model


# pylint: disable=too-many-public-methods
class MainTestCase(unittest.TestCase):
    """
    Tests the main application under app/main.py
    """

    def setUp(self) -> None:
        # pylint: disable=import-outside-toplevel
        from app.main import app as main_app
        self.client = TestClient(main_app)

    def tearDown(self) -> None:
        unstub()

    def test_health__default_get__return_ok(self):
        # GIVEN

        # WHEN
        response = self.client.get("/")

        # THEN
        assert_that(response.status_code, equal_to(OK))

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_prefill_cache__request_valid__return_ok(self,
                                                     data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(
            url=create_url_with_query(url="/cache", data_context=data_context_value, leadquelle="leadquelle"))

        # THEN
        assert_that(response.status_code, equal_to(OK))
        assert_that(json.loads(response.content), equal_to(expected_response))

    @parameterized.expand([[DataContext.TEST.value, DataContext.TEST], [DataContext.PROD.value, DataContext.PROD]])
    def test_prefill_cache__data_context_given__init_service_with_correct_parameters(self,
                                                                                     data_context_value: str,
                                                                                     given_context: DataContext):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        self.client.get(
            url=create_url_with_query(url="/cache", data_context=data_context_value, leadquelle="leadquelle"))

        # THEN
        verify(consors_api).ConsorsApi(config=config[data_context_value], secrets_manager=any,
                                       data_context=given_context)

    @parameterized.expand([["NOT_AVAILABLE"], [None]])
    def test_prefill_cache__data_context_invalid__return_error_422_unprocessable_entity(self, invalid_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(
            url=create_url_with_query(url="/cache", leadquelle="TEST", data_context=invalid_value))

        # THEN
        assert_that(response.status_code, equal_to(UNPROCESSABLE_ENTITY))

    def test_prefill_cache__data_context_missing__return_error_422_unprocessable_entity(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(url=create_url_with_query(url="/cache", leadquelle="TEST"))

        # THEN
        assert_that(response.status_code, equal_to(UNPROCESSABLE_ENTITY))

    def test_prefill_cache__leadquelle_missing__return_error_422_unprocessable_entity(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(
            url=create_url_with_query(url="/cache", data_context="TEST"))

        # THEN
        assert_that(response.status_code, equal_to(UNPROCESSABLE_ENTITY))

    @parameterized.expand([[DataContext.TEST.value, DataContext.TEST], [DataContext.PROD.value, DataContext.PROD]])
    def test_prefill_cache__data_context_given__use_data_context_as_given(self, data_context_value: str,
                                                                          given_data_context: DataContext):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = "Some_Response"
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        self.client.get(
            url=create_url_with_query(url="/cache", data_context=data_context_value, leadquelle="leadquelle"))

        # THEN
        verify(consors_api).ConsorsApi(config=config[data_context_value], secrets_manager=any,
                                       data_context=given_data_context)

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_prefill_cache__request_valid__call_consors_api(self, data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_response = {"string": True}
        when(consors_api_mock).prefill_cache().thenReturn(create_async_mock_response(expected_response))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        self.client.get(
            url=create_url_with_query(url="/cache", data_context=data_context_value, leadquelle="leadquelle"))

        # THEN
        verify(consors_api_mock).prefill_cache()

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_prefill_cache__raise_consors_api_exception__return_bad_request_and_error_message(self,
                                                                                              data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_error_message = "Some error message"
        when(consors_api_mock).prefill_cache().thenRaise(ConsorsApiException(message=expected_error_message))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(
            url=create_url_with_query(url="/cache", data_context=data_context_value, leadquelle="leadquelle"))

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(message_with_detail_text(expected_error_message)))

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_get_product_limits__request_valid__call_consors_api(self, data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api_mock).load_product_limits().thenReturn(create_async_mock_response(PRODUKTGRENZEN_RESPONSE))
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        # WHEN
        self.client.get(url=create_url_with_query(url="/productlimits", data_context=data_context_value,
                                                  leadquelle="leadquelle"))

        # THEN
        verify(consors_api_mock).load_product_limits()

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_get_product_limits__request_valid__return_ok_and_expected_response(self, data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api_mock).load_product_limits().thenReturn(create_async_mock_response(PRODUKTGRENZEN_RESPONSE))
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        # WHEN
        response = self.client.get(url=create_url_with_query(url="/productlimits", data_context=data_context_value,
                                                             leadquelle="leadquelle"))

        # THEN
        assert_that(response.status_code, equal_to(OK))
        assert_that(json.loads(response.content), equal_to(PRODUKTGRENZEN_RESPONSE))

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_get_product_limits__raise_consors_api_exception__return_ok_and_expected_response(self,
                                                                                              data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_error_message = "Could not get available products. Response status_code 400"
        when(consors_api_mock).load_product_limits().thenRaise(ConsorsApiException(message=expected_error_message))
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        # WHEN
        response = self.client.get(url=create_url_with_query(url="/productlimits", data_context=data_context_value,
                                                             leadquelle="leadquelle"))

        # THEN
        assert_that(response.status_code, equal_to(NOT_FOUND))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text({"errors": expected_error_message})))

    @parameterized.expand([[DataContext.TEST.value], [DataContext.PROD.value]])
    def test_get_financial_calculations__request_valid__return_ok_and_expected_response(self, data_context_value):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_kredit_values = {"nettokreditbetrag": 4200, "laufzeit_in_monaten": 12, "monatliche_rate": 392.0,
                                  "effektivzins": 11.8, "sollzins": 12.0, "gesamtkreditbetrag": 4704}

        expected = LoanOfferModel.parse_obj(
            create_consors_api_financial_calculations(**expected_kredit_values)).consorsfinanz
        when(consors_api_mock).dispatch_offer_request(any).thenReturn(
            create_async_mock_response(create_mocked_dispatch_offer_request(**expected_kredit_values)))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(url=create_url_with_query(url="/financialcalculations",
                                                             data_context=data_context_value,
                                                             leadquelle="leadquelle",
                                                             credit_amount=expected_kredit_values["nettokreditbetrag"],
                                                             duration=expected_kredit_values["laufzeit_in_monaten"]))

        # THEN
        given = json.loads(response.content)["consorsfinanz"]

        assert_that(response.status_code, equal_to(OK))
        assert_that(given["produktId"], equal_to(expected.produktId))
        assert_that(given["produkttyp"], equal_to(expected.produkttyp.value))
        assert_that(given["produktbeschreibung"], equal_to(expected.produktbeschreibung))
        assert_that(given["versicherteRisiken"], equal_to(expected.versicherteRisiken))
        assert_that(given["nettokreditbetrag"], equal_to(expected.nettokreditbetrag))
        assert_that(given["laufzeitInMonaten"], equal_to(expected.laufzeitInMonaten))
        assert_that(given["monatlicheRate"], equal_to(expected.monatlicheRate))
        assert_that(given["effektivzins"], equal_to(expected.effektivzins))
        assert_that(given["sollzins"], equal_to(expected.sollzins))
        assert_that(given["gesamtkreditbetrag"], equal_to(expected.gesamtkreditbetrag))
        assert_that(given["pAngV"], equal_to(expected.pAngV))
        assert_that(given["kreditDetails"], equal_to(expected.kreditDetails))

    def test_get_financial_calculations__request_valid__call_consors_api_with_correct_parameters(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_kredit_values = {"nettokreditbetrag": 4200, "laufzeit_in_monaten": 12, "monatliche_rate": 392.0,
                                  "effektivzins": 12.0, "sollzins": 11.6, "gesamtkreditbetrag": 4704}
        when(consors_api_mock).dispatch_offer_request(any).thenReturn(
            create_async_mock_response(create_mocked_dispatch_offer_request(**expected_kredit_values)))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_offer_model = RequestLoanOfferModel(creditAmount=expected_kredit_values["nettokreditbetrag"],
                                                          duration=expected_kredit_values["laufzeit_in_monaten"])

        # WHEN
        self.client.get(url=create_url_with_query(url="/financialcalculations",
                                                  data_context=DataContext.TEST.value,
                                                  leadquelle="leadquelle",
                                                  credit_amount=expected_kredit_values["nettokreditbetrag"],
                                                  duration=expected_kredit_values["laufzeit_in_monaten"]))

        # THEN
        verify(consors_api_mock).dispatch_offer_request(expected_loan_offer_model)

    @parameterized.expand([
        ["Invalid_data_context_Not_defined", "NOT_AVAILABLE", "4200.0", "12"],
        ["Invalid_data_context_None", None, "4200.0", "12"],
        ["Invalid_credit_amount_None", DataContext.TEST.value, None, "12"],
        ["Invalid_credit_amount_Text", DataContext.TEST.value, "ABCD", "12"],
        ["Invalid_duration", DataContext.TEST.value, 4200.0, 12.0],
        ["Invalid_duration", DataContext.TEST.value, 4200.0, None],
    ])
    def test_get_financial_calculations__query_invalid__return_error_422_unprocessable_entity(self,
                                                                                              _: str,
                                                                                              data_context_value: str,
                                                                                              credit_amount: float,
                                                                                              duration: int):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_kredit_values = {"nettokreditbetrag": 4200, "laufzeit_in_monaten": 12, "monatliche_rate": 392.0,
                                  "effektivzins": 12.0, "sollzins": 11.6, "gesamtkreditbetrag": 4704}
        when(consors_api_mock).dispatch_offer_request(any).thenReturn(
            create_async_mock_response(create_mocked_dispatch_offer_request(**expected_kredit_values)))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(url=create_url_with_query(url="/financialcalculations",
                                                             data_context=data_context_value,
                                                             leadquelle="leadquelle",
                                                             credit_amount=credit_amount,
                                                             duration=duration))

        # THEN
        assert_that(response.status_code, equal_to(UNPROCESSABLE_ENTITY))

    def test_get_financial_calculations__raise_loan_dispatch_offer_flow_exception__return_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_kredit_values = {"nettokreditbetrag": 4200, "laufzeit_in_monaten": 12, "monatlich_rate": 392.0,
                                  "effektivzins": 12.0, "sollzins": 11.6, "gesamtkreditbetrag": 4704}
        expected_error = BusinessError(
            errors=[BusinessDataError(key=BusinessDataEnum.BUSINESS_ERROR,
                                      message=f"{ErrorMessages.PRODUCT_IDENTIFIER_ERROR} 4200.0€ auf 12 Monate")])
        when(consors_api_mock).dispatch_offer_request(any).thenRaise(LoanDispatchOfferFlowException(expected_error))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(url=create_url_with_query(url="/financialcalculations",
                                                             data_context=DataContext.TEST.value,
                                                             leadquelle="leadquelle",
                                                             credit_amount=expected_kredit_values["nettokreditbetrag"],
                                                             duration=expected_kredit_values["laufzeit_in_monaten"]))

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text(json.loads(expected_error.json()))))

    def test_get_financial_calculations__raise_consors_api_exception__return_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        expected_kredit_values = {"nettokreditbetrag": 4200, "laufzeit_in_monaten": 12, "monatlich_rate": 392.0,
                                  "effektivzins": 12.0, "sollzins": 11.6, "gesamtkreditbetrag": 4704}
        expected_error_message = "Could not get financial calculations for loan type ICCL"
        when(consors_api_mock).dispatch_offer_request(any).thenRaise(
            ConsorsApiException(message=expected_error_message))

        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)

        # WHEN
        response = self.client.get(url=create_url_with_query(url="/financialcalculations",
                                                             data_context=DataContext.TEST.value,
                                                             leadquelle="leadquelle",
                                                             credit_amount=expected_kredit_values["nettokreditbetrag"],
                                                             duration=expected_kredit_values["laufzeit_in_monaten"]))

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text({"errors": expected_error_message})))

    def test_credit_submission__request_valid__return_ok_with_response_loan_submit_model(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())
        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))

        mocked_response_loan_submit_model = create_response_loan_submit_model()
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenReturn(
            create_async_mock_response(mocked_response_loan_submit_model))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(OK))
        assert_that(json.loads(response.content), equal_to(mocked_response_loan_submit_model))

    def test_credit_submission__request_cause_validation_error__return_bad_request_with_message(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any, data_context=any).thenReturn(consors_api_mock)

        # WHEN
        invalid_json = {}
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"), json=invalid_json)

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))

    @parameterized.expand([
        ["Invalid_data_context_Not_defined", "NOT_AVAILABLE"],
        ["Invalid_data_context_None", None]
    ])
    def test_credit_submission__query_invalid__return_error_422_unprocessable_entity(self, _: str,
                                                                                     data_context_value: str):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())

        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))

        mocked_response_loan_submit_model = create_response_loan_submit_model()
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenReturn(
            create_async_mock_response(mocked_response_loan_submit_model))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=data_context_value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(UNPROCESSABLE_ENTITY))

    def test_credit_submission__raise_loan_submission_flow_exception__return_400_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())
        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))
        expected_error = BusinessError(
            errors=[BusinessDataError(key=BusinessDataEnum.BUSINESS_ERROR,
                                      message=ErrorMessages.PRODUCT_IDENTIFIER_ERROR)])
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenRaise(
            LoanSubmissionFlowException(expected_error))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text(expected_error)))

    def test_credit_submission__raise_consors_api_exception__return_400_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())
        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))
        error_message = "expected_error_message"
        expected_error = BusinessError(
            errors=[BusinessDataError(key="BUSINESS_ERROR", message=error_message)])
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenRaise(
            ConsorsApiException(message=error_message))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text(expected_error)))

    def test_credit_submission__raise_required_field_missing_error__return_400_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())
        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))
        data_errors = [DataError(produktanbieter="Consors Finanz", field="Some field", message="Some error message")]
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenRaise(
            RequiredFieldMissingError(FieldDataError(errors=data_errors)))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(BAD_REQUEST))
        assert_that(json.loads(response.content), equal_to(message_with_detail_text({"errors": data_errors})))

    def test_credit_submission__raise_exception__return_400_bad_request(self):
        # GIVEN
        consors_api_mock = mock(ConsorsApi)
        when(consors_api).ConsorsApi(config=any, secrets_manager=any,
                                     data_context=any).thenReturn(consors_api_mock)
        expected_loan_submission_model = create_request_credit_submission_model(
            credit_amount=4200, duration=12,
            vorgangsnummer="ABCDE",
            vorgang=create_default_vorgang_marktplatz_model())
        mocked_request_json = json.loads(expected_loan_submission_model.json(exclude_none=True))
        error_message_detail = "expected_error_message"
        when(consors_api_mock).submit_loan_calculation_request(expected_loan_submission_model).thenRaise(
            Exception(error_message_detail))

        # WHEN
        response = self.client.post(url=create_url_with_query(url="/financialcalculation",
                                                              data_context=DataContext.TEST.value,
                                                              leadquelle="leadquelle"),
                                    json=mocked_request_json)

        # THEN
        assert_that(response.status_code, equal_to(INTERNAL_SERVER_ERROR))
        assert_that(json.loads(response.content),
                    equal_to(message_with_detail_text(error_message_detail)))

import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.request_credit_submission_model import RequestCreditSubmissionModel
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    AnredeEnum, WohnartEnum, FamilienstandEnum, BeschaeftigungsartEnum
from app.common.errors.field_data_error import FieldEnum, DataError
from app.consorsfinanz.flows.submit.mapping.loan_submit_model_validator import validate_loan_submit_model
from app.consorsfinanz.flows.submit.mapping.validator.error_messages import ErrorMessages


@pytest.mark.asyncio
async def test_validate_subscriber_mapping_success():
    request = RequestCreditSubmissionModel(
        creditAmount=10000,
        duration=12,
        vorgangsnummer="12345",
        vorgang=VorgangMarktplatzModel(
            stammdaten=Stammdaten(
                anredeAs1=AnredeEnum.HERR,
                titelAs1=None,
                vornameAs1="Hans",
                nachnameAs1="Dampf",
                emailAs1="jean-marc.nadal@consorsfinanz.de",
                strasseAs1="Fraunbergstr 18",
                plzAs1="81379",
                ortAs1="Bonn",
                wohnhaftSeitAs1="2014-10-20",
                telefonPrivatAs1="089832432432",
                geburtsnameAs1="foo",
                geburtsdatumAs1="1980-12-11",
                staatsangehoerigkeitAs1="DE",
                geburtslandAs1=None,
                wohnartAs1=WohnartEnum.ZUR_MIETE,
                familienstandAs1=FamilienstandEnum.VERHEIRATET,
                kinder=None,
                iban="DE89370400440532013000",
                einkommenMonatlichAs1=1500,
                beschaeftigungsartAs1=BeschaeftigungsartEnum.ANGESTELLTER,
                beschaeftigtSeitAs1="2014-10-20",
                arbeitgeberNameAs1="Siemens GmbH",
                arbeitgeberStrasseAs1="Hansastr.",
                arbeitgeberHausnummerAs1="11",
                arbeitgeberPlzAs1="80339",
                arbeitgeberOrtAs1="Muenchen",
                voranschriftStrasseAs1="Barstr",
                voranschriftHausnummerAs1="12",
                voranschriftPlzAs1="10713",
                voranschriftOrtAs1="Berlin"
            )
        )
    )

    errors = validate_loan_submit_model(request)

    # THEN
    assert_that(errors, equal_to([
        DataError(field=FieldEnum.BONITAETSANGABEN_MIETAUSGABEN_BETRAGMONATLICH_AS1,
                  message=ErrorMessages.WARM_RENT_ERROR),
        DataError(field=FieldEnum.HAUSNUMMER_AS1, message=ErrorMessages.HOUSENUMBER_ERROR),
        DataError(field=FieldEnum.FINANZIERUNGSZWECKBESCHREIBUNG,
                  message=ErrorMessages.FINANZIERUNGSZWECKBESCHREIBUNG_ERROR)])
                )

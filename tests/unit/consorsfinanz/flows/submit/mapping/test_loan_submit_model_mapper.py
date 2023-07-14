from datetime import datetime
from unittest import mock

import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.request_credit_submission_model import RequestCreditSubmissionModel
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import VorgangMarktplatzModel, Stammdaten, \
    AnredeEnum, TitleEnum, WohnartEnum, FamilienstandEnum, Kind, Bonitaetsangaben, MietAusgaben, \
    BeschaeftigungsartEnum, PartnerCustom, Custom, Antragsdaten
from app.consorsfinanz.flows.submit.mapping.loan_submit_model_mapper import map_loan_submit_model


@pytest.mark.asyncio
async def test_subscriber_mapping_success():  # pylint: disable=missing-function-docstring
    with mock.patch("app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 1, 1)
        mock_date.fromisoformat.return_value = datetime(2009, 1, 1, 0, 0, 0)

        # GIVEN
        request = RequestCreditSubmissionModel(
            creditAmount=10000,
            vorgangsnummer="12345",
            duration=12,
            vorgang=VorgangMarktplatzModel(
                partner=PartnerCustom(custom=[
                    Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-10-20T13:14:07.712+02:00"),
                    Custom(key="finanzierungszweckBeschreibung", value="AMA"),
                    Custom(key="datenweitergabe", value=True),
                    Custom(key="datenweitergabeDirektabschluss", value=True)
                ]),
                antragsdaten=Antragsdaten(
                    antragsvolumen=3000,
                    laufzeitInMonaten=12
                ),
                stammdaten=Stammdaten(
                    anredeAs1=AnredeEnum.HERR,
                    titelAs1=[TitleEnum.DOKTOR],
                    vornameAs1="Hans",
                    nachnameAs1="Dampf",
                    emailAs1="jean-marc.nadal@consorsfinanz.de",
                    strasseAs1="Fraunbergstr",
                    hausnummerAs1="18",
                    plzAs1="81379",
                    ortAs1="Bonn",
                    wohnhaftSeitAs1="2014-10-20",
                    telefonPrivatAs1="089832432432",
                    geburtsnameAs1="foo",
                    geburtsdatumAs1="1980-12-11",
                    staatsangehoerigkeitAs1="DE",
                    geburtslandAs1="DE",
                    wohnartAs1=WohnartEnum.ZUR_MIETE,
                    familienstandAs1=FamilienstandEnum.VERHEIRATET,
                    kinder=[Kind(kindergeldFuer="lisa")],
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
                ),
                bonitaetsangaben=Bonitaetsangaben(
                    mietausgaben=[MietAusgaben(
                        betragMonatlich="100",
                        zugehoerigkeit="as1"
                    )]
                )
            )
        )

        response = map_loan_submit_model(request)
        subscription = response.subscription
        subscriber = subscription.subscribers[0]

    # THEN
    assert_that(subscription.kycPurposeOfLoan, equal_to("AMA"))
    assert_that(subscription.subscriptionBasketInfo.firstPayment, equal_to(1))
    assert_that(subscription.subscriptionBasketInfo.term, equal_to(12))
    assert_that(subscription.subscriptionBasketInfo.price, equal_to(10000))
    assert_that(subscription.bankAccount.iban, equal_to("DE89370400440532013000"))
    assert_that(subscription.bankAccount.accountSince, equal_to("2014-10"))
    assert_that(subscriber.rolePlaying, equal_to("MAIN"))
    assert_that(subscriber.gender, equal_to("MALE"))
    assert_that(subscriber.firstName, equal_to("Hans"))
    assert_that(subscriber.lastName, equal_to("Dampf"))
    assert_that(subscriber.birthName, equal_to("foo"))
    assert_that(subscriber.dateOfBirth, equal_to("1980-12-11"))
    assert_that(subscriber.countryOfBirth, equal_to("276"))
    assert_that(subscriber.nationality, equal_to("276"))
    assert_that(subscriber.housingSituation, equal_to("RENTER"))
    assert_that(subscriber.familySituation, equal_to("MARRIED"))
    assert_that(subscriber.numberOfChildren, equal_to(1))
    assert_that(subscriber.income.netIncome, equal_to(1500))
    assert_that(subscriber.expense.warmRent, equal_to(100))
    assert_that(subscriber.employmentDetails.profession, equal_to("REGULAR_EMPLOYED"))
    assert_that(subscriber.employmentDetails.professionBeginDate, equal_to("2014-10"))
    assert_that(subscriber.employmentDetails.employerAddress.employerName, equal_to("Siemens GmbH"))
    assert_that(subscriber.employmentDetails.employerAddress.employerStreet, equal_to("Hansastr. 11"))
    assert_that(subscriber.employmentDetails.employerAddress.employerCity, equal_to("Muenchen"))
    assert_that(subscriber.employmentDetails.employerAddress.employerZipcode, equal_to("80339"))
    assert_that(subscriber.contactAddress.email, equal_to("jean-marc.nadal@consorsfinanz.de"))
    assert_that(subscriber.contactAddress.street, equal_to("Fraunbergstr 18"))
    assert_that(subscriber.contactAddress.zipcode, equal_to("81379"))
    assert_that(subscriber.contactAddress.city, equal_to("Bonn"))
    assert_that(subscriber.contactAddress.validFrom, equal_to("2014-10"))
    assert_that(subscriber.contactAddress.telephoneMobile, equal_to("089832432432"))
    assert_that(subscriber.consents.isSchufaCallAllowed, equal_to(True))
    # previous address now - 3 years > wohnhaft_seit_as1_date
    assert_that(subscriber.previousAddress.street, equal_to("Barstr 12"))
    assert_that(subscriber.previousAddress.city, equal_to("Berlin"))
    assert_that(subscriber.previousAddress.zipcode, equal_to("10713"))


@pytest.mark.asyncio
async def test_subscriber_mapping_with_none_success():
    with mock.patch("app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 1, 1)
        mock_date.fromisoformat.return_value = datetime(2007, 1, 1, 0, 0, 0)

        # GIVEN
        request = RequestCreditSubmissionModel(
            creditAmount=10000,
            vorgangsnummer="12345",
            duration=12,
            vorgang=VorgangMarktplatzModel(
                partner=PartnerCustom(custom=[
                    Custom(key="zeitpunktKontoeroeffnungAs1", value="2014-10-20"),
                    Custom(key="finanzierungszweckBeschreibung", value="AMA"),
                    Custom(key="datenweitergabe", value=True),
                    Custom(key="datenweitergabeDirektabschluss", value=True)
                ]),
                antragsdaten=Antragsdaten(
                    antragsvolumen=3000,
                    laufzeitInMonaten=12
                ),
                stammdaten=Stammdaten(
                    anredeAs1=AnredeEnum.HERR,
                    titelAs1=None,
                    vornameAs1="Hans",
                    nachnameAs1="Dampf",
                    emailAs1="jean-marc.nadal@consorsfinanz.de",
                    strasseAs1="Fraunbergstr 18",
                    hausnummerAs1="18",
                    plzAs1="81379",
                    ortAs1="Bonn",
                    wohnhaftSeitAs1="2014-10-20",
                    telefonPrivatAs1="089832432432",
                    geburtsnameAs1="foo",
                    geburtsdatumAs1="1980-12-11",
                    staatsangehoerigkeitAs1="DE",
                    geburtslandAs1=None,
                    wohnartAs1=WohnartEnum.BEI_DEN_ELTERN,
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

        response = map_loan_submit_model(request)
        subscriber = response.subscription.subscribers[0]

    # THEN
    assert_that(subscriber.numberOfChildren, equal_to(0))

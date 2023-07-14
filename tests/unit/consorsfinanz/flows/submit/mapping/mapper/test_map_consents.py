import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_consents import map_consents
from app.consorsfinanz.flows.submit.models.request_loan_submit_model import CustomerAdvertisementConsentEnum, Consents
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom, Antragsdaten


@pytest.mark.parametrize("data", [
    {
        "datenweitergabe": True,
        "expected_customerContactedByPhoneAndEmailForPromotions":
            CustomerAdvertisementConsentEnum.POST_EMAIL_TELEPHONE_SELL_CONTACT,
        "antragsvolumen": 3000,
        "laufzeit": 12
    },
    {
        "datenweitergabe": True,
        "expected_customerContactedByPhoneAndEmailForPromotions":
            CustomerAdvertisementConsentEnum.VENDOR_ONLY,
        "antragsvolumen": 4500,
        "laufzeit": 12
    },
    {
        "datenweitergabe": False,
        "expected_customerContactedByPhoneAndEmailForPromotions": None,
        "antragsvolumen": 4500,
        "laufzeit": 12
    }
])
def test_map_consents__mapping_customer_advertisement_consent(data):
    # GIVEN
    partner = PartnerCustom(
        custom=[
            Custom(key="datenweitergabe", value=data["datenweitergabe"]),
            Custom(key="datenweitergabeDirektabschluss", value=None)
        ]
    )
    antragsdaten = Antragsdaten(
        antragsvolumen=data["antragsvolumen"],
        laufzeitInMonaten=data["laufzeit"]
    )

    consents: Consents = map_consents(partner, antragsdaten)

    # THEN
    assert_that(consents.customerContactedByPhoneAndEmailForPromotions,
                equal_to(data["expected_customerContactedByPhoneAndEmailForPromotions"]))


@pytest.mark.parametrize("data", [
    {
        "datenweitergabe": True,
        "expected_isSchufaCallAllowed": True,
    },
    {
        "datenweitergabe": False,
        "expected_isSchufaCallAllowed": False,
    },
    {
        "datenweitergabe": None,
        "expected_isSchufaCallAllowed": False,
    }
])
def test_map_consents__mapping_is_schufa_call_allowed(data):
    # GIVEN
    partner = PartnerCustom(
        custom=[
            Custom(key="datenweitergabe", value=data["datenweitergabe"]),
        ]
    )
    antragsdaten = Antragsdaten(
        antragsvolumen=3000,
        laufzeitInMonaten=12
    )

    consents = map_consents(partner, antragsdaten)

    # THEN
    assert_that(consents.isSchufaCallAllowed, equal_to(data["expected_isSchufaCallAllowed"]))


def test_map_consents_none():
    consents = map_consents(None, None)

    # THEN
    assert_that(consents.isSchufaCallAllowed, equal_to(False))
    assert_that(consents.customerContactedByPhoneAndEmailForPromotions, equal_to(None))


def test_map_consents_custom():
    # GIVEN
    partner = PartnerCustom(custom=[])
    antragsdaten = Antragsdaten()

    consents = map_consents(partner, antragsdaten)

    # THEN
    assert_that(consents.isSchufaCallAllowed, equal_to(False))
    assert_that(consents.customerContactedByPhoneAndEmailForPromotions, equal_to(None))

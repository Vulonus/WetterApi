from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.request_loan_submit_model import ResidencePermitTypeEnum
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import PartnerCustom, Custom, Stammdaten, \
    AufenthaltstitelEnum
from app.consorsfinanz.flows.submit.mapping.mapper.map_identity import map_identity


def test_map_identity():
    # GIVEN
    partner = PartnerCustom(custom=[
        Custom(key="identityAusweisartAs1", value="DEUTSCHER_PERSONALAUSWEIS"),
        Custom(key="identityAusweisnummerAs1", value="L01X00T47"),
        Custom(key="identityAustellendeBehoerdeAs1", value="Stadt Lübeck"),
        Custom(key="identityGueltigbisAs1", value="2030-01-01"),
    ])

    # WHEN
    response = map_identity(Stammdaten(
        aufenthaltstitelAs1=AufenthaltstitelEnum.VISUM,
        aufenthaltBefristetBisAs1="2035-01-01"
    ), partner)

    # THEN
    assert_that(response.identificationType, equal_to("GERMAN_ID_CARD"))
    assert_that(response.validTill, equal_to("2030-01-01"))
    assert_that(response.issuingAuthority, equal_to("Stadt Lübeck"))
    assert_that(response.identificationNumber, equal_to("L01X00T47"))
    assert_that(response.residencePermitType, equal_to(ResidencePermitTypeEnum.RESIDENCE_PERMIT_CARD))
    assert_that(response.residencePermitValidTill, equal_to("2035-01"))


def test_map_identity_none():
    # WHEN
    response = map_identity(None, None)

    # THEN
    assert_that(response, equal_to(None))


def test_map_identity_none_custom():
    # GIVEN
    partner = PartnerCustom(custom=[])

    # WHEN
    response = map_identity(None, partner)

    # THEN
    assert_that(response, equal_to(None))

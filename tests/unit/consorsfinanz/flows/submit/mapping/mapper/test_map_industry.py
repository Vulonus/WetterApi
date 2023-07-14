import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_industry import map_industry
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import BeschaeftigungsartEnum


@pytest.mark.parametrize("data", [
    {"firmaBrancheAs1": "BAUGEWERBE", "industry": "CONSTRUCTION"},
    {"firmaBrancheAs1": "DIENSTLEISTUNGEN", "industry": "SERVICES_INCLUDING_FREELANCE_PROFESSIONS"},
    {"firmaBrancheAs1": "ENERGIE_WASSERVERSORGUNG_BERGBAU", "industry": "MINING_QUARRYING_EARTH"},
    {"firmaBrancheAs1": "ERZIEHUNG_UNTERRICHT", "industry": "OTHER"},
    {"firmaBrancheAs1": "GEBIETSKOERPERSCHAFTEN", "industry": "OTHER"},
    {"firmaBrancheAs1": "GEMEINNUETZIGE_ORGANISATION", "industry": "OTHER"},
    {"firmaBrancheAs1": "GESUNDHEIT_SOZIALWESEN", "industry": "OTHER"},
    {"firmaBrancheAs1": "HANDEL", "industry": "TRADE_SERVICE_REPAIR_VEHICLES_CONSUMER_GOODS"},
    {"firmaBrancheAs1": "HOTEL_GASTRONOMIE", "industry": "SERVICES_INCLUDING_FREELANCE_PROFESSIONS"},
    {"firmaBrancheAs1": "INFORMATION_KOMMUNIKATION", "industry": "OTHER"},
    {"firmaBrancheAs1": "KREDITINSTITUTE_VERSICHERUNGEN", "industry": "FINANCIAL_INSTITUTIONS__INSURANCE_COMPANIES"},
    {"firmaBrancheAs1": "KULTUR_SPORT_UNTERHALTUNG", "industry": "OTHER"},
    {"firmaBrancheAs1": "LANDWIRTSCHAFT_FORSTWIRTSCHAFT_FISCHEREI",
     "industry": "AGRICULTURE_FORESTRY_FISHING_FISH_FARMING"},
    {"firmaBrancheAs1": "OEFFENTLICHER_DIENST", "industry": "OTHER"},
    {"firmaBrancheAs1": "PRIVATE_HAUSHALTE", "industry": "OTHER"},
    {"firmaBrancheAs1": "VERARBEITENDES_GEWERBE", "industry": "MANUFACTURING"},
    {"firmaBrancheAs1": "VERKEHR_LOGISTIK", "industry": "TRAFFIC_MESSAGE_DELIVERY"}
])
def test_map_industry_self_employed(data, vorgang):
    # WHEN
    vorgang.stammdaten.beschaeftigungsartAs1 = BeschaeftigungsartEnum.SELBSTSTAENDIGER
    vorgang.stammdaten.firmaBrancheAs1 = data["firmaBrancheAs1"]
    industry = map_industry(vorgang)

    # THEN
    assert_that(industry, equal_to(data["industry"]))


def test_map_industry_regular_employed(vorgang):
    # WHEN
    industry = map_industry(vorgang)

    # THEN
    assert_that(industry, equal_to(None))

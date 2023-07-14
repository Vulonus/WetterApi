from typing import List

import pytest
from hamcrest import assert_that, equal_to

from app.consorsfinanz.flows.insurance.insurance_service import map_insurance_types, InsuranceTypes


@pytest.mark.parametrize("data", [
    {"key": "DEATH", "value": [InsuranceTypes.DEATH]},
    {"key": "DEATH_DISABILITY_UNEMPLOYMENT", "value": [
        InsuranceTypes.DEATH, InsuranceTypes.DISABILITY, InsuranceTypes.UNEMPLOYMENT]}])
def test_map_insurance_types(data):
    # WHEN
    response: List[str] = map_insurance_types(data["key"])

    # THEN
    assert_that(response, equal_to(data["value"]))


def test_map_insurance_types_none():
    # WHEN
    response: List[str] = map_insurance_types(None)

    # THEN
    assert_that(response, equal_to([]))

import pytest
from hamcrest import assert_that, equal_to

from app.consorsfinanz.flows.submit.mapping.validator.patterns_for_regex import *


@pytest.mark.parametrize("data", [
    {"value": "abc@drklein...de", "result": False},
    {"value": ".@drklein.de", "result": False},
    {"value": "a...b@drklein.de", "result": False},
    {"value": "b----12@drklein.de", "result": False},
    {"value": "----@drklein.de", "result": False},
    {"value": "@example.com", "result": False},
    {"value": "email.example.com", "result": False},
    {"value": "email@example@example.com", "result": False},
    {"value": "firstname.lastname@example.com", "result": True},
    {"value": "email@subdomain.example.com", "result": True},
    {"value": "firstname+lastname@example.com", "result": True},
    {"value": "1234567890@example.com", "result": True},
    {"value": "email@example.co.jp", "result": True},
    {"value": "firstname-lastname@example.com", "result": True},
])
def test_email_pattern(data):
    result = bool(re.fullmatch(email_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"value": "Barstr#", "result": False},
    {"value": "†ÇI2Ô☺║û¬ëÑò☺☼♀}", "result": False},
    {"value": "Barstraße", "result": True},
    {"value": "Bar-Straße", "result": True},
    {"value": "Bar, Straße", "result": True},
    {"value": "Bär, Straße", "result": True},
    {"value": "Bür, Straße", "result": True},
    {"value": "Bör, Straße", "result": True}
])
def test_street_pattern(data):
    result = bool(re.fullmatch(street_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"value": "72--74", "result": False},
    {"value": "†ÇI2Ô☺║û¬ëÑò☺☼♀}", "result": False},
    {"value": "123abcd123 32", "result": False},
    {"value": "ä123", "result": False},
    {"value": "12-13FAX", "result": False},
    {"value": "12", "result": True},
    {"value": "12 F", "result": True},
    {"value": "12F", "result": True},
    {"value": "12-13", "result": True},
    {"value": "12-13FA", "result": True}
])
def test_housenumber_pattern(data):
    result = bool(re.fullmatch(housenumber_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"value": "ABC", "result": False},
    {"value": "23abc", "result": False},
    {"value": "23_54", "result": False},
    {"value": "2355", "result": True},
    {"value": "23 54", "result": False},
    {"value": "23554", "result": True},
    {"value": "23-5546", "result": False}
])
def test_zip_code_pattern(data):
    result = bool(re.fullmatch(zipcode_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"value": "23554", "result": False},
    {"value": "†ÇI2Ô☺║û¬ëÑò☺☼♀}", "result": False},
    {"value": "Ächte_Stadt", "result": False},
    {"value": "Ächte Stadt", "result": True},
    {"value": "Ächte-Stadt", "result": True},
    {"value": "Ächte.Stadt", "result": True},
    {"value": "(Ächte)Stadt", "result": True},
    {"value": "Ächte/Stadt", "result": True},
    {"value": "Üchte/Stadt", "result": True},
    {"value": "Öchte/Stadt", "result": True}
])
def test_city_pattern(data):
    result = bool(re.fullmatch(city_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))


@pytest.mark.parametrize("data", [
    {"value": "+491321584612", "result": False},
    {"value": "abc56465asd", "result": False},
    {"value": "12165432", "result": False},
    {"value": "0", "result": False},
    {"value": "05454 54654", "result": False},
    {"value": "05454/54654", "result": False},
    {"value": "(05454)54654", "result": False},
    {"value": "0145646548", "result": True},
])
def test_mobile_phone_pattern(data):
    result = bool(re.fullmatch(mobile_phone_pattern, data["value"]))

    assert_that(result, equal_to(data["result"]))

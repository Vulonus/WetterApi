import pytest
from hamcrest import assert_that, equal_to

from app.consorsfinanz.flows.submit.models.request_loan_submit_model import EmployerAddress, ContactAddress


@pytest.mark.parametrize("data", [
    {"employer_name": "Gandalf<>?!#$%^", "expected_result": "Gandalf"},
    {"employer_name": "Gándalf☺ Employment", "expected_result": "Gándalf☺ Employment"},
    {"employer_name": "Søren Employment", "expected_result": "Søren Employment"}
])
def test_employer_address_model__provide_employer_name_input__result_matches_expected(data):
    # GIVEN
    employer_name_with_special_characters = data["employer_name"]
    expected_result = data["expected_result"]

    # WHEN
    employer_address = EmployerAddress(employerName=employer_name_with_special_characters)

    # THEN
    assert_that(employer_address.employerName, equal_to(expected_result))


@pytest.mark.parametrize("data", [
    {"employer_street": "Gandalf†", "expected_result": "Gandalf"},
    {"employer_street": "Some(Fancy)-Employer, Street. 12 ", "expected_result": "SomeFancy-Employer, Street. 12 "},
    {"employer_street": "ValidCharacters0123456789.,/", "expected_result": "ValidCharacters0123456789.,/"},
    {"employer_street": "G_``é°²³¹ƒ¶µáóíîôÃ▀×a!?ndalf♥☺", "expected_result": "Gandalf"},
    {"employer_street": "Gándalf☺", "expected_result": "Gndalf"},
    {"employer_street": "Søren", "expected_result": "Sren"},
    {"employer_street": "cç91238641982736189", "expected_result": "c91238641982736189"},
])
def test_employer_address_model__provide_employer_street_input___result_matches_expected(data):
    # GIVEN
    employer_name_with_special_characters = data["employer_street"]
    expected_result = data["expected_result"]

    # WHEN
    employer_address = EmployerAddress(employerStreet=employer_name_with_special_characters)

    # THEN
    assert_that(employer_address.employerStreet, equal_to(expected_result))


@pytest.mark.parametrize("data", [
    {"employer_city": "Gandalf†", "expected_result": "Gandalf"},
    {"employer_city": "Some(Fancy)-Employer. 12 ", "expected_result": "Some(Fancy)-Employer.  "},
    {"employer_city": "EmployerCity./() - 12", "expected_result": "EmployerCity./() - "},
    {"employer_city": "G_``é°²³¹ƒ¶µáóíîôÃ▀×a!?ndalf♥☺", "expected_result": "Gandalf"},
    {"employer_city": "Gándalf☺", "expected_result": "Gndalf"},
    {"employer_city": "Søren", "expected_result": "Sren"},
    {"employer_city": "acç91238641982736189", "expected_result": "ac"}
])
def test_employer_address_model__provide_employer_city_input___result_matches_expected(data):
    # GIVEN
    employer_name_with_special_characters = data["employer_city"]
    expected_result = data["expected_result"]

    # WHEN
    employer_address = EmployerAddress(employerCity=employer_name_with_special_characters)

    # THEN
    assert_that(employer_address.employerCity, equal_to(expected_result))


@pytest.mark.parametrize("data", [
    {"given":
         {"telephoneMobile": "+4917611122230",
          "telephoneLandline": "+4945043132",
          "email": "foo.bar@baz.com",
          "street": "Zum Goldhügel 8",
          "zipcode": "23689",
          "city": "Pansdorf",
          "validFrom": "2022-08-29T11:20:46.238+02:00"
          },
     "expected_result":
         {"telephoneMobile": "017611122230",
          "telephoneLandline": "045043132",
          "email": "foo.bar@baz.com",
          "street": "Zum Goldhügel 8",
          "zipcode": "23689",
          "city": "Pansdorf",
          "validFrom": "2022-08"
          },
     }])
def test_contact_address_model__provide_valid_input__result_matches_expected_after_validation(data):
    # GIVEN
    given_mobile_phone_number = data["given"]["telephoneMobile"]
    given_landline_phone_number = data["given"]["telephoneLandline"]
    given_email = data["given"]["email"]
    given_street = data["given"]["street"]
    given_zipcode = data["given"]["zipcode"]
    given_city = data["given"]["city"]
    given_valid_from = data["given"]["validFrom"]

    # WHEN
    contact_address = ContactAddress(telephoneMobile=given_mobile_phone_number,
                                     telephoneLandline=given_landline_phone_number, email=given_email,
                                     street=given_street,
                                     zipcode=given_zipcode, city=given_city, validFrom=given_valid_from)

    # THEN
    assert_that(contact_address.telephoneMobile, equal_to(data["expected_result"]["telephoneMobile"]))
    assert_that(contact_address.telephoneLandline, equal_to(data["expected_result"]["telephoneLandline"]))
    assert_that(contact_address.email, equal_to(data["expected_result"]["email"]))
    assert_that(contact_address.street, equal_to(data["expected_result"]["street"]))
    assert_that(contact_address.zipcode, equal_to(data["expected_result"]["zipcode"]))
    assert_that(contact_address.city, equal_to(data["expected_result"]["city"]))
    assert_that(contact_address.validFrom, equal_to(data["expected_result"]["validFrom"]))


@pytest.mark.parametrize("data", [
    {"given":
         {"telephoneMobile": "017611122230",
          "telephoneLandline": "045043132",
          "email": "foo.bar@baz.com",
          "street": "Zum Goldhügel 8",
          "zipcode": "23689",
          "city": "Pansdorf",
          "validFrom": "2022-08-29T11:20:46.238+02:00"
          },
     "expected_result":
         {"telephoneMobile": "017611122230",
          "telephoneLandline": "045043132",
          "email": "foo.bar@baz.com",
          "street": "Zum Goldhügel 8",
          "zipcode": "23689",
          "city": "Pansdorf",
          "validFrom": "2022-08"
          },
     }])
def test_contact_address_model__provide_locale_mobile_phone_number_input__use_phone_number_without_conversion(
        data):
    # GIVEN
    given_mobile_phone_number = data["given"]["telephoneMobile"]
    given_landline_phone_number = data["given"]["telephoneLandline"]
    given_email = data["given"]["email"]
    given_street = data["given"]["street"]
    given_zipcode = data["given"]["zipcode"]
    given_city = data["given"]["city"]
    given_valid_from = data["given"]["validFrom"]

    # WHEN
    contact_address = ContactAddress(telephoneMobile=given_mobile_phone_number,
                                     telephoneLandline=given_landline_phone_number, email=given_email,
                                     street=given_street,
                                     zipcode=given_zipcode, city=given_city, validFrom=given_valid_from)

    # THEN
    assert_that(contact_address.telephoneMobile, equal_to(data["expected_result"]["telephoneMobile"]))
    assert_that(contact_address.telephoneLandline, equal_to(data["expected_result"]["telephoneLandline"]))
    assert_that(contact_address.email, equal_to(data["expected_result"]["email"]))
    assert_that(contact_address.street, equal_to(data["expected_result"]["street"]))
    assert_that(contact_address.zipcode, equal_to(data["expected_result"]["zipcode"]))
    assert_that(contact_address.city, equal_to(data["expected_result"]["city"]))
    assert_that(contact_address.validFrom, equal_to(data["expected_result"]["validFrom"]))

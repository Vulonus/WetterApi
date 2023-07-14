import pytest
from hamcrest import assert_that, equal_to

from app.common.util import remove_characters_matching_regex


@pytest.mark.parametrize("data", [
    {"given_string": "ABCDE", "provided_regex": r"ABC", "expected_result": "DE"},
    {"given_string": "ABCabc", "provided_regex": r"[ABC]", "expected_result": "abc"},
    {"given_string": "!?Hello Stranger!", "provided_regex": r"[^!?]", "expected_result": "!?!"},
    {"given_string": "Hello John Cena", "provided_regex": r"John Cena", "expected_result": "Hello "}
])
def test_remove_characters_matching_regex__provide_string_with_regex__removed_characters_as_defined(data):
    # GIVEN
    given_string = data["given_string"]
    provided_regex = data["provided_regex"]
    expected_result = data["expected_result"]

    # WHEN
    string_with_removed_characters = remove_characters_matching_regex(given_string, provided_regex)

    # THEN
    assert_that(string_with_removed_characters, equal_to(expected_result))

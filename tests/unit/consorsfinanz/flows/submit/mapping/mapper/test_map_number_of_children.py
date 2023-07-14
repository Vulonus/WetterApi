from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Kind
from app.consorsfinanz.flows.submit.mapping.mapper.map_number_of_children import map_number_of_children
# from app.consorsfinanz.mapping.mapper.map_profession import map_profession


def test_map_number_of_children():
    # WHEN
    response = map_number_of_children([Kind()])

    # THEN
    assert_that(response, equal_to(1))


def test_map_profession_none():
    # WHEN
    response = map_number_of_children(None)

    # THEN
    assert_that(response, equal_to(0))

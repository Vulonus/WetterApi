from typing import List

import pytest
from hamcrest import assert_that, equal_to

from app.consorsfinanz.flows.submit.mapping.mapper.map_supporting_documents import map_document_id_to_description
from app.consorsfinanz.flows.submit.mapping.mapper.supporting_documents import supporting_documents

parametrzied_documents = [{"key": key, "value": value} for key, value in supporting_documents.items()]


@pytest.mark.parametrize("data", parametrzied_documents)
def test_map_supporting_documents__provide_all_ids_single__return_descriptions_single(data):
    # WHEN
    response: List[str] = map_document_id_to_description([data["key"]])

    # THEN
    assert_that(response, equal_to([data["value"]]))


@pytest.mark.parametrize("data", [
    {
        "dokumente": ["30660", "32100"],
        "expected_result": ["Kopie Ihres Kreditvertrages", "Kopie Ihres aktuellen Rentenbescheides"]
    },
    {
        "dokumente": ["30660", "32100", "50008"],
        "expected_result": ["Kopie Ihres Kreditvertrages", "Kopie Ihres aktuellen Rentenbescheides",
                            "Nachweis über Ihre Aufenthaltserlaubnis"]
    }
])
def test_map_supporting_documents__provide_list_of_ids__return_list_of_descriptions(data):
    # WHEN
    response: List[str] = map_document_id_to_description(data["dokumente"])

    # THEN
    assert_that(response, equal_to(data["expected_result"]))


@pytest.mark.parametrize("data", [
    {"dokumente": ["12345", "98765"], "expected_result": []},
    {"dokumente": [None], "expected_result": []}
])
def test_map_supporting_documents__provide_invalid_ids_or_none__return_empty_list(data):
    # GIVEN
    # WHEN
    response: List[str] = map_document_id_to_description(data["dokumente"])
    # THEN
    assert_that(response, equal_to(data["expected_result"]))

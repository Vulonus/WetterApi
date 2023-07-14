from datetime import datetime
from unittest import mock

from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address import map_previous_address


def test_map_previous_address__provide_wohnhaft_seit_as1_lt_now(vorgang):
    with mock.patch("app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2022, 6, 1)
        # wohnhaftSeitAs1 is always only the date
        mock_date.fromisoformat.return_value = datetime(2020, 5, 1, 0, 0, 0)

        # WHEN
        response = map_previous_address(vorgang)

        # THEN
        assert_that(response.street, equal_to("Barstr 12"))
        assert_that(response.zipcode, equal_to("10713"))
        assert_that(response.city, equal_to("Berlin"))


def test_map_previous_address_wohnhaft_seit_as1_none(vorgang):
    with mock.patch("app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 1, 1)
        mock_date.fromisoformat.return_value = datetime(2009, 1, 1, 0, 0, 0)

        # WHEN
        vorgang.stammdaten.wohnhaftSeitAs1 = None
        response = map_previous_address(vorgang)

        # THEN
        assert_that(response, equal_to(None))


def test_map_previous_address_after_762_days(vorgang):
    with mock.patch("app.consorsfinanz.flows.submit.mapping.mapper.map_previous_address.datetime") as mock_date:
        mock_date.today.return_value = datetime(2010, 2, 1)
        mock_date.fromisoformat.return_value = datetime(2008, 1, 1, 0, 0, 0)

        # WHEN
        response = map_previous_address(vorgang)

        # THEN
        assert_that(response, equal_to(None))

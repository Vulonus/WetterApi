import pytest
from hamcrest import equal_to, assert_that

from app.consorsfinanz.flows.submit.mapping.mapper.map_expense_warm_rent import map_expense_warm_rent
from app.consorsfinanz.flows.submit.models.vorgang_marktplatz_model import Stammdaten, WohnartEnum, Immobilie, \
    Darlehen, Bonitaetsangaben, MietAusgaben


@pytest.mark.parametrize("data", [
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.ZUR_MIETE,
        ),
        "bonitaetsangaben": Bonitaetsangaben(
            mietausgaben=[MietAusgaben(
                betragMonatlich="10",
                zugehoerigkeit="as1"
            )]
        )
    },
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.ZUR_UNTERMIETE,
        ),
        "bonitaetsangaben": Bonitaetsangaben(
            mietausgaben=[MietAusgaben(
                betragMonatlich="11",
                zugehoerigkeit="as1"
            )]
        )
    },
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.BEI_DEN_ELTERN,
        ),
        "bonitaetsangaben": Bonitaetsangaben(
            mietausgaben=[MietAusgaben(
                betragMonatlich="0",
                zugehoerigkeit="as1"
            )]
        )
    }
])
def test_map_expense_warm_rent(data):
    # WHEN
    response = map_expense_warm_rent(data["stammdaten"], data["bonitaetsangaben"])

    # THEN
    bonitaetsangaben_result = Bonitaetsangaben.parse_obj(data["bonitaetsangaben"])
    assert_that(response, equal_to(float(bonitaetsangaben_result.mietausgaben[0].betragMonatlich)))


@pytest.mark.parametrize("data", [
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            immobilien=[Immobilie(
                darlehen=[Darlehen(
                    rateMonatlich=101
                )]
            )]
        ),
        "baufinanzierungsrate": 101
    },
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
            immobilien=[Immobilie(
                darlehen=[Darlehen(
                    rateMonatlich=0
                )]
            )]
        ),
        "baufinanzierungsrate": 0
    },
    {
        "stammdaten": Stammdaten(
            wohnartAs1=WohnartEnum.IM_EIGENEN_HAUS,
        ),
        "baufinanzierungsrate": 0
    }
])
def test_map_expense_warm_rent_eigentum(data):
    # WHEN
    response = map_expense_warm_rent(data["stammdaten"], None)

    # THEN
    assert_that(response, equal_to(data["baufinanzierungsrate"]))


def test_map_expense_warm_rent_none():
    # WHEN
    response = map_expense_warm_rent(None, None)

    # THEN
    assert_that(response, equal_to(0))

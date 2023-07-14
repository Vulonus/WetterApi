from typing import Union

from hamcrest import assert_that, equal_to
from parameterized import parameterized

from app.common.config import Config
from app.common.data_context import DataContext
from app.config import get_config_by_context


@parameterized.expand([
    [DataContext.TEST.value, DataContext.TEST.value],
    [DataContext.PROD.value, DataContext.PROD.value],
    [None, DataContext.TEST.value]])
def test_get_config_by_context__provide_data_context_test__return_corresponding_config(data_context_value: str,
                                                                                       expected_config_stage):
    # GIVEN
    expected_config = create_config_for_data_context(expected_config_stage)

    # WHEN
    returned_config = get_config_by_context(data_context_value)

    # THEN
    assert_that(returned_config, equal_to(expected_config))


def create_config_for_data_context(data_context_value) -> Union[Config, None]:
    if data_context_value == DataContext.TEST.value:
        return Config(
            host="https://green-1.consorsfinanz.de",
            version="6.4",
            tokenRootContext="/common-services/cfg",
            loanRootContext="/ratanet-api/cfg"
        )
    if data_context_value == DataContext.PROD.value:
        return Config(
            host="https://api.consorsfinanz.de",
            version="6.4",
            tokenRootContext="/common-services/cfg",
            loanRootContext="/ratanet-api/cfg"
        )
    return None

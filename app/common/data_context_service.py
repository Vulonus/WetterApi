from fastapi import Header, Query

from app.common.enums import DataContext
from app.config import HOST_MAPPING


class DataContextService:

    @staticmethod
    # pylint: disable=dangerous-default-value
    def determine_from_header(host=Header(None),
                              host_mapping=HOST_MAPPING) -> DataContext:
        if host and host in host_mapping:
            return DataContext[host_mapping[host]]

        return DataContext.TEST

    @staticmethod
    def determine_from_query(data_context=Query("TEST")) -> DataContext:
        return DataContext[data_context]

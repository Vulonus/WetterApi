import json
import logging
from contextlib import suppress

from app.common.errors.field_value_error import FieldValueError, DataError

logger = logging.getLogger(__name__)

api_clients = {
    "5s3a6furosl4rjioapehfajqdi": "ECON PROD",
    "5re6p9t42qt24ru534sgp78oir": "ECON TEST",
    "56obv2c03hf0er0gnfvg4inbsf": "DRKLEINRK"
}


def union(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            union(value, node)
        else:
            destination[key] = value

    return destination


def exclude_optional_dict(model):
    return union(model.dict(exclude_unset=True), model.dict(exclude_none=True))


def exclude_optional_json(model):
    return json.dumps(exclude_optional_dict(model))


def safe_get(data, *keys):
    with suppress(KeyError):
        value = None
        for key in keys:
            try:
                if data is not None and data[key] is not None:
                    if isinstance(data[key], dict):
                        data = data[key]
                    elif isinstance(data[key], list):
                        # pimp with multi index
                        if len(data[key]) > 0:
                            data = data[key][0]
                        else:
                            data = None
                    else:
                        value = data[key]
                else:
                    data = None

            except KeyError:
                return None
        if value is not None:
            return value

        return data


def is_json(my_json):
    try:
        json.loads(my_json)
    except ValueError:
        return False
    return True


def map_validation_error(error):
    errors = [
        DataError(field=str(err["loc"]), message=err["msg"]) for i, err in enumerate(error.errors())
    ]
    logger.info(errors)
    return json.loads(FieldValueError(errors=errors).json())

from json import JSONEncoder
from decimal import Decimal
from typing import Union


class DecimalEncoder(JSONEncoder):
    def default(self, o) -> Union[JSONEncoder, int, float]:
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return JSONEncoder.default(self, o)

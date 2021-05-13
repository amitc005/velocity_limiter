import json
from datetime import timedelta
from decimal import Decimal


def get_start_and_end_week_dates(query_date):
    start = query_date - timedelta(days=query_date.weekday())
    end = start + timedelta(days=6)
    return (
        start.replace(hour=0, minute=0, second=0, microsecond=0),
        end.replace(hour=23, minute=59, second=59, microsecond=0),
    )


def normalized_input_amount(amount):
    if amount[:1] == "$":
        return Decimal(amount[1:])

    return Decimal(amount)


class FileReader:
    def __init__(self, input_file):
        self._input_file = input_file

    def read(self):
        result = {}
        for input_value in self._input_file:
            input_value = json.loads(input_value)
            result[f"{input_value['id']}:{input_value['customer_id']}"] = input_value

        return list(result.values())

import json
from datetime import datetime
from decimal import Decimal
from decimal import InvalidOperation

from src.constants import DATE_FORMATE
from src.models import Transaction


class FileParser:
    def __init__(self, input_file):
        self._input_file = input_file

    def _normalized_input_amount(self, amount):
        if amount[:1] == "$":
            return Decimal(amount[1:])

        return Decimal(amount)

    def _validate_input_data(self, input_data):
        return (
            isinstance(input_data, dict)
            and (
                input_data.get("id")
                and input_data.get("customer_id")
                and input_data.get("load_amount")
                and input_data.get("time")
            )
            and self._validate_date(input_data)
        )

    def _validate_date(self, input_data):
        try:
            datetime.strptime(input_data["time"], DATE_FORMATE)

        except ValueError:
            return False
        else:
            return True

    def _normalized_and_validate_data(self, text):
        try:
            data = json.loads(text)
            if not self._validate_input_data(data):
                raise ValueError

            data["amount"] = self._normalized_input_amount(data["load_amount"])
            return data, True

        except (ValueError, InvalidOperation):
            return text, False

    def parse(self):
        for text in self._input_file:
            data, valid = self._normalized_and_validate_data(text)
            yield Transaction(data) if valid else None

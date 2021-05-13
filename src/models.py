from datetime import datetime
from decimal import Decimal

from .utils import get_start_and_end_week_date
from .utils import normalized_load_amount
from .validators import Validator


class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self._loads = []

    def add_load(self, load):
        load["load_amount"] = normalized_load_amount(load["load_amount"])
        load_record = LoadRecord(load)
        Validator.validate(self, load_record)
        self._loads.append(load_record)

    def filter_by_date(self, load_date):
        return [
            record
            for record in self._loads
            if load_date.date() == record.timestamp.date()
        ]

    def filter_by_week(self, load_date):
        start_date, end_date = get_start_and_end_week_date(load_date)
        return [
            record
            for record in self._loads
            if record.timestamp >= start_date and record.timestamp <= end_date
        ]


class LoadRecord:
    def __init__(self, input_data):
        self.id = input_data["id"]
        self.load_amount = Decimal(input_data["load_amount"])
        self.timestamp = datetime.strptime(input_data["time"], "%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def calculate_total_load_amount(records):
        return Decimal(sum([record.load_amount for record in records]))

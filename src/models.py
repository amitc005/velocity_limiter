from datetime import datetime

from .utils import get_start_and_end_week_date
from .validators import Validator


class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self._loads = []

    def add_load(self, load):
        Validator(load, self).validate()

        self._loads.append(load)

    def filter_by_per_day(self, load_date):
        return [
            record
            for record in self._loads
            if load_date.date()
            == datetime.strptime(record["time"], "%Y-%m-%dT%H:%M:%SZ").date()
        ]

    def filter_by_week(self, load_date):
        start_date, end_date = get_start_and_end_week_date(load_date)
        return [
            record
            for record in self._loads
            if load_date >= start_date and load_date <= end_date
        ]

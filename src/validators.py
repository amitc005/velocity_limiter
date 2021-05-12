import abc
from abc import ABC
from datetime import datetime
from decimal import Decimal

from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT


class AbStractValidator(ABC):
    def __init__(self, customer, load):
        self._customer = customer
        self._load = load
        self._load_date = datetime.strptime(load["time"], "%Y-%m-%dT%H:%M:%SZ")
        self._queried_records = self.get_query()

    @abc.abstractmethod
    def validate():
        pass

    @abc.abstractmethod
    def get_query():
        pass

    def calculate_total_amount(self):
        return Decimal(sum([record["load_amount"] for record in self._queried_records]))


class MaxLoadNumberValidator(AbStractValidator):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def validate(self):
        if len(self._queried_records) == MAX_DAILY_LOAD_NO:
            raise ValueError(
                f"Can not add more than 3 records for date {self._load_date}"
            )

    def get_query(self):
        return self._customer.filter_by_date(self._load_date)


class MaxAmountValidators(AbStractValidator):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def validate(self):
        if (
            self._load["load_amount"] + self.calculate_total_amount()
        ) > MAX_DAILY_LOAD_AMOUNT:
            raise ValueError("Load Amount exceed to 5000")

    def get_query(self):
        return self._customer.filter_by_date(self._load_date)


class MaxLoadWeeklyAmountValidator(AbStractValidator):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def validate(self):
        if (
            self._load["load_amount"] + self.calculate_total_amount()
        ) > MAX_WEEKLY_LOAD_AMOUNT:
            raise ValueError("Weekly Load Amount exceed")

    def get_query(self):
        return self._customer.filter_by_week(self._load_date)


class Validator:
    __validators = [
        MaxLoadNumberValidator,
        MaxAmountValidators,
        MaxLoadWeeklyAmountValidator,
    ]

    @classmethod
    def validate(cls, customer, load):
        for validator_cls in cls.__validators:
            validator_cls(customer, load).validate()

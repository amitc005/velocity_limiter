import abc
from abc import ABC
from decimal import Decimal

from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT


class AbStractValidator(ABC):
    def __init__(self, customer, load):
        self._customer = customer
        self._load = load
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
                f"Can not add more than 3 records for date {self._load.timestamp}"
            )

    def get_query(self):
        return self._customer.filter_by_date(self._load.timestamp)


class MaxAmountValidators(AbStractValidator):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def validate(self):
        from .models import LoadRecord

        if (
            self._load.load_amount
            + LoadRecord.calculate_total_load_amount(self._queried_records)
        ) > MAX_DAILY_LOAD_AMOUNT:
            raise ValueError("Load Amount exceed to 5000")

    def get_query(self):
        return self._customer.filter_by_date(self._load.timestamp)


class MaxLoadWeeklyAmountValidator(AbStractValidator):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def validate(self):
        from .models import LoadRecord

        if (
            self._load.load_amount
            + LoadRecord.calculate_total_load_amount(self._queried_records)
        ) > MAX_WEEKLY_LOAD_AMOUNT:
            raise ValueError(f"Weekly Load Amount exceed {self._queried_records}")

    def get_query(self):
        return self._customer.filter_by_week(self._load.timestamp)


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

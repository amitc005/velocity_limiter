from datetime import datetime
from decimal import Decimal

from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT


class MaxLoadNumberValidator:
    @staticmethod
    def validate(records):
        if len(records) == MAX_DAILY_LOAD_NO:
            raise ValueError("Can not add more than 3 records for date")


class MaxAmountValidators:
    @staticmethod
    def validate(current_load_amount, records):
        total_sum = current_load_amount + Decimal(
            sum([Decimal(record["load_amount"][1:]) for record in records])
        )
        if total_sum > MAX_DAILY_LOAD_AMOUNT:
            raise ValueError("Load Amount exceed to 5000")


class MaxLoadWeeklyAmountValidator:
    @staticmethod
    def validate(current_load_amount, week_record):
        total_week_sum = current_load_amount + Decimal(
            sum([Decimal(record["load_amount"][1:]) for record in week_record])
        )
        if total_week_sum > MAX_WEEKLY_LOAD_AMOUNT:
            raise ValueError("Weekly Load Amount exceed")


class Validator:
    __total_number_cls = [MaxLoadNumberValidator]
    __day_validator_cls = [MaxAmountValidators]
    __weekly_validator_cls = [MaxLoadWeeklyAmountValidator]

    def __init__(self, load, customer):
        self._current_load_date = datetime.strptime(load["time"], "%Y-%m-%dT%H:%M:%SZ")
        self._current_load_amount = Decimal(load["load_amount"][1:])

        self._current_day_records = customer.filter_by_per_day(self._current_load_date)
        self._weekly_records = customer.filter_by_week(self._current_load_date)

    def validate(self):
        for validator_cls in self.__total_number_cls:
            validator_cls.validate(self._current_day_records)

        for validator_cls in self.__day_validator_cls:
            validator_cls.validate(self._current_load_amount, self._current_day_records)

        for validator_cls in self.__weekly_validator_cls:
            validator_cls.validate(self._current_load_amount, self._weekly_records)

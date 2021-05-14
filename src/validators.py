from abc import ABC
from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT
from .constants import UTC_DATE_TIME_FORMAT
from .exceptions import DailyTransactionAmountException
from .exceptions import DailyTransactionLimitException
from .exceptions import WeeklyTransactionAmountException


class BaseLimiter(ABC):
    def __init__(self, customer, transaction):
        self._customer = customer
        self._transaction = transaction

    @abstractmethod
    def check():
        pass


class PerDayTransactionLimiter(BaseLimiter):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def check(self):
        from main import storage

        cache_data = storage.customer_cache.find_cache_by_date(
            self._customer, self._transaction.timestamp
        )
        if len(cache_data) >= MAX_DAILY_LOAD_NO:
            raise DailyTransactionLimitException(
                f"Can not add more than 3 records for date {self._transaction.timestamp}"
            )


class PerDayTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def check(self):
        from main import storage

        cache_data = storage.customer_cache.find_cache_by_date(
            self._customer.customer_id, self._transaction.timestamp.date()
        )

        total_transaction_amount = sum([Decimal(amount) for amount in cache_data])
        if (
            self._transaction.amount + total_transaction_amount
        ) > MAX_DAILY_LOAD_AMOUNT:
            raise DailyTransactionAmountException("Load Amount exceed to 5000")


class PerWeekTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def check(self):
        from main import storage

        cache_data = storage.customer_cache.find_cache_by_week(
            self._customer.customer_id, self._transaction.timestamp.date()
        )

        total_transaction_amount = sum([Decimal(amount) for amount in cache_data])

        if (
            self._transaction.amount + total_transaction_amount
        ) > MAX_WEEKLY_LOAD_AMOUNT:
            raise WeeklyTransactionAmountException(
                f"Weekly Load Amount exceed {self._customer_transactions}"
            )


class TransactionInputValidator:
    def __init__(self, data):
        self.data = data

    def validate(self):
        return (
            isinstance(self.data, dict)
            and (
                self.data.get("id")
                and self.data.get("customer_id")
                and self.data.get("load_amount")
                and self.data.get("time")
            )
            and datetime.strptime(self.data["time"], UTC_DATE_TIME_FORMAT)
        )

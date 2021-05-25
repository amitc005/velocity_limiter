from abc import ABC
from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from .constants import DAILY_LOAD_AMOUNT_LIMIT_ERROR
from .constants import DAILY_NO_LOAD_LIMIT_ERROR
from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT
from .constants import UTC_DATE_TIME_FORMAT
from .constants import WEEKLY_LOAD_AMOUNT_LIMIT_ERROR
from .exceptions import DailyTransactionAmountException
from .exceptions import DailyTransactionLimitException
from .exceptions import WeeklyTransactionAmountException
from .utils import week_date_range


class BaseLimiter(ABC):
    def __init__(self, customer, transaction):
        self._customer = customer
        self._transaction = transaction

    @abstractmethod
    def validate(customer_aggregated):
        pass


class PerDayTransactionLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def validate(self, customer_aggregated):

        _, total_count = customer_aggregated.get(
            self._customer.customer_id, self._transaction.timestamp
        )
        if total_count >= MAX_DAILY_LOAD_NO:
            raise DailyTransactionLimitException(
                DAILY_NO_LOAD_LIMIT_ERROR % self._transaction.timestamp
            )


class PerDayTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def validate(self, customer_aggregated):

        total_amount, _ = customer_aggregated.get(
            self._customer.customer_id, self._transaction.timestamp
        )
        if (self._transaction.amount + Decimal(total_amount)) > MAX_DAILY_LOAD_AMOUNT:
            raise DailyTransactionAmountException(DAILY_LOAD_AMOUNT_LIMIT_ERROR)


class PerWeekTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def validate(self, customer_aggregated):

        amount_list = []
        for date in week_date_range(self._transaction.timestamp.date()):
            amount, _ = customer_aggregated.get(self._customer.customer_id, date)
            if amount:
                amount_list.append(Decimal(amount))

        if (self._transaction.amount + sum(amount_list)) > MAX_WEEKLY_LOAD_AMOUNT:
            raise WeeklyTransactionAmountException(WEEKLY_LOAD_AMOUNT_LIMIT_ERROR)


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

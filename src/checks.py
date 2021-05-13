from abc import ABC
from abc import abstractmethod

from .constants import MAX_DAILY_LOAD_AMOUNT
from .constants import MAX_DAILY_LOAD_NO
from .constants import MAX_WEEKLY_LOAD_AMOUNT


class BaseLimiter(ABC):
    def __init__(self, customer, transaction):
        self._customer = customer
        self._transaction = transaction
        self._customer_transactions = self.get_customer_transactions()

    @abstractmethod
    def check():
        pass

    @abstractmethod
    def get_customer_transactions():
        pass


class PerDayTransactionLimiter(BaseLimiter):
    def __init__(self, customer, load):
        super().__init__(customer, load)

    def check(self):
        if len(self._customer_transactions) == MAX_DAILY_LOAD_NO:
            raise ValueError(
                f"Can not add more than 3 records for date {self._transaction.timestamp}"
            )

    def get_customer_transactions(self):
        return self._customer.get_transactions_by_date(self._transaction.timestamp)


class PerDayTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def check(self):
        from .models import Transaction

        if (
            self._transaction.amount
            + Transaction.calculate_total_amount(self._customer_transactions)
        ) > MAX_DAILY_LOAD_AMOUNT:
            raise ValueError("Load Amount exceed to 5000")

    def get_customer_transactions(self):
        return self._customer.get_transactions_by_date(self._transaction.timestamp)


class PerWeekTransactionAmountLimiter(BaseLimiter):
    def __init__(self, customer, transaction):
        super().__init__(customer, transaction)

    def check(self):
        from .models import Transaction

        if (
            self._transaction.amount
            + Transaction.calculate_total_amount(self._customer_transactions)
        ) > MAX_WEEKLY_LOAD_AMOUNT:
            raise ValueError(f"Weekly Load Amount exceed {self._customer_transactions}")

    def get_customer_transactions(self):
        return self._customer.get_transactions_by_week(self._transaction.timestamp)

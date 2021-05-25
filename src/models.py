from datetime import datetime
from decimal import Decimal

from src.constants import UTC_DATE_TIME_FORMAT
from src.validators import PerDayTransactionAmountLimiter
from src.validators import PerDayTransactionLimiter
from src.validators import PerWeekTransactionAmountLimiter


class Customer:
    __limiter_list = [
        PerDayTransactionLimiter,
        PerDayTransactionAmountLimiter,
        PerWeekTransactionAmountLimiter,
    ]

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def _validate_transaction(self, transaction, aggregated_data):
        for checker_cls in self.__limiter_list:
            checker_cls(self, transaction).validate(aggregated_data)

    def perform_transaction(self, transaction, aggregated_data):
        self._validate_transaction(transaction, aggregated_data)


class Transaction:
    def __init__(self, input_data):
        self.id = input_data["id"]
        self.customer_id = input_data["customer_id"]

        self.amount = self._normalized_input_amount(input_data["load_amount"])
        self.timestamp = datetime.strptime(input_data["time"], UTC_DATE_TIME_FORMAT)

    def _normalized_input_amount(self, amount):
        if amount[:1] == "$":
            return Decimal(amount[1:])

        return Decimal(amount)

    @property
    def transaction_key(self):
        return f"{self.customer_id}:{self.id}"

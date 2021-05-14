from datetime import datetime
from decimal import Decimal

from src.constants import UTC_DATE_TIME_FORMAT
from src.utils import get_start_and_end_week_dates
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
        self._transactions = {}

    def _validate_transaction(self, transaction):
        for checker_cls in self.__limiter_list:
            checker_cls(self, transaction).check()

    def is_transaction_processed(self, id):
        return id in self._transactions or id in self._rejected_transaction_ids

    def perform_transaction(self, transaction):
        self._validate_transaction(transaction)
        self._transactions[transaction.id] = transaction

    def get_transactions_by_date(self, query_date):
        return [
            record
            for record in self._transactions.values()
            if query_date.date() == record.timestamp.date()
        ]

    def get_transactions_by_week(self, query_date):
        start_date, end_date = get_start_and_end_week_dates(query_date)
        return [
            record
            for record in self._transactions.values()
            if record.timestamp >= start_date and record.timestamp <= end_date
        ]


class Transaction(object):
    def __init__(self, input_data):
        self.id = input_data["id"]
        self.customer_id = input_data["customer_id"]

        self.amount = self._normalized_input_amount(input_data["load_amount"])
        self.timestamp = datetime.strptime(input_data["time"], UTC_DATE_TIME_FORMAT)

    def _normalized_input_amount(self, amount):
        if amount[:1] == "$":
            return Decimal(amount[1:])

        return Decimal(amount)

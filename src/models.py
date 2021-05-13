from datetime import datetime
from decimal import Decimal

from src.checks import PerDayTransactionAmountLimiter
from src.checks import PerDayTransactionLimiter
from src.checks import PerWeekTransactionAmountLimiter
from src.constants import DATE_FORMATE
from src.utils import get_start_and_end_week_dates


class Customer:
    __limiter_list = [
        PerDayTransactionLimiter,
        PerDayTransactionAmountLimiter,
        PerWeekTransactionAmountLimiter,
    ]

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self._transactions = {}
        self._rejected_transaction_ids = []

    def _validate_transaction(self, transaction):
        for checker_cls in self.__limiter_list:
            checker_cls(self, transaction).check()

    def is_transaction_processed(self, id):
        return id in self._transactions or id in self._rejected_transaction_ids

    def add_transaction(self, transaction):
        if self.is_transaction_processed(transaction.id):
            return {
                "id": transaction.id,
                "customer_id": transaction.customer_id,
                "accepted": False,
            }

        accepted = True
        try:
            self._validate_transaction(transaction)
            self._transactions[transaction.id] = transaction

        except ValueError:
            accepted = False
            self._rejected_transaction_ids.append(transaction.id)

        return {
            "id": transaction.id,
            "customer_id": self.customer_id,
            "accepted": accepted,
        }

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

        self.amount = Decimal(input_data["amount"])
        self.timestamp = datetime.strptime(input_data["time"], DATE_FORMATE)

    @staticmethod
    def calculate_total_amount(records):
        return Decimal(sum([record.amount for record in records]))

from datetime import datetime
from decimal import Decimal

from .constants import DATE_FORMATE
from .utils import get_start_and_end_week_dates
from .utils import normalized_input_amount
from .validators import Validator


class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self._transactions = []

    def add_transaction(self, input_transaction):
        if self.customer_id != input_transaction["customer_id"]:
            raise ValueError("Customer ID does not match with transaction customer ID")

        input_transaction["amount"] = normalized_input_amount(
            input_transaction["load_amount"]
        )
        transaction = Transaction(input_transaction)
        accepted = True
        try:
            Validator.validate(self, transaction)
            self._transactions.append(transaction)
        except (ValueError, KeyError):
            accepted = False

        return {
            "id": input_transaction["id"],
            "customer_id": input_transaction["customer_id"],
            "accepted": accepted,
        }

    def get_transactions_by_date(self, query_date):
        return [
            record
            for record in self._transactions
            if query_date.date() == record.timestamp.date()
        ]

    def get_transactions_by_week(self, query_date):
        start_date, end_date = get_start_and_end_week_dates(query_date)
        return [
            record
            for record in self._transactions
            if record.timestamp >= start_date and record.timestamp <= end_date
        ]


class Transaction:
    def __init__(self, input_data):
        self.id = input_data["id"]
        self.customer_id = input_data["customer_id"]

        self.amount = Decimal(input_data["amount"])
        self.timestamp = datetime.strptime(input_data["time"], DATE_FORMATE)

    @staticmethod
    def calculate_total_amount(records):
        return Decimal(sum([record.amount for record in records]))

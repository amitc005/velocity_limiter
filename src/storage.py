from abc import ABC
from decimal import Decimal

from .exceptions import DuplicateCustomerException
from .exceptions import DuplicateTransactionException
from .models import Customer


class Storage(ABC):
    def __init__(self):
        pass

    def add(self):
        pass

    def get(self):
        pass

    def exist(self):
        pass

    def update(self):
        pass


class TransactionLogStorage(Storage):
    def __init__(self):
        self._transaction_log = []

    def add(self, key):
        if self.exist(key):
            raise DuplicateTransactionException(f"Transaction already processed: {key}")

        self._transaction_log.append(key)

    def exist(self, key):
        return key in self._transaction_log


class TransactionStorage(Storage):
    def __init__(self):
        self._transactions = {}

    def add(self, transaction):
        self._transactions[transaction.transaction_key] = transaction


class CustomerStorage(Storage):
    def __init__(self):
        self._customer_records = {}

    def get(self, customer_id):
        return self._customer_records.get(customer_id)

    def add(self, customer_id):
        if self.get(customer_id):
            raise DuplicateCustomerException(f"Duplicate customer ID: {customer_id}")

        self._customer_records[customer_id] = Customer(customer_id)
        return self._customer_records[customer_id]


class CustomerAggregatedStorage(Storage):
    DATE_FORMAT = "%Y%m%d"

    def __init__(self):
        self._data = {}

    def update(self, customer_id, transaction):
        key = transaction.timestamp.date().strftime(self.DATE_FORMAT)
        amount = transaction.amount

        data = self._data.get(customer_id)

        if not data:
            self._data[customer_id] = {key: (str(amount), 1)}

        elif not data.get(key):
            data[key] = (str(amount), 1)

        else:
            total_amount, total_count = self._data[customer_id][key]
            new_total_amount, new_count = (
                amount + Decimal(total_amount),
                total_count + 1,
            )
            data[key] = (str(new_total_amount), new_count)

    def get(self, customer_id, date):
        customer_cache = self._data.get(customer_id)
        key = date.strftime(self.DATE_FORMAT)
        if not customer_cache or not customer_cache.get(key):
            return 0, 0

        return customer_cache[key]

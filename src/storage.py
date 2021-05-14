from decimal import Decimal

from .exceptions import DuplicateCustomerException
from .exceptions import DuplicateTransactionException
from .exceptions import TransactionException
from .models import Customer
from .models import Transaction


class ApplicationStorage:
    def __init__(self):
        self._customer_records = {}
        self._processed_transaction = []

    def get_customer(self, customer_id):
        return self._customer_records.get(customer_id)

    def add_customer(self, customer_id):
        if self._customer_records.get(customer_id):
            raise DuplicateCustomerException(f"Duplicate customer ID: {customer_id}")

        self._customer_records[customer_id] = Customer(customer_id)
        return self._customer_records[customer_id]

    def _verify_key(self, key):
        if key in self._processed_transaction:
            raise DuplicateTransactionException(f"Transaction already processed: {key}")

    def _add_process_key(self, key):
        self._verify_key(key)
        self._processed_transaction.append(key)

    def add_transaction(self, data, customer):
        from main import aggregated_storage

        try:
            transaction = Transaction(data)
            process_key = f"{customer.customer_id}:{transaction.id}"
            self._add_process_key(process_key)
            customer.perform_transaction(transaction)
            aggregated_storage.update(customer.customer_id, transaction)

            return {
                "id": data["id"],
                "customer_id": data["customer_id"],
                "accepted": True,
            }

        except TransactionException:
            return {
                "id": data.get("id"),
                "customer_id": data.get("customer_id"),
                "accepted": False,
            }


class CustomerAggregatedStorage:
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

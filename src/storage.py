from decimal import Decimal

from .exceptions import TransactionException
from .models import Customer
from .models import Transaction


class ApplicationStorage:
    def __init__(self):
        self._customer_records = {}
        self._customer_transaction_list = []
        self.customer_cache = CustomerCacheStorage()

    def get_customer(self, customer_id):
        return self._customer_records.get(customer_id)

    def add_customer(self, customer_id):
        if self._customer_records.get(customer_id):
            raise ValueError("Duplicate Customer.")

        self._customer_records[customer_id] = Customer(customer_id)
        return self._customer_records[customer_id]

    def add_transaction(self, data):
        try:
            transaction = Transaction(data)
            customer = self.get_customer(transaction.customer_id) or self.add_customer(
                transaction.customer_id
            )

            transaction_key = f"{customer.customer_id}:{transaction.id}"
            if transaction_key in self._customer_transaction_list:
                raise ValueError(f"Duplicate Transaction Key: {transaction_key}")

            self._customer_transaction_list.append(transaction_key)
            customer.perform_transaction(transaction)
            self.customer_cache.update(customer, transaction)

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


class CustomerCacheStorage:
    DATE_FORMAT = "%Y%m%d"

    def __init__(self):
        self._cache_data = {}

    def update(self, customer, transaction):
        date_key = transaction.timestamp.date().strftime(self.DATE_FORMAT)
        customer_id = customer.customer_id
        amount = transaction.amount
        customer_cache = self._cache_data.get(customer_id)

        if not customer_cache:
            self._cache_data[customer_id] = {date_key: (str(amount), 1)}

        elif not customer_cache.get(date_key):
            customer_cache[date_key] = (str(amount), 1)

        else:
            old_total_amount, old_count = self._cache_data[customer.customer_id][
                date_key
            ]
            new_total_amount, new_count = (
                amount + Decimal(old_total_amount),
                old_count + 1,
            )
            customer_cache[date_key] = (str(new_total_amount), new_count)

    def get(self, customer_id, date):
        customer_cache = self._cache_data.get(customer_id)
        key = date.strftime(self.DATE_FORMAT)

        if not customer_cache or not customer_cache.get(key):
            return 0, 0

        else:
            return customer_cache[key]

from .exceptions import TransactionException
from .models import Customer
from .models import Transaction
from .utils import week_date_range_generator


class ApplicationStorage:
    def __init__(self):
        self._customer_records = {}
        self._customer_transaction_list = []
        self.customer_cache = CustomerCache()

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
            self.customer_cache.update_cache(customer, transaction)

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


class CustomerCache:
    DATE_FORMAT = "%Y%m%d"

    def __init__(self):
        self._cache_data = {}

    def update_cache(self, customer, transaction):
        customer_cache = self._cache_data.get(customer.customer_id)
        date = transaction.timestamp.date().strftime(self.DATE_FORMAT)

        if not customer_cache:
            self._cache_data[customer.customer_id] = {date: [str(transaction.amount)]}
        else:
            customer_cache[date] = customer_cache.get(date, []) + [
                str(transaction.amount)
            ]

    def find_cache_by_date(self, customer_id, date):
        return (
            self._cache_data[customer_id].get(date.strftime(self.DATE_FORMAT), [])
            if self._cache_data.get(customer_id)
            else []
        )

    def find_cache_by_week(self, customer_id, date):
        customer_cache = self._cache_data.get(customer_id)
        result = []
        if not customer_cache:
            return result

        for week_date in week_date_range_generator(date):
            result += customer_cache.get(week_date.strftime(self.DATE_FORMAT), [])

        return result

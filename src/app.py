from .models import Customer


class App:
    def __init__(self):
        self._customer_records = {}

    def add_transaction(self, transaction):
        customer = self._customer_records.get(transaction["customer_id"])
        if not customer:
            customer = self.add_customer(transaction["customer_id"])

        return customer.add_transaction(transaction)

    def add_customer(self, customer_id):
        customer = Customer(customer_id)
        self._customer_records[customer.customer_id] = customer
        return customer

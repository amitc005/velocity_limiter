from .models import Customer


class Storage:
    def __init__(self):
        self._customer_records = {}

    def get_customer(self, customer_id):
        return self._customer_records.get(customer_id)

    def add_customer(self, customer_id):
        if self._customer_records.get(customer_id):
            raise ValueError("Duplicate Customer.")

        self._customer_records[customer_id] = Customer(customer_id)
        return self._customer_records[customer_id]

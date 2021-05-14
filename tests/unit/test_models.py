from datetime import datetime
from decimal import Decimal

import pytest

from src.constants import UTC_DATE_TIME_FORMAT
from src.models import Customer
from src.models import Transaction


class TestCustomer:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.customer = Customer("528")

    def test_create_customer(self):
        customer_id = "1"
        customer = Customer(customer_id)
        assert customer
        assert customer.customer_id == customer_id

    def test_add_transaction(self):
        input_data = [
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$3000.00",
                "time": "2000-01-01T00:00:00Z",
            },
            {
                "id": "30081",
                "customer_id": "528",
                "load_amount": "$1000.00",
                "time": "2000-01-01T01:01:22Z",
            },
            {
                "id": "26540",
                "customer_id": "528",
                "load_amount": "$1000.00",
                "time": "2000-01-02T02:02:44Z",
            },
        ]
        for data in input_data:
            transaction = Transaction(data)
            self.customer.perform_transaction(transaction)

        assert isinstance(self.customer.transaction_list, list)

        len(self.customer.transaction_list) == len(data)
        for transaction in self.customer.transaction_list:
            assert transaction
            assert isinstance(transaction, Transaction)


class TestTransaction:
    @pytest.fixture(autouse=True)
    def set_up(self):
        pass

    def test_create_transaction(self):
        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3000.00",
            "time": "2000-01-01T00:00:00Z",
        }
        transaction = Transaction(data)
        assert transaction
        assert transaction.id == data["id"]
        assert transaction.customer_id == data["customer_id"]

        assert isinstance(transaction.amount, Decimal)
        assert transaction.amount == Decimal(data["load_amount"][1:])

        assert isinstance(transaction.timestamp, datetime)
        assert transaction.timestamp == datetime.strptime(
            data["time"], UTC_DATE_TIME_FORMAT
        )

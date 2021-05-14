from datetime import datetime
from typing import Tuple

import pytest

from main import aggregated_storage
from src.constants import UTC_DATE_TIME_FORMAT
from src.exceptions import DuplicateCustomerException
from src.exceptions import DuplicateTransactionException
from src.models import Customer
from src.models import Transaction
from src.storage import ApplicationStorage
from src.storage import CustomerAggregatedStorage


class TestApplicationStorage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.storage = ApplicationStorage()

    def _verify_aggregated_storage(self, customer_id, date, amount, count):
        record = aggregated_storage.get(customer_id, date)
        assert record[0] == amount
        assert record[1] == count

    def test_add_customer(self):
        customer_id = 1
        assert self.storage.get_customer(customer_id) is None

        customer = self.storage.add_customer(customer_id)
        assert customer
        assert isinstance(customer, Customer)
        assert customer.customer_id == customer_id
        assert self.storage.get_customer(customer_id)

    def test_add_duplicate_customer(self):
        customer_id = 1
        assert self.storage.get_customer(customer_id) is None

        customer = self.storage.add_customer(customer_id)
        assert customer
        assert isinstance(customer, Customer)
        assert customer.customer_id == customer_id
        with pytest.raises(DuplicateCustomerException):
            customer = self.storage.add_customer(customer_id)

    def test_add_transaction(self):
        customer_id = 1
        assert self.storage.get_customer(customer_id) is None
        customer = self.storage.add_customer(customer_id)

        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }

        res = self.storage.add_transaction(data, customer)

        assert isinstance(res, dict)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res

        assert res["id"] == data["id"]
        assert res["customer_id"] in data["customer_id"]
        assert res["accepted"]
        date = datetime.strptime(data["time"], UTC_DATE_TIME_FORMAT)
        self._verify_aggregated_storage(customer_id, date, data["load_amount"][1:], 1)
        # Duplicate
        with pytest.raises(DuplicateTransactionException):
            self.storage.add_transaction(data, customer)


class TestCustomerAggregatedStorage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.storage = CustomerAggregatedStorage()

    def test_get(self):
        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
        date = datetime.strptime(data["time"], UTC_DATE_TIME_FORMAT)
        customer_id = 1
        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        assert len(record) == 2
        total_amount, total_count = record
        assert total_amount == 0
        assert total_amount == total_count

        transaction = Transaction(data)
        self.storage.update(customer_id, transaction)
        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        total_amount, total_count = record
        assert total_amount == data["load_amount"][1:]
        assert total_count == 1

    def test_get_and_update_with_multiple(self):
        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3000.00",
            "time": "2000-01-01T00:00:00Z",
        }
        date = datetime.strptime(data["time"], UTC_DATE_TIME_FORMAT)
        customer_id = 1
        transaction = Transaction(data)
        self.storage.update(customer_id, transaction)

        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        total_amount, total_count = record
        assert total_amount == data["load_amount"][1:]
        assert total_count == 1

        data = {
            "id": "1234",
            "customer_id": "528",
            "load_amount": "$2000.00",
            "time": "2000-01-01T00:00:00Z",
        }
        transaction = Transaction(data)
        self.storage.update(customer_id, transaction)

        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        total_amount, total_count = record
        assert total_amount == "5000.00"
        assert total_count == 2

    def test_get_and_update_with_multiple_with_different_date(self):
        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3000.00",
            "time": "2000-01-01T00:00:00Z",
        }
        date = datetime.strptime(data["time"], UTC_DATE_TIME_FORMAT)
        customer_id = 1
        transaction = Transaction(data)
        self.storage.update(customer_id, transaction)

        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        total_amount, total_count = record
        assert total_amount == data["load_amount"][1:]
        assert total_count == 1

        data = {
            "id": "1234",
            "customer_id": "528",
            "load_amount": "$2000.00",
            "time": "2000-01-02T00:00:00Z",
        }
        transaction = Transaction(data)
        self.storage.update(customer_id, transaction)
        date = datetime.strptime(data["time"], UTC_DATE_TIME_FORMAT)
        record = self.storage.get(customer_id, date)
        assert record
        assert isinstance(record, Tuple)
        total_amount, total_count = record
        assert total_amount == data["load_amount"][1:]
        assert total_count == 1

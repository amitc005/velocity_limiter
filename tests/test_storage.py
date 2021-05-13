import pytest

from src.models import Customer
from src.storage import Storage


class TestStorage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.storage = Storage()

    def test_add_customer(self):
        test_customer_id = "1"
        assert self.storage.customers == {}

        self.storage.add_customer(test_customer_id)
        assert self.storage.customers != {}
        assert len(self.storage.customers.keys()) == 1

    def test_multiple_add_customers(self):
        test_customer_id = "1"
        test_customer_two = "2"

        assert self.storage.customers == {}

        self.storage.add_customer(test_customer_id)
        assert self.storage.customers != {}
        assert len(self.storage.customers.keys()) == 1

        self.storage.add_customer(test_customer_two)
        assert len(self.storage.customers.keys()) == 2

    def test_get_customer(self):
        test_customer_one = "1"
        assert self.storage.customers == {}

        self.storage.add_customer(test_customer_one)
        assert self.storage.customers != {}
        assert len(self.storage.customers.keys()) == 1

        customer = self.storage.get_customer(test_customer_one)
        assert customer
        assert isinstance(customer, Customer)
        assert customer.customer_id == test_customer_one

    def test_get_multiple_customers(self):
        test_customer_one = "1"
        test_customer_two = "2"
        assert self.storage.customers == {}

        self.storage.add_customer(test_customer_one)
        self.storage.add_customer(test_customer_two)
        assert self.storage.customers != {}
        assert len(self.storage.customers.keys()) == 2

        customer_one = self.storage.get_customer(test_customer_one)
        assert customer_one
        assert isinstance(customer_one, Customer)
        assert customer_one.customer_id == test_customer_one

        customer_two = self.storage.get_customer(test_customer_two)
        assert customer_two
        assert isinstance(customer_two, Customer)
        assert customer_two.customer_id == test_customer_two

    def test_add_duplicate_customers(self):
        test_customer_id = "1"
        test_customer_two = "2"
        assert self.storage.customers == {}

        self.storage.add_customer(test_customer_id)
        self.storage.add_customer(test_customer_two)

        assert self.storage.customers != {}
        assert len(self.storage.customers.keys()) == 2
        with pytest.raises(ValueError):
            self.storage.add_customer(test_customer_id)

        with pytest.raises(ValueError):
            self.storage.add_customer(test_customer_two)

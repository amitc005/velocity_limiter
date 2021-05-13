from datetime import datetime
from decimal import Decimal

import pytest

from src.constants import DATE_FORMATE
from src.models import Customer
from src.models import LoadRecord


class TestCustomer:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.customer = Customer("528")

    def test_filter_by_date(self):
        input_load_records = [
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
        for load_record in input_load_records:
            self.customer.add_load(load_record)

        load_date = datetime.strptime("2000-01-01T00:00:00Z", DATE_FORMATE)
        result = self.customer.get_transactions_by_date(load_date)
        assert isinstance(result, list)
        assert len(result) == 2

        self.customer.add_load(
            {
                "id": "30281",
                "customer_id": "528",
                "load_amount": "$1000.00",
                "time": "2000-01-01T01:01:22Z",
            },
        )
        result = self.customer.get_transactions_by_date(load_date)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_filter_by_week(self):
        input_load_records = [
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-06T00:00:00Z",
            },
            {
                "id": "30081",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-05T01:01:22Z",
            },
            {
                "id": "26536",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-08T02:02:44Z",
            },
            {
                "id": "26534",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-04T02:02:44Z",
            },
            {
                "id": "26540",
                "customer_id": "528",
                "load_amount": "$404.56",
                "time": "2021-01-15T02:02:44Z",
            },
        ]
        for load_record in input_load_records:
            self.customer.add_load(load_record)

        load_date = datetime.strptime("2021-01-04T02:02:44Z", DATE_FORMATE)
        result = self.customer.get_transaction_by_week(load_date)
        assert isinstance(result, list)
        assert len(result) == 4

    def test_add_loads_with_max_load_number_exceed_per_day(self):
        records = [
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
                "time": "2000-01-01T02:02:44Z",
            },
        ]
        for input_load in records:
            self.customer.add_load(input_load)

        error_record = {
            "id": "26241",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2000-01-01T02:02:44Z",
        }
        with pytest.raises(ValueError):
            self.customer.add_load(error_record)

    def test_add_loads_with_max_load_amount_exceed_per_day(self):
        records = [
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$3000.00",
                "time": "2000-01-01T00:00:00Z",
            },
            {
                "id": "30081",
                "customer_id": "528",
                "load_amount": "$2000.00",
                "time": "2000-01-01T01:01:22Z",
            },
        ]

        for input_load in records:
            self.customer.add_load(input_load)

        error_record = {
            "id": "26540",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2000-01-01T02:02:44Z",
        }
        with pytest.raises(ValueError):
            self.customer.add_load(error_record)

    def test_add_loads_with_max_load_amount_exceed_per_week(self):
        records = [
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-06T00:00:00Z",
            },
            {
                "id": "30081",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-05T01:01:22Z",
            },
            {
                "id": "26536",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-08T02:02:44Z",
            },
            {
                "id": "26534",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-04T02:02:44Z",
            },
        ]
        for input_load in records:
            self.customer.add_load(input_load)

        error_record = {
            "id": "26540",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2021-01-09T02:02:44Z",
        }
        with pytest.raises(ValueError):
            self.customer.add_load(error_record)

    def test_add_load_with_invalid_date(self):
        input_load = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$5000.00",
            "time": "2021-0-0600:00:00Z",
        }
        with pytest.raises(ValueError):
            self.customer.add_load(input_load)

    def test_add_load_with_with_missing_fields(self):
        input_load = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$5000.00",
        }
        with pytest.raises(KeyError):
            self.customer.add_load(input_load)


class TestLoadRecord:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.customer = Customer("528")

    @pytest.mark.parametrize(
        "input_data, amount",
        [
            (
                [
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
                ],
                "5000.00",
            ),
            (
                [
                    {
                        "id": "15887",
                        "customer_id": "528",
                        "load_amount": "$2340.10",
                        "time": "2021-01-06T00:00:00Z",
                    },
                    {
                        "id": "30081",
                        "customer_id": "528",
                        "load_amount": "$4800.00",
                        "time": "2021-01-05T01:01:22Z",
                    },
                    {
                        "id": "26536",
                        "customer_id": "528",
                        "load_amount": "$5000.00",
                        "time": "2021-01-08T02:02:44Z",
                    },
                    {
                        "id": "26534",
                        "customer_id": "528",
                        "load_amount": "$5000.00",
                        "time": "2021-01-04T02:02:44Z",
                    },
                ],
                "17140.10",
            ),
        ],
    )
    def test_filter_by_date(self, input_data, amount):
        for load in input_data:
            self.customer.add_load(load)
        assert Decimal(amount) == LoadRecord.calculate_total_load_amount(
            self.customer._loads
        )

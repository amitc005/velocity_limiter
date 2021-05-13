from datetime import datetime

import pytest

from src.constants import DATE_FORMATE
from src.models import Customer


class TestCustomer:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.customer = Customer("528")

    def test_filter_by_date(self):
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
            res = self.customer.add_transaction(data)
            assert "id" in res
            assert "customer_id" in res
            assert "accepted" in res

            assert res["id"] == data["id"]
            assert res["customer_id"] == data["customer_id"]
            assert res["accepted"] is True

        txn_date = datetime.strptime("2000-01-01T00:00:00Z", DATE_FORMATE)
        result = self.customer.get_transactions_by_date(txn_date)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_filter_by_week(self):
        input_data = [
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
        for data in input_data:
            res = self.customer.add_transaction(data)
            assert "id" in res
            assert "customer_id" in res
            assert "accepted" in res

            assert res["id"] == data["id"]
            assert res["customer_id"] == data["customer_id"]
            assert res["accepted"] is True

        load_date = datetime.strptime("2021-01-04T02:02:44Z", DATE_FORMATE)
        result = self.customer.get_transactions_by_week(load_date)
        assert isinstance(result, list)
        assert len(result) == 4

    def test_add_loads_with_max_load_number_exceed_per_day(self):
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
                "time": "2000-01-01T02:02:44Z",
            },
        ]
        for data in input_data:
            res = self.customer.add_transaction(data)
            assert "id" in res
            assert "customer_id" in res
            assert "accepted" in res

            assert res["id"] == data["id"]
            assert res["customer_id"] == data["customer_id"]
            assert res["accepted"] is True

        error_record = {
            "id": "26241",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2000-01-01T02:02:44Z",
        }

        res = self.customer.add_transaction(error_record)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res

        assert res["id"] == error_record["id"]
        assert res["customer_id"] == error_record["customer_id"]
        assert res["accepted"] is False

    def test_add_loads_with_max_load_amount_exceed_per_day(self):
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
                "load_amount": "$2000.00",
                "time": "2000-01-01T01:01:22Z",
            },
        ]

        for data in input_data:
            res = self.customer.add_transaction(data)
            assert "id" in res
            assert "customer_id" in res
            assert "accepted" in res

            assert res["id"] == data["id"]
            assert res["customer_id"] == data["customer_id"]
            assert res["accepted"] is True

        error_record = {
            "id": "26540",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2000-01-01T02:02:44Z",
        }

        res = self.customer.add_transaction(error_record)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res

        assert res["id"] == error_record["id"]
        assert res["customer_id"] == error_record["customer_id"]
        assert res["accepted"] is False

    def test_add_loads_with_max_load_amount_exceed_per_week(self):
        input_data = [
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
        for data in input_data:
            res = self.customer.add_transaction(data)
            assert "id" in res
            assert "customer_id" in res
            assert "accepted" in res

            assert res["id"] == data["id"]
            assert res["customer_id"] == data["customer_id"]
            assert res["accepted"] is True

        error_record = {
            "id": "26540",
            "customer_id": "528",
            "load_amount": "$404.56",
            "time": "2021-01-09T02:02:44Z",
        }
        res = self.customer.add_transaction(error_record)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res

        assert res["id"] == error_record["id"]
        assert res["customer_id"] == error_record["customer_id"]
        assert res["accepted"] is False

    def test_add_load_with_invalid_date(self):
        error_data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$5000.00",
            "time": "2021-0-0600:00:00Z",
        }
        res = self.customer.add_transaction(error_data)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res
        assert res["id"] == ""
        assert res["customer_id"] == ""
        assert res["accepted"] is False

    def test_add_load_with_with_missing_fields(self):
        error_data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$5000.00",
        }
        res = self.customer.add_transaction(error_data)
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res
        assert res["id"] == ""
        assert res["customer_id"] == ""
        assert res["accepted"] is False

    def test_add_load_with_with_invalid_input_data(self):
        res = self.customer.add_transaction("")
        assert "id" in res
        assert "customer_id" in res
        assert "accepted" in res
        assert res["id"] == ""
        assert res["customer_id"] == ""
        assert res["accepted"] is False


# class TestLoadRecord:
#     @pytest.fixture(autouse=True)
#     def set_up(self):
#         self.customer = Customer("528")

#     @pytest.mark.parametrize(
#         "input_data, amount",
#         [
#             (
#                 [
#                     {
#                         "id": "15887",
#                         "customer_id": "528",
#                         "load_amount": "$3000.00",
#                         "time": "2000-01-01T00:00:00Z",
#                     },
#                     {
#                         "id": "30081",
#                         "customer_id": "528",
#                         "load_amount": "$1000.00",
#                         "time": "2000-01-01T01:01:22Z",
#                     },
#                     {
#                         "id": "26540",
#                         "customer_id": "528",
#                         "load_amount": "$1000.00",
#                         "time": "2000-01-02T02:02:44Z",
#                     },
#                 ],
#                 "5000.00",
#             ),
#             (
#                 [
#                     {
#                         "id": "15887",
#                         "customer_id": "528",
#                         "load_amount": "$2340.10",
#                         "time": "2021-01-06T00:00:00Z",
#                     },
#                     {
#                         "id": "30081",
#                         "customer_id": "528",
#                         "load_amount": "$4800.00",
#                         "time": "2021-01-05T01:01:22Z",
#                     },
#                     {
#                         "id": "26536",
#                         "customer_id": "528",
#                         "load_amount": "$5000.00",
#                         "time": "2021-01-08T02:02:44Z",
#                     },
#                     {
#                         "id": "26534",
#                         "customer_id": "528",
#                         "load_amount": "$5000.00",
#                         "time": "2021-01-04T02:02:44Z",
#                     },
#                 ],
#                 "17140.10",
#             ),
#         ],
#     )
#     def test_filter_by_date(self, input_data, amount):
#         for load in input_data:
#             self.customer.add_load(load)
#         assert Decimal(amount) == LoadRecord.calculate_total_load_amount(
#             self.customer._loads
#         )

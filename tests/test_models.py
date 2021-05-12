import pytest

from src.app import file_repository


class TestCustomer:
    @pytest.fixture()
    def set_up(self):
        pass

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
            {
                "id": "26241",
                "customer_id": "528",
                "load_amount": "$404.56",
                "time": "2000-01-01T02:02:44Z",
            },
        ]
        expected = [
            {"id": "15887", "customer_id": "528", "accepted": True},
            {"id": "30081", "customer_id": "528", "accepted": True},
            {"id": "26540", "customer_id": "528", "accepted": True},
            {"id": "26241", "customer_id": "528", "accepted": False},
        ]

        output_result = file_repository(records)
        assert output_result == expected

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
            {
                "id": "26540",
                "customer_id": "528",
                "load_amount": "$404.56",
                "time": "2000-01-01T02:02:44Z",
            },
        ]
        expected = [
            {"id": "15887", "customer_id": "528", "accepted": True},
            {"id": "30081", "customer_id": "528", "accepted": True},
            {"id": "26540", "customer_id": "528", "accepted": False},
        ]

        output_result = file_repository(records)
        assert output_result == expected

    def test_add_loads_with_max_load_amount_exceed_per_week(self):
        records = [
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$5000.00",
                "time": "2021-01-03T00:00:00Z",
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
                "time": "2021-01-09T02:02:44Z",
            },
        ]
        expected = [
            {"id": "15887", "customer_id": "528", "accepted": True},
            {"id": "30081", "customer_id": "528", "accepted": True},
            {"id": "26536", "customer_id": "528", "accepted": True},
            {"id": "26534", "customer_id": "528", "accepted": True},
            {"id": "26540", "customer_id": "528", "accepted": False},
        ]

        output_result = file_repository(records)
        assert output_result == expected

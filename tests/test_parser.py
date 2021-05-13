import io
import json
from datetime import datetime
from decimal import Decimal

import pytest

from src.constants import DATE_FORMATE
from src.models import Transaction
from src.parser import FileParser


class TestFileParser:
    @pytest.fixture(autouse=True)
    def set_up(self):
        pass

    def test_parser_with_multiple_records(self):
        file_txt = '{"id":"15887","customer_id":"528","load_amount":"$3318.47","time":"2000-01-01T00:00:00Z"}\n'
        file_txt += '{"id":"30081","customer_id":"154","load_amount":"$1413.18","time":"2000-01-01T01:01:22Z"}\n'
        file_txt += '{"id":"26540","customer_id":"426","load_amount":"$404.56","time":"2000-01-01T02:02:44Z"}\n'
        file_txt += '{"id":"10694","customer_id":"1","load_amount":"$785.11","time":"2000-01-01T03:04:06Z"}\n'
        file_txt += '{"id":"15089","customer_id":"205","load_amount":"$2247.28","time":"2000-01-01T04:05:28Z"}\n'
        file_txt += '{"id":"3211","customer_id":"409","load_amount":"$314.45","time":"2000-01-01T05:06:50Z"}\n'
        file_txt += '{"id":"27106","customer_id":"630","load_amount":"$1404.95","time":"2000-01-01T06:08:12Z"}\n'
        file_txt += '{"id":"7528","customer_id":"273","load_amount":"$5862.58","time":"2000-01-01T07:09:34Z"}\n'
        file_txt += '{"id":"27947","customer_id":"800","load_amount":"$3382.87","time":"2000-01-01T08:10:56Z"}\n'
        with io.StringIO(file_txt) as test_file:
            for transaction in FileParser(test_file).parse():
                assert isinstance(transaction, Transaction)

    def test_parser_with_single_record(self):
        input_data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
        with io.StringIO(json.dumps(input_data)) as test_file:
            for transaction in FileParser(test_file).parse():
                assert isinstance(transaction, Transaction)
                assert transaction.id == input_data["id"]
                assert transaction.customer_id == input_data["customer_id"]
                assert transaction.amount == Decimal(input_data["load_amount"][1:])
                assert transaction.timestamp == datetime.strptime(
                    input_data["time"], DATE_FORMATE
                )

    @pytest.mark.parametrize(
        "invalid_data",
        [
            "asdasdasd",
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "asdsada",
                "time": "2000-01-01T00:00:00Z",
            },
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "asdsada",
                "time": "200sadasdas0-01-01T00:00:00Z",
            },
            {"id": "15887", "customer_id": "528"},
        ],
    )
    def test_parser_with_single_record_with_invalid_data(self, invalid_data):
        transactions = []
        with io.StringIO(json.dumps(invalid_data)) as test_file:
            for transaction in FileParser(test_file).parse():
                assert transaction is None
                transactions.append(transaction)
            else:
                assert transactions

    def test_parser_without_currency_sign(self):
        input_data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
        with io.StringIO(json.dumps(input_data)) as test_file:
            for transaction in FileParser(test_file).parse():
                assert isinstance(transaction, Transaction)
                assert transaction.id == input_data["id"]
                assert transaction.customer_id == input_data["customer_id"]
                assert transaction.amount == Decimal(input_data["load_amount"])
                assert transaction.timestamp == datetime.strptime(
                    input_data["time"], DATE_FORMATE
                )

from datetime import datetime
from decimal import Decimal

import pytest

from src.constants import DATE_FORMATE
from src.utils import get_start_and_end_week_dates
from src.utils import normalized_input_amount


class TestUtil:
    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ["2000-01-02T05:39:38Z", ("1999-12-27T00:00:00Z", "2000-01-02T23:59:59Z")],
            ["2000-01-02T23:59:59Z", ("1999-12-27T00:00:00Z", "2000-01-02T23:59:59Z")],
            ["1999-12-27T00:00:00Z", ("1999-12-27T00:00:00Z", "2000-01-02T23:59:59Z")],
            ["1999-12-26T23:59:59Z", ("1999-12-20T00:00:00Z", "1999-12-26T23:59:59Z")],
        ],
    )
    def test_get_start_and_end_week_date(self, input_date, expected):
        input_date = datetime.strptime(input_date, DATE_FORMATE)
        start_date, end_date = get_start_and_end_week_dates(input_date)
        assert start_date
        assert end_date
        assert start_date.strftime(DATE_FORMATE) == expected[0]
        assert end_date.strftime(DATE_FORMATE) == expected[1]

    @pytest.mark.parametrize(
        "input_value, expected_value",
        [["200.00", Decimal("200.00")], ["$200.00", Decimal("200.00")]],
    )
    def test_normalized_load_amount(self, input_value, expected_value):
        assert normalized_input_amount(input_value) == expected_value

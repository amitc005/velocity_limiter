from datetime import datetime
from typing import Generator

import pytest

from src.constants import UTC_DATE_TIME_FORMAT
from src.utils import week_date_range


class TestUtil:
    @pytest.mark.parametrize(
        "input_date",
        [
            "2021-01-08T05:39:38Z",
            "2000-01-05T23:59:59Z",
            "1999-12-04T00:00:00Z",
            "1999-12-03T23:59:59Z",
        ],
    )
    def test_get_start_and_end_week_date(self, input_date):
        input_date = datetime.strptime(input_date, UTC_DATE_TIME_FORMAT)
        week_date = week_date_range(input_date)
        assert isinstance(week_date, Generator)
        date_list = []
        for date in week_date:
            date_list.append(date)

        assert len(date_list) == 6

        divider = input_date.weekday()

        for date in date_list[:divider]:
            assert input_date >= date

        for date in date_list[divider:]:
            assert input_date < date

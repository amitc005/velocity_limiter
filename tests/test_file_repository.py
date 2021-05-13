# from datetime import datetime
import pytest

# from src.app import FileRepository
# from src.constants import DATE_FORMATE
# from src.models import LoadRecord


class TestFileRepository:
    @pytest.fixture(autouse=True)
    def set_up(self):
        pass

    # def test_file_repo_constructor(self):
    #     with open("tests/extra/input.txt", "r") as input_file:
    #         file_repo = FileRepository(input_file)
    #         assert file_repo
    #         output_values = file_repo.add_records()
    #         customer_562 = file_repo._customer_records["562"]
    #         query_date = datetime.strptime("2000-01-30T05:37:32Z", DATE_FORMATE)
    #         daily = customer_562.filter_by_date(query_date)
    #         weekly = customer_562.filter_by_week(query_date)
    #         total_weekly_sum = LoadRecord.calculate_total_load_amount(weekly)
    #         assert customer_562

import pytest

from main import aggregated_storage
from src.constants import MAX_DAILY_LOAD_AMOUNT
from src.constants import MAX_DAILY_LOAD_NO
from src.exceptions import DailyTransactionAmountException
from src.exceptions import DailyTransactionLimitException
from src.exceptions import WeeklyTransactionAmountException
from src.models import Customer
from src.models import Transaction
from src.validators import PerDayTransactionAmountLimiter
from src.validators import PerDayTransactionLimiter
from src.validators import PerWeekTransactionAmountLimiter
from src.validators import TransactionInputValidator


class TestTransactionInput:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_validator(self):
        data = {
            "id": "15887",
            "customer_id": "528",
            "load_amount": "$3318.47",
            "time": "2000-01-01T00:00:00Z",
        }
        validator = TransactionInputValidator(data)
        assert validator
        assert validator.validate()

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {},
            {"id": "15887", "customer_id": "528"},
            {"id": "15887", "customer_id": "528", "load_amount": "$3318.47"},
            {"id": "15887", "customer_id": "528", "time": "2000-01-01T00:00:00Z"},
            {"customer_id": "528", "time": "2000-01-01T00:00:00Z"},
        ],
    )
    def test_validator_with_missing_fields(self, invalid_data):
        validator = TransactionInputValidator(invalid_data)
        assert validator
        assert not validator.validate()


class TestPerDayValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = Customer("1")
        self.transaction = Transaction(
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$3318.47",
                "time": "2000-01-01T00:00:00Z",
            }
        )

    def test_per_day_validator(self, monkeypatch):
        def mock_get(customer_id, timestamp):
            return 0, 0

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerDayTransactionLimiter(self.customer, self.transaction)
        validator.validate()

    def test_per_day_validator_when_limit_reach(self, monkeypatch):
        def mock_get(customer_id, timestamp):
            return 0, MAX_DAILY_LOAD_NO

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerDayTransactionLimiter(self.customer, self.transaction)
        with pytest.raises(DailyTransactionLimitException):
            validator.validate()


class TestPerDayAmountValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = Customer("1")
        self.transaction = Transaction(
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$3318.47",
                "time": "2000-01-01T00:00:00Z",
            }
        )

    def test_per_day_validator(self, monkeypatch):
        def mock_get(customer_id, timestamp):
            return 0, 0

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerDayTransactionAmountLimiter(self.customer, self.transaction)
        validator.validate()

    def test_per_day_validator_when_limit_reach(self, monkeypatch):
        def mock_get(customer_id, timestamp):
            return MAX_DAILY_LOAD_AMOUNT, 0

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerDayTransactionAmountLimiter(self.customer, self.transaction)
        with pytest.raises(DailyTransactionAmountException):
            validator.validate()


class TestPerWeekAmountValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = Customer("1")
        self.transaction = Transaction(
            {
                "id": "15887",
                "customer_id": "528",
                "load_amount": "$3318.47",
                "time": "2000-01-01T00:00:00Z",
            }
        )

    def test_per_day_validator(self, monkeypatch):
        def mock_get(customer_id, timestamp):
            return 0, 0

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerWeekTransactionAmountLimiter(self.customer, self.transaction)
        validator.validate()

    def test_per_day_validator_when_limit_reach(self, monkeypatch):
        # This will call 5 times so it will exceed limit
        def mock_get(customer_id, timestamp):
            return MAX_DAILY_LOAD_AMOUNT, 0

        monkeypatch.setattr(aggregated_storage, "get", mock_get)
        validator = PerWeekTransactionAmountLimiter(self.customer, self.transaction)
        with pytest.raises(WeeklyTransactionAmountException):
            validator.validate()

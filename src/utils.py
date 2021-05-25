import json
from datetime import timedelta


def week_date_range(date):
    start_date = date - timedelta(days=date.weekday())
    yield start_date

    for increment in range(2, 7):
        yield start_date + timedelta(days=increment)


class TransactionFileIterator:
    def __init__(self, source):
        self._source = source

    def __iter__(self):
        from .models import Transaction
        from src.validators import TransactionInputValidator

        for file_line in self._source:
            try:
                data = json.loads(file_line)
                if not TransactionInputValidator(data).validate():
                    continue
                yield Transaction(data)

            except Exception:
                continue

class TransactionException(Exception):
    """Transaction Exception"""

    pass


class DailyTransactionLimitException(TransactionException):
    pass


class DailyTransactionAmountException(TransactionException):
    pass


class WeeklyTransactionAmountException(TransactionException):
    pass

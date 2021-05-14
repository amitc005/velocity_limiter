from datetime import timedelta


def week_date_range(date):
    start_date = date - timedelta(days=date.weekday())

    yield start_date

    for increment in range(2, 6):
        yield start_date + timedelta(days=increment)

    yield start_date + timedelta(days=6)

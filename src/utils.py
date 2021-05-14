from datetime import timedelta


# def get_start_and_end_week_dates(query_date):
#     start = query_date - timedelta(days=query_date.weekday())
#     end = start + timedelta(days=6)
#     return (
#         start.replace(hour=0, minute=0, second=0, microsecond=0),
#         end.replace(hour=23, minute=59, second=59, microsecond=0),
#     )


def week_date_range(date):
    start_date = date - timedelta(days=date.weekday())

    yield start_date

    for increment in range(2, 6):
        yield start_date + timedelta(days=increment)

    yield start_date + timedelta(days=6)

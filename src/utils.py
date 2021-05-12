from datetime import timedelta


def get_start_and_end_week_date(current_date):
    start = current_date - timedelta(days=current_date.weekday())
    end = start + timedelta(days=6)
    return (
        start.replace(hour=0, minute=0, second=0, microsecond=0),
        end.replace(hour=23, minute=59, second=59, microsecond=0),
    )
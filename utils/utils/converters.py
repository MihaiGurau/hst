from datetime import date, datetime


def to_datetime(dt: str | date) -> datetime:
    """Utility function to convert a string or date to a datetime object."""

    if isinstance(dt, str):
        return datetime.fromisoformat(dt)
    elif isinstance(dt, date):
        return datetime(year=dt.year, month=dt.month, day=dt.day)
    else:
        raise TypeError(
            f"Invalid type {type(dt)} for {dt}. Expected `str` or `datetime.date`."
        )

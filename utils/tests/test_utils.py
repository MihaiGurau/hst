from datetime import date, datetime

import pytest

from utils.converters import to_datetime


def test_to_datetime_with_string():
    assert to_datetime("2021-01-01") == datetime(2021, 1, 1)


def test_to_datetime_with_date():
    assert to_datetime(date(2021, 1, 1)) == datetime(2021, 1, 1)


def test_to_datetime_with_invalid_type():
    with pytest.raises(TypeError) as e:
        to_datetime(123)

    assert (
        str(e.value)
        == "Invalid type <class 'int'> for 123. Expected `str` or `datetime.date`."
    )

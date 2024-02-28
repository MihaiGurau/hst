"""
Source of inspiration: https://arnaudmiribel.github.io/streamlit-extras/extras/mandatory_date_range/
Perhaps I could just use the streamlit-extras library, if I need more than just this date range picker.
"""

from datetime import date, timedelta

import streamlit as st


def date_range_picker(
    title: str,
    default_start: date | None,
    default_end: date | None,
    min_date: date | None = None,
    max_date: date | None = None,
    format: str = "YYYY/MM/DD",
    error_message: str = "Please select both the start and end date.",
    key: str | None = None,
):
    def end(e: str):
        st.error(e)
        st.stop()

    if default_start is None:
        default_start = date.today() - timedelta(days=30)

    if default_end is None:
        default_end = date.today()

    date_range = st.date_input(
        title,
        value=(default_start, default_end),
        min_value=min_date,
        max_value=max_date,
        format=format,
        key=key,
    )

    if (
        date_range is None
        or isinstance(date_range, date)
        or (isinstance(date_range, tuple) and len(date_range) != 2)
        or (not all(isinstance(d, date) for d in date_range))
    ):
        end(error_message)

    try:
        start_date, end_date = date_range[0], date_range[1]  # type: ignore
    except IndexError:
        end(error_message)

    return start_date, end_date

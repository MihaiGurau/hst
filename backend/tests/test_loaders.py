import polars as pl
import pytest
from polars.testing import assert_frame_equal, assert_series_equal

from backend.transformers.core import (
    compute_top_performers_per_day,
    compute_trading_days,
)


@pytest.fixture
def trading_data():
    yield pl.read_csv("tests/testing_data/quotes.csv", try_parse_dates=True)


@pl.Config(verbose=True, tbl_width_chars=100, fmt_table_cell_list_len=10)
def test_compute_trading_days(trading_data: pl.DataFrame):
    trading_days = compute_trading_days(trading_data)

    assert trading_days.shape == (4, 3)
    assert_series_equal(
        trading_days.select("ticker").to_series().sort(),
        pl.Series("ticker", ["AAPL", "GOOGL", "MSFT", "NVDA"]),
    )
    assert trading_days.select("count_trading_days").is_duplicated().all()
    assert trading_days.select("trading_days").is_duplicated().all()


def test_top_performers_per_day(trading_data: pl.DataFrame):
    result = compute_top_performers_per_day(trading_data)
    sample = result.sort("trading_date").head(5).select("ticker", "relative_change")
    assert_frame_equal(
        sample,
        pl.DataFrame(
            data={
                "ticker": ["GOOGL", "GOOGL", "NVDA", "NVDA", "NVDA"],
                "relative_change": [
                    -0.002743,
                    0.012168,
                    0.004836,
                    0.013103,
                    0.05536,
                ],
            }
        ),
        atol=1e-6,
    )

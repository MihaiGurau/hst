import logging
from datetime import datetime
from typing import Iterable

import pandas as pd
import polars as pl
import streamlit as st
import yfinance as yf  # type: ignore
from pyrate_limiter import Duration, Limiter, RequestRate
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket

from backend.transformers.core import compute_top_performers_per_day


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


logger = logging.getLogger(__name__)


@st.cache_data(show_spinner=True)
def download_quotes(
    tickers: Iterable[str], start: datetime, end: datetime
) -> pl.DataFrame:
    dfs: list[pl.DataFrame] = []

    session = CachedLimiterSession(
        limiter=Limiter(
            RequestRate(2, Duration.SECOND * 5)
        ),  # max 2 requests per 5 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"),
    )

    logger.info("Downloading quotes for %s", ", ".join(tickers))

    for ticker in tickers:
        logger.info("Getting %s data...", ticker)

        data: pd.DataFrame = yf.download(
            ticker,
            group_by="ticker",
            period="1d",
            start=start,
            end=end,
            session=session,
        )
        dfs.append(
            pl.from_pandas(data, include_index=True).with_columns(
                pl.lit(ticker).alias("ticker")
            )
        )

        logger.info("Finished getting %s data", ticker)

    logger.info("Finished downloading quotes")

    result = pl.concat(dfs, how="vertical")
    return result.rename(
        {col: col.replace(" ", "_").lower() for col in result.columns}
    ).select(
        [
            "ticker",
            pl.col("date").cast(pl.Date).alias("trading_date"),
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
    )


if __name__ == "__main__":
    quotes = download_quotes(
        ["AAPL", "GOOGL", "MSFT", "NVDA"],
        start=datetime(2024, 1, 1),
        end=datetime(2024, 2, 26),
    )
    quotes.write_csv("tests/testing_data/quotes.csv")
    result = compute_top_performers_per_day(quotes)
    print(result)

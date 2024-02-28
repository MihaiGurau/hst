import logging
from dataclasses import asdict, dataclass
from datetime import timedelta
from functools import cache
from typing import Iterable

import polars as pl
from bs4 import BeautifulSoup
from requests_cache import CachedSession

# FIXME: This import is not working
# from utils.logging_util import setup_logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True, order=True, slots=True)
class Ticker:
    symbol: str
    security: str
    gics_sector: str
    gics_sub_industry: str
    hq_location: str
    date_added: str
    cik: str
    founded: str

    @property
    def pretty_name(self) -> str:
        return f"{self.symbol} - {self.security}"


class SP500Source:

    def fetch(self) -> str:
        """Fetches the S&P 500 constituents from Wikipedia as raw HTML text."""

        logger.info("Fetching SP500 text...")
        with CachedSession(expire_after=timedelta(days=1)) as requests_cache:
            response = requests_cache.get(
                "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            )
            if response.status_code != 200:
                response.raise_for_status()

        return response.text

    @cache
    def extract_tickers(self) -> list[Ticker]:
        """Extracts the S&P 500 constituents from Wikipedia-based table text."""

        text = self.fetch()
        soup = BeautifulSoup(text, "lxml")
        table = soup.find("table", {"class": "wikitable sortable"})
        if table is None:
            raise ValueError("Unable to find SP500 table")

        tickers: list[Ticker] = []

        rows = table.find_all("tr")  # type: ignore
        for row in rows[1:]:  # exclude header
            cols = row.find_all("td")
            ticker = Ticker(*[col.text.strip() for col in cols])
            tickers.append(ticker)

        logger.debug("Fetched %d tickers", len(tickers))

        return sorted(tickers)


def make_ticker_dataframe(tickers: Iterable[Ticker]) -> pl.DataFrame:
    """Creates a Polars dataframe from the given tickers."""

    return pl.from_dicts(
        [asdict(ticker) for ticker in tickers],
        infer_schema_length=None,
    ).with_columns(pl.col("date_added").cast(pl.Date).alias("date_added"))


def fetch_tickers() -> pl.DataFrame:
    source = SP500Source()
    tickers = source.extract_tickers()
    return make_ticker_dataframe(tickers)


def main():
    # setup_logging() # FIXME: not working due to improper import
    source = SP500Source()
    tickers = source.extract_tickers()
    df = make_ticker_dataframe(tickers)
    print(df.head())
    # for i, ticker in enumerate(tickers, 1):
    #     print(f"{i} - {ticker.pretty_name}")


if __name__ == "__main__":
    main()

import logging
from datetime import date
from functools import reduce

import polars as pl
import streamlit as st
from streamlit import session_state as ss

from app.defaults import CONSTANTS, DEFAULTS
from backend.loaders.quotes import download_quotes
from backend.loaders.tickers import fetch_tickers
from backend.transformers.core import compute_top_performers_per_day
from utils.converters import to_datetime
from utils.logging_util import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

logger.info("Running the Hindsight Trader Streamlit script.")

st.set_page_config(
    page_title="Portfolio Simulator",
    page_icon=":chart_with_upwards_trend:",
)

st.title("Hindsight Trader :money_with_wings:")

# Configuration
st.header("Configuration", divider=True, help="Configure the trading simulation.")

# Perform first-time setup. This ensures we only set the defaults once
if "is_initialized" not in ss or not ss.is_initialized:
    ss.is_initialized = True
    ss.update(**DEFAULTS)

# Set trading period
ss.trading_period = st.date_input(  # type: ignore
    "Trading period",
    # value=(ss.start_date, ss.end_date),
    value=ss.trading_period,
    max_value=CONSTANTS["max_trading_date"],
    key="trading_period_date_input",
    format="YYYY/MM/DD",
    help="Select the start and end dates for the perfect trading simulation.",
)

try:
    start_date = ss.trading_period[0]  # type: ignore
    end_date = ss.trading_period[1]  # type: ignore
except IndexError:
    st.warning("Waiting for trading period to be set...")
    st.stop()


# Fetch SP500 tickers
tickers_df = fetch_tickers()

# Display SP500 tickers
st.write("Available S&P 500 tickers")
st.dataframe(tickers_df.to_pandas(), hide_index=True, height=300, width=800)

# Set tickers
# TODO: ensure we can display the tickers in a more user-friendly way (e.g., Ticker.pretty_name)

if "tickers" not in ss:
    ss.tickers = DEFAULTS["tickers"]

ss["tickers"] = st.multiselect(
    "Tickers",
    options=sorted(
        set(tickers_df.get_column("symbol").to_list()).union(DEFAULTS["tickers"])
    ),
    default=ss["tickers"],
    placeholder="Select stocks you want to trade",
)

# Set starting balance
if "starting_balance" not in ss:
    ss["starting_balance"] = DEFAULTS["starting_balance"]

ss["starting_balance"] = st.number_input(
    "Starting balance ($)",
    value=ss["starting_balance"],
    min_value=100,
    max_value=1_000_000,
    step=100,
    key="starting_balance_number_input",
    help="Set the starting balance for the perfect trading simulation.",
)

# # FIXME: This is a temporary workaround to avoid the app crashing when the start & end dates are not both set
# if not start_date or not end_date or not tickers:
#     st.stop()

st.success("Configuration complete! :tada:")

# Get quotes
quotes = download_quotes(
    ss["tickers"],
    start=to_datetime(ss.trading_period[0]),  # type: ignore
    end=to_datetime(ss.trading_period[1]),  # type: ignore
)

# Display quotes
st.header("Quotes", divider=True)
st.write(
    f"Retrieved {quotes.select(pl.len()).item()} quotes for "
    f"{quotes.select('ticker').n_unique()} tickers from {start_date} to {end_date}."
)
st.write("First 5 records:")
st.table(quotes.head(5).to_pandas())

# Calculation time
st.header("Trading results", divider=True)
st.write("Here are your perfect trading results.")

# Show top performers
st.subheader("Top performers", divider=True)
top_performers = compute_top_performers_per_day(quotes).select(
    "trading_date",
    "ticker",
    (100 * pl.col("relative_change")).round(2).alias("pct_change"),
)
st.table(top_performers.to_pandas())

# Show estimated final balance
st.subheader("Estimated final balance", divider=True)
final_balance = reduce(
    lambda balance, change: balance * (1 + change),
    top_performers.select(pl.col("pct_change") / 100).to_series().to_list(),
    ss.starting_balance,
)
st.write(f"Estimated final balance: ${final_balance:.2f}")

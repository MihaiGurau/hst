"""
Stores the default values when initializing the app.
"""

from datetime import date, timedelta

from utils.frozendict import FrozenDict

# Default values for user-configurable settings
DEFAULTS = FrozenDict(
    {
        "start_trading_date": date.today() - timedelta(days=30),
        "end_trading_date": date.today() - timedelta(days=1),
        "trading_period": tuple(
            [date.today() - timedelta(days=30), date.today() - timedelta(days=1)]
        ),
        "tickers": [
            "AAPL",
            "GOOGL",
            "MSFT",
            "NVDA",
            "TSLA",
            "AMZN",
            "C",
            "MS",
            "GS",
            "SLB",
            "PATH",
        ],
        "starting_balance": 1_000,
    }
)

# Constants needed for the app controls
CONSTANTS = FrozenDict(
    {
        "max_trading_date": date.today() - timedelta(days=1),
    }
)

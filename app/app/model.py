from dataclasses import dataclass
from datetime import date


@dataclass
class AppConfig:
    """App config"""

    start_trading_date: date
    end_trading_date: date
    starting_balance: int
    selected_tickers: list[str]

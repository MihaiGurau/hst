import polars as pl


def compute_trading_days(quotes: pl.DataFrame) -> pl.DataFrame:
    """Computes the trading days for each ticker."""

    return quotes.group_by("ticker").agg(
        count_trading_days=pl.count("ticker"),
        trading_days=pl.concat_list("trading_date").flatten().sort(),
    )


def compute_top_performers_per_day(quotes: pl.DataFrame) -> pl.DataFrame:
    """Calculates the top performers per day."""

    return (
        quotes.with_columns(
            ((pl.col("close") - pl.col("open")) / pl.col("open")).alias(
                "relative_change"
            )
        )
        .filter(
            pl.col("relative_change") == pl.max("relative_change").over("trading_date")
        )
        .sort("trading_date")
        .select(
            "trading_date",
            "ticker",
            "relative_change",
        )
    )

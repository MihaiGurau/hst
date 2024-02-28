# Technical project ideas

This document contains various technical that I should / could / might implement in the project.

## Avoiding `yfinance` API calls if tickers or period are a subset of a previously computed call

Say the user selects Jan 1 - Dec 31 2023 as a trading period for AAPL, META, and NVDA stocks.
Currnetly, the app will fetch quote data for this and cache the request.

Now, if the user changes the end date to say Jan 31, this will trigger a new request.
However, we can still reuse the data from the first one, since it's a subset.

Therefore, implementing better caching would be nice to avoid unnecessary API calls.

>NOTE: somehow, removing tickers from the list does not trigger a new call to `download_quotes`.
>This might be due to how the `@st.cache_data` decorator is implemented. Check it out.

There's also a package for this ([yfinance-cache](https://github.com/ValueRaider/yfinance-cache)).
Nonetheless, I could also try to build a smaller version of this myself, since I only need to cache the quotes.

## Fixing UI controls not being updated

Sometimes, changes made in the UI are reversed. They work the second time I try to execute them.
This happens at least for the `st.date_input` and the `st.multiselect`.

I believe it could be related to some faulty interactions or race conditions between the widgets, `st.session_state`, and app reruns.
I have already tried to set the `[runner]` config `fastRereuns = false` in the `.streamlit/config.toml` file, but with no success.

## Better state management

State management feels a bit messy now. It would be nice to have more structure, perhaps using an app config.
Example below, though I am not sure how to use it, other than as a container for `st.session_state` items I need.

For now, the initalization of the session state is done using the `DEFAULTS` dictionary from `app/app/defaults.py`.

```python
# in app/app.models.py
from dataclasses import dataclass
from datetime import date


@dataclass
class AppConfig:
    """App config"""

    start_trading_date: date
    end_trading_date: date
    starting_balance: int
    selected_tickers: list[str]
```

## Logging improvements

I need to improve logging, since it's messy now.

## `Makefile` updates + Poetry

Now that the project is split into three packages, the original `Makefile` is no longer up to date.

I can create one `Makefile` per package, and perhaps also keep a main one for setup / running / testing the whole app.

## Testing

Duh. Add them once the design of the app and backend are more mature.
When I am writing this, I am changing too many things to make it worth it, as I would constantly break the tests.

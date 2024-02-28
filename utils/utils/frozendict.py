from typing import Any


class FrozenDict(dict):
    """Simple dictionary that cannot be modified after initialization."""

    def __init__(self, *args, **kwargs):
        super(FrozenDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key: Any) -> Any:
        return dict.__getitem__(self, key)

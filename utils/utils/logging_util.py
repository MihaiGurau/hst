"""
Source: https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/135_modern_logging/main.py
"""

import json
import logging.config
import logging.handlers
import pathlib

logger = logging.getLogger(__name__)


def setup_logging():
    config_file = pathlib.Path("logging_configs/stderr-json.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)


def main():
    setup_logging()
    logging.basicConfig(level="INFO")
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()

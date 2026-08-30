"""Central logging configuration."""

import logging


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure the application's root logger.
    """
    logging.basicConfig(level=level, format=LOG_FORMAT)

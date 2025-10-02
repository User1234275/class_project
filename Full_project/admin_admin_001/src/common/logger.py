import logging

logger = logging.getLogger("admin-dashboard")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def get_logger(name: str = None):
    return logging.getLogger(name or "admin-dashboard")

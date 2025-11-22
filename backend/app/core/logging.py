# production logs should be structured (JSON) for Grafana/Loki ingestion

import logging
from loguru import logger

def setup_logging():
    logging.getLogger("uvicorn").handlers.clear()
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        format="{time} {level} {message}",
        level="INFO",
        serialize=True,
    )
    return logger


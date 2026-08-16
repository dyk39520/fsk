"""统一日志工具。"""

import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from config import LOG_DIR


LOG_DIR.mkdir(parents=True, exist_ok=True)
EXISTING_LOG_FILES = list(LOG_DIR.glob("test_*.log"))
RUN_NUMBER = len(EXISTING_LOG_FILES) + 1
LOG_FILE = LOG_DIR / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def get_logger(name="po"):
    """获取统一配置的 logger，避免重复添加 handler。"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

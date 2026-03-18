from loguru import logger
import sys

MAX_LEN = 90  # максимальная длина сообщения


def truncate_message(record):
    msg = record["message"]
    if len(msg) > MAX_LEN:
        record["message"] = msg[:MAX_LEN] + "..."  # обрезаем и добавляем "..."
    return record


def add_logger():
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO",
        colorize=True,
        backtrace=False,
        diagnose=False,
        filter=truncate_message,  # применяем функцию обрезки
    )

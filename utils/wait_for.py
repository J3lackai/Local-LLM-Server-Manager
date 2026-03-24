import requests
import time
from requests.exceptions import ConnectionError, Timeout
from loguru import logger


def wait_for_server(self, url="http://localhost:8081", timeout=180, check_interval=2):
    """
    Ожидает загрузки сервера, делая запросы пока не получит 200 OK.

    Args:
        url: URL сервера
        timeout: максимальное время ожидания в секундах (по умолчанию 180 = 3 минуты)
        check_interval: интервал между проверками в секундах

    Raises:
        TimeoutError: если сервер не загрузился за отведённое время
    """
    start_time = time.time()
    last_error = None

    logger.info(f"Ожидание загрузки сервера {url}...")

    while time.time() - start_time < timeout:
        try:
            # Делаем GET запрос к серверу
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                elapsed = time.time() - start_time
                logger.info(f"Сервер загрузился за {elapsed:.1f} секунд")
                return True
            else:
                logger.debug(f"Сервер вернул {response.status_code}, ожидаем...")

        except ConnectionError:
            logger.debug("Сервер ещё не принимает соединения, ждём...")
        except Timeout:
            logger.debug("Таймаут соединения, ждём...")
        except Exception as e:
            last_error = e
            logger.debug(f"Ошибка при проверке: {e}")

        # Ждём перед следующей проверкой
        time.sleep(check_interval)

    # Если вышли по таймауту
    elapsed = time.time() - start_time
    error_msg = f"Сервер не загрузился за {elapsed:.1f} секунд"

    if last_error:
        error_msg += f". Последняя ошибка: {last_error}"

    logger.error(error_msg)
    raise TimeoutError(error_msg)

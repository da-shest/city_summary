import logging
import random
import time
from typing import Any

import requests

from exceptions import ServiceUnavailableError

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 5
TIMEOUT = 10


def get_api_data(url: str, params: dict[str, Any] | None = None) -> dict:
    data = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            if response.status_code >= 500 or response.status_code == 429:
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        delay = float(retry_after)
                        logger.warning(f"Превышен лимит запросов (429). Пауза из Retry-After: {delay} сек.")
                        time.sleep(delay)
                        continue
                response.raise_for_status()
            data = response.json()
            break
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.JSONDecodeError,
        ) as err:
            if attempt == MAX_ATTEMPTS:
                logger.error(f"Достигнуто максимальное число попыток ({MAX_ATTEMPTS}) для URL: {url}")
                raise ServiceUnavailableError(f"Сервис по адресу {url} недоступен после {MAX_ATTEMPTS} попыток.") from err
            delay = 2 ** (attempt - 1) + random.uniform(0, 0.5)
            logger.warning(f"Ошибка при запросе (попытка {attempt}/{MAX_ATTEMPTS}): {err}. Повтор через {delay:.2f} сек.")
            time.sleep(delay)

    return data

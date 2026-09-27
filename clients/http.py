import random
import time
from typing import Any

import requests

MAX_ATTEMPTS = 5
TIMEOUT = 10


def get_api_data(url: str, params: dict[str, Any] | None = None) -> dict:
    data = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            if response.status_code >= 500 or response.status_code == 429:
                response.raise_for_status()
            data = response.json()
            break
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.JSONDecodeError,
        ):
            if attempt == MAX_ATTEMPTS:
                raise
            delay = 2 ** (attempt - 1) + random.uniform(0, 0.5)
            # logger
            time.sleep(delay)

    return data

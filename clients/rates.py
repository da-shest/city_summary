from clients.http import get_api_data

BASE_RATE_URL = "https://api.frankfurter.dev/v2/rate"


def get_rate(currency: str) -> float:
    url = f"{BASE_RATE_URL}/{currency}/RUB"
    data = get_api_data(url)
    validate_rate(data)
    return data["rate"]


def validate_rate(data: dict) -> None:
    for field in ("date", "base", "quote", "rate"):
        if field not in data:
            raise ValueError(f"Отсутствует поле {field}")

    for field, type in (
        ("date", str),
        ("base", str),
        ("quote", str),
        ("rate", float),
    ):
        if not isinstance(data[field], type):
            raise TypeError(f"Поле {field} должно иметь тип {type}")

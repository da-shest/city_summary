class AppError(Exception):
    """Базовое исключение приложения"""


class NotFoundError(AppError):
    """Город или код валюты не найден (код выхода 3)"""


class CityNotFoundError(NotFoundError):
    """Город не найден"""


class CurrencyNotFoundError(NotFoundError):
    """Код валюты не найден"""


class ServiceUnavailableError(AppError):
    """Внешний сервис недоступен после всех retry (код выхода 4)"""

class EmiasClientError(Exception):
    """Общее исключение для ошибок EmiasClient."""

class CSRFTokenNotFoundError(EmiasClientError):
    """Ошибка при получении CSRF токена."""

class APIRequestError(EmiasClientError):
    """Ошибка при выполнении API запроса."""

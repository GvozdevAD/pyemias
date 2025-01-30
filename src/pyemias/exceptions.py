class EmiasClientError(Exception):
    """Общее исключение для ошибок EmiasClient."""

class CSRFTokenNotFoundError(EmiasClientError):
    """Ошибка при получении CSRF токена."""

class APIRequestError(EmiasClientError):
    """Ошибка при выполнении API запроса."""

class InvalidPolicyNumberError(EmiasClientError):
    def __init__(self, policy_number: str):
        super().__init__(
            f"Некорректный номер полиса: {policy_number}. "\
                "Он должен содержать ровно 16 символов."
        )
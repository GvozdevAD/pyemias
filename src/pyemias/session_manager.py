import requests

from datetime import date

from bs4 import BeautifulSoup
from nanoid import generate

from .request_builder import RequestBuilder
from .exceptions import (
    CSRFTokenNotFoundError, 
    APIRequestError
)
from .enums.emias_urls import (
    EmiasURLs, 
    MethodsPassport
)


class SessionManager:
    """
    Менеджер сессий для взаимодействия с API ЕМИАС.
    Отвечает за инициализацию сессии, получение CSRF-токена,
    создание анонимного JWT, отправку запросов и закрытие сессии.
    """
    def __init__(self, jsonrpc: str = "2.0"):
        """
        Инициализация SessionManager.
        
        :param jsonrpc: Версия JSON-RPC, используемая в запросах (по умолчанию "2.0").
        """
        self.session = None
        self.nano_id = generate()
        self.jsonrpc = jsonrpc

    def init_session(
        self,
        jwt_token: str = None
    ) -> requests.Session:
        """
        Инициализирует HTTP-сессию, получает CSRF-токен и устанавливает заголовки.
        
        :param jwt_token: JWT-токен пользователя (если None, создаётся анонимный JWT).
        :return: Объект requests.Session с установленными заголовками.
        """
        self.session = requests.Session()
        csrf_token = self.get_csrf_token()
        self.session.cookies.update({
            "csrf-token-name": "csrftoken",
            "csrf-token-value": csrf_token,
        })
        if jwt_token is None:
            jwt_token = self.create_anonymous_jwt(self.nano_id)
        self.session.cookies.update({"jwt": jwt_token})

        return self.session

    def get_csrf_token(self) -> str:
        """
        Получает CSRF-токен с главной страницы портала ЕМИАС.
        
        :raises APIRequestError: Если запрос не успешен.
        :raises CSRFTokenNotFoundError: Если CSRF-токен отсутствует в HTML-ответе.
        :return: Значение CSRF-токена.
        """
        response = self.session.get(EmiasURLs.HOST.value)
        if response.status_code != 200:
            raise APIRequestError(
                f"Ошибка запроса: код состояния {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "lxml")
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token-value'})
        if not csrf_meta:
            raise CSRFTokenNotFoundError(
                "CSRF-токен не найден."
            )
        
        return csrf_meta["content"]

    def create_anonymous_jwt(
        self, 
        nano_id: str, 
    ) -> str:
        """
        Создаёт анонимный JWT для неавторизованных пользователей.
        
        :param nano_id: Уникальный идентификатор запроса.
        :raises APIRequestError: Если запрос на создание JWT завершился неудачно.
        :return: Анонимный JWT-токен.
        """
        response = self.session.post(
            url= EmiasURLs.api_passport_build_url(
                MethodsPassport.CREATE_ANONYMOUS_JWT
            ),
            json= {
                "id": nano_id, 
                "jsonrpc": "2.0", 
                "method": "create_anonymous_jwt"
            }
        )
        if response.status_code != 200:
            raise APIRequestError(
                f"Ошибка создания JWT: код состояния {response.status_code}"
            )
        return response.json().get("result", {})

    def send_post_request(
            self, 
            method: str, 
            url: str,
            policy_number: str,
            birth_date: date,
            additional_params: dict = None
        ) -> dict:
        """
        Отправляет POST-запрос к API ЕМИАС.
        
        :param method: Название метода API.
        :param url: URL-адрес для запроса.
        :param policy_number: Номер полиса пациента.
        :param birth_date: Дата рождения пациента.
        :param additional_params: Дополнительные параметры для тела запроса.
        :raises APIRequestError: В случае ошибки запроса.
        :return: Ответ API в виде словаря.
        """
        data = RequestBuilder.generate(
            method, 
            self.jsonrpc,
            self.nano_id, 
            str(birth_date), 
            policy_number,
            additional_params
        )
        try:
            response = self.session.post(url=url, json=data, timeout=10)
        except requests.Timeout:
            raise APIRequestError("Превышено время ожидания запроса.")
        except requests.RequestException as _ex:
            raise APIRequestError(f"Ошибка при выполнении запроса: {_ex}")
        
        return self.process_response(response)

    def process_response(
        self, 
        response: requests.Response
    ) -> dict:
        """
        Обрабатывает ответ API, проверяя наличие ошибок.
        
        :param response: Объект ответа requests.Response.
        :raises APIRequestError: Если ответ содержит ошибку или статус код не 200.
        :return: Данные ответа.
        """
        if response.status_code != 200:
            raise APIRequestError(
                f"Ошибка запроса: код состояния {response.status_code}"
            )
        
        try:
            data = response.json()
        except ValueError:
            raise APIRequestError("Ошибка обработки JSON-ответа.")
        
        if "error" in data:
            raise APIRequestError(f"Ошибка API: {data['error']}")
        
        return data.get("result", {})
    
    def close_session(self) -> None:
        """
        Закрывает HTTP-сессию.
        """
        if self.session:
            self.session.close()

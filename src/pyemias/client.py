from datetime import datetime
from nanoid import generate

from .session_manager import SessionManager
from .request_builder import RequestBuilder
from .enums.emias_urls import EmiasURLs, MethodsEmc


class EmiasClient:
    def __init__(
        self, 
        policy_number: str, 
        birth_date: datetime, 
        jwt_token: str = None
    ) -> None:
        self.__policy_number = policy_number
        self.__birth_date = birth_date.date()
        self.jwt_token = jwt_token
        self.jsonrpc = "2.0"
        self.nano_id = generate()
        self.session_manager = SessionManager()
        self.session = None

    def initialize(self):
        """
        Инициализация сессии.
        """
        self.session = self.session_manager.init_session(
            self.nano_id, 
            self.jwt_token
        )
        if self.jwt_token is None:
            self.jwt_token = self.session.headers.get("jwt")
        return self

    def _send_post_request(
            self, 
            method: str, 
            url: str, 
            additional_params: dict = None
        ) -> dict:
        """
        Единая функция для отправки POST-запросов.

        :param method: Название метода API.
        :param url: URL-адрес для отправки запроса.
        :param additional_params: Дополнительные параметры для JSON.
        :return: Данные ответа в виде словаря.
        """
        data = RequestBuilder.generate(
            method, 
            self.jsonrpc,
            self.nano_id, 
            str(self.__birth_date), 
            self.__policy_number,
            additional_params
        )
        # Добавить try ...
        response = self.session.post(url=url, json=data)
        return self.session_manager.process_response(response)

    def get_specialities_info(self) -> list[dict]:
        """
        Получение информации о специализациях.
        """
        return self._send_post_request(
            method=MethodsEmc.GET_SPECIALITIES_INFO.value.strip("/?"),
            url= EmiasURLs.emc_api_build_url(
                MethodsEmc.GET_SPECIALITIES_INFO
            )
        )

    def get_doctors_info(
            self, 
            speciality_id: int
    ) -> list[dict]:
        """
        Получение информации о врачах по ID специальности.

        :param speciality_id: Идентификатор специальности.
        :type speciality_id: int

        :return: 
        :rtype: dict
        """
        return self._send_post_request(
            method= MethodsEmc.GET_DOCTORS_INFO.value.strip("/?"),
            url= EmiasURLs.emc_api_build_url(
                MethodsEmc.GET_DOCTORS_INFO
            ),
            additional_params= {
                "specialityId": speciality_id
            }
        )

    def get_available_resource_schedule_info(
        self,
        speciality_id: int,
        available_resource_id: int,
        complex_resource_id: int
    ) -> dict:
        """
        Получение информации о доступном расписании ресурсов.
        
        :param speciality_id: Идентификатор специальности.
        :param available_resource_id: Идентификатор врача.
        :param complex_resource_id: Идентификатор поликлиники.
        """
        return self._send_post_request(
            method= MethodsEmc.GET_AVAILABLE_RESOURCE_SCHEDULE_INFO.value.strip("/?"),
            url= EmiasURLs.emc_api_build_url(
                MethodsEmc.GET_AVAILABLE_RESOURCE_SCHEDULE_INFO
            ),
            additional_params={
                "specialityId": speciality_id,
                "availableResourceId": available_resource_id,
                "complexResourceId": complex_resource_id
            }
        )

    def __enter__(self):
        return self.initialize()

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.session:
                self.session.close()
        finally:
            if exc_type:
                print(f"Error: {exc_value}")
            return True

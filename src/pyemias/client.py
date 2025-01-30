from .session_manager import SessionManager
from .enums.emias_urls import EmiasURLs, MethodsEmc
from .models.auth_model import AuthPolicyData
from .models.emc_response_model import (
    SpecialitiesResponse
)

class EmiasClient:
    def __init__(
        self, 
        auth_data: AuthPolicyData
    ) -> None:
        self.__policy_number = auth_data.policy_number
        self.__birth_date = auth_data.birth_date
        self.jwt_token = auth_data.jwt
        self.session_manager = SessionManager()

    def initialize(self):
        """
        Инициализация сессии.
        """
        session = self.session_manager.init_session(self.jwt_token)
        if self.jwt_token is None:
            self.jwt_token = session.headers.get("jwt")
        return self


    def get_specialities_info(
            self, 
            as_dict: bool = False
    ) -> list[SpecialitiesResponse] | list[dict]:
        """
        Получение информации о специализациях.
        
        :param as_dict: Если True, возвращает необработанные данные (список словарей).
                    Если False, возвращает список объектов SpecialitiesResponse.
        :return: Список объектов SpecialitiesResponse или список словарей.
        """
        method = MethodsEmc.GET_SPECIALITIES_INFO
        response = self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date

        )
        if as_dict:
            return response
        return [SpecialitiesResponse(**row) for row in response]

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
        method = MethodsEmc.GET_DOCTORS_INFO
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date,
            {"specialityId": speciality_id}
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
        method = MethodsEmc.GET_AVAILABLE_RESOURCE_SCHEDULE_INFO
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date,
            {
                "specialityId": speciality_id,
                "availableResourceId": available_resource_id,
                "complexResourceId": complex_resource_id
            }
        )
    
    def get_appointment_receptions_by_patient(self) -> list[dict]:
        """ Получение действующих записей на прием к врачам """
        method = MethodsEmc.GET_APPOINTMENT_RECEPTIONS_BY_PATIENT
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date
        )

    def get_digital_prescription(self) -> list[dict] | dict:
        """ Получение рецептов """ 
        method = MethodsEmc.DIGITAL_PRESCRIPTION
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date
        )

    # ???
    def get_referrals_info(self):
        """ """
        method = MethodsEmc.GET_REFERRALS_INFO
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date
        )
    
    # ???
    def get_assignments_info(self):
        """ """
        method = MethodsEmc.GET_ASSIGNMENTS_INFO
        return self.session_manager.send_post_request(
            method.value.strip("/?"),
            EmiasURLs.emc_api_build_url(
                method
            ),
            self.__policy_number,
            self.__birth_date
        )

    def __enter__(self):
        return self.initialize()

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.session_manager.close_session()
        finally:
            if exc_type:
                print(f"Error: {exc_value}")
            return True
